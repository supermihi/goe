from goe.controller.components import SensorValues, CurrentSensors, VoltageSensors, Categories
from goe.json_client import CloudJsonClient
from goe.components.common import MetaData, Time
from goe.components import DeviceClientBase


class GoEControllerClient(DeviceClientBase):
    @classmethod
    def supported_components(cls):
        return MetaData, Time, SensorValues, CurrentSensors, VoltageSensors, Categories

    @classmethod
    def cloud(cls, serial_number: str, cloud_api_key: str):
        """Convenience factory method using a cloud JSON client, to which all
        arguments are forwarded."""
        return cls(CloudJsonClient(serial_number=serial_number, cloud_api_key=cloud_api_key, device='controller'))

    get_meta = DeviceClientBase.getter(MetaData)
    get_time = DeviceClientBase.getter(Time)
    get_sensors = DeviceClientBase.getter(SensorValues)
    get_current = DeviceClientBase.getter(CurrentSensors)
    get_voltage = DeviceClientBase.getter(VoltageSensors)
    get_categories = DeviceClientBase.getter(Categories)
