"""Bounded, authorized WAF timing benchmark with a safe amplification mode."""
from __future__ import annotations

import ipaddress
import statistics
import time
from dataclasses import asdict, dataclass
from urllib.parse import urlparse

import httpx


class WafBenchmarkError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class TimingSample:
    url: str
    status_code: int
    elapsed_ms: float
    response_bytes: int


def _is_local_or_private(host: str | None) -> bool:
    if not host:
        return False
    if host in {"localhost", "127.0.0.1", "::1"}:
        return True
    try:
        return ipaddress.ip_address(host).is_private
    except ValueError:
        return host.endswith((".localhost", ".local", ".test"))


class WafTimingBenchmark:
    """Measure clean/test requests without payload mutation or unbounded traffic."""

    def __init__(self, *, lab_mode: bool = False, allowlist: tuple[str, ...] = ()) -> None:
        self.lab_mode = lab_mode
        self.allowlist = allowlist

    def _validate_url(self, url: str, *, amplifier: bool = False) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise WafBenchmarkError(f"invalid URL: {url}")
        if amplifier:
            host = parsed.hostname
            local_target = _is_local_or_private(host)
            allowlisted_lab = any(url.startswith(x) for x in self.allowlist)
            permitted = local_target or (self.lab_mode and allowlisted_lab)
            if not permitted:
                raise WafBenchmarkError(
                    "amplifier URL requires a local/private target, or --lab-mode plus an explicit allowlist"
                )

    def run(
        self,
        *,
        baseline_url: str,
        test_url: str,
        samples: int = 10,
        delay: float = 1.0,
        amplifier_url: str | None = None,
        max_amplifier_bytes: int = 2_000_000,
    ) -> dict:
        if samples < 1 or samples > 30:
            raise WafBenchmarkError("samples must be between 1 and 30")
        if delay < 0.1 or delay > 60:
            raise WafBenchmarkError("delay must be between 0.1 and 60 seconds")
        self._validate_url(baseline_url)
        self._validate_url(test_url)
        if amplifier_url:
            self._validate_url(amplifier_url, amplifier=True)
        urls = [amplifier_url or baseline_url, test_url]
        measurements: list[TimingSample] = []
        with httpx.Client(follow_redirects=True, timeout=15.0) as client:
            for _ in range(samples):
                for url in urls:
                    started = time.perf_counter()
                    response = client.get(url)
                    elapsed = (time.perf_counter() - started) * 1000
                    if url == amplifier_url and len(response.content) > max_amplifier_bytes:
                        raise WafBenchmarkError("amplifier response exceeds configured byte limit")
                    measurements.append(TimingSample(url, response.status_code, elapsed, len(response.content)))
                    time.sleep(delay)
        groups = {url: [x.elapsed_ms for x in measurements if x.url == url] for url in urls}
        return {
            "mode": "lab-or-authorized-bounded",
            "samples": samples,
            "delay_seconds": delay,
            "amplifier_url": amplifier_url,
            "results": {
                url: {
                    "median_ms": round(statistics.median(values), 3),
                    "p95_ms": round(sorted(values)[max(0, int(len(values) * 0.95) - 1)], 3),
                    "min_ms": round(min(values), 3),
                    "max_ms": round(max(values), 3),
                }
                for url, values in groups.items()
            },
            "measurements": [asdict(x) for x in measurements],
        }
