from typing import Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_records() -> List[Dict[str, str]]:
    """Фикстура, которая возвращает список тестовых записей с полями 'state', 'date' и 'amount'"""
    return [
        {"state": "EXECUTED", "date": "2024-11-24", "amount": "100"},  # Преобразовано в строку
        {"state": "PENDING", "date": "2024-11-23", "amount": "50"},  # Преобразовано в строку
        {"state": "CANCELLED", "date": "2024-11-22", "amount": "200"},  # Преобразовано в строку
        {"state": "EXECUTED", "date": "2024-11-22", "amount": "200"},  # Преобразовано в строку
    ]


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("PENDING", 1),
        ("CANCELLED", 1),
        ("FAILED", 0),
        ("", 0),
    ],
)
def test_filter_by_state(sample_records: List[Dict[str, str]], state: str, expected_count: int) -> None:
    """Тестирует функцию filter_by_state на правильность фильтрации записей по состоянию"""
    filtered = filter_by_state(sample_records, state)
    assert len(filtered) == expected_count
    if expected_count > 0:
        assert all(record["state"] == state for record in filtered)


def test_filter_by_state_empty_list() -> None:
    """Тестирует функцию filter_by_state на пустом списке записей"""
    filtered = filter_by_state([], "EXECUTED")
    assert filtered == []


@pytest.mark.parametrize(
    "reverse, expected_dates",
    [
        (True, ["2024-11-24", "2024-11-23", "2024-11-22", "2024-11-22"]),
        (False, ["2024-11-22", "2024-11-22", "2024-11-23", "2024-11-24"]),
    ],
)
def test_sort_by_date(reverse: bool, expected_dates: List[str]) -> None:
    """Тестирует функцию sort_by_date на сортировку записей по дате"""
    sample_records = [
        {"amount": "100", "date": "2024-11-24", "state": "EXECUTED"},
        {"amount": "50", "date": "2024-11-23", "state": "PENDING"},
        {"amount": "200", "date": "2024-11-22", "state": "CANCELLED"},
        {"amount": "200", "date": "2024-11-22", "state": "EXECUTED"},
    ]
    sorted_records = sort_by_date(sample_records, reverse)
    assert [record["date"] for record in sorted_records] == expected_dates


def test_sort_by_date_with_equal_dates(sample_records: List[Dict[str, str]]) -> None:
    """Тестирует функцию sort_by_date на случаи с одинаковыми датами"""
    records = [
        {"state": "EXECUTED", "date": "2024-11-23", "amount": "100"},  # Преобразовано в строку
        {"state": "PENDING", "date": "2024-11-23", "amount": "50"},  # Преобразовано в строку
    ]
    sorted_records = sort_by_date(records)
    assert sorted_records[0]["date"] == sorted_records[1]["date"]
    assert sorted_records[0]["state"] == "EXECUTED"


def test_sort_by_date_invalid_format() -> None:
    """Тестирует функцию sort_by_date на неверно форматированные даты"""
    records = [
        {"state": "EXECUTED", "date": "2024-11-24", "amount": "100"},  # Преобразовано в строку
        {"state": "EXECUTED", "date": "invalid-date", "amount": "200"},  # Преобразовано в строку
    ]
    with pytest.raises(ValueError, match="Invalid date format"):
        sort_by_date(records)


def test_sort_by_date_empty_list() -> None:
    """Тестирует функцию sort_by_date на пустом списке"""
    sorted_records = sort_by_date([])
    assert sorted_records == []
