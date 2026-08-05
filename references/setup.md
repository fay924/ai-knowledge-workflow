# 首次配置向导

每次只完成一个步骤。完成并验证后，再进入下一步。

默认由 AI 执行安装与检测。不要先让用户打开终端、编辑配置文件或寻找 API Key。MCP/OAuth 不可用时，才进入“高级备用方式”。

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

## 3. 连接 Get笔记 MCP（默认）

优先安装 Get笔记官方 MCP 包 `@getnote/mcp`。由 AI 完成安装配置；首次使用时发起 OAuth，用户只负责在浏览器登录。

官方说明：https://doc.biji.com/docs/FmYfw0yXsiXdTtkVzhLcuX8lnxd

给 AI 的自然语言任务：

> 请帮我安装并授权 Get笔记 MCP。请使用官方包 @getnote/mcp，自动完成你能完成的安装；需要登录时再打开浏览器授权，不要让我手动填写 API Key。授权完成后，请读取我最近一条笔记验证连接。

验证：AI 能返回最近一条笔记或明确返回空列表，且没有鉴权错误。

### 高级备用：Get笔记 API

只有当前工具明确不支持 MCP/OAuth 时，才打开 https://www.biji.com/openapi 创建应用，至少授予 `note.content.read`，获取 API Key 和 Client ID。

官方文档：https://doc.biji.com/docs/WOxgwObNNiyMHWk1dl0cJqSxnEd

如果当前 AI 工具已经提供 Get笔记的 `/note config` 或等价授权入口，优先使用该入口。

否则让用户在自己的设备运行：

```bash
python3 scripts/setup.py set-getnote
```

向导会分别隐藏读取 API Key 和 Client ID。若用户账户没有 API 凭证入口，停止并说明需要向 Get笔记官方确认开放接口权限；不得编造入口。

验证：调用笔记列表接口成功，且不输出凭证。

```bash
python3 scripts/fetch_notes.py --max-pages 1
```

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
