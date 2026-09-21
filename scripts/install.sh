#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REDOPS_REPO_URL:-https://github.com/alvinhayy/RedOps.git}"
REF="${REDOPS_REF:-master}"
INSTALL_ROOT="${REDOPS_INSTALL_ROOT:-${HOME}/.local/share/redops}"
BIN_DIR="${REDOPS_BIN_DIR:-${HOME}/.local/bin}"
RUNTIME_DIR="${REDOPS_RUNTIME_DIR:-${HOME}/.config/redops}"

if [[ -t 1 && "${REDOPS_COLOR:-auto}" != "never" ]] || [[ "${REDOPS_COLOR:-}" == "always" ]]; then
  C_RESET=$'\033[0m'; C_DIM=$'\033[2m'; C_BLUE=$'\033[36m'; C_GREEN=$'\033[32m'; C_YELLOW=$'\033[33m'; C_RED=$'\033[31m'
else
  C_RESET=''; C_DIM=''; C_BLUE=''; C_GREEN=''; C_YELLOW=''; C_RED=''
fi

START_TIME=$(date +%s)
phase=0
total_phases=7
log() { printf '%s[%s]%s %s\n' "$C_DIM$(date +%H:%M:%S)" "$1" "$C_RESET" "${*:2}"; }
phase() { phase=$((phase + 1)); log "${C_BLUE}${phase}/${total_phases}${C_RESET}" "$*"; }
ok() { log "${C_GREEN}OK${C_RESET}" "$*"; }
warn() { log "${C_YELLOW}WARN${C_RESET}" "$*" >&2; }
die() { log "${C_RED}FAIL${C_RESET}" "$*" >&2; exit 1; }
trap 'die "Installation failed near line ${LINENO}"' ERR

phase "Checking prerequisites"
command -v python3 >/dev/null 2>&1 || die "python3 is required (3.11+)."
command -v git >/dev/null 2>&1 || die "git is required."
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
ok "python ${python_version} and git detected"

if [ -e "$INSTALL_ROOT" ] && [ ! -d "$INSTALL_ROOT/.git" ]; then
  die "install path exists but is not a RedOps checkout: $INSTALL_ROOT"
fi

phase "Fetching RedOps sources"
mkdir -p "$(dirname "$INSTALL_ROOT")" "$BIN_DIR"
if [ -d "$INSTALL_ROOT/.git" ]; then
  git -C "$INSTALL_ROOT" fetch --quiet --depth 1 origin "$REF"
  git -C "$INSTALL_ROOT" checkout --quiet --detach "FETCH_HEAD"
  ok "updated ${REF} checkout"
else
  git clone --quiet --depth 1 --branch "$REF" "$REPO_URL" "$INSTALL_ROOT"
  ok "downloaded ${REF} checkout"
fi

phase "Creating isolated Python environment"
python3 -m venv "$INSTALL_ROOT/.venv"
"$INSTALL_ROOT/.venv/bin/python" -m pip install --upgrade pip >/dev/null 2>&1
ok "virtualenv ready"

phase "Installing RedOps CLI"
"$INSTALL_ROOT/.venv/bin/python" -m pip install -e "$INSTALL_ROOT" >/dev/null 2>&1
ln -sfn "$INSTALL_ROOT/.venv/bin/redops" "$BIN_DIR/redops"
ok "CLI linked at ${BIN_DIR}/redops"

phase "Configuring CLI adapters"
# Install non-secret CLI adapters without replacing user-customized files.
"$BIN_DIR/redops" install-cli all >/dev/null
ok "Codex, Claude CLI, and OpenCode adapters verified"

phase "Publishing agent manifests"
# Publish generated, non-secret tool/MCP manifests for agents and CLI clients.
mkdir -p "$RUNTIME_DIR"
cp "$INSTALL_ROOT/agents/agent-tools.generated.yaml" "$RUNTIME_DIR/agent-tools.yaml"
cp "$INSTALL_ROOT/agents/mcp-profiles.yaml" "$RUNTIME_DIR/mcp-profiles.yaml"
cat > "$RUNTIME_DIR/mcp.json" <<EOF
{
  "mcpServers": {
    "redops-exegol": {
      "command": "$BIN_DIR/redops",
      "args": ["exegol-mcp"]
    }
  }
}
EOF
ok "tool and Exegol MCP manifests written"

phase "Verifying installation"
provider_count=$("$BIN_DIR/redops" providers | wc -l | tr -d ' ')
ok "${provider_count} providers registered"
if [ -x "$(command -v exegol 2>/dev/null || true)" ]; then
  ok "Exegol CLI detected (runtime remains opt-in)"
else
  warn "Exegol CLI not found; local backend remains the default"
fi
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
  warn "add to PATH: export PATH=\"${BIN_DIR}:\$PATH\""
fi
elapsed=$(( $(date +%s) - START_TIME ))
printf '\n%sRedOps installation complete%s (%ss)\n' "$C_GREEN" "$C_RESET" "$elapsed"
printf '  CLI       %s/redops\n' "$BIN_DIR"
printf '  Adapters  Codex · Claude CLI · OpenCode\n'
printf '  Tools     %s/agent-tools.yaml\n' "$RUNTIME_DIR"
printf '  MCP       %s/mcp.json\n' "$RUNTIME_DIR"
printf '  Next      redops status  |  redops interactive\n'
