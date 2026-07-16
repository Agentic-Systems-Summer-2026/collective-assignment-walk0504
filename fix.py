#!/usr/bin/env bash
# fix_imports.sh — make Python imports simple in this codespace.
# 1. Sets PYTHONPATH to the course repo in ~/.bashrc (idempotent)
# 2. Moves day2-minibuild into the repo, next to common/
# 3. Records the convention in the OpenClaw workspace AGENTS.md
# 4. Verifies that `import common.llm` works
set -euo pipefail

REPO="/workspaces/collective-assignment-walk0504"
WS="$HOME/.openclaw/workspace"
MINIBUILD_SRC="$WS/day2-minibuild"
MINIBUILD_DST="$REPO/day2-minibuild"

echo "== 1. PYTHONPATH in ~/.bashrc =="
LINE="export PYTHONPATH=\"$REPO\""
if grep -qF "$LINE" ~/.bashrc 2>/dev/null; then
  echo "Already present, skipping."
else
  printf '\n# Course repo modules (common/) importable from anywhere\n%s\n' "$LINE" >> ~/.bashrc
  echo "Added."
fi
export PYTHONPATH="$REPO"

echo "== 2. Move day2-minibuild into the repo =="
if [ -d "$MINIBUILD_DST" ]; then
  echo "$MINIBUILD_DST already exists, skipping move."
elif [ -d "$MINIBUILD_SRC" ]; then
  rm -rf "$MINIBUILD_SRC/__pycache__"
  mv "$MINIBUILD_SRC" "$MINIBUILD_DST"
  echo "Moved to $MINIBUILD_DST."
else
  echo "No $MINIBUILD_SRC found, skipping."
fi

echo "== 3. Record convention in workspace docs =="
NOTE="## Python convention
All Python that imports the course repo's \`common\` module lives inside the repo
($REPO), so plain \`python3 script.py\` works.
The .openclaw workspace is for notes and identity files only.
PYTHONPATH is set to the repo in ~/.bashrc as a fallback."
if grep -q "## Python convention" "$WS/AGENTS.md" 2>/dev/null; then
  echo "Convention already documented, skipping."
else
  printf '\n%s\n' "$NOTE" >> "$WS/AGENTS.md"
  echo "Appended to AGENTS.md."
fi

echo "== 4. Verify =="
if python3 -c "import common.llm" 2>/dev/null; then
  echo "OK: 'import common.llm' works."
else
  echo "WARNING: import failed. Check that $REPO/common/llm.py exists." >&2
  exit 1
fi

echo
echo "Done. Open a new terminal (or run: source ~/.bashrc), then:"
echo "  cd $MINIBUILD_DST && python3 workflow.py"
