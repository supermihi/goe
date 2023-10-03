from goe.controller.slices import SensorValues, CurrentSensors, Voltages, Categories
from goe.slices.common import MetaData
from goe.slices import SliceClient


class GoEControllerClient(SliceClient):
    _SLICES = [MetaData, SensorValues, CurrentSensors, Voltages, Categories]
