from pathlib import Path

import pytest


@pytest.fixture()
def get_test_data():
    testdata_path = Path(__file__).resolve().parent.parent.parent / 'testdata'

    def result(path: Path) -> str:
        full_path = testdata_path / path
        return full_path.read_text()

    return result
