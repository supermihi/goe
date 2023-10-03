import json
from pathlib import Path

from goe.controller import GoEControllerClient
from goe.connection import LocalHttpApiConnection
from goe.json_client import JsonResult, GoEJsonClient


def test_local_http_api_access():
    api = LocalHttpApiConnection('goe-controller')
    request = api.create_request(keys=('sse', 'fna'))
    assert request.full_url == 'http://goe-controller/api/status?filter=sse%2Cfna'


def test_goe_controller_api():
    access = LocalHttpApiConnection('goe-controller')
    controller_api = GoEControllerClient(access)
    requst = controller_api.get_status(filter_keys=['ccn', 'ccp'])
    requst['ccn']


class MockClilent(GoEJsonClient):
    def __init__(self, returns: JsonResult):
        self.returns = returns

    def query(self, *, keys=None) -> JsonResult:
        return self.returns


def test_controller_status_all(get_test_data):
    client = MockClilent(json.loads(get_test_data(Path('controller_status_all.json'))))
    controller = GoEControllerClient(client)
    result = controller.get_status()
    assert result is not None