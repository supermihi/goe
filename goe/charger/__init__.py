from goe.charger.components import ChargingStatus, Statistics, Configuration
from goe.json_client import CloudJsonClient
from goe.components import DeviceClientBase
from goe.components.common import MetaData, Time


class GoEChargerClient(DeviceClientBase):
    @classmethod
    def cloud(cls, serial_number: str, cloud_api_key: str):
        return GoEChargerClient(
            CloudJsonClient(device='charger', serial_number=serial_number, cloud_api_key=cloud_api_key))

    @classmethod
    def supported_components(cls):
        return MetaData, Time, Configuration, ChargingStatus, Statistics

    get_meta = DeviceClientBase.getter(MetaData)
    get_time = DeviceClientBase.getter(Time)
    get_config = DeviceClientBase.getter(Configuration)
    get_status = DeviceClientBase.getter(ChargingStatus)
    get_stats = DeviceClientBase.getter(Statistics)
