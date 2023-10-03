import json
import urllib
from collections.abc import Callable, Mapping, Iterable
from http.client import HTTPResponse
from typing import Any
from urllib.request import Request

from goe.connection import ApiConnection, LocalHttpApiConnection, CloudApiConnection

JsonResult = Mapping[str, Any]


class GoEJsonClient:
    """Generic low-level API for go-e products."""

    def __init__(self, connection: ApiConnection, fetch: Callable[[Request], HTTPResponse] = urllib.request.urlopen):
        self.connection = connection
        self._fetch = fetch

    @staticmethod
    def local(hostname_or_ip: str):
        connection = LocalHttpApiConnection(hostname_or_ip)
        return GoEJsonClient(connection)

    @staticmethod
    def cloud(serial_number: str, cloud_api_key: str):
        connection = CloudApiConnection(serial_number, cloud_api_key)
        return GoEJsonClient(connection)

    def query(self, keys: Iterable[str] | None = None) -> JsonResult:
        """Query the status API.

        Args:
            keys: optional sequence of API keys to filter for.
        """
        request = self.connection.create_request(keys)
        with self._fetch(request) as response:
            json_string = response.read().decode()
            return json.loads(json_string)
