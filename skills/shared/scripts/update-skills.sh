#!/bin/bash
# 更新本地 skill 到远端最新版本
# 用法：update-skills.sh [skill-name]
# 无参数: 更新全部
# 指定名称: 只更新该 skill

set -euo pipefail

CLAUDE_DIR="$HOME/.claude"

# 确保工作区干净
if ! git -C "$CLAUDE_DIR" diff --quiet skills/; then
  echo "skills/ 目录有未提交的改动，请先提交或暂存后再更新。"
  echo "运行 git -C ~/.claude stash 暂存改动"
  exit 1
fi

# 拉取最新
echo "拉取远端最新版本..."
git -C "$CLAUDE_DIR" fetch origin main --quiet 2>/dev/null || {
  echo "无法连接远端仓库，请检查网络。"
  exit 1
}

TARGET="${1:-}"

if [ -n "$TARGET" ]; then
  # 更新单个 skill
  if [ ! -d "$CLAUDE_DIR/skills/$TARGET" ]; then
    echo "skill '$TARGET' 不存在。"
    exit 1
  fi
  echo "更新 $TARGET..."
  git -C "$CLAUDE_DIR" checkout origin/main -- "skills/$TARGET/"
  echo "$TARGET 已更新。"
else
  # 更新全部
  echo "更新全部 skills..."
  git -C "$CLAUDE_DIR" checkout origin/main -- skills/
  echo "全部 skills 已更新。"
fi

# 显示更新后的版本
echo ""
echo "当前版本："
for skill_dir in "$CLAUDE_DIR"/skills/*/; do
  [ -f "$skill_dir/SKILL.md" ] || continue
  name=$(basename "$skill_dir")
  [ "$name" = "shared" ] && continue
  version=$(grep -m1 '^version:' "$skill_dir/SKILL.md" 2>/dev/null | sed 's/version:[[:space:]]*//' || echo "—")
  printf "  %-16s %s\n" "$name" "$version"
done
