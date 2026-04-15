#!/bin/bash
# Auto-sync workspace to GitHub cada 2 horas
WORKSPACE="/root/.openclaw/workspace"
cd "$WORKSPACE" || exit 1

# Check if there are changes
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M') UTC" 2>/dev/null
    git push origin master 2>&1
fi
