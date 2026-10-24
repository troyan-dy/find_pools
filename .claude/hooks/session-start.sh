#!/bin/bash
set -euo pipefail

# Only run in Claude Code cloud sessions
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

PYTHON_VERSION="3.15.1"
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

# Prefer uv (preinstalled in cloud containers); fall back to a fresh uv from pip
# if the bundled one does not know about the required Python release yet.
UV="uv"
if ! command -v uv >/dev/null 2>&1 || ! uv python install -q "$PYTHON_VERSION" 2>/dev/null; then
  python3 -m pip install -q --user -U uv 2>/dev/null \
    || python3 -m pip install -q --user --break-system-packages -U uv
  UV="python3 -m uv"
  $UV python install -q "$PYTHON_VERSION"
fi

if [ ! -x .venv/bin/python ] || ! .venv/bin/python -c "import sys; sys.exit(sys.version_info[:2] != (3, 15))"; then
  $UV venv -q --clear --seed -p "$PYTHON_VERSION" .venv
fi

$UV pip install -q -p .venv/bin/python -r requirements.txt -r resuirements.dev.txt

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export PATH=\"$PWD/.venv/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
  echo "export VIRTUAL_ENV=\"$PWD/.venv\"" >> "$CLAUDE_ENV_FILE"
fi
