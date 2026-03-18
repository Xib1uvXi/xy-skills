#!/usr/bin/env python3
"""
TAPD 统一命令行工具

用法: python tapd.py <command> [参数]

命令列表:
  项目相关:
    get_user_participant_projects  获取用户参与的项目列表
    get_workspace_info            获取项目信息
    get_workitem_types            获取需求类别
    get_workspace_users           获取项目成员列表
    get_sub_workspaces            获取子项目信息
    get_workspace_reports         获取项目报告

  需求/任务:
    get_stories_or_tasks          查询需求/任务
    create_story_or_task          创建需求/任务
    update_story_or_task          更新需求/任务
    batch_update_story            批量更新需求（最多50条）
    get_story_or_task_count       获取数量
    get_stories_fields_lable      字段中英文对照
    get_stories_fields_info       字段及候选值
    get_story_changes             获取需求变更历史
    get_task_changes              获取任务变更历史
    get_story_categories          获取需求分类
    get_link_stories              获取需求间关联关系
    get_story_tcase               获取需求与测试用例关联
    get_time_relative_stories     获取需求前后置关系
    get_removed_stories           获取回收站的需求

  缺陷:
    get_bug                       查询缺陷
    create_bug                    创建缺陷
    update_bug                    更新缺陷
    batch_update_bug              批量更新缺陷（最多50条）
    get_bug_count                 获取数量
    get_bug_changes               获取缺陷变更历史
    get_bug_fields_lable          缺陷字段中英文对照
    get_bug_fields_info           缺陷字段及候选值
    get_removed_bugs              获取回收站的缺陷

  迭代:
    get_iterations                查询迭代
    create_iteration              创建迭代
    update_iteration              更新迭代
    get_iterations_count          获取迭代数量
    get_removed_tasks             获取回收站的任务

  评论:
    get_comments                  查询评论
    create_comments               创建评论
    update_comments               更新评论

  附件/图片:
    get_entity_attachments        获取附件
    get_image                     获取图片下载链接

  自定义字段:
    get_entity_custom_fields      获取自定义字段配置

  工作流:
    get_workflows_status_map      状态映射
    get_workflows_all_transitions 状态流转
    get_workflows_last_steps      结束状态
    get_workflows_first_step      起始状态

  测试计划:
    get_test_plans                获取测试计划
    get_test_plan_progress        获取测试计划执行进度

  看板:
    get_board_cards               获取看板工作项
    get_board_columns             获取看板板块

  度量:
    get_life_times                获取状态流转时间

  测试用例:
    get_tcases                    查询测试用例
    create_or_update_tcases       创建/更新测试用例
    create_tcases_batch           批量创建
    get_tcase_categories          获取测试用例目录

  Wiki:
    get_wiki                      查询 Wiki
    create_wiki                   创建 Wiki
    update_wiki                   更新 Wiki

  工时:
    get_timesheets                查询工时
    add_timesheets                填写工时
    update_timesheets             更新工时
    delete_timesheets             删除工时

  待办:
    get_todo                      获取待办

  关联:
    get_related_bugs              获取关联缺陷
    entity_relations              创建关联关系

  发布计划:
    get_release_info              获取发布计划
    get_launch_forms_count        获取发布评审数量
    create_launch_form            创建发布评审

  配置:
    get_modules                   获取模块
    get_versions                  获取版本

  源码:
    get_commit_msg                获取提交关键字

  消息:
    send_qiwei_message            发送企业微信消息

示例:
    python tapd.py get_stories_or_tasks --workspace_id 123 --entity_type stories
    python tapd.py create_story_or_task --workspace_id 123 --name "需求标题"
    python tapd.py get_bug --workspace_id 123 --title "%登录%"
"""

import sys
import re
import json
import argparse
import os
from tapd_client import TAPDClient


def get_tapd_base_url():
    """获取 TAPD 基础 URL"""
    from tapd_client import get_env_check_message
    msg = get_env_check_message()
    if msg:
        print(msg)
        sys.exit(1)

    config_base_url = os.getenv("TAPD_BASE_URL")
    return config_base_url or os.getenv("TAPD_API_BASE_URL", "https://www.tapd.cn").replace("api.tapd.cn", "www.tapd.cn")


def _args_to_dict(args, keys, data=None):
    """从 args 中提取非 None 的键值对到 dict"""
    if data is None:
        data = {}
    for key in keys:
        val = getattr(args, key, None)
        if val is not None:
            data[key] = val
    return data


# ============ 项目相关 ============

