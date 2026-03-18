---
name: tapd
description: TAPD 敏捷研发管理平台集成。使用脚本调用 TAPD API，实现需求、缺陷、任务、迭代、测试用例、Wiki 等实体管理。使用场景包括：(1) 查询/创建/更新/批量更新需求、缺陷、任务、迭代 (2) 管理测试用例和 Wiki (3) 管理评论和工时 (4) 关联需求与缺陷 (5) 获取变更历史和状态流转时间 (6) 获取项目成员和工作流状态
---

# TAPD Skill

本 skill 提供与 TAPD 平台交互的 Python 脚本工具，统一通过 `tapd.py` 调用。

## 环境配置

使用前需要配置以下环境变量：
```bash
export TAPD_ACCESS_TOKEN="你的个人访问令牌"  # 推荐
# 或
export TAPD_API_USER="API账号"
export TAPD_API_PASSWORD="API密钥"

export TAPD_API_BASE_URL="https://api.tapd.cn"  # 可选，默认
export TAPD_BASE_URL="https://www.tapd.cn"      # 可选，默认
export CURRENT_USER_NICK="你的昵称"               # 可选
```

## 使用方式

```bash
python scripts/tapd.py <command> [参数]
```

所有命令默认输出 JSON 格式结果。

## 请求频率限制

TAPD API 有请求频率限制，触发限流后会返回错误。使用时须注意：

1. **避免短时间内密集调用**：连续调用多个 API 时，应在请求间适当间隔（建议 0.5~1 秒）
2. **优先使用批量接口**：更新多条数据时使用 `batch_update_story` / `batch_update_bug`（单次最多 50 条），避免循环逐条更新
3. **按需查询 count**：查询命令默认不再同时请求总数，需要时手动添加 `--with_count`
4. **控制分页大小**：`limit` 参数最大 200，建议按实际需要设置合理值，避免请求过大数据量
5. **避免重复查询**：对于同一请求结果，应缓存使用而非重复调用
6. **遇到限流时**：如返回限流错误，等待数秒后重试，不要立即重试

## 命令列表

### 项目与用户
| 命令 | 说明 |
|------|------|
| `get_user_participant_projects` | 获取用户参与的项目列表 |
| `get_workspace_info` | 获取项目信息 |
| `get_workitem_types` | 获取需求类别 |
| `get_workspace_users` | 获取项目成员列表 |
| `get_sub_workspaces` | 获取子项目信息 |
| `get_workspace_reports` | 获取项目报告 |

### 需求/任务
| 命令 | 说明 |
|------|------|
| `get_stories_or_tasks` | 查询需求/任务 |
| `create_story_or_task` | 创建需求/任务 |
| `update_story_or_task` | 更新需求/任务 |
| `batch_update_story` | 批量更新需求（最多50条） |
| `get_story_or_task_count` | 获取数量 |
| `get_stories_fields_lable` | 字段中英文对照 |
| `get_stories_fields_info` | 字段及候选值 |
| `get_story_changes` | 获取需求变更历史 |
| `get_task_changes` | 获取任务变更历史 |
| `get_story_categories` | 获取需求分类 |
| `get_link_stories` | 获取需求间关联关系 |
| `get_story_tcase` | 获取需求与测试用例关联 |
| `get_time_relative_stories` | 获取需求前后置关系 |
| `get_removed_stories` | 获取回收站的需求 |

### 缺陷
| 命令 | 说明 |
|------|------|
| `get_bug` | 查询缺陷 |
| `create_bug` | 创建缺陷 |
| `update_bug` | 更新缺陷 |
| `batch_update_bug` | 批量更新缺陷（最多50条） |
| `get_bug_count` | 获取数量 |
| `get_bug_changes` | 获取缺陷变更历史 |
| `get_bug_fields_lable` | 缺陷字段中英文对照 |
| `get_bug_fields_info` | 缺陷字段及候选值 |
| `get_removed_bugs` | 获取回收站的缺陷 |

### 迭代
| 命令 | 说明 |
|------|------|
| `get_iterations` | 查询迭代 |
| `create_iteration` | 创建迭代 |
| `update_iteration` | 更新迭代 |
| `get_iterations_count` | 获取迭代数量 |
| `get_removed_tasks` | 获取回收站的任务 |

### 评论
| 命令 | 说明 |
|------|------|
| `get_comments` | 查询评论 |
| `create_comments` | 创建评论 |
| `update_comments` | 更新评论 |

### 附件/图片
| 命令 | 说明 |
|------|------|
| `get_entity_attachments` | 获取附件 |
| `get_image` | 获取图片下载链接 |

### 自定义字段
| 命令 | 说明 |
|------|------|
| `get_entity_custom_fields` | 获取自定义字段配置 |

