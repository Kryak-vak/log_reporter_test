import json
from pathlib import Path

import pytest
from faker import Faker

fake = Faker()


@pytest.fixture(scope="function")
def fake_log_data() -> list[dict]:
    first_fake_path = fake.uri_path()
    second_fake_path = fake.uri_path()
    
    fake_data = [
        {
            "url": first_fake_path,
            "response_time": fake.pyfloat(min_value=0.0, max_value=10.0, right_digits=4),
            "other": "other_value"
        },
        {
            "url": first_fake_path,
            "response_time": fake.pyfloat(min_value=0.0, max_value=10.0, right_digits=4),
            "other": "other_value"
        },
        {
            "url": second_fake_path,
            "response_time": fake.pyfloat(min_value=0.0, max_value=10.0, right_digits=4),
            "other": "other_value"
        }
    ]

    return fake_data


@pytest.fixture(scope="function")
def fake_log_file(fake_log_data: list[dict]):
    log_path = Path('tests/data/test.log')
    with open(log_path, "w", encoding="utf-8") as file:
        for entry in fake_log_data:
            file.write(json.dumps(entry) + "\n")
    
    return log_path
