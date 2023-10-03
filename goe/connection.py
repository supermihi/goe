from abc import ABC, abstractmethod
from typing import Iterable
from urllib.parse import urlencode
from urllib.request import Request


class ApiConnection(ABC):
    @abstractmethod
    def create_request(self, keys: Iterable[str] | None = None) -> Request:
        raise NotImplementedError()

    @staticmethod
    def urlencode_keys(keys: Iterable[str]):
        return urlencode(dict(filter=','.join(keys)))


class LocalHttpApiConnection(ApiConnection):

    def __init__(self, hostname_or_ip: str):
        self.url = f'http://{hostname_or_ip}/api'

    def create_request(self, keys: Iterable[str] | None = None) -> Request:
        query = ApiConnection.urlencode_keys(keys or [])
        return Request(f'{self.url}/status?{query}')


class CloudApiConnection(ApiConnection):
    def __init__(self, serial_number: str, cloud_api_key: str):
        self.url = f'https://{serial_number}.api.controller.go-e.io/api'
        self.cloud_api_key = cloud_api_key

    def create_request(self, keys: Iterable[str] | None = None) -> Request:
        query = ApiConnection.urlencode_keys(keys or [])
        return Request(f'{self.url}/status?{query}', headers={'Authorization': f'Bearer {self.cloud_api_key}'})
