#!/bin/bash
# PreToolUse hook: block destructive commands per team policy.
INPUT=$(cat)
COMMAND=$(printf '%s' "$INPUT" | python3 -c "import sys,json;print(json.load(sys.stdin).get('tool_input',{}).get('command','') or '')" 2>/dev/null)

if printf '%s' "$COMMAND" | grep -qE 'rm -rf|rm -fr|git push (--force|-f)|DROP TABLE|DROP DATABASE|mkfs'; then
  echo "Blocked by team policy (block-dangerous-commands): $COMMAND" >&2
  exit 2
fi
exit 0
