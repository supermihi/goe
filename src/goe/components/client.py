from __future__ import annotations

import itertools
from abc import ABC, abstractmethod
from collections.abc import Sequence, Callable
from typing import Type, TypeVar

from goe.components.component import ComponentBase
from goe.json_client import GoEJsonClient, LocalJsonClient

T = TypeVar('T', bound=ComponentBase)


class DeviceClientBase(ABC):
    """Base class for high-level go-e device clients, using the 'components' API."""

    def __init__(self, json_client: GoEJsonClient):
        self.json_client = json_client

    @classmethod
    def local(cls, host: str):
        """Convenience factory method using a local JSON client."""
        return cls(LocalJsonClient(host))

    @classmethod
    @abstractmethod
    def supported_components(cls) -> Sequence[Type[ComponentBase]]:
        """Return a list of StatusComponent subclasses supported by this API."""
        raise NotImplementedError()

    def get_many(self, components: Sequence[Type[ComponentBase]], **kwargs):
        """Query multiple status components at once."""
        keys = itertools.chain(*(component_type.keys() for component_type in components))
        result = self.json_client.query(keys=keys, **kwargs)
        return [component_type.parse(result) for component_type in components]

    @staticmethod
    def getter(component_type: Type[T]) -> Callable[[DeviceClientBase], T]:
        """Helper for subclasses to create single-component query methods.

        Use like this:

        >>> class MyClient(DeviceClientBase):
        >>>     @classmethod
        >>>     def supported_components(cls) -> Sequence[Type[ComponentBase]]:
        >>>         return MyComponent, MetaData
        >>>
        >>>     get_my_component = DeviceClientBase.getter(MyComponent)"""

        def get_component(self: DeviceClientBase, **kwargs):
            result = self.json_client.query(keys=component_type.keys(), **kwargs)
            return component_type.parse(result)

        return get_component
