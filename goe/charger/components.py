from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import timedelta

from goe.charger.enums import PhaseSwitchMode, CarState, Error, CableLockState, ChargingStateDetail, CableLockMode
from goe.json_client import JsonResult
from goe.components import ComponentBase
from goe.components.common import PerPhaseWithN, PerPhase


@dataclass
class Statistics(ComponentBase):
    """Long-term charger statistics."""

    energy_total_wh: int
    reboot_count: int
    uptime: timedelta

    @classmethod
    def keys(cls) -> Sequence[str]:
        return 'eto', 'rbc', 'rbt'

    @classmethod
    def name(cls) -> str:
        return 'stats'

    @classmethod
    def parse(cls, result: JsonResult) -> Statistics:
        uptime = timedelta(milliseconds=result['rbt'])
        return Statistics(energy_total_wh=(result['eto']),
                          uptime=uptime, reboot_count=result['rbc'])


@dataclass
class Configuration(ComponentBase):
    """Charging-related configuration.

    Args:
        energy_limit: Total charging energy limit, in Wh (None if disabled).
        phase_switch_mode: configured phase switching mode.
        three_phase_switch_level: minimum solar power (in W) required to switch to 3-phase charging.
        current_limit_presets: Current limits (in A) that can be set by pressing the button at the Charger.
    """

    @classmethod
    def keys(cls) -> Sequence[str]:
        return 'dwo', 'psm', 'spl3', 'clp', 'lck'

    @classmethod
    def name(cls) -> str:
        return 'config'

    energy_limit: float | None
    phase_switch_mode: PhaseSwitchMode
    three_phase_switch_level: float
    current_limit_presets: Sequence[float]
    cable_lock_mode: CableLockMode

    @classmethod
    def parse(cls, result: JsonResult) -> Configuration:
        return Configuration(energy_limit=result['dwo'],
                             phase_switch_mode=PhaseSwitchMode(result['psm']),
                             three_phase_switch_level=result['spl3'],
                             current_limit_presets=result['clp'],
                             cable_lock_mode=CableLockMode(result['lck']))


@dataclass(frozen=True)
class ChargingEnergies:
    voltage: PerPhaseWithN[float]
    current: PerPhase[float]
    power: PerPhaseWithN[float]
    power_total: float
    power_factor: PerPhaseWithN[float]

    @staticmethod
    def from_nrg(nrg: Sequence[float]):
        """Creates ChargingEnergies from the 'nrg' array of a go-e Charger API status."""
        # from spec, nrg array is
        # U (L1, L2, L3, N), I (L1, L2, L3), P (L1, L2, L3, N, Total), pf (L1, L2, L3, N)
        voltage = PerPhaseWithN(*nrg[0:4])
        current = PerPhase(*nrg[4:7])
        power = PerPhaseWithN(*nrg[7:11])
        power_total = nrg[11]
        power_factor = PerPhaseWithN(*nrg[12:])
        return ChargingEnergies(voltage, current, power, power_total, power_factor)


@dataclass(frozen=True)
class ChargingStatus(ComponentBase):
    """Status related to the current charging session.

        Args:
            allowed_to_charge_now: is the car allowed to charge at all now?
            allowed_current_now: how many Ampere is the car allowed to charge now?
        """

    @classmethod
    def keys(cls) -> Sequence[str]:
        return 'alw', 'acu', 'tpa', 'car', 'err', 'cus', 'modelStatus', 'wh', 'nrg', 'pnp'

    @classmethod
    def name(cls) -> str:
        return 'charging_status'

    allowed_to_charge_now: bool
    allowed_current_now: int | None
    power_average_30s: float
    car_state: CarState
    error: Error | None
    cable_lock: CableLockState
    state_detail: ChargingStateDetail
    energy_since_connected: float
    energies: ChargingEnergies
    number_of_phases: int

    @classmethod
    def parse(cls, result: JsonResult) -> ChargingStatus:
        error = result['err']
        return ChargingStatus(allowed_to_charge_now=result['alw'],
                              allowed_current_now=result['acu'],
                              power_average_30s=result['tpa'],
                              car_state=CarState(result['car']),
                              error=None if error in (None, 0) else Error(error),
                              cable_lock=CableLockState(result['cus']),
                              state_detail=ChargingStateDetail(result['modelStatus']),
                              energy_since_connected=result['wh'],
                              energies=ChargingEnergies.from_nrg(result['nrg']),
                              number_of_phases=result['pnp'])
