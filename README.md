<h1 align="center">
  <img src="assets/banner.svg?v=acffd23" alt="RedOps / Red Team Operators" width="900"><br>
</h1>

<h4 align="center">RedOps / Red Team Operators — source-grounded pentest knowledge, agent workflows, and safe tool execution.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/platform-Python%203.11%2B-blue">
  <img src="https://img.shields.io/badge/index-SQLite%20FTS5-6f42c1">
  <img src="https://img.shields.io/badge/providers-Z.ai%20%7C%20DeepSeek%20%7C%20OrcaRouter-orange">
  <img src="https://img.shields.io/badge/execution-Exegol-green">
  <img src="https://img.shields.io/badge/license-MIT-blue">
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#rag-mcp">RAG MCP</a> •
  <a href="#agent-cli-integrations">CLI Integrations</a> •
  <a href="#safety-boundary">Safety</a>
</p>

---

RedOps (**Red Team Operators**) adalah framework RAG lokal untuk knowledge pentest yang
dapat ditelusuri kembali ke sumbernya. Gunakan hanya pada sistem yang Anda miliki atau
memiliki izin eksplisit untuk diuji.

## Features

- ingestion Markdown yang idempotent dan heading-aware;
- dual-corpus RAG untuk teknik/metodologi (`knowledge/`) dan writeup (`writeups/`);
- hybrid retrieval: SQLite FTS5 + cosine vector dengan reciprocal-rank fusion;
- embedding hashing lokal tanpa API sebagai konfigurasi awal;
- adaptor embedding dan chat API yang kompatibel dengan OpenAI;
- jawaban dengan sitasi dan fallback extractive saat tidak ada LLM;
- CLI dan REST API FastAPI;
- MCP RAG read-only (`redops rag-mcp`) untuk pencarian knowledge/writeup;
- backend eksekusi tool lokal atau Exegol dengan argv aman tanpa shell;
- 10 profil agent berbasis niche dengan wiring Exegol dan tool yang eksplisit;
- provenance berupa judul, heading, path lokal, dan URL asli;
- provider registry untuk local extractive, OpenAI, Z.ai, DeepSeek, dan OrcaRouter;
- installer adapter native untuk Codex, Claude CLI, OpenCode, ZCode, Cursor, Gemini,
  Copilot, Windsurf, Amp, dan Crush;
- bounded WAF timing benchmark dengan guardrail anti-DoS.

## Agent Profiles

RedOps bukan mobile-only. Router agent membaca niche knowledge, tool, MCP, dan guardrail
masing-masing dari [`agents/registry.yaml`](agents/registry.yaml):

| Agent | Fokus | Profil |
|---|---|---|
| AD | Active Directory, Entra ID, BloodHound, LDAP | [`ad.md`](agents/ad.md) |
| Windows Red Team | Windows recon, privilege escalation, LOLBAS | [`windows-redteam.md`](agents/windows-redteam.md) |
| Web | Web app, API, browser, WAF, CSRF/XSRF | [`web.md`](agents/web.md) |
| Cloud | AWS, Azure, GCP, IAM, storage, workload | [`cloud.md`](agents/cloud.md) |
| Mobile | Android/iOS, Frida, APK/IPA, runtime | [`mobile.md`](agents/mobile.md) |
| Reversing | Binary analysis, malware triage, Ghidra/radare2 | [`reversing-tools.md`](agents/reversing-tools.md) |
| Network | Network, protocol, wireless, pivoting | [`network.md`](agents/network.md) |
| Container/DevOps | Docker, Kubernetes, CI/CD, supply chain | [`container-devops.md`](agents/container-devops.md) |
| Web3 | Smart contract, DeFi, wallet, DApp | [`web3.md`](agents/web3.md) |
| RAG Curator | Ingest, niche classification, noise cleanup, QA | [`rag-curator.md`](agents/rag-curator.md) |

Semua agent mendapatkan MCP `redops-rag` untuk retrieval knowledge/writeup. Exegol tetap
menjadi backend eksekusi utama; connector lain hanya dipakai jika profil dan scope
membutuhkannya. Lihat [tool matrix](agents/skill-tool-matrix.yaml) dan
[MCP setup](docs/MCP-SETUP.md).

### Skills

Skill dipilih berdasarkan task, bukan dipasang ke semua agent:

