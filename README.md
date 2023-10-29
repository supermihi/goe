# goe – Python API client for go-e Chargers and go-e Controllers

The goe package provides easy access to the HTTP APIs of electric vehicle chargers and controllers
by [go-e](https://go-e.com).

```
$ pipx run goe --host 192.168.178.148 charger charging_status

ChargingStatus(allowed_to_charge_now=True,
               allowed_current_now=6,
               power_average_30s=1255.236,
               car_state=<CarState.Idle: 1>,
               error=None,
               cable_lock=<CableLockState.Locked: 3>,
               state_detail=<ChargingStateDetail.ChargingBecausePvSurplus: 12>,
               energy_since_connected=12344.07,
               energies=ChargingEnergies(voltage=PerPhaseValuesWithN(phase_1=233.12, phase_2=233.12, phase_3=234.36, neutral=2.17),
                                         current=PerPhaseValues(phase_1=0, phase_2=0, phase_3=0),
                                         power=PerPhaseValuesWithN(phase_1=0, phase_2=0, phase_3=0, neutral=0),
                                         power_total=0,
                                         power_factor=PerPhaseValuesWithN(phase_1=0, phase_2=0, phase_3=0, neutral=0)),
               number_of_phases=1)
```

# Features

- use local and cloud API connections using the same interface
- no dependencies – Python standard library only
- powerful command-line interface
- filtered queries for faster queries and reduced server load
- extensible and hackable

# Status
As of now, there is only one developer and one known user. It works for me, but I focus on the features that I need.
Please submit issues and / or pull requests if you miss something.

See [Status.md](Status.md) for details about which keys are supported by the components API. The JSON API of course
supports all API keys, by design.

# High-Level Charger / Controller API Clients

This package contains high-level, easy-to-use API clients for both the go-e Charger v2 HTTP API
and the go-e Controller HTTP API.

Building upon the [JSON API](#json-api), these

- parse the raw JSON result into typed Python objects with self-explaining names
- group the queryable status into components (e.g.: "WiFi", "charging status", "sensor values") that can be queried
  individually

### Charger Example

```python
>>> from goe.charger import GoEChargerClient
>>>  # create a Charger local API client
>>> charger = GoEChargerClient.local('192.168.1.2')
>>> charger.get_meta()  # query device info
MetaData(serial_number='123456',
         friendly_name='my Wallbox',
         firmware_version='055.7')

>>> status = charger.get_status()  # query current charging data
>>> energies = status.energies
>>> print(energies.power)
PerPhaseWithN(phase_1=1239, phase_2=1190, phase_3=1540, neutral=0)
```

### Controller Example

```python
>>> from goe.controller import GoEControllerClient
>>>  # create a Controller cloud API client
>>> controller = GoEControllerClient.cloud(serial_number='123456', cloud_api_key='secret')
>>> controller.get_meta()
MetaData(serial_number='123456',
         friendly_name='My Controller',
         firmware_version='1.0.6')

>>> categories = controller.get_categories()  # by-category sensor values
>>> print(categories[:2])
[(CategoryStatus(name='Home',
                 power=248.6361,
                 energy_in=114684.6,
                 energy_out=7826.659,
                 current=PerPhaseValuesWithN(phase_1=13.85199, phase_2=12.94702, phase_3=13.27633, neutral=None)),
  CategoryStatus(name='Grid',
                 power=-4486.617,
                 energy_in=47386.92,
                 energy_out=483994.9,
                 current=PerPhaseValuesWithN(phase_1=6.473037, phase_2=6.319575, phase_3=6.584583, neutral=None))
  ]
```

### Querying Multiple Components at Once

The high-level API lets you query for multiple components at once, resulting in only
a single call to the device or cloud API:

```python
>>> voltages, currents, meta = controller.get_many([Voltages, Currents, MetaData])
```

# JSON API

The JSON API client provides unified access to both the local
and cloud HTTP APIs of any go-e Charger or go-e Controller.

It returns the raw JSON data returned from the API, which gives
users the maximum flexibility. For most use cases, the higher-level
structured APIs (see below) are more convenient.

```python
>>> from goe.json_client import LocalJsonClient, CloudJsonClient
>>> local_client = LocalJsonClient('192.168.1.1')
>>> local_client.query()
{'alw': False, 'acu': None, 'adi': True, 'dwo': None, 'tpa': 0, [...]}

>>> cloud_client = CloudJsonClient(serial_number='123456', device='controller', cloud_api_key='secret')
>>> cloud_client.query()
{'alw': False, 'acu': None, 'adi': True, 'dwo': None, 'tpa': 0, [...]}

```

You can (
and [should](https://github.com/goecharger/go-eCharger-API-v2/blob/main/http-en.md#getting-all-values-in-one-request))
restrict the amount of data returend by specifying a set of supported
API keys ([controller](https://github.com/goecharger/go-eController-API/blob/main/apikeys-en.md),
[charger](https://github.com/goecharger/go-eCharger-API-v2/blob/main/apikeys-en.md))
to query for:

```python
>>> local_client.query(keys=['sse', 'fna'])
{'sse': '123456', 'fna': 'my go-e Wallbox (car port)'}
```

# Extending

It is easy to extend or customize the components used by the high-level APIs, e.g. if some
API keys are not (yet) implemented by this library or if the predefined grouping of API
keys into components does not fit your needs.

To create a custom component, subclass `ComponentBase` like this:

```python

@dataclass
class MyComponent(ComponentBase):
    @classmethod
    def keys(cls):
      return 'iaw', 'awe'  # API keys to fetch for this component
    
    @classmethod
    def name(cls):
      return 'my_component'

    is_awesome: bool
    awesomeness: int

    @classmethod
    def parse(cls, result: JsonResult) -> MyComponent:
        return MyComponent(result['iaw'], result['awe'])
```

and use like this:

```python
>>> client: GoEJsonClient = ...
>>> my_component = MyComponent.query(client)
```