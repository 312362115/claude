# 分支管理与发布规范

## 分支策略

```
main（受保护，PR 合入，禁止直接 push）
  ├── feat/xxx     新功能
  ├── fix/xxx      Bug 修复
  └── refactor/xxx 重构清理
```

### 规则

- **main 分支**：始终保持可用状态，所有改动通过 PR 合入
- **功能分支**：从 main 切出，命名 `feat/<简短描述>`、`fix/<简短描述>`、`refactor/<简短描述>`
- **生命周期**：短命分支，完成后 PR 合入 main，合入后删除
- **合并方式**：单人开发用 squash merge，保持 main 历史干净；多人协作时按需选择

### 操作流程

```bash
# 1. 切出功能分支
git checkout -b feat/flowchart-direction main

# 2. 开发 + 提交（可以有多个 commit）
git add ... && git commit -m "feat(diagram): ..."

# 3. 推送 + 创建 PR
git push -u origin feat/flowchart-direction
gh pr create --title "feat(diagram): 流程图支持多方向布局"

# 4. Review + 合入（squash merge）
gh pr merge --squash

# 5. 清理
git checkout main && git pull
git branch -d feat/flowchart-direction
```

---

## 发布策略

### 版本号

采用**日期版本**，格式 `vYYYY.MM.DD`：

```
v2026.04.02   ← 第一个正式 release
v2026.04.15   ← 下次有实质性改动时
```

同一天有多个 release 时追加序号：`v2026.04.02.2`

### 发布时机

不固定周期，满足以下条件之一时发布：

- 完成一个有实际价值的功能（新图表类型、新 skill 能力等）
- 修复了影响使用的 bug
- 积累了一批小改动值得打包发布

### 发布流程

```bash
# 1. 确保 main 是最新的
git checkout main && git pull

# 2. 生成 changelog（从上次 tag 到现在）
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# 3. 打 tag
git tag -a v2026.04.02 -m "v2026.04.02: 流程图横向布局 + Graphviz 清理 + SKILL review"

# 4. 推送 tag
git push origin v2026.04.02

# 5. 创建 GitHub Release
gh release create v2026.04.02 --title "v2026.04.02" --notes "$(cat <<'EOF'
## Highlights

- **流程图多方向布局**：DAG 模式支持 DOWN/RIGHT/UP/LEFT，AI 自动选择合适流向
- **Deep-Research 清理 Graphviz**：删除 graphviz 依赖，图表生成统一对齐 Diagram skill
- **截图规范统一**：禁止手动 Playwright，收口到 capture.py/bridge.py
- **图表链路验证**：42/42 全量通过（10 统计图 + 29 结构图 + 3 PNG 抽样）

## Changes

（git log 输出粘贴到这里）
EOF
)"
```

### Release Notes 格式

```markdown
## Highlights
- 3-5 条核心改动，面向用户描述价值

## Changes
- 完整 commit 列表（从 git log 生成）

## Breaking Changes
- 如有不兼容变更，显著标注
```

---

## 注意事项

- 开发阶段（功能密集迭代期）可以在 main 直接 commit，但稳定后应切换到 PR 流程
- tag 一旦推送不要删除或移动，保持版本可追溯
- 不需要 CHANGELOG.md 文件，GitHub Releases 就是 changelog