| Skill | Agent utama | Kegunaan |
|---|---|---|
| `mobile-vuln-hunt` | Mobile | Hunt vulnerability Android/iOS dari hasil decompile dan runtime lab |
| `reverse-engineer` | Reversing, Mobile | Static analysis APK/IPA/native/bundled web |
| `afl-fuzzing` | Mobile | Greybox fuzzing native Android dengan AFL++ |
| `flutter-dart-code-review` | Mobile | Review keamanan dan kualitas Flutter/Dart |
| `browser-vuln-hunting` | Web | Riset vulnerability browser dan PoC terisolasi |
| `orchestration` | Semua agent | Dispatch, status, dan koordinasi worker |

### MCP

Deployment RedOps menggunakan MCP read-only untuk knowledge dan MCP eksekusi terisolasi:

| MCP | Peran |
|---|---|
| **RedOps RAG** | Retrieval teknik/metodologi dan writeup dengan provenance; tidak menjalankan command |
| **Exegol MCP** | Menyediakan environment CLI terisolasi untuk tool agent; command diteruskan sebagai argv tanpa shell |

### CLI tools per agent

Daftar berikut dihasilkan otomatis dari registry agent dan skill matrix, sehingga required/
optional tools milik skill selalu ikut ke agent pemiliknya:

<!-- BEGIN GENERATED AGENT TOOLS -->
| Agent | Required tools (registry + owned skills) | Optional tools (registry + owned skills) |
|---|---|---|
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
<!-- END GENERATED AGENT TOOLS -->

Regenerasi setelah mengubah registry atau skill:

```bash
python scripts/sync_agent_tools.py
python scripts/sync_agent_tools.py --check
```

Slash command skill juga ditemukan otomatis oleh `redops install-cli claude` dan
`redops install-cli opencode`: setiap file Markdown di `commands/` (termasuk
`.agents/commands/` pada repository skill) disalin apa adanya. RedOps memindai
skill di direktori kerja, `~/.agents`, dan `~/.codex`; tambahkan lokasi lain dengan
`--skill-path` atau `REDOPS_SKILL_PATHS` (dipisahkan `:` di macOS/Linux). File
command yang sudah ada tidak ditimpa kecuali memakai `--force`.

Tool names are capability requirements; health-check them inside Exegol before use.
Install only what the approved engagement needs and keep credentials outside the corpus.

## Installation

RedOps dapat dipasang sebagai CLI mandiri dengan Python 3.11+:

One-liner (macOS/Linux):

```bash
curl -fsSL https://raw.githubusercontent.com/alvinhayy/RedOps/master/scripts/install.sh | bash
```

Installer menyimpan checkout di `~/.local/share/redops` dan CLI di
`~/.local/bin`. Selain RedOps, adapter `redops-rag` dipasang ke provider CLI yang
didukung secara idempoten. Override dengan `REDOPS_INSTALL_ROOT`,
`REDOPS_BIN_DIR`, `REDOPS_RUNTIME_DIR`, atau `REDOPS_REF`. Installer juga menulis
manifest tools dan konfigurasi MCP Exegol non-secret ke `~/.config/redops/`. Tool
assessment seperti `bloodhound-python` dijalankan di image Exegol/lingkungan yang
disetujui; installer tidak memasang tool ofensif ke host secara diam-diam. Installer
tidak menghapus data dan tidak melakukan `git reset --hard`.

Pada terminal interaktif, installer memeriksa required/optional tools dan menawarkan
instalasi dependency Python yang didukung dengan konfirmasi `y/n`. Tekan `n` untuk
melewati dan gunakan Exegol. MCP mobile `uiautomator2` juga opsional dan ditawarkan
terpisah. Untuk otomasi CI, gunakan `REDOPS_AUTO_INSTALL_TOOLS=never|always` dan
`REDOPS_AUTO_INSTALL_MCP=never|always`.

Manual dengan pipx:

```bash
pipx install git+https://github.com/alvinhayy/RedOps.git
# atau dari checkout lokal:
pip install -e '.[dev]'
```

Periksa instalasi dan daftar provider:

```bash
redops --help
redops providers
```

## Quick Start

