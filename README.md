# xy-skills

Claude Code 自定义技能插件集，包含产品规格访谈、开发计划生成和 TAPD 项目管理集成。

## 安装

```shell
# 从 GitHub 安装
/plugin marketplace add <owner>/xy-skills
/plugin install xy-skills@xy-skills

# 本地安装（开发测试）
/plugin marketplace add ./path/to/xy-skills
/plugin install xy-skills@xy-skills
```

## 技能列表

| 技能 | 命令 | 说明 |
|------|------|------|
| oc-spec | `/oc-spec` | 通过系统化访谈生成产品规格文档 |
| oc-plan | `/oc-plan` | 从规格文档生成分阶段开发计划 |
| tapd | `/tapd` | TAPD 敏捷研发管理平台集成 |

## oc-spec：产品规格访谈器

通过多轮深度访谈，帮助你系统化地梳理产品需求，输出完整的规格文档。

### 使用场景

- 新项目启动前梳理需求
- 已有想法需要系统化整理
- 在编码前厘清设计决策

### 使用方式

```
/oc-spec
```

或者直接用自然语言触发："帮我梳理一下需求"、"我想理清楚要做什么"、"编码前先问我几个关键问题"。

### 工作流程

1. Claude 会以每轮 3-5 个问题的节奏进行访谈
2. 问题聚焦于影响实现的关键决策，按优先级覆盖：核心范围 → 数据模型 → 边界情况 → 用户体验 → 安全 → 性能 → 可扩展性
3. 每轮结束后展示覆盖进度
4. 所有关键领域覆盖后，生成规格文档

### 输出

规格文档写入项目的 `.claude/spec/` 目录，包含：概述、范围定义（MVP/未来/排除）、功能需求、技术架构、用户体验、安全模型、性能要求、决策日志等。

## oc-plan：开发计划生成器

从规格文档生成结构化的开发计划，将任务拆分到最小模块，带依赖追踪和进度管理。

### 使用场景

- 已有规格文档，需要拆分开发任务
- 需要追踪开发进度
- 需要了解任务间的依赖关系

### 使用方式

```
/oc-plan
```

或者直接说："根据规格生成开发计划"、"帮我拆分任务"。

### 工作流程

1. 读取 `.claude/spec/` 中的规格文档
2. 进入计划模式（plan mode），分析并拆分任务
3. 按阶段组织：基础设施 → 核心功能 → 集成 → 完善
4. 每个任务拆分到原子级别（单文件/单逻辑单元），标注依赖关系
5. 交互式优化计划后，输出到 `.claude/plan/`

### 进度追踪

计划生成后支持进度管理：

```
"标记 P1-001 为完成"
"哪些任务被阻塞了？"
"下一步可以做什么？"
```

状态标记：`[ ]` 未开始 · `[x]` 已完成 · `[~]` 进行中 · `[!]` 被阻塞

### 文件约定

规格和计划文件名一一对应：
- `.claude/spec/auth.md` → `.claude/plan/auth.md`

## tapd：TAPD 项目管理集成

通过 Python 脚本调用 TAPD API，在 Claude Code 中直接管理需求、缺陷、任务、迭代等。

### 环境配置

使用前需设置环境变量：

```bash
export TAPD_ACCESS_TOKEN="你的个人访问令牌"  # 推荐
# 或
export TAPD_API_USER="API账号"
export TAPD_API_PASSWORD="API密钥"
```

### 使用方式

```
/tapd
```

或者直接说："查看需求详情"、"创建一个缺陷"、"查询当前迭代"。

### 支持的功能

- **需求/任务**：查询、创建、更新、字段信息
- **缺陷**：查询、创建、更新
- **迭代**：查询、创建、更新
- **测试用例**：查询、创建、批量创建
- **评论**：查询、创建、更新
- **工时**：查询、填写、更新
- **Wiki**：查询、创建、更新
- **工作流**：状态映射、状态流转
- **关联**：需求与缺陷关联
- **其他**：附件、图片、发布计划、源码提交关键字、企微消息

### 常用示例

```bash
# 查询需求
python scripts/tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories --name "%登录%"

# 创建缺陷
python scripts/tapd.py create_bug --workspace_id 123 --title "登录异常" --priority_label "高"

# 查询迭代
python scripts/tapd.py get_iterations --workspace_id 123

# 填写工时
python scripts/tapd.py add_timesheets --workspace_id 123 --entity_type story --entity_id $ID --timespent 4 --spentdate "2024-01-08"
```

## 推荐工作流

```
/oc-spec  →  .claude/spec/feature.md  →  /oc-plan  →  .claude/plan/feature.md  →  开发实现
```

1. 用 `oc-spec` 通过访谈梳理需求，生成规格文档
2. 用 `oc-plan` 将规格拆分为分阶段开发计划
3. 按计划逐个实现任务，用进度追踪管理状态
4. 如有 TAPD 项目，用 `tapd` 同步需求和缺陷状态
