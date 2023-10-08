import json
from pathlib import Path

from goe.controller import GoEControllerClient
from goe.test_utils import MockClient


def test_controller_status_all(get_test_data):
    client = MockClient(json.loads(get_test_data(Path('controller_status_all.json'))))
    controller = GoEControllerClient(client)
    result = controller.get_many(GoEControllerClient.supported_components())
    assert len(result) == len(GoEControllerClient.supported_components())
