# Skill-to-tool wiring audit

This document explains how the installed mobile/reversing skills map onto RedOps
profiles. The machine-readable source is [`../agents/skill-tool-matrix.yaml`](../agents/skill-tool-matrix.yaml).

## Summary

| Skill | Owner | Required baseline | Optional MCP | Main gaps |
|---|---|---|---|---|
| `mobile-vuln-hunt` | `mobile_agent` | `rg`, `adb` | Exegol, uiautomator2, Burp | No Frida/drozer/semgrep MCP; iOS tools platform-dependent |
| `reverse-engineer` | `reversing_tools_agent`, `mobile_agent` | `file`, `strings`, `find`, `unzip` | Exegol, Ghidra, radare2 | No decompiler/class-dump/secret-scanner MCP |
| `afl-fuzzing` | `mobile_agent` | `adb` | Exegol, bounded terminal, radare2 | No AFL++/NDK/device-fuzzing MCP |

## Runtime rules

1. Resolve the profile from the engagement type before selecting a connector.
2. Verify every executable inside Exegol or the approved MCP; registry entries do not
   prove installation.
3. Prefer Exegol, then a specialist MCP, then the bounded terminal. The terminal is
   argv-only, workspace-limited, and not an unrestricted host shell.
4. Mobile work is Android/iOS only. BloodHound is exclusively owned by `ad_agent` and
   is not a mobile fallback.
5. Static analysis receives copies of authorized artifacts and records hashes. Dynamic
   testing requires a disposable authorized device/emulator and test scope.

## Gaps and handling

The skills mention tools that are not MCP servers in `.mcp.json.example`: Semgrep,
Drozer, Frida/frida-ios-dump, Android NDK/AFL++, Android decompilers, iOS class-dump,
and secret scanners. These remain optional capabilities. The agent must report a gap,
use static or offline fallback, or use an existing Exegol image after a health check;
it must not install dependencies or invent a connector automatically.

The reverse-engineer skill contains a local instruction to show all extracted values.
RedOps takes the safer repository policy: secrets and credentials remain in the private
engagement workspace and are referenced by evidence location in shared reports.

See [`agents/tools.md`](../agents/tools.md) for the common connector health-check and
source policy, and [`agents/mcp-profiles.yaml`](../agents/mcp-profiles.yaml) for the
current connector profile names.
