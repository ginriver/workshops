#!/bin/bash
# Stop hook: quality gate.
# The Agent may not finish while pytest is failing; exit 2 forces it to keep working.
input=$(cat)

# Prevent infinite loops: if this Stop hook already blocked once, allow completion.
stop_hook_active=$(printf '%s' "$input" | python3 -c "import sys,json;print(str(json.load(sys.stdin).get('stop_hook_active',False)).lower())" 2>/dev/null)
if [ "$stop_hook_active" = "true" ]; then
  exit 0
fi

cwd=$(printf '%s' "$input" | python3 -c "import sys,json;print(json.load(sys.stdin).get('cwd',''))" 2>/dev/null)
[ -n "$cwd" ] && cd "$cwd" 2>/dev/null

# Only act inside this repository.
if [ ! -d tests ]; then
  exit 0
fi

PY=python3
if [ -x .venv/bin/python ]; then
  PY=.venv/bin/python
fi

if ! "$PY" -m pytest -q > /tmp/cal-tracker-quality-gate.log 2>&1; then
  echo "Quality gate failed: pytest has failures. Fix them before completing (log: /tmp/cal-tracker-quality-gate.log)." >&2
  exit 2
fi
exit 0
