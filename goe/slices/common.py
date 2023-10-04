from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta, datetime, tzinfo, timezone
from enum import Enum
from typing import Self

from goe.json_client import JsonResult
from goe.slices.slice import StatusSlice

"""Status API slices shared between multiple device types."""


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


class TimeServerSyncStatus(Enum):
    Reset = 0
    Completed = 1
    InProgress = 2


class TimeZoneDaylightSavingMode(Enum):
    NoDaylightSaving = 0
    EuropeanSummerTime = 1
    USDaylightTime = 2


@dataclass(frozen=True)
class Time(StatusSlice):
    KEYS = 'tse', 'tsss', 'tof', 'tds', 'utc', 'loc'
    NAME = 'time'

    time_server_enabled: bool
    time_server_sync_status: TimeServerSyncStatus
    timezone_offset: timedelta
    daylight_saving: TimeZoneDaylightSavingMode
    utc_time: datetime
    local_time: datetime

    @classmethod
    def parse(cls, result: JsonResult) -> Self:
        utc_time = datetime.fromisoformat(result['utc']).replace(tzinfo=timezone.utc)
        # go-e puts a space before the offset, but datetime doesn't expect that
        local_time = datetime.fromisoformat(result['loc'].replace(' +', '+'))
        return Time(time_server_enabled=result['tse'],
                    time_server_sync_status=TimeServerSyncStatus(result['tsss']),
                    timezone_offset=timedelta(minutes=result['tof']),
                    daylight_saving=TimeZoneDaylightSavingMode(result['tds']),
                    utc_time=utc_time,
                    local_time=local_time
                    )
