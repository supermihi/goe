from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from goe.json_client import JsonResult
from goe.components import ComponentBase
from goe.components.common import PerPhaseWithN


@dataclass
class VoltageSensor:
    """Measurement of a single voltage sensor.

    Args:
        name (str): The sensor name.
        values (PerPhaseValuesWithN): Measured voltages.
    """
    name: str
    values: PerPhaseWithN[float]


class VoltageSensors(ComponentBase, list[VoltageSensor]):
    @classmethod
    def keys(cls) -> Sequence[str]:
        return 'usn', 'usv'

    @classmethod
    def name(cls) -> str:
        return 'voltages'

    @classmethod
    def parse(cls, result: JsonResult):
        return [VoltageSensor(name, PerPhaseWithN(v['u1'], v['u2'], v['u3'], v['uN'])) for name, v in
                zip(result['usn'], result['usv'])]


@dataclass
class CurrentSensorStatus:
    """Status of a current sensor.

    Args:
        name (str): Sensor name.
        current (float): Measured current (in A).
        power (float): Measured power (in W).
        power_factor (float): Measured power factor (between -1 and 1).
        phase (int): Number of the phase associated to this sensor.
        inverted (bool): Whether the sensor is inverted.
    """
    name: str
    current: float
    power: float
    power_factor: float
    phase: int
    inverted: bool


class CurrentSensors(ComponentBase, tuple[CurrentSensorStatus, ...]):
    @classmethod
    def name(cls) -> str:
        return 'currents'

    @classmethod
    def keys(cls) -> Sequence[str]:
        return 'isn', 'isv', 'ips', 'iim'

    @classmethod
    def parse(cls, result: JsonResult):
        isn = result['isn']
        isv = result['isv']
        ips = result['ips']
        iim = result['iim']

        result = CurrentSensors(
            CurrentSensorStatus(name=name, current=values['i'], power=values['p'], power_factor=values['f'],
                                phase=phase,
                                inverted=is_inverted) for
            name, values, phase, is_inverted in zip(isn, isv, ips, iim)
        )
        return result


@dataclass
class CategoryStatus:
    name: str
    power: float | None
    energy_in: float
    energy_out: float
    current: PerPhaseWithN[float | None]


class Categories(ComponentBase, tuple[CategoryStatus, ...]):
    @classmethod
    def keys(cls) -> Sequence[str]:
        return 'ccn', 'ccp', 'cec', 'cpc'

    @classmethod
    def name(cls) -> str:
        return 'categories'

    @classmethod
    def parse(cls, result: JsonResult):
        category_names = result.get('ccn')
        category_powers = result.get('ccp')
        energy_counters = result.get('cec')
        phase_currents = result.get('cpc')
        return Categories(CategoryStatus(name=name, power=power, energy_in=energies[0], energy_out=energies[1],
                                         current=PerPhaseWithN(*currents)) for
                          name, power, energies, currents in
                          zip(category_names, category_powers, energy_counters, phase_currents))


@dataclass
class SensorValues(ComponentBase):
    """Convenience component; combines 'Categories', 'VoltagesSensors' and 'CurrentSensors'."""

    @classmethod
    def keys(cls) -> Sequence[str]:
        return tuple(Categories.keys()) + tuple(VoltageSensors.keys()) + tuple(CurrentSensors.keys())

    @classmethod
    def name(cls) -> str:
        return 'sensors'

    categories: Categories
    voltages: VoltageSensors
    currents: CurrentSensors

    @classmethod
    def parse(cls, status: JsonResult) -> SensorValues:
        voltages = VoltageSensors.parse(status)
        currents = CurrentSensors.parse(status)
        categories = Categories.parse(status)
        return SensorValues(categories, voltages, currents)
