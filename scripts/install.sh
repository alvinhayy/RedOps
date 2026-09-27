#!/usr/bin/env bash
set -euo pipefail

# Source checkout + tool/MCP setup only. No RedOps CLI, database, or provider setup.
repo_url="${REDOPS_REPO_URL:-https://github.com/alvinhayy/RedOps.git}"
repo_ref="${REDOPS_REF:-master}"
install_root="${REDOPS_INSTALL_ROOT:-${HOME}/.local/share/redops}"
script_path="${BASH_SOURCE[0]:-}"

log() { printf '[RedOps] %s\n' "$*"; }
warn() { printf '[RedOps] WARN: %s\n' "$*" >&2; }
ask() {
  if [[ "${REDOPS_AUTO_INSTALL_MCP:-ask}" == always ]]; then return 0; fi
  if [[ "${REDOPS_AUTO_INSTALL_MCP:-ask}" == never || ! -r /dev/tty ]]; then return 1; fi
  local reply
  read -r -p "$1 [y/N] " reply < /dev/tty
  [[ "$reply" =~ ^[Yy]([Ee][Ss])?$ ]]
}

command -v git >/dev/null || { warn 'git is required'; exit 1; }
command -v python3 >/dev/null || { warn 'python3 is required'; exit 1; }

if [[ -n "$script_path" && -f "$script_path" ]]; then
  project_root="$(cd "$(dirname "$script_path")/.." && pwd)"
  log "Using checkout: $project_root"
else
  project_root="$install_root"
  if [[ -e "$project_root" && ! -d "$project_root/.git" ]]; then
    warn "Install path exists but is not a Git checkout: $project_root"
    exit 1
  fi
  if [[ -d "$project_root/.git" ]]; then
    if [[ -n "$(git -C "$project_root" status --porcelain)" ]]; then
      warn "Install checkout has local changes; update manually: $project_root"
      exit 1
    fi
    log "Updating $project_root"
    git -C "$project_root" fetch --quiet --depth 1 origin "$repo_ref"
    git -C "$project_root" checkout --quiet --detach FETCH_HEAD
  else
    log "Fetching $repo_url ($repo_ref)"
    mkdir -p "$(dirname "$project_root")"
    git clone --quiet --depth 1 --branch "$repo_ref" "$repo_url" "$project_root"
  fi
fi

log 'Checking host tools (Exegol may provide missing specialist tools)'
python3 "$project_root/scripts/check_tools.py"

if command -v exegol >/dev/null; then
  log 'Exegol CLI found; verify Docker and container separately'
else
  warn 'Exegol CLI not found; follow https://docs.exegol.com/'
fi
if ! command -v herdr >/dev/null; then warn 'Herdr CLI not found; follow https://herdr.dev/'; fi
if ! command -v opencode >/dev/null; then warn 'OpenCode CLI not found; follow https://opencode.ai/docs/'; fi
if command -v redops >/dev/null; then
  warn "Legacy redops CLI remains on PATH ($(command -v redops)); this workspace does not use it"
fi

if ! command -v exegol-mcp >/dev/null; then
  if ask 'Install official Exegol MCP with pipx?'; then
    if command -v pipx >/dev/null; then pipx install exegol-mcp
    else warn 'pipx missing; install pipx, then run: pipx install exegol-mcp'; fi
  fi
fi
if command -v exegol-mcp >/dev/null; then
  python3 "$project_root/scripts/setup_mcp.py"
else
  warn 'Exegol MCP not configured; install exegol-mcp and rerun this script'
fi

log 'Validating agent resource and MCP wiring'
python3 "$project_root/scripts/check_tools.py" --wiring

log "Ready: open $project_root in Herdr/OpenCode; use /status then /solve"
