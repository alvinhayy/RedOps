#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REDOPS_REPO_URL:-https://github.com/alvinhayy/RedOps.git}"
REF="${REDOPS_REF:-master}"
INSTALL_ROOT="${REDOPS_INSTALL_ROOT:-${HOME}/.local/share/redops}"
BIN_DIR="${REDOPS_BIN_DIR:-${HOME}/.local/bin}"
RUNTIME_DIR="${REDOPS_RUNTIME_DIR:-${HOME}/.config/redops}"

die() { printf 'redops install: %s\n' "$*" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || die "python3 is required (3.11+)."
command -v git >/dev/null 2>&1 || die "git is required."

if [ -e "$INSTALL_ROOT" ] && [ ! -d "$INSTALL_ROOT/.git" ]; then
  die "install path exists but is not a RedOps checkout: $INSTALL_ROOT"
fi

mkdir -p "$(dirname "$INSTALL_ROOT")" "$BIN_DIR"
if [ -d "$INSTALL_ROOT/.git" ]; then
  git -C "$INSTALL_ROOT" fetch --depth 1 origin "$REF"
  git -C "$INSTALL_ROOT" checkout --detach "FETCH_HEAD"
else
  git clone --depth 1 --branch "$REF" "$REPO_URL" "$INSTALL_ROOT"
fi

python3 -m venv "$INSTALL_ROOT/.venv"
"$INSTALL_ROOT/.venv/bin/python" -m pip install --upgrade pip >/dev/null
"$INSTALL_ROOT/.venv/bin/python" -m pip install -e "$INSTALL_ROOT" >/dev/null
ln -sfn "$INSTALL_ROOT/.venv/bin/redops" "$BIN_DIR/redops"

# Install non-secret CLI adapters without replacing user-customized files.
"$BIN_DIR/redops" install-cli all >/dev/null

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

printf 'RedOps installed at %s\n' "$INSTALL_ROOT"
printf 'CLI: %s/redops\n' "$BIN_DIR"
printf 'RAG adapters: Codex, Claude CLI, and OpenCode\n'
printf 'Tool manifest: %s/agent-tools.yaml\n' "$RUNTIME_DIR"
printf 'MCP profile/config: %s/mcp-profiles.yaml and %s/mcp.json\n' "$RUNTIME_DIR" "$RUNTIME_DIR"
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
  printf 'Add to PATH: export PATH="%s:$PATH"\n' "$BIN_DIR"
fi
"$BIN_DIR/redops" providers
