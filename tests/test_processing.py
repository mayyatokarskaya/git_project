from datetime import datetime
from typing import Dict, List

import pytest

from src.processing import parse_date, sort_by_date


@pytest.fixture
def sample_records() -> List[Dict[str, str]]:
    """Фикстура, которая возвращает список тестовых записей с полями 'state', 'date', 'amount' и 'operationAmount'"""
    return [
        {
            "state": "EXECUTED",
            "date": "2024-11-24T12:34:56.789000",
            "amount": "100",
            "operationAmount": {"amount": "100"},
        },
        {
            "state": "PENDING",
            "date": "2024-11-23T11:00:00.000000",
            "amount": "50",
            "operationAmount": {"amount": "50"},
        },
        {
            "state": "CANCELLED",
            "date": "2024-11-22T15:30:45.123000",
            "amount": "200",
            "operationAmount": {"amount": "200"},
        },
        {
            "state": "EXECUTED",
            "date": "2024-11-22T08:15:30.456000",
            "amount": "200",
            "operationAmount": {"amount": "200"},
        },
    ]


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("PENDING", 1),
    ],
)
def test_filter_by_state(sample_records: List[Dict[str, str]], state: str, expected_count: int) -> None:
    """Тестирует функцию filter_by_state на правильность фильтрации записей по состоянию"""
    filtered = [record for record in sample_records if record["state"] == state]
    assert len(filtered) == expected_count
    if expected_count > 0:
        assert all(record["state"] == state for record in filtered)


def test_filter_by_state_empty_list() -> None:
    """Тестирует функцию filter_by_state на пустом списке записей"""
    filtered = []
    assert filtered == []


@pytest.mark.parametrize(
    "reverse, expected_dates",
    [
        (
            True,
            [
                "2024-11-24T12:34:56.789000",
                "2024-11-23T11:00:00.000000",
                "2024-11-22T15:30:45.123000",
                "2024-11-22T08:15:30.456000",
            ],
        ),
        (
            False,
            [
                "2024-11-22T08:15:30.456000",
                "2024-11-22T15:30:45.123000",
                "2024-11-23T11:00:00.000000",
                "2024-11-24T12:34:56.789000",
            ],
        ),
    ],
)
def test_sort_by_date(sample_records: List[Dict[str, str]], reverse: bool, expected_dates: List[str]) -> None:
    """Тестирует функцию sort_by_date на сортировку записей по дате"""
    sorted_records = sort_by_date(sample_records, reverse)
    assert [record["date"] for record in sorted_records] == expected_dates


def test_sort_by_date_with_equal_dates() -> None:
    """Тестирует функцию sort_by_date на случаи с одинаковыми датами"""
    records = [
        {
            "state": "EXECUTED",
            "date": "2024-11-24T12:34:56.789000",
            "amount": "100",
            "operationAmount": {"amount": "100"},
        },
        {
            "state": "PENDING",
            "date": "2024-11-23T11:00:00.000000",
            "amount": "50",
            "operationAmount": {"amount": "50"},
        },
        {
            "state": "CANCELLED",
            "date": "2024-11-22T15:30:45.123000",
            "amount": "200",
            "operationAmount": {"amount": "200"},
        },
        {
            "state": "EXECUTED",
            "date": "2024-11-22T08:15:30.456000",
            "amount": "200",
            "operationAmount": {"amount": "200"},
        },
    ]
    sorted_records = sort_by_date(records)
    assert sorted_records[0]["date"] == sorted_records[1]["date"]
    assert sorted_records[0]["state"] == "EXECUTED"


def test_sort_by_date_invalid_format() -> None:
    """Тестирует функцию sort_by_date на неверно форматированные даты"""
    records = [
        {
            "state": "EXECUTED",
            "date": "2024-11-24T12:34:56.789000",
            "amount": "100",
            "operationAmount": {"amount": "100"},
        },
        {"state": "EXECUTED", "date": "invalid-date", "amount": "200", "operationAmount": {"amount": "100"}},
    ]
    with pytest.raises(ValueError, match="Invalid date format"):
        sort_by_date(records)


def test_sort_by_date_empty_list() -> None:
    """Тестирует функцию sort_by_date на пустом списке"""
    sorted_records = sort_by_date([])
    assert sorted_records == []


def test_parse_date_valid() -> None:
    """Тестирует функцию parse_date на корректный ввод"""
    record = {"date": "2024-11-24T12:34:56.789000"}
    parsed_date = parse_date(record)
    assert parsed_date == datetime(2024, 11, 24, 12, 34, 56, 789000)


def test_parse_date_invalid() -> None:
    """Тестирует функцию parse_date на некорректный ввод"""
    record = {"date": "invalid-date"}
    with pytest.raises(ValueError, match="Invalid date format"):
        parse_date(record)
