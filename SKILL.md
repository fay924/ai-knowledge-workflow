---
name: capture-to-notion
description: 将 Get笔记中的语音、文字和链接整理后写入用户自己的 Notion 极简 PARA 系统。用于首次安装、检查授权、拉取新笔记、确认分类、写入 Notes，以及排查同步失败。
---

# Capture to Notion

帮助新手完成一条可验证路径：Get笔记输入，AI 整理，Notion Notes 沉淀。

## 首次运行

1. 运行 `python3 scripts/setup.py status`。
2. 缺少配置时，读取并执行 [references/setup.md](references/setup.md)。一次只引导一个步骤。
3. 运行 `python3 scripts/setup.py verify`。所有检查通过前，不拉取或写入。
4. 用 Notion 能力读取用户复制后的产品根页面，按 [references/notion-contract.md](references/notion-contract.md) 动态发现数据库和模板。
5. 将发现结果写入本机配置；不得把数据库 ID 写回 Skill。
6. 询问用户从现在开始还是导入历史。默认运行 `python3 scripts/state.py baseline`，只处理安装后的新内容。
7. 引导用户输入一条测试笔记，完整跑通后才宣布安装完成。

禁止在对话、日志、错误信息中回显完整密钥。禁止要求用户把密钥提交到 GitHub。

## 日常流程

1. 运行 `python3 scripts/fetch_notes.py --record-seen` 拉取预览。
2. 查询现有 Projects、Areas、Resources，再判断最小关联。
3. 展示标题、摘要、建议位置和理由。
4. 等用户确认。
5. 对确认项运行 `python3 scripts/fetch_notes.py --detail NOTE_ID`。
6. 写入 Notes，并按需关联一个 Project、Area 或 Resource。
7. 写入成功后运行 `python3 scripts/state.py mark written NOTE_ID`。

不得自动创建 Project、Area 或 Resource。需要新容器时，先单独确认。

## 极简分类

- Project：有明确结果，完成后结束。
- Area：需要长期负责，没有结束日期。
- Resource：以后会反复查阅的稳定主题。
- 无法判断：只写入 Notes，不设置关联。

Notes 是内容主体。PARA 是关联位置，不把一条笔记复制到多个数据库。

## 正文规则

- 默认使用 Get笔记智能改写内容，适度分段，不压缩成一句话。
- 保留原始链接、来源和关键细节。
- 不读取录音原始转写或网页全文，除非用户明确要求。
- 多个主题混在一条笔记时，先展示拆分方案。
- 写入字段必须符合 [references/notion-contract.md](references/notion-contract.md)。

## 定时运行

定时任务只拉取、分析并通知，不自动写入。用户确认后再写入 Notion。

## 完成标准

只有同时满足以下条件，才算交付完成：

- 用户在 Get笔记创建了一条新的语音、文字或链接笔记。
- Skill 成功拉取该内容。
- 用户确认 AI 给出的整理结果。
- 内容写入复制后的 Notes 数据库。
- Command Center 能看到该笔记。
- Project、Area 或 Resource 关联符合用户预期；无法判断时保持未关联。
