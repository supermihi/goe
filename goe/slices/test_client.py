import pytest

from goe.slices.client import SliceClient
from goe.slices.slice import StatusSlice


def test_slice_client_needs_SLICES():
    with pytest.raises(TypeError):
        class TestSliceClient(SliceClient):
            pass


def test_slice_client_adds_getter():
    class TestSliceA(StatusSlice):
        NAME = 'test_a'

    class TestSliceB(StatusSlice):
        NAME = 'test_b'

    class TestSliceClient(SliceClient):
        _SLICES = TestSliceA, TestSliceB

    assert hasattr(TestSliceClient, 'get_test_a')
    assert hasattr(TestSliceClient, 'get_test_b')
