from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from goe.json_client import JsonResult, GoEJsonClient


class ComponentBase(ABC):
    """Represents once component of the status API, i.e., a coherent subset of the
    entire status JSON structure.
    """

    @classmethod
    @abstractmethod
    def keys(cls) -> Sequence[str]:
        """When subclassing, set this to the API keys that need to be queried for this component."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """Short name for this component. Used for CLI script."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def parse(cls, result: JsonResult):
        """Extract and parse this component from a JSON result."""
        raise NotImplementedError()

    @classmethod
    def query(cls, client: GoEJsonClient):
        """Convenience method to query required API keys and then parse."""
        json_result = client.query(keys=cls.keys())
        result = cls.parse(json_result)
        return result
