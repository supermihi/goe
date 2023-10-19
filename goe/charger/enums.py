from enum import Enum


class CarState(Enum):
    UnknownOrError = 0
    Idle = 1
    Charging = 2
    WaitCar = 3
    Complete = 4
    Error = 5


class Error(Enum):
    # NoError = 0 parsed as None
    FiAc = 1
    FiDc = 2
    Phase = 3
    Overvolt = 4
    Overamp = 5
    Diode = 6
    PpInvalid = 7
    GndInvalid = 8
    ContactorStuck = 9
    ContactorMiss = 10
    FiUnknown = 11
    Unknown = 12
    Overtemp = 13
    NoComm = 14
    StatusLockStuckOpen = 15
    StatusLockStuckLocked = 16
    Reserved20 = 20
    Reserved21 = 21
    Reserved22 = 22
    Reserved23 = 23
    Reserved24 = 24


class CableLockState(Enum):
    Unknown = 0
    Unlocked = 1
    UnlockFailed = 2
    Locked = 3
    LockFailed = 4
    LockUnlockPowerOutage = 5


class PhaseSwitchMode(Enum):
    Auto = 0
    Force_1 = 1
    Force_3 = 2


class CableLockMode(Enum):
    Default = 0
    AutoUnlock = 1
    AlwaysLock = 2
    ForceUnlock = 3


class ChargingStateDetail(Enum):
    """Detailed charging status including reason why charging is on or off.

    Called 'ModelStatus' in the upstream API docs.
    """
    NotChargingBecauseNoChargeCtrlData = 0
    NotChargingBecauseOverTemperature = 1
    NotChargingBecauseAccessControlWait = 2
    ChargingBecauseForceStateOn = 3
    NotChargingBecauseForceStateOff = 4
    NotChargingBecauseScheduler = 5
    NotChargingBecauseEnergyLimit = 6
    ChargingBecauseAwattarPriceLow = 7
    ChargingBecauseAutomaticStopTestCharging = 8
    ChargingBecauseAutomaticStopNotEnoughTime = 9
    ChargingBecauseAutomaticStop = 10
    ChargingBecauseAutomaticStopNoClock = 11
    ChargingBecausePvSurplus = 12
    ChargingBecauseFallbackGoEDefault = 13
    ChargingBecauseFallbackGoEScheduler = 14
    ChargingBecauseFallbackDefault = 15
    NotChargingBecauseFallbackGoEAwattar = 16
    NotChargingBecauseFallbackAwattar = 17
    NotChargingBecauseFallbackAutomaticStop = 18
    ChargingBecauseCarCompatibilityKeepAlive = 19
    ChargingBecauseChargePauseNotAllowed = 20
    NotChargingBecauseSimulateUnplugging = 22
    NotChargingBecausePhaseSwitch = 23
    NotChargingBecauseMinPauseDuration = 24
