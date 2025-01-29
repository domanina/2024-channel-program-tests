import random
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field

from consts.consts import TEST_IMAGE_URL, TEST_USER_NAME, TEST_USER_EMAIL, ADMIN_USER_ROLE
from tools.helper import generate_random_string


class ItemType(Enum):
    TEST = "test"
    EVENT = "event"


class ChannelType(Enum):
    TEST_CH = "testch"
    TEST_FGHG = "testfg"

ch_to_item_type_map = {
    ChannelType.TEST_CH.value: ItemType.TEST.value,
    ChannelType.TEST_FGHG.value: ItemType.TEST.value,
}


# @dataclass
class AppItemModel(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    description: Optional[str] = None
    images: Optional[str] = None
    name: Optional[str] = None
    roles: Optional[List[str]] = None
    startTime: Optional[int] = Field(serialization_alias="start_time")
    endTime: Optional[int] = Field(serialization_alias="end_time")


def create_item(
        type: str = ChannelType.TEST_CH.value,
        is_actual_item: bool = True
):
    if is_actual_item:
        start_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        end_time = int((datetime.now() + timedelta(hours=2)).timestamp())
    else:
        start_time = int((datetime.now() - timedelta(days=15)).timestamp())
        end_time = int((datetime.now() - timedelta(days=14)).timestamp())

    type_map_stream_id = ch_to_item_type_map.get(type)

    return AppItemModel(
        type=type_map_stream_id,
        images=TEST_IMAGE_URL,
        name=TEST_USER_NAME,
        roles=[ADMIN_USER_ROLE],
        startTime=start_time,
        endTime=end_time,
        description=generate_random_string(),
    )
