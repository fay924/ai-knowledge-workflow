# 首次配置向导

每次只完成一个步骤。完成并验证后，再进入下一步。

默认由 AI 执行安装与检测。不要让用户编辑代码或配置文件。Notion 使用官方 MCP OAuth；得到大脑个人接入需要用户在官方开放平台取得 Client ID 与 API Key，再由 AI 安全写入本机配置。

## 统一安装提示词

将下面整段交给 Codex。用户只替换 Notion 根页面链接；仓库公开后，Skill 地址无需修改。

> 请作为安装向导，按顺序帮我完成 AI 知识工作流安装。每次只处理一个步骤，验证成功后再进入下一步；你能自动完成的操作直接完成，需要我登录、授权或复制凭证时，再用简单中文告诉我具体点击位置。第一，连接官方 Notion MCP，并读取我的产品根页面与 Notes 数据库验证读写权限：［Notion 产品根页面链接］。第二，连接得到大脑：打开 https://www.biji.com/openapi，引导我创建“个人开发”应用并取得 Client ID，再创建 API Key；使用官方包 @getnote/mcp 完成配置。凭证只用于本机配置，不要回显，不要写入文档或 GitHub。连接后读取最近一条笔记验证。第三，从 https://github.com/fay924/ai-knowledge-workflow 安装完整的“AI 知识工作流”Skill，它内部包含 Capture 和 Daily Echo，不要分开安装。最后带我新建并同步一条测试笔记，确认它写入预期 Notion 位置，并完成一次 Daily Echo。任何一步失败时先说明原因和下一步，不要跳过验证。

## 1. 准备 Notion 模板

1. 打开卖家提供的 Notion 模板链接。
2. 点击右上角“复制”，复制到自己的工作区。
3. 打开复制后的产品根页面。
4. 复制该页面链接。

询问用户产品根页面链接。读取页面后，按 `notion-contract.md` 检查四个必需数据库，并记录可选数据库。

## 2. 连接 Notion MCP（默认）

先检查当前 AI 工具是否已有 Notion MCP。没有时，由 AI 使用 Notion 官方远程 MCP 地址 `https://mcp.notion.com/mcp` 完成配置，并发起 OAuth。

官方说明：

- 中文帮助：https://www.notion.com/zh-cn/help/notion-mcp
- 各 AI 工具接入方式：https://developers.notion.com/guides/mcp/get-started-with-mcp

用户也可以在 Notion 桌面端进入：头像 → 偏好 → Notion MCP → 选择正在使用的 AI 工具。

AI 应向用户提供可直接发送的自然语言任务，而不是代码：

> 请帮我连接官方 Notion MCP。请自动完成你能完成的安装；需要我登录时再打开授权页面。授权后，请读取这个 Notion 产品根页面及 Notes 数据库，并明确告诉我是否具备读取和写入权限：［粘贴产品根页面链接］

验证：真实读取根页面、Notes schema，并创建一条测试页面后删除或由用户确认保留。仅显示“已配置”不算成功。

### 高级备用：Notion API

只有当前工具明确不支持 MCP/OAuth 时使用：

1. 打开 https://www.notion.so/my-integrations 。
2. 创建内部集成，启用读取、插入和更新内容权限。
3. 回到复制后的产品根页面，把该集成添加到页面连接。
4. 在用户本机运行 `python3 scripts/setup.py set-notion-token`，按隐藏输入提示粘贴 Token。

验证：能读取产品根页面，并能读取 Notes 数据库 schema。

## 3. 连接得到大脑

官方入口：https://www.biji.com/openapi

API 目前仅对会员开放。先按当前 AI 工具选择路径。

### WorkBuddy 或支持 ClawHub Skill 的平台

把下面一句话发给 AI：

> 请安装得到大脑技能，帮我记录和查找笔记。技能地址：https://clawhub.ai/iswalle/getnote

安装后读取最近一条笔记验证。此路径只完成得到大脑连接；完整系统仍须连接 Notion，并安装本仓库的 AI 知识工作流 Skill。

### Codex、Claude Code、Cursor 等支持 MCP 的工具

1. 打开官方开放平台并登录。
2. 在“应用管理”创建应用，类型选择“个人开发”，复制 Client ID（`cli_xxx`）。
3. 在“API Key”创建 Key（`gk_live_xxx`）。Key 只完整显示一次，立即安全保存。
4. 由 AI 使用官方包 `@getnote/mcp` 完成配置；不要让用户编辑 MCP JSON。
5. 配置完成后，运行 `python3 scripts/setup.py set-getnote-connector` 记录已使用宿主连接器。

若宿主无法管理 MCP 凭证，再让用户在自己的设备运行：

```bash
python3 scripts/setup.py set-getnote
```

向导会隐藏读取 API Key 和 Client ID。不得在对话、截图、日志或 GitHub 中回显凭证。

验证：调用笔记列表接口成功，且不输出凭证。

```bash
python3 scripts/fetch_notes.py --max-pages 1
```

验证：AI 能返回最近一条笔记，或明确返回空列表，且没有鉴权错误。

## WorkBuddy 完整系统边界

WorkBuddy 5.3.8 的项目技能入口只支持“本地上传”或“技能中心”，没有任意 GitHub 地址安装入口。当前只能把 WorkBuddy 作为得到大脑极简入口。

完整支持前还必须完成：

- 把本 Skill 打包为 WorkBuddy 可上传的本地安装包，或发布到 SkillHub。
- 连接官方 Notion MCP，并读写用户复制后的数据库。
- 在写入后继续执行 Daily Echo。

以上验证完成前，完整系统使用 Codex。禁止把只安装得到大脑 Skill 描述成整套系统安装完成，也不要让用户把 GitHub 地址直接发给 WorkBuddy 安装。

## 4. 发现 Notion 结构

读取产品根页面，发现四个数据库和真实字段。将映射保存到本机配置：

```bash
python3 scripts/setup.py set-notion-map --root-page PAGE_ID --notes DATA_SOURCE_ID --projects DATA_SOURCE_ID --areas DATA_SOURCE_ID --resources DATA_SOURCE_ID
```

## 5. 设置首次同步范围

默认只处理安装完成后的新内容：

```bash
python3 scripts/state.py baseline
```

如果用户明确要求导入历史，跳过该命令，并先说明首次会出现较多待确认内容。

## 6. 首条笔记验收

1. 用户在 Get笔记新建内容：“这是我的第一条 AI 第二大脑测试笔记。”
2. 拉取新笔记。
3. 展示整理结果，等用户确认。
4. 写入 Notes；无法判断 PARA 时不设置关联。
5. 将新页面登记到 `echo_state.py`，自动执行一次每日回响。
6. 有真实连接时说明原因；没有连接时明确显示“暂无强碰撞”。
7. 请用户在 Command Center 确认可见。

测试通过后，才提示可以设置每日定时检查。
