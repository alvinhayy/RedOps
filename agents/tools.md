# Agent tooling and MCP wiring

Companion to [`registry.yaml`](registry.yaml). Tool names are requested capabilities,
not claims that a binary is installed. Agents must health-check inside the selected
Exegol image or approved MCP before use. If unavailable, use the bounded-terminal
fallback or report the capability gap; never silently use an unrestricted host shell.

`required` means the workflow pauses or reports a limitation when absent. `optional`
means the workflow may continue with a documented limitation.

## Sources

| Source | Use |
|---|---|
| Exegol | First-choice isolated CLI/tool execution; verify availability in the image |
| MCP | Burp, Camoufox, BloodHound, uiautomator2, Ghidra, or radare2 connector; verify health/capabilities |
| Local | RedOps/RAG helpers and explicitly approved workspace files through bounded argv |

### Generated CLI tool union

<!-- BEGIN GENERATED AGENT TOOL MATRIX -->
| Agent | Required tools (registry + owned skills) | Optional tools (registry + owned skills) |
|---|---|---|
| `orchestrator_agent` | `redops` | — |
| `ad_agent` | `bloodhound-python`, `impacket`, `ldapsearch`, `netexec`, `nmap` | `bloodyad`, `certipy`, `kerbrute` |
| `windows_redteam_agent` | `lolbas`, `powerview`, `seatbelt`, `winpeas` | `mimikatz` |
| `web_agent` | `burp`, `httpx`, `nmap` | `camoufox`, `ffuf`, `nuclei`, `xsrfprobe` |
| `cloud_agent` | `aws`, `az`, `gcloud` | `pacu`, `prowler`, `scoutsuite` |
| `mobile_agent` | `adb`, `apktool`, `file`, `find`, `frida`, `jadx`, `objection`, `rg`, `strings`, `unzip` | `afl-fuzz`, `androguard`, `baksmali`, `clang`, `class-dump`, `codesign`, `dex2jar`, `docker`, `drozer`, `ghidra`, `gitleaks`, `ios-deploy`, `llvm-objdump`, `make`, `ndk-build`, `nm`, `node`, `npx`, `otool`, `plutil`, `radare2`, `semgrep`, `timeout`, `trufflehog`, `uiautomator2` |
| `reversing_tools_agent` | `file`, `find`, `ghidra`, `objdump`, `radare2`, `strings`, `unzip` | `androguard`, `apktool`, `baksmali`, `capa`, `class-dump`, `codesign`, `dex2jar`, `docker`, `floss`, `gitleaks`, `jadx`, `node`, `npx`, `otool`, `plutil`, `rizin`, `trufflehog`, `yara` |
| `network_agent` | `netexec`, `nmap`, `tshark` | `masscan`, `responder`, `wireshark` |
| `container_devops_agent` | `docker`, `kubectl`, `trivy` | `grype`, `helm`, `kube-bench`, `syft` |
| `web3_agent` | `cast`, `mythril`, `slither` | `burp`, `echidna`, `foundry`, `semgrep` |
| `rag_curator_agent` | `markdown-tools`, `python`, `redops` | `jq`, `pandoc`, `ripgrep` |
<!-- END GENERATED AGENT TOOL MATRIX -->

## Profiles

### `orchestrator_agent`

- Required: RedOps CLI and `redops-rag` MCP.
- Role: classify the task, retrieve cited context, gate authorization, and delegate to
  the narrowest specialist. It does not execute target commands.
- Fallback: return a bounded routing plan from local retrieval when the specialist or
  provider is unavailable.

### `ad_agent`

- Required: `nmap`, `ldapsearch`, NetExec, Impacket, `bloodhound-python`.
- Optional: Kerbrute, Certipy, BloodyAD.
- Source/checks: Exegol (`command -v nmap ldapsearch netexec bloodhound-python`; `python -c 'import impacket'`).
- Fallback: offline LDAP/BloodHound export analysis. BloodHound data stays in the authorized AD scope.

### `windows_redteam_agent`

