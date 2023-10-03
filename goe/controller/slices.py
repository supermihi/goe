from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from goe.json_client import JsonResult
from goe.slices import StatusSlice


@dataclass
class VoltageSensorValues:
    """Current values of a voltage sensor.

    Args:
        name (str): The sensor name.
        u_1 (float): Phase1 voltage.
        u_2 (float): Phase 2 voltage.
        u_3 (float): Phase 3 voltage.
        u_N (float): Neutral wire voltage.
    """
    name: str
    u_1: float
    u_2: float
    u_3: float
    u_N: float


class Voltages(StatusSlice, list[VoltageSensorValues]):
    KEYS = 'usn', 'usv'
    NAME = 'voltages'

    @classmethod
    def parse(cls, result: JsonResult) -> Self:
        usn = result['usn']
        usv = result['usv']
        return [VoltageSensorValues(name, v['u1'], v['u2'], v['u3'], v['uN']) for name, v in zip(usn, usv)]


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


class CurrentSensors(StatusSlice, list[CurrentSensorStatus]):
    KEYS = 'isn', 'isv', 'ips', 'iim'
    NAME = 'currents'

    @classmethod
    def parse(cls, result: JsonResult) -> Self:
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
    current_phase_1: float | None
    current_phase_2: float | None
    current_phase_3: float | None
    current_phase_N: float | None


class Categories(StatusSlice, list[CategoryStatus]):
    KEYS = 'ccn', 'ccp', 'cec', 'cpc'
    NAME = 'categories'

    @classmethod
    def parse(cls, result: JsonResult) -> Self:
        category_names = result.get('ccn')
        category_powers = result.get('ccp')
        energy_counters = result.get('cec')
        phase_currents = result.get('cpc')
        return Categories(CategoryStatus(name=name, power=power, energy_in=energies[0], energy_out=energies[1],
                                         current_phase_1=currents[0], current_phase_2=currents[1],
                                         current_phase_3=currents[2],
                                         current_phase_N=currents[3]) for
                          name, power, energies, currents in
                          zip(category_names, category_powers, energy_counters, phase_currents))


@dataclass
class SensorValues(StatusSlice):
    KEYS = Categories.KEYS + Voltages.KEYS + CurrentSensors.KEYS
    NAME = 'sensors'

    categories: Categories
    voltages: Voltages
    currents: CurrentSensors

    @classmethod
    def parse(cls, status: JsonResult) -> SensorValues:
        voltages = Voltages.parse(status)
        currents = CurrentSensors.parse(status)
        categories = Categories.parse(status)
        return SensorValues(categories, voltages, currents)