def cmd_get_user_participant_projects(args):
    """获取用户参与的项目列表"""
    client = TAPDClient()
    data = {"nick": args.nick} if args.nick else {"nick": client.nick or ""}
    result = client.get_user_participant_projects(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workspace_info(args):
    """获取项目信息"""
    client = TAPDClient()
    result = client.get_workspace_info({"workspace_id": args.workspace_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workitem_types(args):
    """获取需求类别"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name"], {"workspace_id": args.workspace_id})
    result = client.get_workitem_types(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workspace_users(args):
    """获取项目成员列表"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}
    if args.fields:
        data["fields"] = args.fields
    result = client.get_workspace_users(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_sub_workspaces(args):
    """获取子项目信息"""
    client = TAPDClient()
    data = _args_to_dict(args, ["template_id"],
                         {"workspace_id": args.workspace_id})
    result = client.get_sub_workspaces(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workspace_reports(args):
    """获取项目报告"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "title", "author", "limit", "page", "fields"],
                         {"workspace_id": args.workspace_id})
    result = client.get_workspace_reports(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 需求/任务相关 ============

def cmd_get_stories_or_tasks(args):
    """查询需求/任务"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}
    data["entity_type"] = args.entity_type or "stories"
    _args_to_dict(args, ["id", "name", "status", "v_status", "owner",
                         "creator", "priority_label", "iteration_id",
                         "limit", "page"], data)

    # 获取详情时（指定 id）默认包含 description
    fields_param = args.fields
    if args.id:
        if not fields_param:
            fields_param = "description"
        elif "description" not in fields_param:
            fields_param = fields_param + ",description"
    data["fields"] = fields_param

    result = client.get_stories(data)

    # 过滤字段
    fields_param = data.get('fields')
    if isinstance(result, dict) and 'data' in result:
        result['data'] = client.filter_fields(result['data'], fields_param)

    # 获取详情时，自动处理图片
    if args.id and result.get('data'):
        for item in result['data']:
            story = item.get('Story', {})
            description = story.get('description', '')
            img_paths = re.findall(r'<img[^>]+src="([^"]+)"', description)
            if img_paths:
                images = []
                for img_path in img_paths:
                    try:
                        if img_path.startswith('http://') or img_path.startswith('https://'):
                            images.append({
                                "path": img_path,
                                "download_url": img_path,
                                "filename": ""
                            })
                        else:
                            img_result = client.get_image({
                                "workspace_id": args.workspace_id,
                                "image_path": img_path
                            })
                            if img_result.get('data', {}).get('Attachment'):
                                att = img_result['data']['Attachment']
                                images.append({
                                    "path": img_path,
                                    "download_url": att.get('download_url'),
                                    "filename": att.get('filename')
                                })
                    except Exception:
                        continue
                if images:
                    item['images'] = images

    tapd_base_url = get_tapd_base_url()
    url_template = client.get_story_or_task_url_template(args.workspace_id, data["entity_type"], tapd_base_url)

    output = {
        "url_template": url_template,
        "data": result.get('data', []),
    }
    if getattr(args, 'with_count', False):
        output["count"] = client.get_story_count(data)
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create_story_or_task(args):
    """创建需求/任务"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id, "name": args.name}
    data["entity_type"] = args.entity_type or "stories"
    _args_to_dict(args, ["description", "priority_label", "owner",
                         "iteration_id", "iteration_name", "category_id",
                         "workitem_type_id", "release_id", "parent_id",
                         "size", "version", "module"], data)
    if args.story_id and data.get("entity_type") == "tasks":
        data["story_id"] = args.story_id

    result = client.create_or_update_story(data)

    tapd_base_url = get_tapd_base_url()
    url_template = client.get_story_or_task_url_template(args.workspace_id, data["entity_type"], tapd_base_url)

    output = {
        "url_template": url_template,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update_story_or_task(args):
    """更新需求/任务"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id, "id": args.id}
    data["entity_type"] = args.entity_type or "stories"
    _args_to_dict(args, ["name", "description", "v_status", "status",
                         "priority_label", "owner"], data)

    result = client.create_or_update_story(data)

    tapd_base_url = get_tapd_base_url()
    url_template = client.get_story_or_task_url_template(args.workspace_id, data["entity_type"], tapd_base_url)

    output = {
        "url_template": url_template,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_get_story_or_task_count(args):
    """获取需求/任务数量"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id}
    data["entity_type"] = args.entity_type or "stories"
    _args_to_dict(args, ["id", "name", "status"], data)

    result = client.get_story_count(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_stories_fields_lable(args):
    """获取字段中英文对照"""
    client = TAPDClient()
    result = client.get_stories_fields_lable({"workspace_id": args.workspace_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_stories_fields_info(args):
    """获取字段及候选值"""
    client = TAPDClient()
    result = client.get_stories_fields_info({"workspace_id": args.workspace_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_story_changes(args):
    """获取需求变更历史"""
    client = TAPDClient()
    data = _args_to_dict(args, ["story_id", "creator", "created", "change_field",
                                "limit", "page", "order", "fields"],
                         {"workspace_id": args.workspace_id})
    result = client.get_story_changes(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_task_changes(args):
    """获取任务变更历史"""
    client = TAPDClient()
    data = _args_to_dict(args, ["task_id", "creator", "created", "change_field",
                                "limit", "page", "order", "fields"],
                         {"workspace_id": args.workspace_id})
    result = client.get_task_changes(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_batch_update_story(args):
    """批量更新需求"""
    client = TAPDClient()
    try:
        workitems = json.loads(args.workitems_json)
    except json.JSONDecodeError:
        print("错误: --workitems_json 必须是有效的 JSON 格式")
        sys.exit(1)

    data = {
        "workspace_id": args.workspace_id,
        "workitems": workitems
    }
    result = client.batch_update_story(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_story_categories(args):
    """获取需求分类"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "parent_id", "limit", "page"],
                         {"workspace_id": args.workspace_id})
    result = client.get_story_categories(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_link_stories(args):
    """获取需求与其它需求的关联关系"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id, "story_id": args.story_id}
    result = client.get_link_stories(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_story_tcase(args):
    """获取需求与测试用例关联关系"""
    client = TAPDClient()
    data = _args_to_dict(args, ["include_test_plan"],
                         {"workspace_id": args.workspace_id, "story_id": args.story_id})
    result = client.get_story_tcase(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_time_relative_stories(args):
    """获取需求前后置关系"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id, "story_id": args.story_id}
    result = client.get_time_relative_stories(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_removed_stories(args):
    """获取回收站的需求"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "creator", "limit", "page"],
                         {"workspace_id": args.workspace_id})
    result = client.get_removed_stories(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 缺陷相关 ============

def cmd_get_bug(args):
    """查询缺陷"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "title", "status", "v_status",
                                "priority_label", "severity", "owner",
                                "limit", "page"],
                         {"workspace_id": args.workspace_id})

    # 获取详情时（指定 id）默认包含 description
    fields_param = args.fields
    if args.id:
        if not fields_param:
            fields_param = "description"
        elif "description" not in fields_param:
            fields_param = fields_param + ",description"
    data["fields"] = fields_param

    result = client.get_bug(data)

    # 过滤字段
    fields_param = data.get('fields')
    if isinstance(result, dict) and 'data' in result:
        result['data'] = client.filter_fields(result['data'], fields_param)

    tapd_base_url = get_tapd_base_url()

    output = {
        "base_url": tapd_base_url,
        "data": result.get('data', []),
    }
    if getattr(args, 'with_count', False):
        output["count"] = client.get_bug_count(data)
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create_bug(args):
    """创建缺陷"""
    client = TAPDClient()
    data = _args_to_dict(args, ["description", "priority_label", "severity",
                                "current_owner", "cc", "reporter",
                                "iteration_id", "release_id", "module", "feature"],
                         {"workspace_id": args.workspace_id, "title": args.title})

    result = client.create_or_update_bug(data)

    tapd_base_url = get_tapd_base_url()
    bug_id = result.get("data", {}).get("Bug", {}).get("id")
    url = f"{tapd_base_url}/{args.workspace_id}/bugtrace/bugs/view/{bug_id}" if bug_id else ""

    output = {
        "url": url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update_bug(args):
    """更新缺陷"""
    client = TAPDClient()
    data = _args_to_dict(args, ["title", "description", "v_status", "status",
                                "priority_label", "severity", "current_owner"],
                         {"workspace_id": args.workspace_id, "id": args.id})

    result = client.create_or_update_bug(data)

    tapd_base_url = get_tapd_base_url()

    output = {
        "base_url": tapd_base_url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_get_bug_count(args):
    """获取缺陷数量"""
    client = TAPDClient()
    data = _args_to_dict(args, ["title", "status"],
                         {"workspace_id": args.workspace_id})

    result = client.get_bug_count(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_bug_changes(args):
    """获取缺陷变更历史"""
    client = TAPDClient()
    data = _args_to_dict(args, ["bug_id", "author", "created", "field",
                                "limit", "page", "order", "fields"],
                         {"workspace_id": args.workspace_id})
    result = client.get_bug_changes(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_bug_fields_lable(args):
    """获取缺陷字段中英文对照"""
    client = TAPDClient()
    result = client.get_bug_fields_lable({"workspace_id": args.workspace_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_bug_fields_info(args):
    """获取缺陷字段及候选值"""
    client = TAPDClient()
    result = client.get_bug_fields_info({"workspace_id": args.workspace_id})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_batch_update_bug(args):
    """批量更新缺陷"""
    client = TAPDClient()
    try:
        workitems = json.loads(args.workitems_json)
    except json.JSONDecodeError:
        print("错误: --workitems_json 必须是有效的 JSON 格式")
        sys.exit(1)

    data = {
        "workspace_id": args.workspace_id,
        "workitems": workitems
    }
    result = client.batch_update_bug(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_removed_bugs(args):
    """获取回收站的缺陷"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "creator", "limit", "page"],
                         {"workspace_id": args.workspace_id})
    result = client.get_removed_bugs(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 迭代相关 ============

def cmd_get_iterations(args):
    """查询迭代"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "status"],
                         {"workspace_id": args.workspace_id})

    result = client.get_iterations(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_iteration(args):
    """创建迭代"""
    client = TAPDClient()
    data = _args_to_dict(args, ["creator", "description", "status", "label", "parent_id"],
                         {"workspace_id": args.workspace_id, "name": args.name,
                          "startdate": args.startdate, "enddate": args.enddate})

    result = client.create_or_update_iteration(data)

    tapd_base_url = get_tapd_base_url()
    iteration_id = result.get("data", {}).get("Iteration", {}).get("id")
    url = f"{tapd_base_url}/{args.workspace_id}/prong/iterations/card_view/{iteration_id}" if iteration_id else ""

    output = {
        "url": url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update_iteration(args):
    """更新迭代"""
    client = TAPDClient()
    data = _args_to_dict(args, ["name", "startdate", "enddate", "status"],
                         {"workspace_id": args.workspace_id, "id": args.id,
                          "current_user": args.current_user})

    result = client.create_or_update_iteration(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_iterations_count(args):
    """获取迭代数量"""
    client = TAPDClient()
    data = _args_to_dict(args, ["name", "status"],
                         {"workspace_id": args.workspace_id})
    result = client.get_iterations_count(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_removed_tasks(args):
    """获取回收站的任务"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "creator", "limit", "page"],
                         {"workspace_id": args.workspace_id})
    result = client.get_removed_tasks(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 评论相关 ============

def cmd_get_comments(args):
    """查询评论"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "entry_type", "entry_id", "author",
                                "limit", "page"],
                         {"workspace_id": args.workspace_id})

    result = client.get_comments(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_comments(args):
    """创建评论"""
    client = TAPDClient()
    data = _args_to_dict(args, ["author", "root_id", "reply_id"],
                         {"workspace_id": args.workspace_id,
                          "entry_type": args.entry_type,
                          "entry_id": args.entry_id,
                          "description": args.description})

    result = client.create_comments(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_update_comments(args):
    """更新评论"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "id": args.id,
        "description": args.description,
        "change_creator": args.change_creator
    }

    result = client.create_comments(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 附件/图片相关 ============

def cmd_get_entity_attachments(args):
    """获取附件"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "entry_id": args.entry_id,
        "type": args.type
    }

    result = client.get_attachments(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_image(args):
    """获取图片下载链接"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "image_path": args.image_path
    }

    result = client.get_image(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 自定义字段 ============

def cmd_get_entity_custom_fields(args):
    """获取自定义字段配置"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "entity_type": args.entity_type
    }

    result = client.get_entity_custom_fields(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 工作流相关 ============

def cmd_get_workflows_status_map(args):
    """获取状态映射"""
    client = TAPDClient()
    data = _args_to_dict(args, ["workitem_type_id"],
                         {"workspace_id": args.workspace_id, "system": args.system})
    result = client.get_workflows_status_map(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workflows_all_transitions(args):
    """获取状态流转"""
    client = TAPDClient()
    data = _args_to_dict(args, ["workitem_type_id"],
                         {"workspace_id": args.workspace_id, "system": args.system})
    result = client.get_workflows_all_transitions(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workflows_last_steps(args):
    """获取结束状态"""
    client = TAPDClient()
    data = _args_to_dict(args, ["workitem_type_id", "type"],
                         {"workspace_id": args.workspace_id, "system": args.system})
    result = client.get_workflows_last_steps(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_workflows_first_step(args):
    """获取起始状态"""
    client = TAPDClient()
    data = _args_to_dict(args, ["workitem_type_id", "type"],
                         {"workspace_id": args.workspace_id, "system": args.system})
    result = client.get_workflows_first_step(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 度量相关 ============

def cmd_get_life_times(args):
    """获取状态流转时间"""
    client = TAPDClient()
    data = _args_to_dict(args, ["limit", "page", "order", "fields"],
                         {"workspace_id": args.workspace_id,
                          "entity_type": args.entity_type,
                          "entity_id": args.entity_id})
    result = client.get_life_times(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 测试用例相关 ============

def cmd_get_tcases(args):
    """查询测试用例"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "category_id", "status",
                                "type", "priority", "limit", "page"],
                         {"workspace_id": args.workspace_id})

    result = client.get_tcases(data)

    tapd_base_url = get_tapd_base_url()

    output = {
        "base_url": tapd_base_url,
        "data": json.dumps(result, ensure_ascii=False, indent=2),
    }
    if getattr(args, 'with_count', False):
        output["count"] = json.dumps(client.get_tcases_count(data), ensure_ascii=False, indent=2)
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create_or_update_tcases(args):
    """创建/更新测试用例"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "category_id", "status",
                                "precondition", "steps", "expectation",
                                "type", "priority"],
                         {"workspace_id": args.workspace_id})

    result = client.create_tcases(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_tcases_batch(args):
    """批量创建测试用例"""
    client = TAPDClient()

    if not args.tcases_json:
        print("错误: 需要提供 --tcases_json 参数")
        sys.exit(1)

    try:
        tcases = json.loads(args.tcases_json)
    except json.JSONDecodeError:
        print("错误: --tcases_json 必须是有效的 JSON 格式")
        sys.exit(1)

    for tcase in tcases:
        if 'workspace_id' not in tcase:
            tcase['workspace_id'] = args.workspace_id

    result = client.create_tcases_batch_save(tcases)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_tcase_categories(args):
    """获取测试用例目录"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "limit", "page"],
                         {"workspace_id": args.workspace_id})
    result = client.get_tcase_categories(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 测试计划相关 ============

def cmd_get_test_plans(args):
    """获取测试计划"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "status", "creator",
                                "limit", "page", "fields"],
                         {"workspace_id": args.workspace_id})
    result = client.get_test_plans(data)
    output = {"data": result.get('data', [])}
    if getattr(args, 'with_count', False):
        output["count"] = client.get_test_plans_count(data)
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_get_test_plan_progress(args):
    """获取测试计划执行进度"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id, "test_plan_id": args.test_plan_id}
    result = client.get_test_plan_progress(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 看板相关 ============

def cmd_get_board_cards(args):
    """获取看板工作项"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "b_board_id", "b_column_id", "owner",
                                "status", "name", "limit", "page", "fields"],
                         {"workspace_id": args.workspace_id})
    result = client.get_board_cards(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_board_columns(args):
    """获取看板板块"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "board_id", "limit", "page", "fields"],
                         {"workspace_id": args.workspace_id})
    result = client.get_board_columns(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ Wiki 相关 ============

def cmd_get_wiki(args):
    """查询 Wiki"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "creator", "limit", "page"],
                         {"workspace_id": args.workspace_id})

    result = client.get_wiki(data)

    tapd_base_url = get_tapd_base_url()

    output = {
        "base_url": tapd_base_url,
        "data": json.dumps(result, ensure_ascii=False, indent=2),
    }
    if getattr(args, 'with_count', False):
        output["count"] = json.dumps(client.get_wiki_count(data), ensure_ascii=False, indent=2)
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create_wiki(args):
    """创建 Wiki"""
    client = TAPDClient()
    data = _args_to_dict(args, ["name", "markdown_description", "creator",
                                "note", "parent_wiki_id"],
                         {"workspace_id": args.workspace_id})

    result = client.create_wiki(data)

    tapd_base_url = get_tapd_base_url()
    wiki_id = result.get("data", {}).get("Wiki", {}).get("id")
    url = f"{tapd_base_url}/{args.workspace_id}/markdown_wikis/show/#{wiki_id}" if wiki_id else ""

    output = {
        "url": url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_update_wiki(args):
    """更新 Wiki"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "markdown_description",
                                "note", "parent_wiki_id"],
                         {"workspace_id": args.workspace_id})

    result = client.create_wiki(data)

    tapd_base_url = get_tapd_base_url()
    wiki_id = result.get("data", {}).get("Wiki", {}).get("id")
    url = f"{tapd_base_url}/{args.workspace_id}/markdown_wikis/show/#{wiki_id}" if wiki_id else ""

    output = {
        "url": url,
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============ 工时相关 ============

def cmd_get_timesheets(args):
    """查询工时"""
    client = TAPDClient()
    data = _args_to_dict(args, ["entity_type", "entity_id", "owner",
                                "spentdate", "limit", "page"],
                         {"workspace_id": args.workspace_id})

    result = client.get_timesheets(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_add_timesheets(args):
    """填写工时"""
    client = TAPDClient()
    data = _args_to_dict(args, ["owner", "memo", "timeremain"],
                         {"workspace_id": args.workspace_id,
                          "entity_type": args.entity_type,
                          "entity_id": args.entity_id,
                          "timespent": args.timespent,
                          "spentdate": args.spentdate})

    result = client.update_timesheets(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_update_timesheets(args):
    """更新工时"""
    client = TAPDClient()
    data = _args_to_dict(args, ["memo", "timeremain"],
                         {"workspace_id": args.workspace_id,
                          "id": args.id, "timespent": args.timespent})

    result = client.update_timesheets(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_delete_timesheets(args):
    """删除工时"""
    client = TAPDClient()
    data = {"workspace_id": args.workspace_id, "id": args.id}
    result = client.delete_timesheets(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 待办相关 ============

def cmd_get_todo(args):
    """获取待办"""
    client = TAPDClient()
    data = {
        "entity_type": args.entity_type,
        "user_nick": args.user_nick or client.nick
    }

    result = client.get_todo(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 关联相关 ============

def cmd_get_related_bugs(args):
    """获取关联缺陷"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "story_id": args.story_id
    }

    result = client.get_related_bugs(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_entity_relations(args):
    """创建关联关系"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "source_type": args.source_type,
        "target_type": args.target_type,
        "source_id": args.source_id,
        "target_id": args.target_id
    }

    result = client.add_entity_relations(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 发布计划 ============

def cmd_get_release_info(args):
    """获取发布计划"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "status", "limit"],
                         {"workspace_id": args.workspace_id})

    result = client.get_release_info(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_launch_forms_count(args):
    """获取发布评审数量"""
    client = TAPDClient()
    data = _args_to_dict(args, ["title", "status", "creator"],
                         {"workspace_id": args.workspace_id})
    result = client.get_launch_forms_count(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create_launch_form(args):
    """创建发布评审"""
    client = TAPDClient()
    data = _args_to_dict(args, ["title", "creator", "template_id"],
                         {"workspace_id": args.workspace_id})
    result = client.create_launch_form(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 配置相关 ============

def cmd_get_modules(args):
    """获取模块"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "limit", "page"],
                         {"workspace_id": args.workspace_id})
    result = client.get_modules(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_get_versions(args):
    """获取版本"""
    client = TAPDClient()
    data = _args_to_dict(args, ["id", "name", "status", "limit", "page"],
                         {"workspace_id": args.workspace_id})
    result = client.get_versions(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 源码提交关键字 ============

def cmd_get_commit_msg(args):
    """获取提交关键字"""
    client = TAPDClient()
    data = {
        "workspace_id": args.workspace_id,
        "object_id": args.object_id,
        "type": args.type
    }

    result = client.get_scm_copy_keywords(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============ 企业微信消息 ============

def cmd_send_qiwei_message(args):
    """发送企业微信消息"""
    client = TAPDClient()
    result = client.send_message({"msg": args.msg})
    print(result)


# ============ 主程序 ============

def build_parser():
    """构建命令行解析器"""
    parser = argparse.ArgumentParser(
        description="TAPD 统一命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )

    subparsers = parser.add_subparsers(dest="command", title="命令")

    # ============ 项目相关 ============
    p = subparsers.add_parser("get_user_participant_projects", help="获取用户参与的项目列表")
    p.set_defaults(func=cmd_get_user_participant_projects)
    p.add_argument("--nick", help="用户昵称")

    p = subparsers.add_parser("get_workspace_info", help="获取项目信息")
    p.set_defaults(func=cmd_get_workspace_info)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")

    p = subparsers.add_parser("get_workitem_types", help="获取需求类别")
    p.set_defaults(func=cmd_get_workitem_types)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="需求类别名称")

    p = subparsers.add_parser("get_workspace_users", help="获取项目成员列表")
    p.set_defaults(func=cmd_get_workspace_users)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--fields", help="字段列表 (user,role_id,email)")

    p = subparsers.add_parser("get_sub_workspaces", help="获取子项目信息")
    p.set_defaults(func=cmd_get_sub_workspaces)
    p.add_argument("--workspace_id", required=True, type=int, help="父项目ID")
    p.add_argument("--template_id", type=int, help="项目模板ID")

    p = subparsers.add_parser("get_workspace_reports", help="获取项目报告")
    p.set_defaults(func=cmd_get_workspace_reports)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="报告ID")
    p.add_argument("--title", help="报告标题")
    p.add_argument("--author", help="创建人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--fields", help="字段列表")

    # ============ 需求/任务 ============
    p = subparsers.add_parser("get_stories_or_tasks", help="查询需求/任务")
    p.set_defaults(func=cmd_get_stories_or_tasks)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", choices=["stories", "tasks"], help="类型")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="标题（模糊匹配）")
    p.add_argument("--status", help="状态")
    p.add_argument("--v_status", help="状态（中文）")
    p.add_argument("--owner", help="处理人")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--iteration_id", help="迭代ID")
    p.add_argument("--limit", type=int, default=10, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--fields", help="字段列表")
    p.add_argument("--with_count", action="store_true", help="同时查询总数")

    p = subparsers.add_parser("create_story_or_task", help="创建需求/任务")
    p.set_defaults(func=cmd_create_story_or_task)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--name", required=True, help="标题")
    p.add_argument("--entity_type", choices=["stories", "tasks"], help="类型")
    p.add_argument("--description", help="描述")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--owner", help="处理人")
    p.add_argument("--iteration_id", help="迭代ID")
    p.add_argument("--iteration_name", help="迭代名称")
    p.add_argument("--category_id", help="需求分类ID")
    p.add_argument("--workitem_type_id", help="需求类别ID")
    p.add_argument("--release_id", help="发布计划ID")
    p.add_argument("--parent_id", help="父需求ID")
    p.add_argument("--story_id", help="关联需求ID（任务）")
    p.add_argument("--size", help="规模点")
    p.add_argument("--version", help="版本")
    p.add_argument("--module", help="模块")

    p = subparsers.add_parser("update_story_or_task", help="更新需求/任务")
    p.set_defaults(func=cmd_update_story_or_task)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="需求/任务ID")
    p.add_argument("--entity_type", choices=["stories", "tasks"], help="类型")
    p.add_argument("--name", help="标题")
    p.add_argument("--description", help="描述")
    p.add_argument("--v_status", help="状态（中文）")
    p.add_argument("--status", help="状态")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--owner", help="处理人")

    p = subparsers.add_parser("get_story_or_task_count", help="获取需求/任务数量")
    p.set_defaults(func=cmd_get_story_or_task_count)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", choices=["stories", "tasks"], help="类型")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="标题")
    p.add_argument("--status", help="状态")

    p = subparsers.add_parser("get_stories_fields_lable", help="获取字段中英文对照")
    p.set_defaults(func=cmd_get_stories_fields_lable)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")

    p = subparsers.add_parser("get_stories_fields_info", help="获取字段及候选值")
    p.set_defaults(func=cmd_get_stories_fields_info)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")

    p = subparsers.add_parser("get_story_changes", help="获取需求变更历史")
    p.set_defaults(func=cmd_get_story_changes)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--story_id", help="需求ID")
    p.add_argument("--creator", help="操作人")
    p.add_argument("--created", help="变更时间")
    p.add_argument("--change_field", help="变更字段")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--order", help="排序规则")
    p.add_argument("--fields", help="字段列表")

    p = subparsers.add_parser("get_task_changes", help="获取任务变更历史")
    p.set_defaults(func=cmd_get_task_changes)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--task_id", help="任务ID")
    p.add_argument("--creator", help="操作人")
    p.add_argument("--created", help="变更时间")
    p.add_argument("--change_field", help="变更字段")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--order", help="排序规则")
    p.add_argument("--fields", help="字段列表")

    p = subparsers.add_parser("batch_update_story", help="批量更新需求（最多50条）")
    p.set_defaults(func=cmd_batch_update_story)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--workitems_json", required=True, help='工作项列表 (JSON格式, 如 [{"id":123,"status":"done"}])')

    p = subparsers.add_parser("get_story_categories", help="获取需求分类")
    p.set_defaults(func=cmd_get_story_categories)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="分类ID")
    p.add_argument("--name", help="分类名称")
    p.add_argument("--parent_id", help="父分类ID")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    p = subparsers.add_parser("get_link_stories", help="获取需求与其它需求的关联关系")
    p.set_defaults(func=cmd_get_link_stories)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--story_id", required=True, help="需求ID")

    p = subparsers.add_parser("get_story_tcase", help="获取需求与测试用例关联关系")
    p.set_defaults(func=cmd_get_story_tcase)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--story_id", required=True, help="需求ID")
    p.add_argument("--include_test_plan", type=int, choices=[0, 1], help="是否包含测试计划")

    p = subparsers.add_parser("get_time_relative_stories", help="获取需求前后置关系")
    p.set_defaults(func=cmd_get_time_relative_stories)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--story_id", required=True, help="需求ID")

    p = subparsers.add_parser("get_removed_stories", help="获取回收站的需求")
    p.set_defaults(func=cmd_get_removed_stories)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="需求ID")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    # ============ 缺陷 ============
    p = subparsers.add_parser("get_bug", help="查询缺陷")
    p.set_defaults(func=cmd_get_bug)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--title", help="标题（模糊匹配）")
    p.add_argument("--status", help="状态")
    p.add_argument("--v_status", help="状态（中文）")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--severity", help="严重程度")
    p.add_argument("--owner", help="处理人")
    p.add_argument("--limit", type=int, default=10, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--fields", help="字段列表")
    p.add_argument("--with_count", action="store_true", help="同时查询总数")

    p = subparsers.add_parser("create_bug", help="创建缺陷")
    p.set_defaults(func=cmd_create_bug)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--title", required=True, help="标题")
    p.add_argument("--description", help="描述")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--severity", help="严重程度")
    p.add_argument("--current_owner", help="处理人")
    p.add_argument("--cc", help="抄送人")
    p.add_argument("--reporter", help="创建人")
    p.add_argument("--iteration_id", help="迭代ID")
    p.add_argument("--release_id", help="发布计划ID")
    p.add_argument("--module", help="模块")
    p.add_argument("--feature", help="特性")

    p = subparsers.add_parser("update_bug", help="更新缺陷")
    p.set_defaults(func=cmd_update_bug)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="缺陷ID")
    p.add_argument("--title", help="标题")
    p.add_argument("--description", help="描述")
    p.add_argument("--v_status", help="状态（中文）")
    p.add_argument("--status", help="状态")
    p.add_argument("--priority_label", help="优先级")
    p.add_argument("--severity", help="严重程度")
    p.add_argument("--current_owner", help="处理人")

    p = subparsers.add_parser("get_bug_count", help="获取缺陷数量")
    p.set_defaults(func=cmd_get_bug_count)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--title", help="标题")
    p.add_argument("--status", help="状态")

    p = subparsers.add_parser("get_bug_changes", help="获取缺陷变更历史")
    p.set_defaults(func=cmd_get_bug_changes)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--bug_id", help="缺陷ID")
    p.add_argument("--author", help="操作人")
    p.add_argument("--created", help="变更时间")
    p.add_argument("--field", help="变更字段")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--order", help="排序规则")
    p.add_argument("--fields", help="字段列表")

    p = subparsers.add_parser("get_bug_fields_lable", help="获取缺陷字段中英文对照")
    p.set_defaults(func=cmd_get_bug_fields_lable)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")

    p = subparsers.add_parser("get_bug_fields_info", help="获取缺陷字段及候选值")
    p.set_defaults(func=cmd_get_bug_fields_info)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")

    p = subparsers.add_parser("batch_update_bug", help="批量更新缺陷（最多50条）")
    p.set_defaults(func=cmd_batch_update_bug)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--workitems_json", required=True, help='工作项列表 (JSON格式, 如 [{"id":123,"status":"done"}])')

    p = subparsers.add_parser("get_removed_bugs", help="获取回收站的缺陷")
    p.set_defaults(func=cmd_get_removed_bugs)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="缺陷ID")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    # ============ 迭代 ============
    p = subparsers.add_parser("get_iterations", help="查询迭代")
    p.set_defaults(func=cmd_get_iterations)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--status", help="状态")

    p = subparsers.add_parser("create_iteration", help="创建迭代")
    p.set_defaults(func=cmd_create_iteration)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--name", required=True, help="名称")
    p.add_argument("--startdate", required=True, help="开始日期")
    p.add_argument("--enddate", required=True, help="结束日期")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--description", help="描述")
    p.add_argument("--status", help="状态")
    p.add_argument("--label", help="标签")
    p.add_argument("--parent_id", help="父迭代ID")

    p = subparsers.add_parser("update_iteration", help="更新迭代")
    p.set_defaults(func=cmd_update_iteration)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="迭代ID")
    p.add_argument("--current_user", required=True, help="变更人")
    p.add_argument("--name", help="名称")
    p.add_argument("--startdate", help="开始日期")
    p.add_argument("--enddate", help="结束日期")
    p.add_argument("--status", help="状态")

    p = subparsers.add_parser("get_iterations_count", help="获取迭代数量")
    p.set_defaults(func=cmd_get_iterations_count)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--status", help="状态")

    p = subparsers.add_parser("get_removed_tasks", help="获取回收站的任务")
    p.set_defaults(func=cmd_get_removed_tasks)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="任务ID")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    # ============ 评论 ============
    p = subparsers.add_parser("get_comments", help="查询评论")
    p.set_defaults(func=cmd_get_comments)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="评论ID")
    p.add_argument("--entry_type", help="评论类型")
    p.add_argument("--entry_id", help="业务对象ID")
    p.add_argument("--author", help="评论人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    p = subparsers.add_parser("create_comments", help="创建评论")
    p.set_defaults(func=cmd_create_comments)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entry_type", required=True, help="评论类型")
    p.add_argument("--entry_id", required=True, help="业务对象ID")
    p.add_argument("--description", required=True, help="内容")
    p.add_argument("--author", help="评论人")
    p.add_argument("--root_id", help="根评论ID")
    p.add_argument("--reply_id", help="回复ID")

    p = subparsers.add_parser("update_comments", help="更新评论")
    p.set_defaults(func=cmd_update_comments)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="评论ID")
    p.add_argument("--description", required=True, help="内容")
    p.add_argument("--change_creator", required=True, help="变更人")

    # ============ 附件/图片 ============
    p = subparsers.add_parser("get_entity_attachments", help="获取附件")
    p.set_defaults(func=cmd_get_entity_attachments)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entry_id", required=True, help="业务对象ID")
    p.add_argument("--type", required=True, help="业务对象类型")

    p = subparsers.add_parser("get_image", help="获取图片下载链接")
    p.set_defaults(func=cmd_get_image)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--image_path", required=True, help="图片路径")

    # ============ 自定义字段 ============
    p = subparsers.add_parser("get_entity_custom_fields", help="获取自定义字段配置")
    p.set_defaults(func=cmd_get_entity_custom_fields)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", required=True, help="实体类型")

    # ============ 工作流 ============
    p = subparsers.add_parser("get_workflows_status_map", help="获取状态映射")
    p.set_defaults(func=cmd_get_workflows_status_map)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--system", required=True, help="系统名 (bug/story)")
    p.add_argument("--workitem_type_id", help="需求类别ID")

    p = subparsers.add_parser("get_workflows_all_transitions", help="获取状态流转")
    p.set_defaults(func=cmd_get_workflows_all_transitions)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--system", required=True, help="系统名 (bug/story)")
    p.add_argument("--workitem_type_id", help="需求类别ID")

    p = subparsers.add_parser("get_workflows_last_steps", help="获取结束状态")
    p.set_defaults(func=cmd_get_workflows_last_steps)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--system", required=True, help="系统名 (bug/story)")
    p.add_argument("--workitem_type_id", help="需求类别ID")
    p.add_argument("--type", help="节点类型")

    p = subparsers.add_parser("get_workflows_first_step", help="获取起始状态")
    p.set_defaults(func=cmd_get_workflows_first_step)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--system", required=True, help="系统名 (bug/story)")
    p.add_argument("--workitem_type_id", help="需求类别ID")
    p.add_argument("--type", help="节点类型")

    # ============ 度量 ============
    p = subparsers.add_parser("get_life_times", help="获取状态流转时间")
    p.set_defaults(func=cmd_get_life_times)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", required=True, help="对象类型 (story/bug/task)")
    p.add_argument("--entity_id", required=True, help="对象ID")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--order", help="排序规则")
    p.add_argument("--fields", help="字段列表")

    # ============ 测试用例 ============
    p = subparsers.add_parser("get_tcases", help="查询测试用例")
    p.set_defaults(func=cmd_get_tcases)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--category_id", help="用例目录ID")
    p.add_argument("--status", help="状态")
    p.add_argument("--type", help="用例类型")
    p.add_argument("--priority", help="用例等级")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--with_count", action="store_true", help="同时查询总数")

    p = subparsers.add_parser("create_or_update_tcases", help="创建/更新测试用例")
    p.set_defaults(func=cmd_create_or_update_tcases)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="测试用例ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--category_id", help="用例目录ID")
    p.add_argument("--status", help="状态")
    p.add_argument("--precondition", help="前置条件")
    p.add_argument("--steps", help="用例步骤")
    p.add_argument("--expectation", help="预期结果")
    p.add_argument("--type", help="用例类型")
    p.add_argument("--priority", help="用例等级")

    p = subparsers.add_parser("create_tcases_batch", help="批量创建测试用例")
    p.set_defaults(func=cmd_create_tcases_batch)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--tcases_json", required=True, help="测试用例列表 (JSON格式)")

    p = subparsers.add_parser("get_tcase_categories", help="获取测试用例目录")
    p.set_defaults(func=cmd_get_tcase_categories)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="目录ID")
    p.add_argument("--name", help="目录名称")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    # ============ 测试计划 ============
    p = subparsers.add_parser("get_test_plans", help="获取测试计划")
    p.set_defaults(func=cmd_get_test_plans)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="测试计划ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--status", help="状态")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--fields", help="字段列表")
    p.add_argument("--with_count", action="store_true", help="同时查询总数")

    p = subparsers.add_parser("get_test_plan_progress", help="获取测试计划执行进度")
    p.set_defaults(func=cmd_get_test_plan_progress)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--test_plan_id", required=True, help="测试计划ID")

    # ============ 看板 ============
    p = subparsers.add_parser("get_board_cards", help="获取看板工作项")
    p.set_defaults(func=cmd_get_board_cards)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="工作项ID")
    p.add_argument("--b_board_id", help="看板ID")
    p.add_argument("--b_column_id", help="栏目ID")
    p.add_argument("--owner", help="处理人")
    p.add_argument("--status", help="状态")
    p.add_argument("--name", help="标题")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--fields", help="字段列表")

    p = subparsers.add_parser("get_board_columns", help="获取看板板块")
    p.set_defaults(func=cmd_get_board_columns)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="板块ID")
    p.add_argument("--name", help="板块名称")
    p.add_argument("--board_id", help="看板ID")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--fields", help="字段列表")

    # ============ Wiki ============
    p = subparsers.add_parser("get_wiki", help="查询 Wiki")
    p.set_defaults(func=cmd_get_wiki)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="ID")
    p.add_argument("--name", help="标题")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")
    p.add_argument("--with_count", action="store_true", help="同时查询总数")

    p = subparsers.add_parser("create_wiki", help="创建 Wiki")
    p.set_defaults(func=cmd_create_wiki)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--name", required=True, help="标题")
    p.add_argument("--markdown_description", help="内容")
    p.add_argument("--creator", help="创建人")
    p.add_argument("--note", help="备注")
    p.add_argument("--parent_wiki_id", help="父Wiki ID")

    p = subparsers.add_parser("update_wiki", help="更新 Wiki")
    p.set_defaults(func=cmd_update_wiki)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="Wiki ID")
    p.add_argument("--name", help="标题")
    p.add_argument("--markdown_description", help="内容")
    p.add_argument("--note", help="备注")
    p.add_argument("--parent_wiki_id", help="父Wiki ID")

    # ============ 工时 ============
    p = subparsers.add_parser("get_timesheets", help="查询工时")
    p.set_defaults(func=cmd_get_timesheets)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", help="对象类型")
    p.add_argument("--entity_id", help="对象ID")
    p.add_argument("--owner", help="创建人")
    p.add_argument("--spentdate", help="日期")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    p = subparsers.add_parser("add_timesheets", help="填写工时")
    p.set_defaults(func=cmd_add_timesheets)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--entity_type", required=True, help="对象类型")
    p.add_argument("--entity_id", required=True, help="对象ID")
    p.add_argument("--timespent", required=True, help="花费工时")
    p.add_argument("--spentdate", required=True, help="日期")
    p.add_argument("--owner", help="创建人")
    p.add_argument("--memo", help="备注")
    p.add_argument("--timeremain", help="剩余工时")

    p = subparsers.add_parser("update_timesheets", help="更新工时")
    p.set_defaults(func=cmd_update_timesheets)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="工时ID")
    p.add_argument("--timespent", required=True, help="花费工时")
    p.add_argument("--memo", help="备注")
    p.add_argument("--timeremain", help="剩余工时")

    p = subparsers.add_parser("delete_timesheets", help="删除工时")
    p.set_defaults(func=cmd_delete_timesheets)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", required=True, help="工时ID")

    # ============ 待办 ============
    p = subparsers.add_parser("get_todo", help="获取待办")
    p.set_defaults(func=cmd_get_todo)
    p.add_argument("--entity_type", required=True, help="对象类型 (story/bug/task)")
    p.add_argument("--user_nick", help="用户昵称")

    # ============ 关联 ============
    p = subparsers.add_parser("get_related_bugs", help="获取关联缺陷")
    p.set_defaults(func=cmd_get_related_bugs)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--story_id", required=True, help="需求ID")

    p = subparsers.add_parser("entity_relations", help="创建关联关系")
    p.set_defaults(func=cmd_entity_relations)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--source_type", required=True, help="源对象类型")
    p.add_argument("--target_type", required=True, help="目标对象类型")
    p.add_argument("--source_id", required=True, help="源对象ID")
    p.add_argument("--target_id", required=True, help="目标对象ID")

    # ============ 发布计划 ============
    p = subparsers.add_parser("get_release_info", help="获取发布计划")
    p.set_defaults(func=cmd_get_release_info)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="发布计划ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--status", help="状态")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")

    p = subparsers.add_parser("get_launch_forms_count", help="获取发布评审数量")
    p.set_defaults(func=cmd_get_launch_forms_count)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--title", help="标题")
    p.add_argument("--status", help="状态")
    p.add_argument("--creator", help="创建人")

    p = subparsers.add_parser("create_launch_form", help="创建发布评审")
    p.set_defaults(func=cmd_create_launch_form)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--template_id", required=True, help="模板ID")
    p.add_argument("--title", help="标题")
    p.add_argument("--creator", help="创建人")

    # ============ 配置 ============
    p = subparsers.add_parser("get_modules", help="获取模块")
    p.set_defaults(func=cmd_get_modules)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="模块ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    p = subparsers.add_parser("get_versions", help="获取版本")
    p.set_defaults(func=cmd_get_versions)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--id", help="版本ID")
    p.add_argument("--name", help="名称")
    p.add_argument("--status", help="状态 (0=未关闭, 1=已关闭)")
    p.add_argument("--limit", type=int, default=30, help="返回数量限制")
    p.add_argument("--page", type=int, default=1, help="页码")

    # ============ 源码 ============
    p = subparsers.add_parser("get_commit_msg", help="获取提交关键字")
    p.set_defaults(func=cmd_get_commit_msg)
    p.add_argument("--workspace_id", required=True, type=int, help="项目ID")
    p.add_argument("--object_id", required=True, help="对象ID")
    p.add_argument("--type", required=True, help="对象类型 (story/task/bug)")

    # ============ 消息 ============
    p = subparsers.add_parser("send_qiwei_message", help="发送企业微信消息")
    p.set_defaults(func=cmd_send_qiwei_message)
    p.add_argument("--msg", required=True, help="消息内容 (Markdown格式)")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, 'func'):
        print(__doc__)
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
