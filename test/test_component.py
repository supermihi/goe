import pytest

from goe.components.component import ComponentBase


def test_component_subclass_must_override_parse():
    class TestComponent(ComponentBase):
        pass

    with pytest.raises(TypeError):
        TestComponent()