- Required: PowerView, Seatbelt, winPEAS, LOLBAS corpus.
- Optional: Mimikatz, only when explicitly authorized.
- Source/checks: Exegol or authorized Windows host; verify script/binary hash and non-invasive help/version.
- Fallback: static script review and RAG. A LOLBAS entry is not permission to execute it.

### `web_agent`

- Required: `nmap`, httpx, Burp MCP.
- Optional: Nuclei, Camoufox MCP, ffuf, XSRFProbe (`xsrfprobe`).
- Source/checks: Exegol (`command -v nmap httpx xsrfprobe`); Burp/Camoufox MCP health/capabilities; Nuclei/ffuf version check.
- Fallback: offline request/response and OpenAPI analysis; no traffic without confirmed scope.
- XSRFProbe guardrail: active CSRF checks only against disposable local/staging targets with explicit scope,
  bounded crawl/rate, and test accounts; review forms before submission and never target production/shared tenants.

### `cloud_agent`

- Required: AWS, Azure (`az`), and GCP (`gcloud`) clients.
- Optional: ScoutSuite, Prowler, Pacu.
- Source/checks: Exegol or bounded terminal for read-only exports; `command -v aws az gcloud` and provider identity checks only after scope confirmation.
- Fallback: offline IAM, IaC, and cloud-export review; no mutation by default.

### `mobile_agent`

- Required: ADB, JADX, apktool, Frida, Objection.
- Optional: uiautomator2 MCP, Ghidra MCP, radare2 MCP, ios-deploy, class-dump.
- Source/checks: Exegol (`adb devices -l`; `command -v jadx apktool frida objection`); MCP health/capabilities for device and reverse-engineering connectors.
- Fallback: static APK/AAB/IPA analysis. **BloodHound is forbidden for this profile.**

### `reversing_tools_agent`

- Required: Ghidra, radare2, `strings`, `objdump`.
- Optional: rizin, capa, YARA, FLOSS.
- Source/checks: Ghidra/radare2 MCP or Exegol; `command -v r2 strings objdump`; verify input hash before analysis.
- Fallback: offline strings/symbol/disassembly extraction; never launch unknown samples on the host.

### `network_agent`

- Required: `nmap`, NetExec, tshark.
- Optional: masscan, Wireshark, Responder.
- Source/checks: Exegol (`command -v nmap netexec tshark`); masscan only after explicit scoped CIDR/rate limit; tshark version for PCAP work.
- Fallback: offline banner/PCAP analysis. Masscan never runs outside declared scope.

### `container_devops_agent`

- Required: Docker, Trivy, kubectl.
- Optional: Helm, kube-bench, Syft, Grype.
- Source/checks: Exegol or disposable lab; `command -v docker trivy kubectl`; check selected context before `docker version`/`kubectl version --client`.
- Fallback: offline image/manifest/IaC scanning; no cluster mutation or image push.

### `web3_agent`

- Required: Slither, Mythril, Foundry `cast`.
- Optional: Foundry toolchain, Echidna, Burp MCP, Semgrep.
- Source/checks: Exegol (`command -v slither myth cast`); Burp/Ghidra/radare2 MCP capabilities when used.
- Fallback: offline source/bytecode review. Dynamic calls are testnet-only unless explicitly authorized; never expose private keys.

### `rag_curator_agent`

- Required: RedOps CLI, Python, Markdown tools.
- Optional: ripgrep, jq, Pandoc.
- Source/checks: local bounded terminal (`redops stats`; `python --version`; `command -v rg jq pandoc`). No target MCP.
- Fallback: standard-library Markdown/front-matter processing and `redops ingest`.
- Never execute code extracted from scraped pages; preserve provenance, licenses, hashes, and audit decisions.

## MCP boundary summary

- BloodHound Python (`bloodhound-python`): `ad_agent` only; graph UI/MCP is not required.
- Burp: web, mobile, and web3 profiles, each with separate traffic scope.
- Camoufox: web profile only.
- uiautomator2: mobile profile only.
- Ghidra/radare2: mobile, reversing, and web3 for local authorized artifacts.
- Terminal MCP: bounded argv/workspace fallback; never an unrestricted host shell.
