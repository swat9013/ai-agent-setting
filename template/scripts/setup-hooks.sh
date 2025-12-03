#!/bin/bash
# Setup Git hooks for automatic context sync

set -e

HOOKS_DIR=".git/hooks"
PRE_COMMIT="$HOOKS_DIR/pre-commit"

if [ ! -d ".git" ]; then
    echo "Error: Not a git repository"
    exit 1
fi

echo "=== Setting up Git hooks ==="

# Create hooks directory if needed
mkdir -p "$HOOKS_DIR"

# Create or append to pre-commit hook
if [ -f "$PRE_COMMIT" ]; then
    # Check if already configured
    if grep -q "sync-context" "$PRE_COMMIT"; then
        echo "Pre-commit hook already configured"
        exit 0
    fi
    echo "" >> "$PRE_COMMIT"
    echo "# AI Context sync" >> "$PRE_COMMIT"
else
    echo "#!/bin/bash" > "$PRE_COMMIT"
    echo "" >> "$PRE_COMMIT"
    echo "# AI Context sync" >> "$PRE_COMMIT"
fi

cat >> "$PRE_COMMIT" << 'EOF'
if [ -f "scripts/sync-context.py" ]; then
    python3 scripts/sync-context.py
    git add AGENTS.md CLAUDE.md \
        .cursor/rules/ .cursor/commands/ \
        .github/instructions/ \
        .claude/commands/ .claude/agents/ 2>/dev/null || true
fi
EOF

chmod +x "$PRE_COMMIT"

echo "Created: $PRE_COMMIT"
echo ""
echo "Git hooks setup complete!"
echo "Context will be synced automatically on commit."
