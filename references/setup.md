# 首次配置向导

每次只完成一个步骤。完成并验证后，再进入下一步。

## 1. 准备 Notion 模板

1. 打开卖家提供的 Notion 模板链接。
2. 点击右上角“复制”，复制到自己的工作区。
3. 打开复制后的产品根页面。
4. 复制该页面链接。

询问用户产品根页面链接。读取页面后，按 `notion-contract.md` 检查四个必需数据库，并记录可选数据库。

## 2. 授权 Notion

优先使用当前 AI 工具自带的 Notion 登录授权。让用户在浏览器完成登录，不要求其把 Token 发到对话中。

授权完成后运行 `python3 scripts/setup.py set-notion-connector`，再由 AI 实际读取产品根页面、Notes schema，并执行一次测试读取。只有真实读取成功才算授权通过；`setup.py status` 不能替代连通性验证。

如果当前工具不支持 Notion 登录授权：

1. 打开 https://www.notion.so/my-integrations 。
2. 创建内部集成，启用读取、插入和更新内容权限。
3. 回到复制后的产品根页面，把该集成添加到页面连接。
4. 在用户本机运行 `python3 scripts/setup.py set-notion-token`，按隐藏输入提示粘贴 Token。

验证：能读取产品根页面，并能读取 Notes 数据库 schema。

## 3. 授权 Get笔记

打开 https://www.biji.com 并登录。

如果当前 AI 工具已经提供 Get笔记的 `/note config` 或等价授权入口，优先使用该入口。

否则让用户在自己的设备运行：

```bash
python3 scripts/setup.py set-getnote
```

向导会分别隐藏读取 API Key 和 Client ID。若用户账户没有 API 凭证入口，停止并说明需要向 Get笔记官方确认开放接口权限；不得编造入口。

验证：调用笔记列表接口成功，且不输出凭证。

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
