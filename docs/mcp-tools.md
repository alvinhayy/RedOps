# Optional MCP tool routing

RedOps uses an Exegol-first policy. Connectors below are setup-specific and are
not installed or started automatically.

| Connector | Role | Policy |
|---|---|---|
| `redops-exegol` | Isolated pentest tools | Default execution backend |
| `burp` | Authorized HTTP(S) proxy/intercept | Only in-scope traffic |
| `camoufox` | Scoped browser automation | Only approved flows |
| `uiautomator2` | Android UI/device automation | Disposable authorized device |
| `ghidra` | Structured project/import/decompile/analysis | Local authorized files; never execute targets |
| `radare2` | Disassembly, strings, symbols, xrefs, scripting | Isolated local binaries; never execute targets |
| `terminal-bounded` | Local helper commands | Explicit approval, allowlisted argv, workspace-only |

Use [`.mcp.json.example`](../.mcp.json.example) as a non-secret template. Never
commit tokens, passwords, cookies, private keys, or graph exports containing
credential/domain metadata.

## Routing and safety

1. Prefer Exegol for tools and analysis whenever the image provides them.
2. Burp is only for proxying/intercepting explicitly authorized traffic.
3. Camoufox is only for an approved browser flow; keep headless mode enabled.
4. BloodHound collection uses `bloodhound-python` only for the AD/identity agent and
   an authorized AD graph; it is not a mobile connector or MCP requirement. Graph
   data can expose sensitive identities, group membership, sessions, and credential metadata.
5. Ghidra and radare2 receive local, authorized files only. Static analysis must
   not launch an app or execute a target binary.
6. Terminal MCP is not a host shell: enforce argv-only commands, an explicit
   allowlist, a dedicated workspace, no pipelines/redirections/substitution, and
   per-command approval.

## Health/read-only checks

```bash
redops exegol status
adb devices -l
curl --fail --silent http://127.0.0.1:1337/v0.1/health || true  # Burp, if supported
command -v bloodhound-python || true  # AD agent collector, preferably inside Exegol
command -v r2
test -d "$GHIDRA_PROJECT_DIR"
```

Connector versions differ; use their advertised `capabilities`/`health` method
and stop if it is unavailable. For BloodHound (AD/identity only), verify the Neo4j/BloodHound lab
instance and scope before importing data. For Ghidra/r2, verify the input hash
and analysis workspace before opening a file.

## Environment placeholders

```bash
export BURP_API_URL=http://127.0.0.1:1337
export BURP_API_TOKEN='<secret-manager-injection>'
export CAMOUFOX_HEADLESS=true
export GHIDRA_PROJECT_DIR="$PWD/engagements/current/ghidra"
export R2_WORKSPACE="$PWD/engagements/current/static"
export TERMINAL_MCP_WORKSPACE="$PWD/engagements/current"
export TERMINAL_MCP_ALLOWED_COMMANDS=adb,frida,jadx,apktool,pytest,redops
```

The placeholders above are illustrative only. Exegol remains the default even
when optional connector variables are present.
