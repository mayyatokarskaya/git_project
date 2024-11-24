import pytest
from src.processing import filter_by_state
from src.processing import sort_by_date


# Фикстура с тестовыми данными
@pytest.fixture
def sample_records():
    return [
        {"state": "EXECUTED", "date": "2024-11-24", "amount": 100},
        {"state": "PENDING", "date": "2024-11-23", "amount": 50},
        {"state": "CANCELLED", "date": "2024-11-22", "amount": 200},
        {"state": "EXECUTED", "date": "2024-11-22", "amount": 200},
    ]

# Параметризация тестов для различных состояний
@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 2),
    ("PENDING", 1),
    ("CANCELLED", 1),
    ("FAILED", 0),  # Нет записей с таким состоянием
    ("", 0),        # Пустое состояние
])
def test_filter_by_state(sample_records, state, expected_count):
    filtered = filter_by_state(sample_records, state)
    assert len(filtered) == expected_count
    if expected_count > 0:
        assert all(record["state"] == state for record in filtered)

def test_filter_by_state_empty_list():
    filtered = filter_by_state([], "EXECUTED")
    assert filtered == []


# Фикстура с тестовыми данными
@pytest.fixture
def sample_records():
    return [
        {"state": "EXECUTED", "date": "2024-11-24", "amount": 100},
        {"state": "PENDING", "date": "2024-11-23", "amount": 50},
        {"state": "EXECUTED", "date": "2024-11-23", "amount": 150},
        {"state": "CANCELLED", "date": "2024-11-22", "amount": 200},
    ]

# Параметризация тестов для сортировки
@pytest.mark.parametrize("reverse, expected_dates", [
    (True, ["2024-11-24", "2024-11-23", "2024-11-23", "2024-11-22"]),  # Убывание
    (False, ["2024-11-22", "2024-11-23", "2024-11-23", "2024-11-24"]),  # Возрастание
])
def test_sort_by_date(sample_records, reverse, expected_dates):
    sorted_records = sort_by_date(sample_records, reverse)
    assert [record["date"] for record in sorted_records] == expected_dates

def test_sort_by_date_with_equal_dates(sample_records):
    # Записи с одинаковыми датами, но разными состояниями
    records = [
        {"state": "EXECUTED", "date": "2024-11-23", "amount": 100},
        {"state": "PENDING", "date": "2024-11-23", "amount": 50},
    ]
    sorted_records = sort_by_date(records)
    # Должны быть отсортированы по умолчанию по состоянию или по другим признакам
    assert sorted_records[0]["date"] == sorted_records[1]["date"]
    assert sorted_records[0]["state"] == "EXECUTED"  # Например, предполагается, что 'EXECUTED' идет первым

def test_sort_by_date_invalid_format():
    records = [
        {"state": "EXECUTED", "date": "2024-11-24", "amount": 100},
        {"state": "EXECUTED", "date": "invalid-date", "amount": 200},
    ]
    with pytest.raises(ValueError):
        sort_by_date(records)

def test_sort_by_date_empty_list():
    sorted_records = sort_by_date([])
    assert sorted_records == []