from typing import Optional, Dict, Any

import requests

from requests import request, Response
from consts.consts import Colors
from tools.helper import pretty_log_request
from tools.logger import get_logger

logger = get_logger(name="logger")


class ApiClient:
    def __init__(self, url: str):
        assert url, "Url must be set"
        self._url = url

    @property
    def url(self):
        return self._url

    def _perform_request(self, method: str, path: str, api_key: Optional[str] = None, **kwargs) -> Response:
        headers = {
            "Accept": "application/json"
        }
        url = self.url + path

        if api_key:
            headers["api-key"] = api_key

        try:
            response = request(method=method, url=url, headers=headers, verify=False, **kwargs)
            pretty_log_request(response=response, method=method, **kwargs)
            return response
        except requests.RequestException as e:
            logger.exception(f"\n{Colors.RED.value}Request to '{path}' failed: {e}{Colors.BLACK.value}")

    def _get(self, path: str, api_key: Optional[str] = None, params: Optional[Dict[str, Any]] = None, **kwargs):
        return self._perform_request("GET", path, api_key=api_key, params=params, **kwargs)

    def _post(self, path: str, api_key: Optional[str] = None, **kwargs):
        return self._perform_request("POST", path, api_key=api_key, **kwargs)

    def _delete(self, path: str, api_key: Optional[str] = None, **kwargs):
        return self._perform_request("DELETE", path, api_key=api_key, **kwargs)

    def _put(self, path: str, api_key: Optional[str] = None,  **kwargs):
        return self._perform_request("PUT", path, api_key=api_key, **kwargs)
