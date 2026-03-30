#!/bin/bash
# PostToolUse hook: detect .md file writes and notify Claude to ask user about preview
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_response.filePath // ""')

if [[ "$file_path" == *.md ]]; then
    cat <<EOF
{"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "刚才写入了 markdown 文件: $file_path — 请询问用户是否要在浏览器中打开预览。如果用户确认，运行: python3 ~/.claude/skills/preview-md/scripts/md-preview.py \"$file_path\""}}
EOF
fi
