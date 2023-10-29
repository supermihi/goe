# API Key Support Status

## Charger

Based on https://github.com/goecharger/go-eCharger-API-v2/blob/main/apikeys-en.md with write-only fields removed.

| Key                 | component?     | R/W | Description                                                                          |
|---------------------|----------------|-----|--------------------------------------------------------------------------------------|
| rfb                 | -              | R   | Relay Feedback                                                                       |
| alw                 | ChargingStatus | R   | Is the car allowed to charge at all now?                                             |
| acu                 | ChargingStatus | R   | How many ampere is the car allowed to charge now?                                    |
| adi                 | -              | R   | Is the 16A adapter used? Limits the current to 16A                                   |
| dwo                 | Configuration  | R/W | charging energy limit, measured in Wh, null means disabled, not the next-trip energy |
| tpa                 | ChargingStatus | R   | 30 seconds total power average (used to get better next-trip predictions)            |
| sse                 | MetaData       | R   | serial number                                                                        |
| eto                 | Statistics     | R   | energy_total, measured in Wh                                                         |
| wifis               | -              | R/W | wifi configurations with ssids and keys                                              |
| scan                | -              | R   | wifi scan result                                                                     |
| scaa                | -              | R   | wifi scan age                                                                        |
| wst                 | -              | R   | WiFi STA status                                                                      |
| wsc                 | -              | R   | WiFi STA error count                                                                 |
| wsm                 | -              | R   | WiFi STA error message                                                               |
| wsms                | -              | R   | WiFi state machine state (None=0, Scanning=1, Connecting=2, Connected=3)             |
| ccw                 | -              | R   | Currently connected WiFi                                                             |
| wfb                 | -              | R   | WiFi failed mac addresses                                                            |
| wcb                 | -              | R   | WiFi current mac address                                                             |
| wpb                 | -              | R   | WiFi planned mac addresses                                                           |
| nif                 | -              | R   | Default route                                                                        |
| dns                 | -              | R   | DNS server                                                                           |
| host                | -              | R   | hostname used on STA interface                                                       |
| rssi                | -              | R   | RSSI signal strength                                                                 |
| tse                 | Time           | R/W | time server enabled (NTP)                                                            |
| tsss                | Time           | R   | time server sync status                                                              |
| tof                 | Time           | R/W | timezone offset in minutes                                                           |
| tds                 | Time           | R/W | timezone daylight saving mode                                                        |
| utc                 | Time           | R/W | utc time                                                                             |
| loc                 | Time           | R   | local time                                                                           |
| led                 | -              | R   | internal infos about currently running led animation                                 |
| lbr                 | -              | R/W | led_bright, 0-255                                                                    |
| lmo                 | -              | R/W | logic mode                                                                           |
| ama                 | -              | R/W | ampere_max limit                                                                     |
| clp                 | -              | R/W | current limit presets, max. 5 entries                                                |
| bac                 | -              | R/W | Button allow Current change                                                          |
| sdp                 | -              | R/W | Button Allow Force change                                                            |
| lbp                 | -              | R   | lastButtonPress in milliseconds                                                      |
| amp                 | -              | R/W | requestedCurrent in Ampere, used for display on LED ring and logic calculations      |
| fna                 | MetaData       | R/W | friendlyName                                                                         |
| cid                 | -              | R/W | color_idle, format: #RRGGBB                                                          |
| cwc                 | -              | R/W | color_waitcar, format: #RRGGBB                                                       |
| cch                 | -              | R/W | color_charging, format: #RRGGBB                                                      |
| cfi                 | -              | R/W | color_finished, format: #RRGGBB                                                      |
| ust                 | -              | R/W | unlock_setting                                                                       |
| lck                 | -              | R   | Effective lock setting, as sent to Charge Ctrl                                       |
| sch_week            | -              | R/W | scheduler_weekday, control enum values: Disabled=0, Inside=1, Outside=2              |
| sch_satur           | -              | R/W | scheduler_saturday, control enum values: Disabled=0, Inside=1, Outside=2             |
| sch_sund            | -              | R/W | scheduler_sunday, control enum values: Disabled=0, Inside=1, Outside=2               |
| nmo                 | -              | R/W | norway_mode / ground check enabled when norway mode is disabled (inverted)           |
| fsp                 | -              | R   | force_single_phase                                                                   |
| acs                 | -              | R/W | access_control user setting (Open=0, Wait=1)                                         |
| frc                 | -              | R/W | forceState (Neutral=0, Off=1, On=2)                                                  |
| rbc                 | Statistics     | R   | reboot_counter                                                                       |
| rbt                 | Statistics     | R   | time since boot in milliseconds                                                      |
| car                 | ChargingStatus | R   | carState, null if internal error                                                     |
| err                 | ChargingStatus | R   | error, null if internal error                                                        |
| cbl                 | -              | R   | cable_current_limit in A                                                             |
| pha                 | -              | R   | phases                                                                               |
| wh                  | ChargingStatus | R   | energy in Wh since car connected                                                     |
| trx                 | -              | R/W | transaction (RFID card)                                                              |
| fwv                 | MetaData       | R   | FW_VERSION                                                                           |
| ccu                 | -              | R   | charge controller update progress (null if no update is in progress)                 |
| oem                 | -              | R   | OEM manufacturer                                                                     |
| typ                 | -              | R   | Devicetype                                                                           |
| fwc                 | -              | R   | firmware from CarControl                                                             |
| ccrv                | -              | R   | chargectrl recommended version                                                       |
| lse                 | -              | R/W | led_save_energy                                                                      |
| cdi                 | -              | R   | charging duration info                                                               |
| lccfi               | -              | R   | lastCarStateChangedFromIdle (in ms)                                                  |
| lccfc               | -              | R   | lastCarStateChangedFromCharging (in ms)                                              |
| lcctc               | -              | R   | lastCarStateChangedToCharging (in ms)                                                |
| tma                 | -              | R   | temperature sensors                                                                  |
| amt                 | -              | R   | temperatureCurrentLimit                                                              |
| nrg                 | ChargingStatus | R   | energy array                                                                         |
| modelStatus         | ChargingStatus | R   | Reason why we allow charging or not right now                                        |
| lmsc                | -              | R   | last model status change                                                             |
| mca                 | -              | R/W | minChargingCurrent                                                                   |
| awc                 | -              | R/W | awattar country (Austria=0, Germany=1)                                               |
| awp                 | -              | R/W | awattarMaxPrice in ct                                                                |
| awcp                | -              | R   | awattar current price                                                                |
| ido                 | -              | R   | Inverter data override                                                               |
| frm                 | -              | R   | roundingMode PreferPowerFromGrid=0, Default=1, PreferPowerToGrid=2                   |
| fup                 | -              | R/W | usePvSurplus                                                                         |
| awe                 | -              | R/W | useAwattar                                                                           |
| fst                 | -              | R/W | startingPower in watts                                                               |
| fmt                 | -              | R/W | minChargeTime in milliseconds                                                        |
| att                 | -              | R/W | automatic stop time in seconds since day begin                                       |
| ate                 | -              | R/W | automatic stop energy in Wh                                                          |
| ara                 | -              | R/W | automatic stop remain in aWATTar                                                     |
| acp                 | -              | R/W | allowChargePause (car compatiblity)                                                  |
| cco                 | -              | R/W | car consumption (only stored for app)                                                |
| esk                 | -              | R/W | energy set kwh (only stored for app)                                                 |
| fzf                 | -              | R/W | zeroFeedin                                                                           |
| pgt                 | -              | R/W | pGridTarget in W                                                                     |
| sh                  | -              | R/W | stopHysteresis in W                                                                  |
| psh                 | -              | R/W | phaseSwitchHysteresis in W                                                           |
| po                  | -              | R/W | prioOffset in W                                                                      |
| zfo                 | -              | R/W | zeroFeedinOffset in W                                                                |
| psmd                | -              | R/W | forceSinglePhaseDuration (in milliseconds)                                           |
| sumd                | -              | R/W | simulate unpluging duration (in milliseconds)                                        |
| mpwst               | -              | R/W | min phase wish switch time (in milliseconds)                                         |
| mptwt               | -              | R/W | min phase toggle wait time (in milliseconds)                                         |
| ferm                | -              | R   | effectiveRoundingMode                                                                |
| mmp                 | -              | R   | maximumMeasuredChargingPower (debug)                                                 |
| tlf                 | -              | R   | testLadungFinished (debug)                                                           |
| tls                 | -              | R   | testLadungStarted (debug)                                                            |
| atp                 | -              | R   | nextTripPlanData (debug)                                                             |
| lpsc                | -              | R   | last pv surplus calculation                                                          |
| inva                | -              | R   | age of inverter data                                                                 |
| pgrid               | -              | R   | pGrid in W                                                                           |
| ppv                 | -              | R   | pPv in W                                                                             |
| pakku               | -              | R   | pAkku in W                                                                           |
| deltap              | -              | R   | deltaP                                                                               |
| pnp                 | ChargingStatus | R   | numberOfPhases                                                                       |
| deltaa              | -              | R   | deltaA                                                                               | 
| pvopt_avergagePGrid | -              | R   | averagePGrid                                                                         |
| pvopt_avergagePPV   | -              | R   | averagePPv                                                                           |
| pvopt_avergagePAkku | -              | R   | averagePAkku                                                                         |
| mci                 | -              | R/W | minimumChargingInterval in milliseconds (0 means disabled)                           |
| mcpd                | -              | R/W | minChargePauseDuration in milliseconds (0 means disabled)                            |
| mcpea               | -              | R/W | minChargePauseEndsAt (set to null to abort current minChargePauseDuration)           |
| su                  | -              | R/W | simulateUnpluggingShort                                                              |
| sua                 | -              | R/W | simulateUnpluggingAlways                                                             |
| hsa                 | -              | R/W | httpStaAuthentication                                                                |
| var                 | -              | R   | variant: max Ampere value of unit (11: 11kW/16A, 22: 22kW/32A)                       |
| loe                 | -              | R/W | Load balancing enabled                                                               |
| log                 | -              | R/W | load_group_id                                                                        |
| lop                 | -              | R/W | load_priority                                                                        |
| lof                 | -              | R/W | load_fallback                                                                        |
| map                 | -              | R/W | load_mapping (uint8_t[3])                                                            |
| upo                 | -              | R/W | unlock_power_outage                                                                  |
| pwm                 | -              | R   | phase wish mode for debugging                                                        |
| lfspt               | -              | R   | last force single phase toggle                                                       |
| fsptws              | -              | R   | force single phase toggle wished since                                               |
| spl3                | Configuration  | R/W | threePhaseSwitchLevel                                                                |
| psm                 | Configuration  | R/W | phaseSwitchMode (Auto=0, Force_1=1, Force_3=2)                                       |
| ocu                 | -              | R   | list of available firmware branches                                                  |
| cwe                 | -              | R/W | cloud websocket enabled"                                                             |
| cus                 | ChargingStatus | R   | Cable unlock status                                                                  |
| ffb                 | -              | R   | lock feedback (NoProblem=0, ProblemLock=1, ProblemUnlock=2)                          |
| fhz                 | -              | R   | Stromnetz frequency (~50Hz) or 0 if unknown                                          |
| loa                 | -              | R   | load balancing ampere                                                                |
| lot                 | -              | R/W | load balancing total amp                                                             |
| loty                | -              | R/W | load balancing type (Static=0, Dynamic=1)                                            |
| cards               | -              | R/W |                                                                                      |
| ocppe               | -              | R/W | OCPP enabled                                                                         |
| ocppu               | -              | R/W | OCPP server url                                                                      |
| ocppg               | -              | R/W | OCPP use global CA Store                                                             |
| ocppcn              | -              | R/W | OCPP skipCertCommonNameCheck                                                         |
| ocppss              | -              | R/W | OCPP skipServerVerification                                                          |
| ocpps               | -              | R   | OCPP started                                                                         |
| ocppc               | -              | R   | OCPP connected                                                                       |
| ocppca              | -              | R   | OCPP connected (timestamp in milliseconds since reboot)                              |
| ocppa               | -              | R   | OCPP connected and accepted                                                          |
| ocppaa              | -              | R   | OCPP connected and accepted (timestamp in milliseconds since reboot)                 |
| ocpph               | -              | R/W | OCPP heartbeat interval                                                              |
| ocpph               | -              | R/W | OCPP meter values sample interval                                                    |
| ocpph               | -              | R/W | OCPP clock aligned data interval                                                     |
| ocppd               | -              | R/W | OCPP dummy card id                                                                   |
| ocppr               | -              | R/W | OCPP rotate phases on charger                                                        |
| ocpple              | -              | R   | OCPP last error                                                                      |
| ocpplea             | -              | R   | OCPP last error (timestamp in milliseconds since reboot)                             |
| ocpprl              | -              | R/W | OCPP remote logging (usually only enabled by go-e support to allow debugging)        |
| ocppck              | -              | R/W | OCPP client key                                                                      |
| ocppcc              | -              | R/W | OCPP client cert                                                                     |
| ocppsc              | -              | R/W | OCPP server cert                                                                     |

