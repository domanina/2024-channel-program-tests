import os
import pytest

from config.config import API_KEY
from consts.consts import FIRST_USER_ROLE, SECOND_USER_ROLE, ADMIN_USER_ROLE, WRONG_CREDS
from http import HTTPStatus

from services.app_mgmt.models.app_item_model import create_item, ChannelType
from tools.helper import check_status_code
from tools.logger import get_logger

logger = get_logger(name="logger")


@allure.suite("DELETE item tests")
class TestDeleteItem:
    @pytest.mark.parametrize("wrong_creds", WRONG_CREDS)
    @allure.title("DELETE data - access denied with wrong api key")
    def test_delete_access_denied(self, app_mgmt_api_client, wrong_creds):
        response = app_mgmt_api_client.delete_item_data(item_id=666, api_key=wrong_creds)
        check_status_code(response, HTTPStatus.FORBIDDEN)

    @allure.title("DELETE item successfully")
    def test_delete_item(self, app_mgmt_api_client):
        item_obj_req = create_item()
        item_obj_req_json = item_obj_req.model_dump(exclude_none=True)
        response = app_mgmt_api_client.post_item_data(payload=item_obj_req_json, api_key=API_KEY)

        item_id = response.json()["id"]
        response = app_mgmt_api_client.delete_item_data(item_id=item_id, api_key=API_KEY)
        check_status_code(response, HTTPStatus.OK)

        with allure.step("Check item was deleted via GET request - response body is empty"):
            response = app_mgmt_api_client.get_item_data(api_key=API_KEY, item_id=item_id)
            assert response.json() == [], f"Test failed. Different actual body : {response.json()}"

    @allure.title("DELETE deleted item")
    def test_delete_item_twice(self, app_mgmt_api_client):
        item_obj_req = create_item()
        item_obj_req_json = item_obj_req.model_dump(exclude_none=True)
        response = app_mgmt_api_client.post_item_data(payload=item_obj_req_json, api_key=API_KEY)
        item_id = response.json()["id"]
        app_mgmt_api_client.delete_item_data(item_id=item_id, api_key=API_KEY)
        response = app_mgmt_api_client.delete_item_data(item_id=item_id, api_key=API_KEY)
        check_status_code(response, HTTPStatus.OK)
