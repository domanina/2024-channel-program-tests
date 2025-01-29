import allure
from dateutil import parser
from datetime import datetime, timezone


def convert_to_iso_format(time):
    if isinstance(time, int):
        return datetime.fromtimestamp(time, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    else:
        dt = parser.parse(time)
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
