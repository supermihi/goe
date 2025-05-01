import pytest

from goe.json_client import LocalJsonClient, CloudJsonClient


def test_local_http_url():
    client = LocalJsonClient('goe-controller')
    assert client.base_url == 'http://goe-controller/api'


def test_cloud_missing_arg():
    with pytest.raises(ValueError):
        CloudJsonClient(cloud_api_key='123')


def test_cloud_invalid_device():
    with pytest.raises(ValueError):
        CloudJsonClient(cloud_api_key='123', serial_number='123', device='foo')
