#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REDOPS_REPO_URL:-https://github.com/alvinhayy/RedOps.git}"
REF="${REDOPS_REF:-master}"
INSTALL_ROOT="${REDOPS_INSTALL_ROOT:-${HOME}/.local/share/redops}"
BIN_DIR="${REDOPS_BIN_DIR:-${HOME}/.local/bin}"

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
ln -sfn "$INSTALL_ROOT/scripts/claude-zai" "$BIN_DIR/claude-zai"
ln -sfn "$INSTALL_ROOT/scripts/redops-zai" "$BIN_DIR/redops-zai"

printf 'RedOps installed at %s\n' "$INSTALL_ROOT"
printf 'CLI: %s/redops\n' "$BIN_DIR"
printf 'Claude Z.ai launcher: %s/claude-zai\n' "$BIN_DIR"
printf 'RAG adapters: Codex, Claude CLI, and OpenCode\n'
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
  printf 'Add to PATH: export PATH="%s:$PATH"\n' "$BIN_DIR"
fi
"$BIN_DIR/redops" providers