### 工作流
| 命令 | 说明 |
|------|------|
| `get_workflows_status_map` | 状态映射 |
| `get_workflows_all_transitions` | 状态流转 |
| `get_workflows_last_steps` | 结束状态 |
| `get_workflows_first_step` | 起始状态 |

### 度量
| 命令 | 说明 |
|------|------|
| `get_life_times` | 获取状态流转时间 |

### 测试用例
| 命令 | 说明 |
|------|------|
| `get_tcases` | 查询测试用例 |
| `create_or_update_tcases` | 创建/更新测试用例 |
| `create_tcases_batch` | 批量创建测试用例 |
| `get_tcase_categories` | 获取测试用例目录 |

### 测试计划
| 命令 | 说明 |
|------|------|
| `get_test_plans` | 获取测试计划 |
| `get_test_plan_progress` | 获取测试计划执行进度 |

### 看板
| 命令 | 说明 |
|------|------|
| `get_board_cards` | 获取看板工作项 |
| `get_board_columns` | 获取看板板块 |

### Wiki
| 命令 | 说明 |
|------|------|
| `get_wiki` | 查询 Wiki |
| `create_wiki` | 创建 Wiki |
| `update_wiki` | 更新 Wiki |

### 工时
| 命令 | 说明 |
|------|------|
| `get_timesheets` | 查询工时 |
| `add_timesheets` | 填写工时 |
| `update_timesheets` | 更新工时 |
| `delete_timesheets` | 删除工时 |

### 待办
| 命令 | 说明 |
|------|------|
| `get_todo` | 获取待办 |

### 关联
| 命令 | 说明 |
|------|------|
| `get_related_bugs` | 获取关联缺陷 |
| `entity_relations` | 创建关联关系 |

### 发布计划
| 命令 | 说明 |
|------|------|
| `get_release_info` | 获取发布计划 |
| `get_launch_forms_count` | 获取发布评审数量 |
| `create_launch_form` | 创建发布评审 |

### 配置
| 命令 | 说明 |
|------|------|
| `get_modules` | 获取模块 |
| `get_versions` | 获取版本 |

### 源码
| 命令 | 说明 |
|------|------|
| `get_commit_msg` | 获取提交关键字 |

### 消息
| 命令 | 说明 |
|------|------|
| `send_qiwei_message` | 发送企业微信消息 |

## 使用示例

### 查询需求

```bash
# 查询指定需求
python scripts/tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories --id 1167459320001114969

# 模糊搜索需求
python scripts/tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories --name "%登录%" --limit 20

# 查询指定状态的需求
python scripts/tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories --v_status "已验收"
```

### 创建需求

```bash
python scripts/tapd.py create_story_or_task --workspace_id 123 \
    --name "用户登录功能" \
    --description "## 需求描述\n用户可以通过账号密码登录系统" \
    --priority_label "高" \
    --owner "zhangsan" \
    --iteration_name "Sprint 1"
```

### 更新需求状态

```bash
python scripts/tapd.py update_story_or_task --workspace_id 123 \
    --id 1167459320001114969 \
    --v_status "实现中"
```

### 查询缺陷

```bash
python scripts/tapd.py get_bug --workspace_id 123 --title "%登录失败%" --priority_label "高"
```

### 创建缺陷

```bash
python scripts/tapd.py create_bug --workspace_id 123 \
    --title "登录页面显示异常" \
    --description "输入正确密码后提示错误" \
    --priority_label "高" \
    --severity "严重"
```

### 迭代管理

```bash
# 查询迭代
python scripts/tapd.py get_iterations --workspace_id 123

# 创建迭代
python scripts/tapd.py create_iteration --workspace_id 123 \
    --name "Sprint 1" \
    --startdate "2024-01-01" \
    --enddate "2024-01-14" \
    --creator "zhangsan"
```

### 工时管理

```bash
# 查询工时
python scripts/tapd.py get_timesheets --workspace_id 123 --entity_type story --entity_id 1167459320001114969

# 填写工时
python scripts/tapd.py add_timesheets --workspace_id 123 \
    --entity_type story \
    --entity_id 1167459320001114969 \
    --timespent "4" \
    --spentdate "2024-01-08" \
    --memo "开发登录功能"
```

### 评论管理

```bash
# 查询评论
python scripts/tapd.py get_comments --workspace_id 123 \
    --entry_type stories \
    --entry_id 1167459320001114969

# 创建评论
python scripts/tapd.py create_comments --workspace_id 123 \
    --entry_type stories \
    --entry_id 1167459320001114969 \
    --description "看起来不错，可以继续完善"
```

### 关联需求与缺陷

```bash
# 查询需求关联的缺陷
python scripts/tapd.py get_related_bugs --workspace_id 123 --story_id 1167459320001114969

# 创建关联
python scripts/tapd.py entity_relations --workspace_id 123 \
    --source_type story \
    --target_type bug \
    --source_id 1167459320001114969 \
    --target_id 1167459320001114970
```

