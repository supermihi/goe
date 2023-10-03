import pytest

from goe.slices.slice import StatusSlice


def test_slice_subclass_must_override_parse():
    class TestSlice(StatusSlice):
        pass

    with pytest.raises(TypeError):
        TestSlice()
