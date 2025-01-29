from enum import Enum

TIMEOUT_SEC = 5
TEST_IMAGE_URL = "demo.jpg"
TEST_IMAGE_URL_T = "demot.jpg"
TEST_USER_NAME = "test"
TEST_USER_EMAIL = "test@test.de"
ADMIN_USER_ROLE = "test_a"
FIRST_USER_ROLE = "test"
SECOND_USER_ROLE = "test_2"

WRONG_CREDS = ["wrong", None, "83737838"]


class Colors(Enum):
    BLACK = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[92m"
    YELLOW = "\033[33m"


class TypeString(Enum):
    CHAR_NUM_UPPER = "char_num_upper"
    CHAR_NUM_LOWER = "char_num_lower"
    CHAR_UPPER = "char_upper"
    CHAR_LOWER = "char_lower"
