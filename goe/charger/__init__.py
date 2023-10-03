from goe.charger.slices import ChargingStatus, Statistics
from goe.slices import SliceClient
from goe.slices.common import MetaData


class GoEChargerClient(SliceClient):
    _SLICES = MetaData, ChargingStatus, Statistics
