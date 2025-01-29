import json
import random
import string
from http import HTTPStatus

import allure
from deepdiff import DeepDiff

from requests import Response
from jsonschema import validate
from consts.consts import Colors, TypeString
from tools.logger import get_logger

logger = get_logger(name="logger")


@allure.step
def valid_schema(data: object, schema_file: str):
    with open(schema_file) as f:
        schema = json.load(f)
        validate(instance=data, schema=schema)


@allure.step("Compare received status code with expected")
def check_status_code(response: Response, expected_status_code: int):
    expected_code = expected_status_code.value if isinstance(expected_status_code, HTTPStatus) else expected_status_code
    with allure.step(f"Expected status code: {expected_code}"):
        pass
    with allure.step(f"Actual status code: {response.status_code}"):
        pass
    assert response.status_code == expected_status_code, \
            (f"Test failed. HTTP status is : {response.status_code},({response.text}), "
             f"expected  HTTP status: {expected_status_code}")


def pretty_log_request(response: Response, method: str, **kwargs):
    logger.info(f"{Colors.GREEN.value}{method} request to {response.url}{Colors.BLACK.value}")
    if kwargs.get("json") is not None:
        logger.info(f"{Colors.GREEN.value}Request body is {kwargs.get('json')}{Colors.BLACK.value}")
    logger.info(f"Response status is: {response.status_code}")
    logger.info(f"Response body is {response.text}")


def generate_random_string(length: int = 20, string_type: str = "") -> str:
    if string_type:
        if string_type == TypeString.CHAR_NUM_UPPER.value:
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        elif string_type == TypeString.CHAR_NUM_LOWER.value:
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        elif string_type == TypeString.CHAR_UPPER.value:
            return ''.join(random.choices(string.ascii_uppercase, k=length))
        elif string_type == TypeString.CHAR_LOWER.value:
            return ''.join(random.choices(string.ascii_lowercase, k=length))
    else:
        prefix = "qa-test-"
        suffix_length = length - len(prefix)
        if suffix_length <= 0:
            raise ValueError("Length should be greater than the length of the prefix")

        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=suffix_length))
        return prefix + suffix


def assert_body(expected: dict, actual: dict, excluded: list = None):
    mismatches = []
    for key, value in expected.items():
        if key in excluded:
            continue
        if actual.get(key) != value:
            mismatches.append(f"{key}: expected {value}, got {actual.get(key)}")

    if mismatches:
        allure.attach("\n".join(mismatches), name="Mismatches", attachment_type=allure.attachment_type.TEXT)
        assert not mismatches, f"Test failed.Different actual body. Mismatches: {mismatches}"
