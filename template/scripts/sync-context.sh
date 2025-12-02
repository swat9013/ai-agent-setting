#!/bin/bash
# Sync .ai/context.md to tool-specific files

set -e

SOURCE=".ai/context.md"
AGENTS_DIR=".ai/agents"

if [ ! -f "$SOURCE" ]; then
    echo "Error: $SOURCE not found"
    exit 1
fi

echo "=== Syncing context files ==="

# Line count check
LINE_COUNT=$(wc -l < "$SOURCE" | tr -d ' ')
if [ "$LINE_COUNT" -gt 300 ]; then
    echo "Warning: context.md is $LINE_COUNT lines (target: 200, max: 300)"
    echo "Consider running compression"
elif [ "$LINE_COUNT" -gt 200 ]; then
    echo "Note: context.md is $LINE_COUNT lines (target: 200)"
fi

# Cursor
cp "$SOURCE" .cursorrules 2>/dev/null && echo "Synced: .cursorrules"

if [ -d "$AGENTS_DIR" ]; then
    mkdir -p .cursor/rules
    for f in "$AGENTS_DIR"/*.md; do
        [ -f "$f" ] && cp "$f" .cursor/rules/ 2>/dev/null
    done
    echo "Synced: .cursor/rules/"
fi

# GitHub Copilot
mkdir -p .github
cp "$SOURCE" .github/copilot-instructions.md && echo "Synced: .github/copilot-instructions.md"

# Claude Code
cp "$SOURCE" CLAUDE.md
if [ -d "$AGENTS_DIR" ]; then
    echo -e "\n---\n\n# Agents" >> CLAUDE.md
    for f in "$AGENTS_DIR"/*.md; do
        if [ -f "$f" ]; then
            echo "" >> CLAUDE.md
            cat "$f" >> CLAUDE.md
            echo "" >> CLAUDE.md
        fi
    done
    echo "Synced: CLAUDE.md (with agents)"
else
    echo "Synced: CLAUDE.md"
fi

echo ""
echo "=== Sync completed! ==="
