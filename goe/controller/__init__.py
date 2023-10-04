from goe.controller.slices import SensorValues, CurrentSensors, Voltages, Categories
from goe.slices.common import MetaData, Time
from goe.slices import SliceClient


class GoEControllerClient(SliceClient):
    _SLICES = MetaData, Time, SensorValues, CurrentSensors, Voltages, Categories
