from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta, datetime, timezone
from enum import Enum
from typing import Generic, Sequence, TypeVar

from goe.json_client import JsonResult
from goe.components.component import ComponentBase

"""Status API components shared between multiple device types."""


@dataclass(frozen=True)
class MetaData(ComponentBase):
    """Device metadata. This is identical for both the go-e controller and the go-e charger."""

    serial_number: str
    friendly_name: str
    firmware_version: str

    @classmethod
    def keys(cls) -> Sequence[str]:
        return 'sse', 'fna', 'fwv'

    @classmethod
    def name(cls) -> str:
        return 'meta'

    @classmethod
    def parse(cls, result: JsonResult) -> MetaData:
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
class Time(ComponentBase):
    @classmethod
    def keys(cls) -> Sequence[str]:
        return 'tse', 'tsss', 'tof', 'tds', 'utc', 'loc'

    @classmethod
    def name(cls) -> str:
        return 'time'

    time_server_enabled: bool
    time_server_sync_status: TimeServerSyncStatus
    timezone_offset: timedelta
    daylight_saving: TimeZoneDaylightSavingMode
    utc_time: datetime
    local_time: datetime

    @classmethod
    def parse(cls, result: JsonResult) -> Time:
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


T = TypeVar('T')


class PerPhase(Generic[T], Sequence[T]):

    def __init__(self, phase_1: T, phase_2: T, phase_3: T):
        self._values = (phase_1, phase_2, phase_3)

    def __getitem__(self, index):
        return self._values.__getitem__(index)

    def __len__(self):
        return self._values.__len__()

    @property
    def phase_1(self):
        return self._values[0]

    @property
    def phase_2(self):
        return self._values[1]

    @property
    def phase_3(self):
        return self._values[2]

    def __repr__(self):
        return f'PerPhaseValues(phase_1={self.phase_1}, phase_2={self.phase_2}, phase_3={self.phase_3})'

    def __hash__(self):
        return self._values.__hash__()

    def __eq__(self, other):
        return isinstance(other, PerPhase) and self._values.__eq__(other._values)


class PerPhaseWithN(PerPhase[T]):
    def __init__(self, value_1, value_2, value_3, neutral):
        super().__init__(value_1, value_2, value_3)
        self._values = (value_1, value_2, value_3, neutral)

    @property
    def neutral(self):
        return self._values[3]

    def __repr__(self):
        return f'PerPhaseValuesWithN(phase_1={self.phase_1}, phase_2={self.phase_2}, phase_3={self.phase_3}, neutral={self.neutral})'
