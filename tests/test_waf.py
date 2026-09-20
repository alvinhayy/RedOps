import httpx
import pytest

from redops_rag.waf import WafBenchmarkError, WafTimingBenchmark


def test_amplifier_requires_local_or_allowlisted_target():
    with pytest.raises(WafBenchmarkError):
        WafTimingBenchmark().run(
            baseline_url="https://example.com/", test_url="https://example.com/?x=1",
            amplifier_url="https://example.com/large", samples=1, delay=0.1,
        )


def test_local_amplifier_is_bounded(monkeypatch):
    class FakeClient:
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def get(self, url): return httpx.Response(200, content=b"ok", request=httpx.Request("GET", url))

    monkeypatch.setattr("redops_rag.waf.httpx.Client", lambda **_: FakeClient())
    monkeypatch.setattr("redops_rag.waf.time.sleep", lambda _: None)
    result = WafTimingBenchmark().run(
        baseline_url="http://127.0.0.1/base", test_url="http://127.0.0.1/test",
        amplifier_url="http://127.0.0.1/long", samples=2, delay=0.1,
    )
    assert result["samples"] == 2
    assert len(result["measurements"]) == 4


def test_sample_limit():
    with pytest.raises(WafBenchmarkError):
        WafTimingBenchmark().run(baseline_url="http://localhost/a", test_url="http://localhost/b", samples=31)


def test_lab_mode_still_requires_explicit_allowlist():
    with pytest.raises(WafBenchmarkError):
        WafTimingBenchmark(lab_mode=True).run(
            baseline_url="https://staging.example.com/a",
            test_url="https://staging.example.com/b",
            amplifier_url="https://staging.example.com/long",
            samples=1,
            delay=0.1,
        )
