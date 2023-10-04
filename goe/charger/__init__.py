from goe.charger.slices import ChargingStatus, Statistics, Configuration
from goe.slices import SliceClient
from goe.slices.common import MetaData, Time


class GoEChargerClient(SliceClient):
    _SLICES = MetaData, Time, Configuration, ChargingStatus, Statistics
