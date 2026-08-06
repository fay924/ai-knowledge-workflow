# AI 知识工作流

把散落在 Get笔记中的语音、文字和链接整理到 Notion，并在写入后自动连接历史知识，形成“每日回响”。

你只需要安装一个 Skill。`Capture` 和 `Daily Echo` 是其中的两个连续模块：

```text
Get笔记 → Capture 整理与分类 → 确认后写入 Notion → Daily Echo 连接历史知识
```

## 你可以用它做什么

- 从 Get笔记读取新记录，包括语音、文字和链接。
- 根据内容建议标题、摘要和 PARA 位置。
- 经你确认后写入 Notion，而不是自动乱改笔记库。
- 写入成功后自动运行 Daily Echo，寻找互补、矛盾、推进、复用或证据关系。
- 没有真实关联时明确显示“暂无强碰撞”，不强行联想。

## 开始前准备

1. 安装并登录 [Codex](https://openai.com/codex/)。
2. 注册并登录 [Get笔记](https://www.biji.com/)。
3. 注册并登录 [Notion](https://www.notion.com/zh-cn)。
4. 复制 [十一的 AI 第二大脑｜极简 PARA Command Center V2](https://app.notion.com/p/3b329dca92f781e398e0e3057e52b8c9) 到自己的 Notion 工作区。

## 一段话完成安装

把下面整段话复制给 Codex：

> 请从 https://github.com/fay924/ai-knowledge-workflow 安装“AI 知识工作流”Skill。请作为安装向导，每次只处理一个步骤，验证成功后再继续。先连接官方 Notion MCP，并读取我复制后的 Command Center V2 页面和 Notes 数据库；再使用官方包 @getnote/mcp 连接 Get笔记。你能自动完成的操作直接完成，只有登录、授权或复制页面链接时再让我操作。不要回显凭证，也不要让我手动修改代码或配置文件。连接完成后，带我同步一条新笔记，确认它写入预期的 Notion 位置，并完成一次 Daily Echo。

首次连接时，Codex 会逐步引导你完成 Notion 与 Get笔记授权。MCP 或 OAuth 不可用时，才会进入 API 备用方式。

## 怎样算安装成功

- 能读取安装后新增的一条 Get笔记。
- 能展示整理结果和建议位置，并等待你确认。
- 确认后能写入复制后的 Notes 数据库。
- 写入后能自动完成一次 Daily Echo。
- 你能在 Notion 中找到笔记，并独立重复第二次。

## 日常怎么用

你可以直接对 Codex 说：

- “同步我今天的新笔记。”
- “把这条内容整理到 Notion。”
- “记一下：我想研究适合新人的知识管理方法。”
- “对刚写入的笔记做一次每日回响。”

## 安全边界

- Capture 写入前必须获得你的确认。
- Daily Echo 默认只读分析；修改旧笔记、创建任务或建立关系前必须再次确认。
- Skill 不会把 API Key、数据库 ID、本机路径或个人笔记写入 GitHub。
- 默认从安装完成后的新内容开始同步，避免首次导入全部历史笔记。

## 仓库结构

```text
SKILL.md                 AI 执行入口
references/setup.md      首次安装向导
references/capture.md    Capture 处理规则
references/daily-echo.md Daily Echo 处理规则
references/notion-contract.md  Notion 数据结构约定
scripts/                 API 备用路径与本地状态管理
```

详细执行规则写在 `SKILL.md` 和 `references/` 中；README 只用于帮助使用者理解和安装。

## 许可

[MIT License](LICENSE)
