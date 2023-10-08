from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar, Self

from goe.json_client import JsonResult, GoEJsonClient


class ComponentBase(ABC):
    """Represents once component of the status API, i.e., a coherent subset of the
    entire status JSON structure.
    """
    KEYS: ClassVar[tuple[str, ...]]
    """When subclassing, set this to the API keys that need to be queried for this component."""
    NAME: ClassVar[str]
    """Short name for this component. Used for CLI script."""

    @classmethod
    @abstractmethod
    def parse(cls, result: JsonResult) -> Self:
        """Extract and parse this component from a JSON result."""
        raise NotImplementedError()

    @classmethod
    def query(cls, client: GoEJsonClient) -> Self:
        """Convenience method to query required API keys and then parse."""
        json_result = client.query(keys=cls.KEYS)
        result = cls.parse(json_result)
        return result
