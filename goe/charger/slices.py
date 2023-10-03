from dataclasses import dataclass
from typing import Self

from goe.charger.enums import PhaseSwitchMode, CarState, Error, CableLockStatus, ModelStatus
from goe.json_client import JsonResult
from goe.slices import StatusSlice


@dataclass
class Statistics(StatusSlice):
    KEYS = ('eto',)
    NAME = 'stats'

    energy_total_wh: int | None

    @classmethod
    def parse(cls, result: JsonResult) -> Self:
        energy_total = result['eto']
        return Statistics(energy_total_wh=energy_total)


@dataclass
class Configuration(StatusSlice):
    KEYS = 'dwo', 'psm', 'spl3'
    NAME = 'config'

    energy_limit_wh: float | None
    phase_switch_mode: PhaseSwitchMode | None
    three_phase_switch_level_W: float | None

    @classmethod
    def parse(cls, result: JsonResult) -> Self:
        energy_limit = result['dwo']
        phase_switch_mode = result['psm']
        switch_level = result['spl3']
        return Configuration(energy_limit_wh=energy_limit,
                             phase_switch_mode=None if phase_switch_mode is None else PhaseSwitchMode(
                                 phase_switch_mode), three_phase_switch_level_W=switch_level)


@dataclass
class ChargingStatus(StatusSlice):
    KEYS = 'alw', 'acu', 'tpa', 'car', 'err', 'cus', 'modelStatus'
    NAME = 'charging_status'

    allowed_to_charge_now: bool
    allowed_current_now: int | None
    power_average_30s: float
    car_state: CarState
    error: Error | None
    cable_lock: CableLockStatus
    status: ModelStatus

    @classmethod
    def parse(cls, result: JsonResult) -> Self:
        allowed_to_charge = result['alw']
        allowed_current = result['acu']
        power_average = result['tpa']
        car_state = result['car']
        error = result['err']
        cable_lock = result['cus']
        model_status = result['modelStatus']
        return ChargingStatus(allowed_to_charge_now=allowed_to_charge,
                              allowed_current_now=allowed_current,
                              power_average_30s=power_average,
                              car_state=CarState(car_state),
                              error=None if error in (None, 0) else Error(error),
                              cable_lock=CableLockStatus(cable_lock),
                              status=ModelStatus(model_status))
