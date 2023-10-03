from goe.slices.common import MetaData


def test_parse_metadata():
    json_result = {'sse': '123456', 'fna': 'friendly name', 'fwv': 'v1.2.3'}
    metadata = MetaData.parse(json_result)
    assert metadata == MetaData('123456', 'friendly name', 'v1.2.3')