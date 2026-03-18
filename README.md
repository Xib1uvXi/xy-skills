# xy-skills

Claude Code 自定义技能插件集。

## 安装

```shell
# 添加市场源
/plugin marketplace add Xib1uvXi/xy-skills

# 安装全部技能
/plugin install xy-skills@xy-skills

# 或只安装单个技能
/plugin install oc-spec@xy-skills         # 产品规格访谈器
/plugin install oc-plan@xy-skills         # 开发计划生成器
/plugin install tapd@xy-skills            # TAPD 项目管理集成
/plugin install go-code-review@xy-skills  # Go 代码审查
/plugin install kratos-tdd@xy-skills      # Kratos TDD
```

也可以在项目的 `.claude/settings.json` 中配置自动安装：

```json
{
  "extraKnownMarketplaces": {
    "xy-skills": {
      "source": { "source": "github", "repo": "Xib1uvXi/xy-skills" }
    }
  },
  "enabledPlugins": { "xy-skills@xy-skills": true }
}
```

## 技能一览

| 技能 | 命令 | 说明 |
|------|------|------|
| oc-spec | `/oc-spec` | 通过系统化访谈生成产品规格文档，输出到 `.claude/spec/` |
| oc-plan | `/oc-plan` | 从规格文档生成分阶段开发计划，输出到 `.claude/plan/` |
| tapd | `/tapd` | TAPD 敏捷研发管理集成（需求、缺陷、迭代、工时等） |
| go-code-review | `/go-code-review` | Go 代码审查（Kratos/gRPC/GORM），P0-P3 分级报告到 `.claude/issues/` |
| kratos-tdd | `/kratos-tdd` | Kratos 微服务 TDD，Red-Green-Refactor + DDD 分层（biz→data→service→server） |

## tapd 环境配置

```bash
export TAPD_ACCESS_TOKEN="你的个人访问令牌"  # 推荐
# 或
export TAPD_API_USER="API账号"
export TAPD_API_PASSWORD="API密钥"
```

## 推荐工作流

```
/oc-spec → /oc-plan → /kratos-tdd → /go-code-review → /tapd
```

需求访谈 → 计划拆分 → TDD 开发 → 代码审查 → 同步 TAPD
