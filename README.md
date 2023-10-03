# goe – Python API client for go-e Chargers and go-e Controllers

The goe package provides easy access to the HTTP APIs of electric vehicle chargers and controllers
by [go-e](https://go-e.com).

# Features

- supports [go-e Controller API](https://github.com/goecharger/go-eController-API)
  and [go-e Charger API (v2)](https://github.com/goecharger/go-eCharger-API-v2)
- supports local HTTP and go-e cloud API using the same interface
- no dependencies – Python standard library only
- comes with a powerful command-line interface for easy scripting and testing
- filtered queries for faster queries and reduced server load
- extensible and hackable

# High-Level Slice API
This package contains high-level API clients for both the go-e Charger and the
go-e Controller.

They are centered around the concept of a _slice_ – a subset of the device status data
that forms a logical component (e.g.: metadata slice, current sensor value slice).

Every slice can be queried individually and is parsed into a typed dataclass object that uses
self-explaining and documented field names.

The slice-based API facilitates most use cases without needing to consult the official
API specification. If you need more flexibility, this package also provides access to the
raw [JSON API](#json-api).
)

### Charger Example
```python
>>> from goe.charger import GoEChargerClient
>>> # create a Charger local API client
>>> charger = GoEChargerClient.local('192.168.1.2')
>>> charger.get_meta() # query device info
MetaData(serial_number='123456',
          friendly_name='my Wallbox',
          firmware_version='055.7')

>>> charger.get_charging_status() # query current charging data
[ChargingStatus(allowed_to_charge_now=False,
                allowed_current_now=None,
                power_average_30s=0,
                car_state=<CarState.Idle: 1>,
                error=None,
                cable_lock=<CableLockStatus.Locked: 3>,
                status=<ModelStatus.NotChargingBecauseFallbackAwattar: 17>)
```

### Controller Example
```python
>>> from goe.controller import GoEControllerClient
>>> # create a Controller cloud API client
>>> controller = GoEControllerClient.cloud(serial_number='123456', cloud_api_key='secret')
>>> controller.get_meta()
MetaData(serial_number='123456',
         friendly_name='My Controller',
         firmware_version='1.0.6')

>>> controller.get_categories() # by-category sensor values
[[CategoryStatus(name='Home',
                 power=248.9663,
                 energy_in=73433.59,
                 energy_out=7826.659,
                 current_phase_1=1.54793,
                 current_phase_2=0.925657,
                 current_phase_3=0.608566,
                 current_phase_N=None),
  CategoryStatus(name='Grid',
                 power=230.6368,
                 energy_in=29181.21,
                 energy_out=305853.6,
                 current_phase_1=1.239844,
                 current_phase_2=0.589963,
                 current_phase_3=0.278742,
                 current_phase_N=None),
  CategoryStatus(name='Car',
                 power=None,
                 energy_in=0,
                 energy_out=0,
                 current_phase_1=None,
                 current_phase_2=None,
                 current_phase_3=None,
                 current_phase_N=None),
  CategoryStatus(name='Relais',
                 power=None,
                 energy_in=0,
                 energy_out=0,
                 current_phase_1=None,
                 current_phase_2=None,
                 current_phase_3=None,
                 current_phase_N=None),
  CategoryStatus(name='Solar',
                 power=18.32956,
                 energy_in=345030.1,
                 energy_out=2.82422,
                 current_phase_1=0.308085,
                 current_phase_2=0.335694,
                 current_phase_3=0.329825,
                 current_phase_N=None)]

```

### Querying Multiple Slices at Once
The slice API lets you query for multiple slices at once, resulting in only
a single call to the device or cloud API:
```python
>>> voltages, currents, meta = controller.get_slices(Voltages, Currents, MetaData)
```
# JSON API

The JSON API client provides unified access to both the local
and cloud HTTP APIs of any go-e Charger or go-e Controller.

It returns the raw JSON data returned from the API, which gives
users the maximum flexibility. For most use cases, the higher-level
structured APIs (see below) are more convenient.

```python
>> > from goe.json_client import GoEJsonClient
>> > local_client = GoEJsonClient.local('192.168.1.1')
>> > local_client.query()
{'alw': False, 'acu': None, 'adi': True, 'dwo': None, 'tpa': 0, [...]}

>> > cloud_client = GoEJsonClient.cloud(serial_number='123456', cloud_api_key='secret')
>> > cloud_client.query_stats()
{'alw': False, 'acu': None, 'adi': True, 'dwo': None, 'tpa': 0, [...]}

```

You can (
and [should](https://github.com/goecharger/go-eCharger-API-v2/blob/main/http-en.md#getting-all-values-in-one-request))
restrict the amount of data returend by specifying a set of supported
API keys ([controller](https://github.com/goecharger/go-eController-API/blob/main/apikeys-en.md),
[charger](https://github.com/goecharger/go-eCharger-API-v2/blob/main/apikeys-en.md))
to query for:

```python
>> > local_client.query(keys=['sse', 'fna'])
{'sse': '123456', 'fna': 'my go-e Wallbox (car port)'}
```

# Extending
It is easy to extend or customize the slices used by the high-level APIs, e.g. if some
API keys are not (yet) implemented by this library or if the predefined grouping of API
keys into slices does not fit your needs.

To create a custom slice, subclass `StatusSlice` like this:

```python

@dataclass
class MySlice(StatusSlice):
    KEYS = 'iaw', 'awe'  # API keys to fetch for this slice
    NAME = 'my_slice'

    is_awesome: bool
    awesomeness: int

    @classmethod
    def parse(cls, result: JsonResult) -> MySlice:
        return MySlice(result['iaw'], result['awe'])
```
and use like this:

```python
>>> client = GoEJsonClient(...)
>>> my_slice = MySlice.query(client)
```