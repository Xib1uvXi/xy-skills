"""
TAPD API 客户端封装

使用前请设置环境变量：
- TAPD_ACCESS_TOKEN: 个人访问令牌（推荐）
- TAPD_API_USER: API 账号
- TAPD_API_PASSWORD: API 密钥
- TAPD_API_BASE_URL: API 地址（默认 https://api.tapd.cn）
- TAPD_BASE_URL: TAPD Web 地址（默认 https://www.tapd.cn）
- CURRENT_USER_NICK: 当前用户昵称
"""

import os
import base64
import json
from typing import Optional, Dict, Any, List
import requests


def check_env_vars():
    """检查环境变量是否已设置"""
    access_token = os.getenv("TAPD_ACCESS_TOKEN")
    api_user = os.getenv("TAPD_API_USER")
    api_password = os.getenv("TAPD_API_PASSWORD")
    return access_token or (api_user and api_password)


def get_env_check_message():
    """获取环境变量检查消息"""
    access_token = os.getenv("TAPD_ACCESS_TOKEN")
    api_user = os.getenv("TAPD_API_USER")

    if access_token or api_user:
        return None

    return """
错误: TAPD 访问凭证未设置

请先设置以下环境变量之一：

方案 1：使用个人访问令牌（推荐）
  export TAPD_ACCESS_TOKEN="你的个人访问令牌"
  获取方式：https://www.tapd.cn/personal_settings/index?tab=personal_token

方案 2：使用 API 账号密码
  export TAPD_API_USER="你的API账号"
  export TAPD_API_PASSWORD="你的API密钥"

设置后重新运行脚本。
"""


