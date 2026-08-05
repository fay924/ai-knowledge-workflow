# Daily Echo 模块

每条成功写入的新笔记都接受一次连接扫描。默认只读分析；任何 Notion 更新仍须用户确认。

## 执行顺序

1. 运行 `python3 scripts/echo_state.py pending` 读取全部 `queued` 和 `error` 记录。
2. 读取新页面的标题、正文、来源、关联和时间。
3. 提取 3–6 个有区分度的主题、对象、目标、问题或动作。
4. 搜索 Notes 和 Projects；存在 Tasks、Ideas、AI 方法与实验库时一并搜索。需要理解上下文时再读取 Areas、Resources。
5. 排除当前页面、纯标题相似项和只有共同大类的内容。
6. 读取候选的足够正文和属性，确认连接真实存在。
7. 标记 `collision_found`、`no_collision` 或 `error`，展示后标记 `mark-shown`。

## 有效连接

至少满足一项：

- 互补：合并后形成更完整的方法或方案。
- 矛盾：新旧判断冲突，值得重新决策或验证。
- 推进：新笔记能解除现有项目的阻塞。
- 复用：旧方法能用于新场景，并能说明具体用法。
- 证据：新内容支持、削弱或更新旧结论。
- 行动汇合：多条材料已经足以形成一次具体测试或下一步。

只有相同词语、同一宽泛主题或无法产生新判断，不算有效连接。

## 展示

标题使用 `每日回响｜YYYY-MM-DD`。每条新笔记最多展示 3 个历史对象和 2 项行动建议，必须说明“为什么有关”。没有有效连接时显示“暂无强碰撞”。

建议使用稳定编号 `E-YYYYMMDD-NN`。有实际操作建议时运行：

```bash
python3 scripts/echo_state.py propose --proposal-id E-YYYYMMDD-01 --source-note-id ID --action append_note --target-page-id PAGE_ID --summary "建议"
```

## 用户确认后的最小变更

1. 优先追加既有 Note。
2. 形成可独立检索的新判断时，建议新建 Note。
3. 形成可直接完成的下一步时，建议创建 Task，并优先关联现有 Project。
4. 只有多步目标且有明确完成条件时，才建议新建 Project。
5. 未经确认，不修改正文、关系、优先级，也不创建任何对象。
