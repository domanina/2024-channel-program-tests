import json
from typing import Optional, List
import allure
from requests import Response

from consts.consts import ADMIN_USER_ROLE
from services.api_client.api_client import ApiClient
from config.config import BASE_URL
from tools.singleton import Singleton


class ChannelMgmtApi(ApiClient, metaclass=Singleton):
    def __init__(self, url=BASE_URL):
        super().__init__(url=url)

    @allure.step("Get request to get item")
    def get_item_data(self, api_key: str, item_id: Optional[str] = None, roles: Optional[List[str]] = None) -> Response:
        path = "/..."
        if roles is None:
            roles = [ADMIN_USER_ROLE]
        roles_param = json.dumps(roles)

        params = {"id": item_id, "roles": roles_param} if item_id else {"roles": roles_param}
        return self._get(path=path, api_key=api_key, params=params, json=None)

    @allure.step("POST request to create item")
    def post_item_data(self, payload: dict, api_key: str) -> Response:
        path = "/..."
        return self._post(path=path, json=payload, api_key=api_key)

    @allure.step("PUT request to update item")
    def put_item_data(self, payload: dict, api_key: str) -> Response:
        path = "/..."
        return self._put(path=path, json=payload, api_key=api_key)

    @allure.step("DELETE request to delete item")
    def delete_item_data(self, item_id: int, api_key: str, roles: Optional[List[str]] = None) -> Response:
        path = "/..."
        if roles is None:
            roles = [ADMIN_USER_ROLE]
        payload = {
            "id": item_id,
            "roles": roles
        }

        return self._delete(path=path, json=payload, api_key=api_key)
