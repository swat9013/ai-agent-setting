#!/bin/bash
# AI Context Template Installer
# Downloads and sets up the template in your project

set -e

REPO="swat9013/ai-agent-setting"
BRANCH="main"

echo "=== AI Context Template Installer ==="
echo ""

# Check if already initialized
if [ -d ".ai" ]; then
    read -p ".ai directory already exists. Overwrite? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

# Download template
echo "Downloading template..."
curl -sL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" -o /tmp/ai-agent-setting.tar.gz

# Extract template/ directory
echo "Extracting..."
tar -xzf /tmp/ai-agent-setting.tar.gz -C /tmp

# Copy .ai and docs (exclude .gitignore to preserve existing one)
cp -r /tmp/ai-agent-setting-$BRANCH/template/.ai .
cp -r /tmp/ai-agent-setting-$BRANCH/template/docs .

# Copy .gitignore only if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cp /tmp/ai-agent-setting-$BRANCH/template/.gitignore .
fi

# Cleanup
rm -rf /tmp/ai-agent-setting.tar.gz /tmp/ai-agent-setting-$BRANCH

# Set permissions
chmod +x .ai/scripts/*.sh 2>/dev/null || true

echo ""
echo "Template installed successfully!"
echo ""

# Git hooks setup (optional)
if [ -d ".git" ]; then
    read -p "Setup Git hooks for automatic sync? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        bash .ai/scripts/setup-hooks.sh
    fi
fi

echo ""
echo "Next steps:"
echo "  1. Edit .ai/context.md to add your project context"
echo "  2. Run: python3 .ai/scripts/sync-context.py"
echo ""
echo "Done!"
