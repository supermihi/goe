import json
from abc import abstractmethod, ABC
from collections.abc import Mapping, Iterable
from datetime import timedelta
from typing import Any, Literal
from urllib.parse import urlencode
from urllib.request import Request, urlopen

JsonResult = Mapping[str, Any]


class GoEJsonClient(ABC):
    """Client for querying the JSON API of go-e products."""

    @abstractmethod
    def query(self, keys: Iterable[str] | None = None, timeout: timedelta | None = None) -> JsonResult:
        """Query the status API.

        Args:
            keys: optional sequence of API keys to filter for.
            timeout: optional timeout for the underlying HTTP call.
        """
        raise NotImplementedError()


def urlencode_keys(keys: Iterable[str]):
    return urlencode(dict(filter=','.join(keys)))


def seconds_or_none(td: timedelta | None) -> float | None:
    return None if td is None else td.total_seconds()


class LocalJsonClient(GoEJsonClient):

    def __init__(self, hostname_or_ip: str):
        self.base_url = f'http://{hostname_or_ip}/api'

    def query(self, keys: Iterable[str] | None = None, timeout: timedelta | None = None) -> JsonResult:
        query = urlencode_keys(keys or [])
        full_url = f'{self.base_url}/status?{query}'
        with urlopen(full_url, timeout=seconds_or_none(timeout)) as response:
            json_string = response.read().decode()
            return json.loads(json_string)


class CloudJsonClient(GoEJsonClient):
    """Client for calling tho go-e cloud API."""

    def __init__(self, cloud_api_key: str, serial_number: str = None, device: Literal['controller', 'charger'] = None,
                 domain: str = None):
        if domain is None:
            if device is None or serial_number is None:
                raise ValueError('either domain or serial and device must be given')
            match device:
                case 'controller':
                    subdomain = 'controller'
                case 'charger':
                    subdomain = 'v3'
                case _:
                    raise ValueError('invalid device. Must be one of "controller", "charger"')
            self.domain = f'https://{serial_number}.api.{subdomain}.go-e.io'
        else:
            self.domain = domain
        self.cloud_api_key = cloud_api_key

    def query(self, keys: Iterable[str] | None = None, timeout: timedelta | None = None) -> JsonResult:
        query = urlencode_keys(keys or [])
        request = Request(f'{self.domain}/api/status?{query}', headers=self.headers)
        with urlopen(request, timeout=seconds_or_none(timeout)) as response:
            json_string = response.read().decode()
            return json.loads(json_string)

    @property
    def headers(self):
        return {'Authorization': f'Bearer {self.cloud_api_key}'}
