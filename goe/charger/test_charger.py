from goe.charger import GoEChargerClient
from goe.test_utils import MockClient


def test_get_meta():
    json_client = MockClient({'sse': '123', 'fwv': '1.0', 'fna': 'my device'})
    charger = GoEChargerClient(json_client)
    result = charger.get_meta()
    assert result.friendly_name == 'my device'
