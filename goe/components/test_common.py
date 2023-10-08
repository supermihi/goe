from datetime import timedelta, datetime, timezone

from goe.components.common import MetaData, Time, TimeServerSyncStatus, TimeZoneDaylightSavingMode, PerPhase


def test_per_phase():
    values = PerPhase[float](1, 2.5, 3)

    assert values[0] == 1
    assert values[1:] == (2.5, 3)
    assert len(values) == 3


def test_parse_metadata():
    json_result = {'sse': '123456', 'fna': 'friendly name', 'fwv': 'v1.2.3'}
    metadata = MetaData.parse(json_result)
    assert metadata == MetaData('123456', 'friendly name', 'v1.2.3')


def test_parse_time():
    json_result = {"tse": True, "tsss": 1, "tof": 60, "tds": 1, "utc": "2023-10-04T17:13:58.381",
                   "loc": "2023-10-04T19:13:58.383 +02:00"}
    parsed_time = Time.parse(json_result)

    expected = Time(time_server_enabled=True, time_server_sync_status=TimeServerSyncStatus.Completed,
                    timezone_offset=timedelta(minutes=60),
                    daylight_saving=TimeZoneDaylightSavingMode.EuropeanSummerTime,
                    utc_time=datetime(2023, 10, 4, 17, 13, 58, 381_000, tzinfo=timezone.utc),
                    local_time=datetime(2023, 10, 4, 19, 13, 58, 383_000, tzinfo=timezone(offset=timedelta(hours=2)))
                    )
    assert parsed_time == expected