Persyaratan: Python 3.11+ dan SQLite yang mendukung FTS5.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
redops ingest
redops stats
redops query "Bagaimana melakukan enumerasi Active Directory?"
# Batasi retrieval ke corpus tertentu
redops query "jalur privilege escalation Linux" --corpus knowledge
redops query "kasus serupa" --corpus writeups
```

Lihat status runtime tanpa menampilkan secret, atau gunakan shell interaktif:

```bash
redops status
redops interactive
redops rag-mcp
```

Di shell interaktif, masukkan pertanyaan langsung. Gunakan `/help`, `/status`,
`/stats`, `/sources`, `/generate`, `/extractive`, atau `/quit`.

Variabel `.env` tidak otomatis dimuat oleh aplikasi. Ekspor variabel yang diperlukan,
atau jalankan dengan alat seperti `dotenv`/Docker Compose. Default aman dan lokal bisa
langsung dipakai tanpa `.env`.

## Agent CLI Integrations

Installer membuat skill/command kecil yang memanggil CLI RedOps, tanpa menyalin secret
atau mengubah konfigurasi provider. Jalankan dry-run lebih dahulu:

```bash
redops install-cli all --dry-run
redops install-cli codex
redops install-cli claude
redops install-cli opencode
# Jalankan dari checkout skill, atau tunjukkan root skill secara eksplisit
redops install-cli all --skill-path /path/to/Mobile-ReverseSkill
```

Target default mencakup `~/.codex`, `~/.claude`, `~/.config/opencode`, `~/.agents`,
`~/.cursor`, dan `~/.gemini`. Gunakan `--workspace /path/to/project` untuk menghasilkan
format workspace-only Copilot (`.github/prompts`) dan Windsurf (`.windsurf/workflows`).
Override path dengan `CODEX_HOME`, `CLAUDE_HOME`, `OPENCODE_HOME`, `AGENTS_HOME`,
`CURSOR_HOME`, atau `GEMINI_HOME`; gunakan `--force` hanya jika ingin mengganti adapter
yang sudah ada. Detail format provider tersedia di [`docs/providers.md`](docs/providers.md).
Setelah instalasi, restart CLI terkait agar skill/command baru dimuat. Konfigurasi MCP
non-secret ditulis ke `~/.config/redops/mcp.json`.

Untuk menjalankan API:

```bash
redops serve --host 0.0.0.0 --port 8000
curl -s http://localhost:8000/health
curl -s http://localhost:8000/v1/query \
  -H 'content-type: application/json' \
  -d '{"question":"Jelaskan jalur enumerasi LDAP", "top_k":6}'
```

Dokumentasi interaktif tersedia di `http://localhost:8000/docs`.

## Exegol Tool Execution

