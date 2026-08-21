#!/usr/bin/env bash
# macOS / Linux Bash wrapper for sync_agent_template.py
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/sync_agent_template.py"

python3 "$PY_SCRIPT" "$@"
exit $?