## Controller

Based on https://github.com/goecharger/go-eController-API/blob/main/apikeys-en.md.

| Key   | Component?     | R/W | Description                                                   |
|-------|----------------|-----|---------------------------------------------------------------|
| sse   | MetaData       | R   | serial number                                                 |
| wifis | -              | R/W | wifi configurations with ssids and keys                       |
| scan  | -              | R   | wifi scan result                                              |
| lwf   | -              | R   | last wifi connect failed (milliseconds since boot)            |
| scaa  | -              | R   | wifi scan age                                                 |
| wst   | -              | R   | WiFi STA status                                               |
| wsc   | -              | R   | WiFi STA error count                                          |
| wsm   | -              | R   | WiFi STA error message                                        |
| wsl   | -              | R   | WiFi STA error messages log                                   |
| wsms  | -              | R   | WiFi state machine state                                      |
| ccw   | -              | R   | Currently connected WiFi                                      |
| wfb   | -              | R   | WiFi failed mac addresses (bssids)                            |
| wcb   | -              | R   | WiFi current mac address (bssid connecting to)                |
| wpb   | -              | R   | WiFi planned mac addresses (future bssids)                    |
| nif   | -              | R   | Default route                                                 |
| cce   | -              | R   | Currently connected Ethernet                                  |
| dns   | -              | R   | dns servers                                                   |
| host  | -              | R   | configured hostname                                           |
| rssi  | -              | R   | RSSI signal strength                                          |
| wda   | -              | R/W | disable AccessPoint when cloud is connected                   |
| tse   | Time           | R/W | time server enabled                                           |
| tsss  | Time           | R   | time server sync status (RESET=0, COMPLETED=1, IN_PROGRESS=2) |
| tof   | Time           | R/W | timezone offset in minutes                                    |
| tds   | Time           | R/W | timezone daylight saving mode                                 |
| utc   | Time           | R/W | utc time                                                      |
| loc   | Time           | R   | local time                                                    |
| fna   | MetaData       | R/W | friendlyName                                                  |
| rbc   | -              | R   | reboot_counter                                                |
| rbt   | -              | R   | time since boot in milliseconds                               |
| fwv   | MetaData       | R   | FW_VERSION                                                    |
| oem   | -              | R   | OEM manufacturer                                              |
| typ   | -              | R   | Devicetype                                                    |
| awc   | -              | R/W | awattar country (Austria=0, Germany=1,...)                    |
| awp   | -              | R/W | awattarMaxPrice in ct                                         |
| awcp  | -              | R   | awattar current price                                         |
| awpl  | -              | W   | awattar price list                                            |
| hsa   | -              | W   | httpStaAuthentication                                         |
| oct   | -              | W   | ota from cloud url trigger                                    |
| ocu   | -              | R   | ota from cloud url, url to download new firmware code from    |
| cwe   | -              | R/W | cloud websocket enabled                                       |
| clea  | -              | R   | Cloud last error (age)                                        |
| cle   | -              | R   | Cloud last error                                              |
| mme   | -              | R/W | modbus master enabled                                         |
| mmh   | -              | R/W | modbus master host                                            |
| mmp   | -              | R/W | modbus master port                                            |
| men   | -              | R/W | modbus slave enabled                                          |
| msp   | -              | R/W | modbus slave port (requires off/on toggle)                    |
| msb   | -              | R/W | modbus slave swap bytes                                       |
| msr   | -              | R/W | modbus slave swap registers                                   |
| data  | -              | R   | grafana token from cloud for app                              |
| dll   | -              | R   | download link for app csv export                              |
| hai   | -              | R/W | httpApiEnabled (allows /api/status and /api/set requests)     |
| mce   | -              | R/W | MQTT enabled                                                  |
| mcu   | -              | R/W | MQTT broker url                                               |
| mcr   | -              | R/W | MQTT readonly (don't allow api writes from mqtt broker)       |
| mtp   | -              | R/W | MQTT topic prefix (set to null to reset back to the default)  |
| mqg   | -              | R/W | MQTT useGlobalCaStore                                         |
| mqcn  | -              | R/W | MQTT skipCertCommonNameCheck                                  |
| mqss  | -              | R/W | MQTT skipServerVerification                                   |
| mcs   | -              | R   | MQTT started                                                  |
| mcc   | -              | R   | MQTT connected                                                |
| mcca  | -              | R   | MQTT connected (age)                                          |
| mlr   | -              | R   | MQTT last error                                               |
| mlra  | -              | R   | MQTT last error (age)                                         |
| ccn   | Categories     | R/W | controller category names                                     |
| ccp   | Categories     | R   | controller category powers                                    |
| cec   | Categories     | R   | controller energy counters                                    |
| cpc   | Categories     | R   | controller category phase currents                            |
| ccf   | Categories     | R/W | Controller category factors                                   |
| bri   | -              | R   | brightness sensor                                             |
| usn   | VoltageSensors | R   | voltage sensor names                                          |
| usv   | VoltageSensors | R   | voltage sensor values (use usn for sensor names)              |
| isn   | CurrentSensors | R   | current sensor names                                          |
| isv   | CurrentSensors | R   | current sensor values (use isn for sensors names)             |
| ips   | CurrentSensors | R/W | current phase selections                                      |
| iim   | CurrentSensors | R/W | invert current measurement                                    |
| mece  | -              | R/W | mecmeterEnabled                                               |
| mecu  | -              | R/W | mecmeterUrl                                                   |
| mecd  | -              | R   | Mecmeter current data                                         |
| mecf  | -              | R/W | Mecmeter category factors                                     |
