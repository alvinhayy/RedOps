#!/usr/bin/env python3
"""Launch Claude Code against the Z.ai Anthropic-compatible endpoint."""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


def main() -> None:
    config_path = Path.home() / ".config/opencode/opencode.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read Z.ai config: {config_path}") from exc
    try:
        options = config["provider"]["zai"]["options"]
        api_key = options["apiKey"]
    except (KeyError, TypeError) as exc:
        raise SystemExit(f"Z.ai provider config is incomplete: {config_path}") from exc

    if not api_key:
        raise SystemExit(f"Z.ai API key is empty: {config_path}")

    # Process-scoped overrides: the normal `claude` command and OAuth remain untouched.
    os.environ.update(
        ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic",
        ANTHROPIC_AUTH_TOKEN=api_key,
        ANTHROPIC_DEFAULT_OPUS_MODEL="glm-5.3",
        ANTHROPIC_DEFAULT_SONNET_MODEL="glm-5.3",
        ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-5.3-flash",
    )
    os.environ.setdefault("API_TIMEOUT_MS", "3000000")

    claude = shutil.which("claude")
    if not claude:
        raise SystemExit("Claude CLI is not installed or not available on PATH")
    os.execv(claude, [claude, *sys.argv[1:]])


if __name__ == "__main__":
    main()
