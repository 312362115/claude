#!/bin/bash
# 检查本地 skill 是否有远端更新
# 用法：
#   check-updates.sh                  # 检查全部，有更新时输出详情
#   check-updates.sh --skill <name>   # 只检查单个 skill（skill 执行后自动调用）
#   check-updates.sh --force          # 忽略缓存强制检查
#
# 频次控制：默认每天最多 fetch 一次，用时间戳文件缓存

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"
SKILLS_DIR="$CLAUDE_DIR/skills"
CACHE_FILE="$CLAUDE_DIR/.skill-update-check"
CHECK_INTERVAL=86400  # 24 小时（秒）

SKILL_FILTER=""
FORCE=false

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --skill) SKILL_FILTER="$2"; shift 2 ;;
    --force) FORCE=true; shift ;;
    *) shift ;;
  esac
done

# 频次控制：检查是否需要 fetch
need_fetch=true
if [ "$FORCE" = false ] && [ -f "$CACHE_FILE" ]; then
  last_check=$(cat "$CACHE_FILE" 2>/dev/null || echo "0")
  now=$(date +%s)
  elapsed=$((now - last_check))
  if [ "$elapsed" -lt "$CHECK_INTERVAL" ]; then
    need_fetch=false
  fi
fi

if [ "$need_fetch" = true ]; then
  # 静默 fetch，超时 5 秒
  if git -C "$CLAUDE_DIR" fetch origin main --quiet 2>/dev/null; then
    date +%s > "$CACHE_FILE"
  else
    # 网络失败时静默退出，不阻塞 skill 执行
    exit 0
  fi
fi

updates=()
details=()

check_skill() {
  local skill_name="$1"
  local skill_dir="$SKILLS_DIR/$skill_name"

  [ -f "$skill_dir/SKILL.md" ] || return

  # 读取本地版本
  local local_version
  local_version=$(grep -m1 '^version:' "$skill_dir/SKILL.md" 2>/dev/null | sed 's/version:[[:space:]]*//' || echo "")
  [ -z "$local_version" ] && return

  # 读取远端版本
  local remote_content
  remote_content=$(git -C "$CLAUDE_DIR" show "origin/main:skills/$skill_name/SKILL.md" 2>/dev/null || echo "")
  [ -z "$remote_content" ] && return

  local remote_version
  remote_version=$(echo "$remote_content" | grep -m1 '^version:' | sed 's/version:[[:space:]]*//' || echo "")
  [ -z "$remote_version" ] && return

  if [ "$local_version" != "$remote_version" ]; then
    updates+=("$skill_name ($local_version → $remote_version)")

    # 读取远端 CHANGELOG 中最新版本的变更
    local remote_changelog
    remote_changelog=$(git -C "$CLAUDE_DIR" show "origin/main:skills/$skill_name/CHANGELOG.md" 2>/dev/null || echo "")
    if [ -n "$remote_changelog" ]; then
      local changelog_block
      changelog_block=$(echo "$remote_changelog" | awk '/^## /{n++} n==1' | tail -n +2)
      details+=("$skill_name  $local_version → $remote_version")
      if [ -n "$changelog_block" ]; then
        while IFS= read -r line; do
          details+=("  $line")
        done <<< "$changelog_block"
      fi
      details+=("")
    fi
  fi
}

if [ -n "$SKILL_FILTER" ]; then
  check_skill "$SKILL_FILTER"
else
  for skill_dir in "$SKILLS_DIR"/*/; do
    [ -f "$skill_dir/SKILL.md" ] || continue
    skill_name=$(basename "$skill_dir")
    [ "$skill_name" = "shared" ] && continue
    check_skill "$skill_name"
  done
fi

# 输出结果
if [ ${#updates[@]} -eq 0 ]; then
  # 无更新时不输出任何内容（不干扰 skill 正常输出）
  exit 0
fi

if [ -n "$SKILL_FILTER" ]; then
  # 单 skill 模式：一行提示
  echo "update: ${updates[0]}，仓库: https://github.com/312362115/claude"
  echo "更新命令: ~/.claude/skills/shared/scripts/update-skills.sh $SKILL_FILTER"
else
  # 全量模式：详细输出
  echo "有 ${#updates[@]} 个 skill 可更新："
  echo ""
  for line in "${details[@]}"; do
    echo "$line"
  done
  echo "更新命令: ~/.claude/skills/shared/scripts/update-skills.sh [skill-name|--all]"
fi
