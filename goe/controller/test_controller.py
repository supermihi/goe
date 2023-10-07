import json
from pathlib import Path

from goe.controller import GoEControllerClient
from goe.json_client import JsonResult, GoEJsonClient


class MockClient(GoEJsonClient):
    def __init__(self, returns: JsonResult):
        self.returns = returns

    def query(self, *, keys=None) -> JsonResult:
        return self.returns


def test_controller_status_all(get_test_data):
    client = MockClient(json.loads(get_test_data(Path('controller_status_all.json'))))
    controller = GoEControllerClient(client)
    result = controller.get_slices(*GoEControllerClient._SLICES)
    assert len(result) == len(GoEControllerClient._SLICES)