### 工作流

```bash
# 获取状态映射
python scripts/tapd.py get_workflows_status_map --workspace_id 123 --system story

# 获取可流转状态
python scripts/tapd.py get_workflows_all_transitions --workspace_id 123 --system story

# 获取起始状态
python scripts/tapd.py get_workflows_first_step --workspace_id 123 --system story
```

### 变更历史

```bash
# 查询需求变更历史
python scripts/tapd.py get_story_changes --workspace_id 123 --story_id 1167459320001114969

# 查询缺陷变更历史
python scripts/tapd.py get_bug_changes --workspace_id 123 --bug_id 1167459320001114970

# 查询任务变更历史
python scripts/tapd.py get_task_changes --workspace_id 123 --task_id 1167459320001114971
```

### 批量更新

```bash
# 批量更新需求（最多50条）
python scripts/tapd.py batch_update_story --workspace_id 123 \
    --workitems_json '[{"id":"1167459320001114969","status":"done"},{"id":"1167459320001114970","v_status":"已完成"}]'

# 批量更新缺陷
python scripts/tapd.py batch_update_bug --workspace_id 123 \
    --workitems_json '[{"id":"1167459320001114969","status":"resolved"}]'
```

### 项目成员

```bash
# 获取项目成员
python scripts/tapd.py get_workspace_users --workspace_id 123

# 获取指定字段
python scripts/tapd.py get_workspace_users --workspace_id 123 --fields "user,role_id,email"
```

### 度量

```bash
# 获取状态流转时间
python scripts/tapd.py get_life_times --workspace_id 123 --entity_type story --entity_id 1167459320001114969
```

## 常用命令速查

```bash
# 需求
python scripts/tapd.py get_stories_or_tasks --workspace_id $WS_ID --entity_type stories
python scripts/tapd.py create_story_or_task --workspace_id $WS_ID --name "标题"
python scripts/tapd.py update_story_or_task --workspace_id $WS_ID --id $ID --v_status "状态"

# 缺陷
python scripts/tapd.py get_bug --workspace_id $WS_ID
python scripts/tapd.py create_bug --workspace_id $WS_ID --title "标题"

# 迭代
python scripts/tapd.py get_iterations --workspace_id $WS_ID
python scripts/tapd.py create_iteration --workspace_id $WS_ID --name "Sprint X" --startdate "2024-01-01" --enddate "2024-01-14"

# 工时
python scripts/tapd.py add_timesheets --workspace_id $WS_ID --entity_type story --entity_id $ID --timespent 4 --spentdate "2024-01-08"

# 评论
python scripts/tapd.py create_comments --workspace_id $WS_ID --entry_type stories --entry_id $ID --description "评论内容"
```

## 状态值说明

| 类型 | 字段 | 可用值 |
|------|------|--------|
| 需求优先级 | `priority_label` | High / Middle / Low / Nice To Have |
| 缺陷优先级 | `priority_label` | urgent / high / medium / low / insignificant |
| 缺陷严重程度 | `severity` | fatal / serious / normal / prompt / advice |
| 任务状态 | `status` | open / progressing / done |
| 迭代状态 | `status` | open / done |

## Claude 使用方式

当用户需要与 TAPD 交互时：

1. **读取脚本**：了解命令用法
2. **构建命令**：根据需求构建参数
3. **执行脚本**：使用 Bash 工具运行
4. **处理结果**：解析输出，分析数据

示例工作流：
```
用户: "查看需求 1167459320001114969 的详情"

Claude:
1. python scripts/tapd.py get_stories_or_tasks --workspace_id 67459320 --entity_type stories --id 1167459320001114969
2. 分析返回的需求信息
```

### 图片处理

当获取需求详情时，`get_stories_or_tasks` 命令会自动解析 description 中的图片并获取下载链接。

**返回结果包含 `images` 字段**：
```json
{
  "data": [
    {
      "Story": { "id": "1167459320001114969", "name": "需求标题", ... },
      "images": [
        {
          "path": "/tfl/captures/2026-01/tapd_67459320_base64_1767668922_121.png",
          "download_url": "https://file.tapd.cn/attachments/tmp_download/...?salt=...&time=...",
          "filename": "tapd_67459320_base64_1767668922_121.png"
        }
      ]
    }
  ]
}
```

**处理步骤**：
1. 从返回结果中读取 `images` 数组
2. 使用 `download_url` 访问或下载图片
3. 图片链接有效期约 300 秒

**手动获取图片**（备用方式）：
```bash
# 如果需要单独获取某张图片
python scripts/tapd.py get_image --workspace_id 67459320 --image_path "/tfl/captures/2026-01/tapd_xxx.png"
```

## 文件结构

```
scripts/
├── tapd.py           # 统一入口脚本（43个子命令）
├── tapd_client.py    # TAPD API 客户端
└── requirements.txt
```
