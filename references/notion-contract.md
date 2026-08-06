# Notion 极简 PARA 契约

首次配置时从用户提供的产品根页面动态发现数据库。禁止依赖作者工作区 ID。

## 必需数据库

| 数据库 | 必需字段 | 可选字段 |
| --- | --- | --- |
| Notes | 标题（title） | 来源、原始链接、创建时间、Project、Area、Resource |
| Projects | 项目（title） | 状态、完成日期、Area、Resource、相关笔记 |
| Areas | 领域（title） | 启用、相关笔记、相关项目、Resource |
| Resources | 主题（title） | 相关领域、相关笔记、相关项目 |

允许标题字段名称不同，但类型必须是 `title`。配置时记录真实名称。

## 可选数据库

Tasks、Ideas、AI 方法与实验不是极简版安装前提。存在时记录真实数据库和字段，Daily Echo 可以把它们纳入扫描；不存在时只扫描 Notes、Projects，并在需要创建对应对象时先向用户说明当前模板没有该数据库。

## 动态发现

1. 读取产品根页面及子页面。
2. 查找名称匹配 Notes、Projects、Areas、Resources 的必需数据库，并识别 Tasks、Ideas、AI 方法与实验等可选数据库。
3. 读取各数据库 schema。
4. 以字段类型为主、字段名称为辅匹配属性。
5. 出现多个候选时让用户选择，禁止猜测。
6. 保存产品根页面 ID、四个 data source ID、字段映射和模板 ID。

## 写入 Notes

最低写入：标题和正文。

有对应字段时再写入：

- 来源：`得到大脑`
- 原始链接：来源 URL
- Project、Area、Resource：用户确认后的页面关系

不要求每条笔记都有 PARA 关联。无法判断时保持未关联。

## 模板

Notes 和 Projects 应有默认模板。Areas、Resources 模板属于推荐项，不阻断首次闭环。

创建页面时优先使用数据库默认模板。若当前运行环境无法应用模板，先写入完整正文，不得因排版阻断记录。
