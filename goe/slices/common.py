from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from goe.json_client import JsonResult
from goe.slices.slice import StatusSlice


@dataclass(frozen=True)
class MetaData(StatusSlice):
    """Device metadata. This is identical for both the go-e controller and the go-e charger."""
    NAME = 'meta'
    KEYS = 'sse', 'fna', 'fwv'

    serial_number: str
    friendly_name: str
    firmware_version: str

    @classmethod
    def parse(cls, result: JsonResult) -> Self:
        return MetaData(serial_number=result['sse'],
                        friendly_name=result['fna'],
                        firmware_version=result['fwv'])
