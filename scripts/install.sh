#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-}"
TARGET_PROJECT="${2:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE="$REPO_ROOT/gaply-engineering-playbook"

if [[ ! -f "$SOURCE/SKILL.md" ]]; then
  echo "ERROR: Canonical skill not found at $SOURCE" >&2
  exit 1
fi

copy_skill() {
  local destination_root="$1"
  mkdir -p "$destination_root"
  rm -rf "$destination_root/gaply-engineering-playbook"
  cp -R "$SOURCE" "$destination_root/"
  echo "Installed: $destination_root/gaply-engineering-playbook"
}

case "$MODE" in
  claude-project)
    copy_skill "$TARGET_PROJECT/.claude/skills"
    ;;
  claude-global)
    copy_skill "$HOME/.claude/skills"
    ;;
  codex-project)
    copy_skill "$TARGET_PROJECT/.agents/skills"
    ;;
  codex-global)
    copy_skill "$HOME/.agents/skills"
    ;;
  *)
    cat <<USAGE
Usage:
  ./scripts/install.sh claude-project [/path/to/project]
  ./scripts/install.sh claude-global
  ./scripts/install.sh codex-project [/path/to/project]
  ./scripts/install.sh codex-global
USAGE
    exit 2
    ;;
esac