Exegol harus sudah terpasang dan container telah disiapkan sesuai dokumentasi resmi
di [docs.exegol.com](https://docs.exegol.com/). Gunakan hanya terhadap target dengan
otorisasi tertulis. RedOps tidak mengubah isolasi, jaringan, atau hak akses Exegol.

```bash
export REDOPS_EXECUTION_BACKEND=exegol
export REDOPS_EXEGOL_CONTAINER=redops
export REDOPS_EXEGOL_IMAGE=full
export REDOPS_EXEGOL_TIMEOUT=120
redops exegol status
redops exegol exec -- nmap -sV 192.0.2.10
```

`redops exegol exec -- ...` meneruskan setiap argumen sebagai daftar argv dan tidak
menjalankan shell. `REDOPS_EXEGOL_TMP=true` meneruskan opsi temporary container dan
`REDOPS_EXEGOL_VERBOSE=true` meneruskan verbose ke Exegol. Backend default tetap `local`;
set `REDOPS_EXECUTION_BACKEND=exegol` secara eksplisit untuk menggunakan Exegol.

## Agent mobile

Gunakan [`agents/mobile.md`](agents/mobile.md) dan [dokumentasi mobile](docs/mobile-agent.md)
untuk workflow APK/AAB/IPA: detect stack, static analysis, attack-surface review,
vulnerability hunt, konfirmasi Frida/Exegol di lab lokal, dan fuzzing native
opsional pada emulator offline. Static analysis tidak menjalankan aplikasi target;
semua pengujian harus memiliki otorisasi tertulis.

Runtime Android bersifat opsional dan dilakukan pada emulator/device lab yang disposable.
Exegol tetap diprioritaskan untuk tool CLI; `uiautomator2` hanya ditambahkan jika MCP
mobile tersebut memang dibutuhkan.

## RAG MCP

RedOps menyediakan MCP read-only yang mengikuti pola dual-corpus RedDelta: corpus teknik
di `knowledge/` dan corpus writeup di `writeups/`. Jalankan melalui stdio:

```bash
redops rag-mcp
```

Tool yang tersedia adalah `search_knowledge`, `search_writeups`, dan `knowledge_stats`.
MCP ini hanya mengambil sumber yang sudah diindeks dan mengembalikan provenance RedOps;
ia tidak dapat menjalankan Exegol, mengubah target, atau membaca API key. Setelah menambah
atau membersihkan Markdown, rebuild index:

```bash
redops ingest --force
redops stats
```

### MCP Exegol

Untuk produksi, gunakan paket resmi Exegol MCP (`pipx install exegol-mcp`) dan
ikuti `exegol-mcp --print-config`. Endpoint HTTP dan bearer token harus dikelola
oleh secret manager atau environment eksternal; RedOps tidak menyimpan token.
RedOps menyediakan adapter stdio opsional yang tipis:

```bash
export REDOPS_EXECUTION_BACKEND=exegol
redops exegol-mcp
```

Adapter hanya menyediakan `exegol_status` dan `exegol_exec` (command wajib berupa
list argv, tanpa shell). Contoh konfigurasi klien:

```json
{"mcpServers":{"redops-rag":{"command":"redops","args":["rag-mcp"]},"redops-exegol":{"command":"redops","args":["exegol-mcp"]}}}
```

## Model Providers

RedOps mendukung provider yang tersedia di konfigurasi OpenCode: local extractive, OpenAI,
Z.ai/GLM, DeepSeek, dan OrcaRouter. Lihat [docs/providers.md](docs/providers.md) untuk
environment variable, model selector, dan command CLI masing-masing provider. Registry dapat
dilihat tanpa menampilkan secret:

```bash
redops providers
redops providers --json
```

## WAF Timing Benchmark (Bounded)

RedOps menyediakan benchmark timing untuk target yang telah diotorisasi. Amplifikasi
hanya memakai URL response yang dipilih eksplisit, maksimum 30 sampel, delay minimum
100 ms, dan batas ukuran response. Payload besar, POST/DoS, IP rotation, dan cross-site
timing tidak diimplementasikan. `--lab-mode` hanya memperbolehkan amplifier lokal/private
atau URL yang dimasukkan ke allowlist untuk staging/lab milik sendiri.

```bash
redops waf benchmark \
  --baseline-url https://staging.example.test/normal \
  --test-url https://staging.example.test/test \
  --amplifier-url https://staging.example.test/long-response \
  --allowlist https://staging.example.test/ --samples 10 --delay 1
```

Gunakan hanya pada aplikasi milik sendiri atau engagement dengan izin tertulis.

Default `hash` bersifat ringan dan cukup untuk bootstrap, tetapi model embedding khusus
akan meningkatkan relevansi semantik. Endpoint OpenAI resmi maupun server lokal yang
menyediakan API kompatibel dapat digunakan:

```bash
export REDOPS_EMBEDDING_PROVIDER=openai
export REDOPS_EMBEDDING_MODEL=text-embedding-3-small
export REDOPS_LLM_PROVIDER=openai
export REDOPS_LLM_MODEL=gpt-4.1-mini
export REDOPS_API_BASE_URL=https://api.openai.com/v1
export REDOPS_API_KEY='...'
redops ingest --force
redops query "Apa indikator delegation yang berisiko?"
```

Jangan commit API key. Perubahan provider/model/dimensi embedding memerlukan
`redops ingest --force` agar query dan index tetap konsisten.

## Knowledge Format

Semua `knowledge/**/*.md` dan, jika tersedia, `writeups/**/*.md` akan diindeks. Front matter berikut direkomendasikan agar
sitasi mengarah ke sumber asli:

```markdown
---
title: Kerberos Delegation
source_url: https://example.org/original-page
fetched_at: 2026-09-20T00:00:00Z
---

# Kerberos Delegation
...
```

Corpus dan alat refresh di dalam `knowledge/` serta `writeups/` dikelola terpisah dari
framework. Setelah refresh, jalankan `redops ingest`; hanya dokumen berubah yang dihitung
ulang. Gunakan `--corpus knowledge` atau `--corpus writeups` pada query untuk membatasi
retrieval.

## Testing

```bash
pytest
ruff check .
```

## Design Notes

Backend SQLite melakukan pemindaian vector in-process dan menyimpan metadata corpus.
Ini sederhana dan ideal untuk corpus dokumentasi kecil/menengah. Untuk jutaan chunk,
implementasikan backend `IndexStore` dengan vector database tanpa mengubah antarmuka
service/API. Fallback extractive bukan LLM: ia mengembalikan cuplikan sumber, sehingga
selalu eksplisit dan dapat diverifikasi.

## Safety Boundary

- Scope, authorization, and test accounts must be confirmed before active traffic.
- Exegol is the preferred execution backend; commands are passed as argv without a shell.
- Mobile and WAF workflows are limited to disposable local/staging environments where noted.
- Do not commit API keys, MCP tokens, credentials, session cookies, or engagement data.
- Review the relevant agent profile in [`agents/`](agents/) before delegating work.
