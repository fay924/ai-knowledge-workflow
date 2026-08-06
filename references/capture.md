# Capture 模块

## 拉取路径

1. 优先使用已授权的 Get笔记 MCP 拉取新增笔记；MCP 不可用时才运行 `python3 scripts/fetch_notes.py --record-seen`。仅拉取预览并登记待处理状态。
2. 查询现有 Projects、Areas、Resources，判断最小有用关联。
3. 展示标题、摘要、建议位置和理由。
4. 等待用户确认；确认项标记为 `confirmed`，拒绝项标记为 `skipped`。
5. 只对确认项运行 `python3 scripts/fetch_notes.py --detail NOTE_ID`。
6. 写入 Notes，并按用户确认设置 Project、Area 或 Resource 关联。
7. 写入成功后运行：

```bash
python3 scripts/state.py mark written NOTE_ID
python3 scripts/echo_state.py enqueue --note-id NOTE_ID --notion-page-id PAGE_ID --title TITLE --source getnote --written-at ISO_TIME
```

8. 整批笔记均为 `written` 或 `skipped` 后运行 `python3 scripts/state.py commit` 更新正式检查点，再统一执行 Daily Echo。

## 直接输入路径

用户说“记一下”“记到 Notion”“保存链接”时：

1. 分析目标库、最小关联和正文形式。
2. 展示建议并等待确认。
3. 确认后写入。
4. 用 Notion 页面 ID 作为来源 ID 登记回响队列。
5. 自动执行 Daily Echo。

## 内容规则

- 预览只用于确认，不能作为最终正文。
- 默认使用 Get笔记智能改写内容，保留原始链接和关键细节。
- 不读取录音原始转写或网页全文，除非用户明确要求。
- 多个主题混在一条笔记时，先展示拆分方案。
- 无法判断 PARA 位置时，只写入 Notes，不设置关联。
- 定时检查只拉取、分析并通知，不自动写入。
