import pytest

from db_actions.app_db_reader import delete_test_data
from services.app_mgmt.app_mgmt_api import ChannelMgmtApi


@pytest.fixture(scope="session")
def app_mgmt_api_client():
    api = ChannelMgmtApi()
    yield api


@pytest.fixture(scope="class", autouse=True)
def delete_test_entries_from_db():
    yield
    delete_test_data()
