# Claude Code 全局配置安装指南

> 将本仓库中 git 跟踪的配置文件（skills、CLAUDE.md、scripts 等），安装到新环境已有的 `~/.claude/` 目录中。
> 不改变 `~/.claude/` 的目录结构，只复制需要的文件进去。

## 仓库地址

```
git@github.com:312362115/claude.git
```

## 安装步骤

### 一键安装

```bash
# 克隆到临时目录
TMPDIR=$(mktemp -d)
git clone git@github.com:312362115/claude.git "$TMPDIR"

# 自动同步所有 git 跟踪的文件（排除 .gitignore、README.md、settings.json）
cd "$TMPDIR"
git ls-files | grep -v -E '^(\.gitignore|README\.md|settings\.json)$' | while read -r f; do
  mkdir -p ~/.claude/"$(dirname "$f")"
  cp "$f" ~/.claude/"$f"
done

# 合并 settings.json（需要 jq）
if command -v jq &>/dev/null; then
  LOCAL=~/.claude/settings.json
  REMOTE="$TMPDIR/settings.json"
  if [ -f "$LOCAL" ]; then
    # 将仓库的 enabledPlugins 和 extraKnownMarketplaces 合并到本地
    jq -s '.[0] * {
      enabledPlugins: (.[0].enabledPlugins // {} ) * (.[1].enabledPlugins // {}),
      extraKnownMarketplaces: (.[0].extraKnownMarketplaces // {}) * (.[1].extraKnownMarketplaces // {})
    }' "$LOCAL" "$REMOTE" > "$LOCAL.tmp" && mv "$LOCAL.tmp" "$LOCAL"
    echo "settings.json: 已合并 enabledPlugins 和 extraKnownMarketplaces"
  else
    cp "$REMOTE" "$LOCAL"
    echo "settings.json: 本地不存在，直接复制"
  fi
else
  echo "⚠ 未安装 jq，跳过 settings.json 合并。请手动处理或先安装 jq: brew install jq"
fi

# 清理临时目录
rm -rf "$TMPDIR"
```

这样无论后续新增多少 skill、script 或文档，只要提交到 git，安装脚本都会自动覆盖过去。

### 验证

```bash
ls ~/.claude/CLAUDE.md         # 全局规范
ls ~/.claude/skills/           # 自定义 skills
ls ~/.claude/scripts/          # 辅助脚本
```

## 让 Claude 帮你安装

在新环境的 Claude Code 中直接说：

> 请阅读 https://raw.githubusercontent.com/312362115/claude/main/README.md ，按照里面的步骤把配置安装到 ~/.claude/ 目录

## 更新配置

当仓库有更新时，重新执行一键安装脚本即可覆盖旧文件。

## 注意事项

- **不会覆盖** `config.json`（含 API key）、`projects/`（项目级 memory）等未入版本控制的运行时文件
- `settings.json` 采用合并策略：只将仓库中的 `enabledPlugins` 和 `extraKnownMarketplaces` 合并到本地，不覆盖本地其他设置
- 合并依赖 `jq`，macOS 安装：`brew install jq`，Linux：`apt install jq`
- 插件缓存（`plugins/cache/`）会由 Claude Code 根据 `settings.json` 自动下载
