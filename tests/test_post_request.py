import os
import time

import pytest

from config.config import API_KEY
from consts.consts import FIRST_USER_ROLE, SECOND_USER_ROLE, ADMIN_USER_ROLE
from http import HTTPStatus

from services.app_mgmt.models.app_item_model import create_item, ChannelType
from tools.helper import check_status_code
from tools.logger import get_logger

logger = get_logger(name="logger")


@allure.suite("POST item tests")
class TestPostitem:

    @allure.title("POST valid item - only required fields")
    def test_post_item_data(self, app_mgmt_api_client):
        item_obj_req = create_item()
        item_obj_req_json = item_obj_req.model_dump(exclude_none=True)
        response = app_mgmt_api_client.post_item_data(payload=item_obj_req_json, api_key=API_KEY)
        check_status_code(response, HTTPStatus.OK)
        compare_item_object_with_post_response(item_obj_req, response.json())

    @allure.title("POST invalid item - not exist channel id type")
    def test_post_item_not_exist_stream_id(self, app_mgmt_api_client):
        item_obj_req = create_item(item_type="not_exist")
        item_obj_req_json = item_obj_req.model_dump(exclude_none=True)
        response = app_mgmt_api_client.post_item_data(payload=item_obj_req_json, api_key=API_KEY)
        check_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.parametrize("field, invalid_len", [
        ("description", "a" * 1001),
        ("type", "a" * 251),
        ("title", "a" * 201),
        ("name", "a" * 501),
        ("images", "a" * 1001),
    ])
    @allure.title("POST invalid item - length of value out of range")
    def test_post_item_data_invalid_data_len(self, app_mgmt_api_client, field, invalid_len):
        item_obj_req = create_item()
        item_obj_req_json = item_obj_req.model_dump(exclude_none=True)
        item_obj_req_json[field] = invalid_len
        response = app_mgmt_api_client.post_item_data(payload=item_obj_req_json, api_key=API_KEY)
        check_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.parametrize("startTime, endTime", [
        ("2023-02-16T12:24:55.000Z", "2023-02-16T13:24:55.000Z"),
        ("05.03.2024 22:30:00", "05.03.2024 23:30:00"),
        ("2023/02/16 13:24:55", "2023/02/16 14:24:55"),
        ("16 Feb 2023 13:24:55", "16 Feb 2023 14:24:55")
    ])
    @allure.title("POST valid item - different date formats")
    def test_post_item_data_iso_date(self, app_mgmt_api_client, startTime, endTime):
        item_obj_req = create_item()
        item_obj_req.startTime = startTime
        item_obj_req.endTime = endTime
        item_obj_req_json = item_obj_req.model_dump(exclude_none=True)
        response = app_mgmt_api_client.post_item_data(payload=item_obj_req_json, api_key=API_KEY)
        check_status_code(response, HTTPStatus.OK)
        compare_item_object_with_post_response(item_obj_req, response.json())
