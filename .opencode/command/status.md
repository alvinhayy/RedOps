---
description: Show RedOps workspace, Exegol and specialist-session readiness.
---

Use the native OpenCode references and Herdr read-only session inspection to report:

- active Herdr workspace and `ai-*` specialist tabs;
- whether the Exegol workspace/session is reachable;
- `python3 scripts/check_tools.py --wiring` results: role knowledge paths,
  `precompiled-binaries/MANIFEST.json`, engagement ledger convention and MCP assignments;
- `opencode mcp list` connection status for each assigned server, including Docker/Burp
  prerequisites; configured is not the same as connected;
- missing required tools in `.opencode/tools.json`, checked on host and (when running)
  in the selected Exegol container.

Do not start scans, mutate a target, expose credentials, or infer authorization from a
healthy runtime.
