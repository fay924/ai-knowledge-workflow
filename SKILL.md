---
name: ai-knowledge-workflow
description: 将 Get笔记中的语音、文字和链接整理到用户自己的 Notion PARA 系统，并在写入后自动执行每日回响，连接历史笔记、项目与可选知识库。用于首次安装、授权配置、拉取或记录笔记、确认分类、写入 Notion、寻找新旧内容关联、提出行动建议，以及排查同步或回响失败。
---

# AI Knowledge Workflow

只向用户呈现一个完整系统：记录 → 整理 → 沉淀 → 回响。Capture 与 Daily Echo 是内部模块，不要求用户分别安装。

## 首次运行

1. 运行 `python3 scripts/setup.py status`。
2. 缺少配置时，完整读取并执行 [references/setup.md](references/setup.md)，一次只引导一个步骤。
3. 运行 `python3 scripts/setup.py verify`。所有必需检查通过前，不拉取或写入。
4. `verify` 只检查本机配置是否齐全；必须实际读取 Notion 根页面和 Notes schema，不能把配置存在误判为连接成功。
5. 从用户复制后的产品根页面动态发现数据库，遵循 [references/notion-contract.md](references/notion-contract.md)。
6. 默认设置“从现在开始”的同步基线。
7. 用一条新笔记完成 Capture 写入和 Daily Echo 回响，全部通过后才宣布安装完成。

禁止在对话、日志、错误信息或仓库中回显完整密钥、数据库 ID、本机路径和用户笔记。

## 日常入口

- 用户要求拉取、同步、整理、记录或写入笔记：完整读取并执行 [references/capture.md](references/capture.md)。
- Capture 成功写入后：自动完整读取并执行 [references/daily-echo.md](references/daily-echo.md)，无需用户再次提醒。
- 用户单独要求“回响”“碰撞笔记”“寻找关联”或“回看新旧笔记”：直接执行 Daily Echo 模块。

## 全局边界

- Capture 写入前必须获得用户确认。
- Daily Echo 默认只读分析；修改旧页面、创建任务或建立关系前必须再次确认。
- 不自动创建 Area、Resource 或 Project。
- 没有真实连接时明确输出“暂无强碰撞”，不得强行联想。
- 回响失败不回滚已经成功写入的笔记；保留错误状态供下次重试。

## 完成标准

- 能读取用户安装后新增的一条 Get笔记。
- 能展示整理结果和建议位置，并等待用户确认。
- 能把确认内容写入用户复制后的 Notes 数据库。
- 能自动登记并执行一次每日回响。
- 有真实连接时说明原因；没有连接时明确显示“暂无强碰撞”。
- 用户能在 Notion 中找到笔记，并能独立重复完成第二次。
