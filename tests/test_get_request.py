import os
from datetime import timedelta

import pytest
from concurrent.futures import ThreadPoolExecutor, as_completed

from config.config import API_KEY
from consts.consts import WRONG_CREDS
from helpers.helper import *
from http import HTTPStatus

from services.app_mgmt.models.app_item_model import create_item, ItemType, ChannelType
from tools.helper import check_status_code
from tools.logger import get_logger

logger = get_logger(name="logger")


@allure.suite("GET items tests")
class TestGetItem:

    @allure.title("Get all Items")
    def test_get_all_data(self, app_mgmt_api_client):
        response = app_mgmt_api_client.get_item_data(api_key=API_KEY)
        check_status_code(response, HTTPStatus.OK)

    @pytest.mark.parametrize("wrong_creds", WRONG_CREDS)
    @allure.title("Access denied with wrong api key")
    def test_get_all_data_access_denied(self, app_mgmt_api_client, wrong_creds):
        response = app_mgmt_api_client.get_item_data(api_key=wrong_creds)
        check_status_code(response, HTTPStatus.FORBIDDEN)

    @pytest.mark.parametrize("item_id", [-1, "not_exist", 2345678765432])
    @allure.title("Get one item - empty result with not exist item_id")
    def test_get_empty_not_exist_id(self, app_mgmt_api_client, item_id):
        response = app_mgmt_api_client.get_item_data(api_key=API_KEY, item_id=item_id)
        check_status_code(response, HTTPStatus.OK)
        assert response.json() == [], f"Test failed. Different actual body : {response.json()}"

    @pytest.mark.parametrize("item_type", [type.value for type in ItemType])
    @allure.title("Get one item by id with full body - every item Type")
    def test_get_created_item_full(self, app_mgmt_api_client, item_type):
        obj_req = create_item()
        bj_req_json = obj_req.model_dump(exclude_none=True)
        response = app_mgmt_api_client.post_item_data(payload=bj_req_json, api_key=API_KEY)
        item_id = response.json()["id"]

        response_get = app_mgmt_api_client.get_item_data(api_key=API_KEY, item_id=item_id)
        check_status_code(response_get, HTTPStatus.OK)
        compare_object_with_get_response(obj_req, response_get.json()[0])

    @pytest.mark.parametrize("startTime, endTime", [
        ("2023-02-16T12:24:55.000Z", "2023-02-16T13:24:55.000Z"),
        ("05.03.2024 22:30:00", "05.03.2024 23:30:00"),
        ("2023/02/16 13:24:55", "2023/02/16 14:24:55"),
        ("16 Feb 2023 13:24:55", "16 Feb 2023 14:24:55")
    ])
    @allure.title("Get one item by id created with different time formats")
    def test_get_created_item_iso_date(self, app_mgmt_api_client, startTime, endTime):
        obj_req = create_item()
        obj_req_json = obj_req.model_dump(exclude_none=True)
        obj_req_json["startTime"] = convert_to_iso_format(obj_req.startTime)
        obj_req_json["endTime"] = convert_to_iso_format(obj_req.endTime)
        response = app_mgmt_api_client.post_item_data(payload=obj_req_json, api_key=API_KEY)
        item_id = response.json()["id"]

        response_get = app_mgmt_api_client.get_item_data(api_key=API_KEY, item_id=item_id)
        check_status_code(response_get, HTTPStatus.OK)
        compare_object_with_get_response(obj_req, response_get.json()[0])


    @allure.title("Test item data retrieval performance with multiple parallel requests")
    def test_item_retrieval_performance(self, app_mgmt_api_client):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(app_mgmt_api_client.get_item_data, api_key=API_KEY) for _ in range(10)]
            for future in as_completed(futures):
                response = future.result()
                assert response.status_code == HTTPStatus.OK, f"Request failed with status code {response.status_code}"


    @allure.title("Get item with unknown role in query param")
    def test_get_unknown_role(self, app_mgmt_api_client):
        response = app_mgmt_api_client.get_item_data(api_key=API_KEY, roles=["unknown"])
        check_status_code(response, HTTPStatus.OK)
        assert response.json() == [], f"Test failed. Different actual body : {response.json()}"
