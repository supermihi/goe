from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Self

from goe.json_client import JsonResult, GoEJsonClient


class StatusSlice(ABC):
    KEYS: ClassVar[tuple[str, ...]]
    """When subclassing, set this to the API keys that need to be queried for this slice."""
    NAME: ClassVar[str]
    """Short name for this slice. Used in generated 'get_<NAME>()' accessors and CLI."""

    @classmethod
    @abstractmethod
    def parse(cls, result: JsonResult) -> Self:
        """Parse this slice from a JsonResult."""
        raise NotImplementedError()

    @classmethod
    def query(cls, client: GoEJsonClient) -> Self:
        """Convenience method to query required API keys and then parse."""
        json_result = client.query(keys=cls.KEYS)
        result = cls.parse(json_result)
        return result