class TAPDClient:
    """TAPD API 客户端"""

    def __init__(self):
        # 检查环境变量
        env_msg = get_env_check_message()
        if env_msg:
            print(env_msg)
            raise ValueError("TAPD 访问凭证未设置")

        self.access_token = os.getenv("TAPD_ACCESS_TOKEN")
        self.api_user = os.getenv("TAPD_API_USER")
        self.api_password = os.getenv("TAPD_API_PASSWORD")
        self.base_url = os.getenv("TAPD_API_BASE_URL", "https://api.tapd.cn")
        self._nick = os.getenv("CURRENT_USER_NICK")
        self._nick_fetched = bool(self._nick)
        self._mini_project_cache = {}

        if self.access_token:
            self.headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
                "Via": "mcp"
            }
        elif self.api_user and self.api_password:
            auth_str = f"{self.api_user}:{self.api_password}"
            self.headers = {
                "Authorization": f"Basic {base64.b64encode(auth_str.encode()).decode()}",
                "Content-Type": "application/json",
                "Via": "mcp"
            }

    @property
    def nick(self):
        if not self._nick_fetched and self.access_token:
            self._nick_fetched = True
            self._nick = self.get_user_info() or self._nick
        return self._nick

    def _make_request(self, method: str, endpoint: str,
                      params: Optional[Dict] = None,
                      data: Optional[Dict] = None) -> Dict:
        """发送 API 请求"""
        url = f"{self.base_url}/{endpoint}"
        separator = '&' if '?' in url else '?'
        url = f"{url}{separator}s=mcp"

        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def is_cloud_env(self) -> bool:
        """判断是否为 CLOUD 环境"""
        return 'api.tapd.cn' in self.base_url

    def _to_long_id(self, single_id: str, workspace_id: str) -> str:
        """将短 ID 转换为长 ID"""
        single_id = single_id.strip()
        if single_id.isdigit() and len(single_id) <= 9:
            padded_id = single_id.zfill(9)
            pre_id = "11" if self.is_cloud_env() else "10"
            return f"{pre_id}{workspace_id}{padded_id}"
        return single_id

    def _convert_id(self, params: Dict, key: str, workspace_id: str):
        """转换 ID 为长 ID"""
        if key in params and workspace_id:
            id_val = str(params[key])
            if "," in id_val:
                id_list = id_val.split(",")
                params[key] = ",".join([self._to_long_id(i, workspace_id) for i in id_list])
            else:
                params[key] = self._to_long_id(id_val, workspace_id)

    # ============ 用户相关 ============

    def get_user_info(self) -> Optional[str]:
        """获取用户信息"""
        try:
            response = self._make_request("GET", "users/info")
            return response.get("data", {}).get("nick")
        except Exception:
            return None

    def get_user_participant_projects(self, data: Dict) -> Dict:
        """获取用户参与的项目列表"""
        return self._make_request("GET", "workspaces/user_participant_projects", params=data)

    # ============ 项目相关 ============

    def get_workspace_info(self, data: Dict) -> Dict:
        """获取项目信息"""
        return self._make_request("GET", "workspaces/get_workspace_info", params=data)

    def get_workitem_types(self, data: Dict) -> Dict:
        """获取需求类别"""
        return self._make_request("GET", "workitem_types", params=data)

    def get_workspace_users(self, params: Dict) -> Dict:
        """获取项目成员列表"""
        return self._make_request("GET", "workspaces/users", params=params)

    def get_sub_workspaces(self, params: Dict) -> Dict:
        """获取子项目信息"""
        return self._make_request("GET", "workspaces/sub_workspaces", params=params)

    def get_workspace_reports(self, params: Dict) -> Dict:
        """获取项目报告"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "workspace_reports", params=default_params)

    # ============ 需求/任务相关 ============

    def get_stories(self, params: Dict) -> Dict:
        """获取需求或任务"""
        entity_type = params.get("entity_type", "stories")
        workspace_id = str(params.get("workspace_id", ""))

        self._convert_id(params, "id", workspace_id)

        default_params = {"page": 1, "limit": 10}
        default_params.update(params)
        return self._make_request("GET", entity_type, params=default_params)

    def get_story_count(self, params: Dict) -> Dict:
        """获取需求数量"""
        entity_type = params.get("entity_type", "stories")
        return self._make_request("GET", f"{entity_type}/count", params=params)

    def create_or_update_story(self, data: Dict) -> Dict:
        """创建/更新需求或任务"""
        entity_type = data.get("entity_type", "stories")
        workspace_id = str(data.get("workspace_id", ""))

        self._convert_id(data, "id", workspace_id)

        if self.nick:
            if 'id' in data:
                data['current_user'] = self.nick
            else:
                data['creator'] = self.nick

        return self._make_request("POST", entity_type, data=data)

    def get_stories_fields_lable(self, data: Dict) -> Dict:
        """获取字段中英文对照"""
        workspace_id = data.get("workspace_id")
        return self._make_request("GET", f"stories/get_fields_lable?workspace_id={workspace_id}")

    def get_stories_fields_info(self, data: Dict) -> Dict:
        """获取字段及候选值"""
        workspace_id = data.get("workspace_id")
        return self._make_request("GET", f"stories/get_fields_info?workspace_id={workspace_id}")

    def get_story_changes(self, params: Dict) -> Dict:
        """获取需求变更历史"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "story_changes", params=default_params)

    def get_task_changes(self, params: Dict) -> Dict:
        """获取任务变更历史"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "task_changes", params=default_params)

    def batch_update_story(self, data: Dict) -> Dict:
        """批量更新需求（最多50条）"""
        if self.nick:
            for item in data.get("workitems", []):
                item.setdefault("current_user", self.nick)
        return self._make_request("POST", "stories/batch_update_story", data=data)

    def get_story_categories(self, params: Dict) -> Dict:
        """获取需求分类"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "story_categories", params=default_params)

    def get_link_stories(self, params: Dict) -> Dict:
        """获取需求与其它需求的关联关系"""
        return self._make_request("GET", "stories/get_link_stories", params=params)

    def get_story_tcase(self, params: Dict) -> Dict:
        """获取需求与测试用例关联关系"""
        return self._make_request("GET", "stories/get_story_tcase", params=params)

    def get_time_relative_stories(self, params: Dict) -> Dict:
        """获取需求前后置关系"""
        return self._make_request("GET", "stories/get_time_relative_stories", params=params)

    def get_removed_stories(self, params: Dict) -> Dict:
        """获取回收站的需求"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "stories/get_removed_stories", params=default_params)

    # ============ 缺陷相关 ============

    def get_bug(self, params: Dict) -> Dict:
        """获取缺陷"""
        workspace_id = str(params.get("workspace_id", ""))
        self._convert_id(params, "id", workspace_id)

        default_params = {"page": 1, "limit": 10}
        default_params.update(params)
        return self._make_request("GET", "bugs", params=default_params)

    def get_bug_count(self, params: Dict) -> Dict:
        """获取缺陷数量"""
        return self._make_request("GET", "bugs/count", params=params)

    def create_or_update_bug(self, data: Dict) -> Dict:
        """创建或更新缺陷"""
        workspace_id = str(data.get("workspace_id", ""))
        self._convert_id(data, "id", workspace_id)

        if self.nick:
            if 'id' in data:
                data['current_user'] = self.nick
            else:
                data['reporter'] = self.nick

        return self._make_request("POST", "bugs", data=data)

    def get_bug_changes(self, params: Dict) -> Dict:
        """获取缺陷变更历史"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "bug_changes", params=default_params)

    def get_bug_fields_lable(self, data: Dict) -> Dict:
        """获取缺陷字段中英文对照"""
        workspace_id = data.get("workspace_id")
        return self._make_request("GET", f"bugs/get_fields_lable?workspace_id={workspace_id}")

    def get_bug_fields_info(self, data: Dict) -> Dict:
        """获取缺陷字段及候选值"""
        workspace_id = data.get("workspace_id")
        return self._make_request("GET", f"bugs/get_fields_info?workspace_id={workspace_id}")

    def batch_update_bug(self, data: Dict) -> Dict:
        """批量更新缺陷（最多50条）"""
        if self.nick:
            for item in data.get("workitems", []):
                item.setdefault("current_user", self.nick)
        return self._make_request("POST", "bugs/batch_update_bug", data=data)

    def get_removed_bugs(self, params: Dict) -> Dict:
        """获取回收站的缺陷"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "bugs/get_removed_bugs", params=default_params)

    # ============ 迭代相关 ============

    def get_iterations(self, data: Dict) -> Dict:
        """获取迭代"""
        return self._make_request("GET", "iterations", params=data)

    def create_or_update_iteration(self, data: Dict) -> Dict:
        """创建/更新迭代"""
        if self.nick:
            if 'id' in data:
                data['current_user'] = self.nick
            else:
                data['creator'] = self.nick
        return self._make_request("POST", "iterations", data=data)

    def get_iterations_count(self, params: Dict) -> Dict:
        """获取迭代数量"""
        return self._make_request("GET", "iterations/count", params=params)

    def get_removed_tasks(self, params: Dict) -> Dict:
        """获取回收站的任务"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "tasks/get_removed_tasks", params=default_params)

    # ============ 评论相关 ============

    def get_comments(self, params: Dict) -> Dict:
        """获取评论"""
        default_params = {"page": 1, "limit": 10}
        default_params.update(params)
        return self._make_request("GET", "comments", params=default_params)

    def create_comments(self, data: Dict) -> Dict:
        """创建评论"""
        workspace_id = str(data.get("workspace_id", ""))
        self._convert_id(data, "entry_id", workspace_id)

        if self.nick:
            if 'id' in data:
                data['change_creator'] = self.nick
            else:
                data['author'] = self.nick

        return self._make_request("POST", "comments", data=data)

    # ============ 附件相关 ============

    def get_attachments(self, params: Dict) -> Dict:
        """获取附件"""
        return self._make_request("GET", "attachments", params=params)

    def get_attachment_download_url(self, params: Dict) -> Dict:
        """获取附件下载链接"""
        return self._make_request("GET", "attachments/down", params=params)

    def get_image(self, params: Dict) -> Dict:
        """获取图片下载链接"""
        return self._make_request("GET", "files/get_image", params=params)

    # ============ 自定义字段 ============

    def get_entity_custom_fields(self, data: Dict) -> Dict:
        """获取自定义字段配置"""
        workspace_id = data.get("workspace_id")
        entity_type = data.get("entity_type", "stories")
        return self._make_request("GET", f"{entity_type}/custom_fields_settings?workspace_id={workspace_id}")

    # ============ 工作流相关 ============

    def get_workflows_status_map(self, data: Dict) -> Dict:
        """获取状态映射"""
        return self._make_request("GET", "workflows/status_map", params=data)

    def get_workflows_all_transitions(self, data: Dict) -> Dict:
        """获取状态流转"""
        return self._make_request("GET", "workflows/all_transitions", params=data)

    def get_workflows_last_steps(self, data: Dict) -> Dict:
        """获取结束状态"""
        return self._make_request("GET", "workflows/last_steps", params=data)

    def get_workflows_first_step(self, data: Dict) -> Dict:
        """获取起始状态"""
        return self._make_request("GET", "workflows/first_step", params=data)

    # ============ 度量相关 ============

    def get_life_times(self, params: Dict) -> Dict:
        """获取状态流转时间"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "life_times", params=default_params)

    # ============ 测试用例相关 ============

    def get_tcases(self, params: Dict) -> Dict:
        """获取测试用例"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "tcases", params=default_params)

    def get_tcases_count(self, params: Dict) -> Dict:
        """获取测试用例数量"""
        return self._make_request("GET", "tcases/count", params=params)

    def create_tcases(self, data: Dict) -> Dict:
        """创建测试用例"""
        if self.nick:
            if 'id' in data:
                data['modifier'] = self.nick
            else:
                data['creator'] = self.nick
        return self._make_request("POST", "tcases", data=data)

    def create_tcases_batch_save(self, data: List[Dict]) -> Dict:
        """批量创建测试用例"""
        if self.nick:
            for tcase in data:
                tcase.setdefault('creator', self.nick)
        return self._make_request("POST", "tcases/batch_save", data=data)

    def get_tcase_categories(self, params: Dict) -> Dict:
        """获取测试用例目录"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "tcase_categories", params=default_params)

    # ============ 测试计划相关 ============

    def get_test_plans(self, params: Dict) -> Dict:
        """获取测试计划"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "test_plans", params=default_params)

    def get_test_plans_count(self, params: Dict) -> Dict:
        """获取测试计划数量"""
        return self._make_request("GET", "test_plans/count", params=params)

    def get_test_plan_progress(self, params: Dict) -> Dict:
        """获取测试计划执行进度"""
        return self._make_request("GET", "test_plans/get_test_plan_progress", params=params)

    # ============ 看板相关 ============

    def get_board_cards(self, params: Dict) -> Dict:
        """获取看板工作项"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "board_cards", params=default_params)

    def get_board_columns(self, params: Dict) -> Dict:
        """获取看板板块"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "board_columns", params=default_params)

    # ============ Wiki 相关 ============

    def get_wiki(self, params: Dict) -> Dict:
        """获取 Wiki"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "tapd_wikis", params=default_params)

    def get_wiki_count(self, params: Dict) -> Dict:
        """获取 Wiki 数量"""
        return self._make_request("GET", "tapd_wikis/count", params=params)

    def create_wiki(self, data: Dict) -> Dict:
        """创建/更新 Wiki"""
        if self.nick:
            if 'id' in data:
                data['modifier'] = self.nick
            else:
                data['creator'] = self.nick
        return self._make_request("POST", "tapd_wikis", data=data)

    # ============ 工时相关 ============

    def get_timesheets(self, params: Dict) -> Dict:
        """获取工时"""
        return self._make_request("GET", "timesheets", params=params)

    def update_timesheets(self, data: Dict) -> Dict:
        """创建/更新工时"""
        if self.nick:
            data['owner'] = self.nick
        return self._make_request("POST", "timesheets", data=data)

    def delete_timesheets(self, data: Dict) -> Dict:
        """删除工时"""
        return self._make_request("POST", "timesheets/delete", data=data)

    # ============ 待办相关 ============

    def get_todo(self, data: Dict) -> Dict:
        """获取待办"""
        entity_type = data.get("entity_type")
        user_nick = data.get("user_nick", self.nick)
        return self._make_request("GET", f"users/todo/{user_nick}/{entity_type}")

    # ============ 关联相关 ============

    def get_related_bugs(self, data: Dict) -> Dict:
        """获取关联缺陷"""
        return self._make_request("GET", "stories/get_related_bugs", params=data)

    def add_entity_relations(self, data: Dict) -> Dict:
        """创建关联关系"""
        return self._make_request("POST", "relations", data=data)

    # ============ 发布计划 ============

    def get_release_info(self, params: Dict) -> Dict:
        """获取发布计划"""
        return self._make_request("GET", "releases", params=params)

    def get_launch_forms_count(self, params: Dict) -> Dict:
        """获取发布评审数量"""
        return self._make_request("GET", "launch_forms/count", params=params)

    def create_launch_form(self, data: Dict) -> Dict:
        """创建发布评审"""
        if self.nick:
            data.setdefault('creator', self.nick)
        return self._make_request("POST", "launch_forms", data=data)

    # ============ 配置相关 ============

    def get_modules(self, params: Dict) -> Dict:
        """获取模块"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "modules", params=default_params)

    def get_versions(self, params: Dict) -> Dict:
        """获取版本"""
        default_params = {"page": 1, "limit": 30}
        default_params.update(params)
        return self._make_request("GET", "versions", params=default_params)

    # ============ 源码提交关键字 ============

    def get_scm_copy_keywords(self, data: Dict) -> Dict:
        """获取提交关键字"""
        workspace_id = str(data.get("workspace_id", ""))
        self._convert_id(data, "object_id", workspace_id)
        return self._make_request("GET", "svn_commits/get_scm_copy_keywords", params=data)

    # ============ 企业微信消息 ============

    def send_message(self, data: Dict) -> str:
        """发送企业微信消息"""
        bot_url = os.getenv("BOT_URL")
        msg = data.get("msg", "")

        if '@' in msg:
            chat_data = {
                'msgtype': 'markdown',
                'markdown': {'content': msg}
            }
        else:
            chat_data = {
                'msgtype': 'markdown_v2',
                'markdown_v2': {'content': msg}
            }

        response = requests.post(
            url=bot_url,
            headers={'Content-Type': 'application/json'},
            json=chat_data,
            timeout=500
        )
        return response.text

    # ============ 分类相关 ============

    def get_category_id(self, data: Dict) -> Dict:
        """获取需求分类 ID"""
        return self._make_request("GET", "story_categories", params=data)

    # ============ 工具方法 ============

    @staticmethod
    def _unwrap_entity(item: dict):
        """解包实体包装器，返回 (entity_key, inner_dict)"""
        for key in ('Story', 'Bug', 'Task', 'Iteration'):
            if key in item and isinstance(item[key], dict):
                return key, item[key]
        return None, item

    @staticmethod
    def _wrap_entity(entity_key, obj: dict) -> dict:
        """根据 entity_key 重新包装"""
        return {entity_key: obj} if entity_key else obj

    def _filter_obj_fields(self, obj: dict, entity_key, fields: list = None) -> dict:
        """过滤单个对象的字段"""
        new_obj = {}
        for k, v in obj.items():
            if k.startswith('custom_field_') and (v is None or v == '') and (not fields or k not in fields):
                continue
            if k.startswith('description') and entity_key != 'Iteration' and (not fields or k not in fields):
                continue
            if k.startswith('custom_plan_field_') and v == '0':
                continue
            new_obj[k] = v
        return new_obj

    def filter_fields(self, data_list: List, fields_param: Optional[str] = None) -> List:
        """过滤字段"""
        if not data_list:
            return data_list

        if isinstance(fields_param, str):
            fields = [f.strip() for f in fields_param.split(',') if f.strip()]
        elif isinstance(fields_param, list):
            fields = fields_param
        else:
            fields = []

        filtered = []
        for item in data_list:
            if isinstance(item, dict):
                entity_key, obj = self._unwrap_entity(item)
                new_obj = self._filter_obj_fields(obj, entity_key, fields)
                filtered.append(self._wrap_entity(entity_key, new_obj))
            else:
                filtered.append(item)
        return filtered

    def filter_fields_for_create_or_update(self, item: Dict) -> Dict:
        """过滤创建/更新的字段"""
        if not item:
            return item
        entity_key, obj = self._unwrap_entity(item)
        new_obj = self._filter_obj_fields(obj, entity_key)
        return self._wrap_entity(entity_key, new_obj)

    def get_story_or_task_url_template(self, workspace_id: int, entity_type: str, tapd_base_url: str) -> str:
        """获取 URL 模板"""
        is_mini = self.check_mini_project(workspace_id)
        if entity_type == 'tasks':
            return f'{tapd_base_url}/{workspace_id}/prong/tasks/view/{{id}}'
        else:
            if is_mini:
                return f'{tapd_base_url}/tapd_fe/t/index/{workspace_id}?workitemId={{id}}'
            else:
                return f'{tapd_base_url}/{workspace_id}/prong/stories/view/{{id}}'

    def check_mini_project(self, workspace_id: int) -> bool:
        """判断是否轻协作项目（结果缓存）"""
        if workspace_id not in self._mini_project_cache:
            data = {"workspace_id": workspace_id}
            ret = self.get_workspace_info(data)
            self._mini_project_cache[workspace_id] = (
                ret.get('data', {}).get('Workspace', {}).get('category') == 'mini_project'
            )
        return self._mini_project_cache[workspace_id]
