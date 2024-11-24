import pytest
from typing import Dict, List
from datetime import datetime


def filter_by_state(records: List[Dict[str, str]], state: str = "EXECUTED") -> List[Dict[str, str]]:
    """Фильтрует список словарей по значению ключа 'state'"""
    return [record for record in records if record.get("state") == state]


def sort_by_date(records: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """Сортирует список словарей по дате (ключ 'date')."""
    return sorted(records, key=lambda record: record["date"], reverse=reverse)


@pytest.fixture
def sample_records() -> List[Dict[str, str]]:
    """Фикстура для создания тестовых данных"""
    return [
        {"id": "1", "state": "EXECUTED", "date": "2023-11-23"},
        {"id": "2", "state": "CANCELED", "date": "2023-11-22"},
        {"id": "3", "state": "EXECUTED", "date": "2023-11-24"},
        {"id": "4", "state": "PENDING", "date": "2023-11-21"},
    ]


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),  # Должно быть 2 записи с состоянием EXECUTED
        ("CANCELED", 1),  # 1 запись с состоянием CANCELED
        ("PENDING", 1),   # 1 запись с состоянием PENDING
        ("FAILED", 0),    # Нет записей с состоянием FAILED
    ]
)
def test_filter_by_state(sample_records: List[Dict[str, str]], state: str, expected_count: int):
    """Тестирование фильтрации по состоянию"""
    filtered_records = filter_by_state(sample_records, state)
    assert len(filtered_records) == expected_count, f"Expected {expected_count} records with state {state}, but got {len(filtered_records)}"


@pytest.mark.parametrize(
    "records, reverse, expected_order",
    [
        (
            [
                {"id": "1", "state": "EXECUTED", "date": "2023-11-23"},
                {"id": "2", "state": "CANCELED", "date": "2023-11-22"},
                {"id": "3", "state": "EXECUTED", "date": "2023-11-24"},
            ],
            True,
            ["3", "1", "2"],  # Ожидаемый порядок: сначала 2023-11-24, потом 2023-11-23, и наконец 2023-11-22
        ),
        (
            [
                {"id": "1", "state": "EXECUTED", "date": "2023-11-23"},
                {"id": "2", "state": "CANCELED", "date": "2023-11-22"},
                {"id": "3", "state": "EXECUTED", "date": "2023-11-24"},
            ],
            False,
            ["2", "1", "3"],  # Ожидаемый порядок: сначала 2023-11-22, потом 2023-11-23, и наконец 2023-11-24
        ),
        (
            [
                {"id": "1", "state": "EXECUTED", "date": "2023-11-23"},
                {"id": "2", "state": "EXECUTED", "date": "2023-11-23"},
                {"id": "3", "state": "EXECUTED", "date": "2023-11-23"},
            ],
            True,
            ["1", "2", "3"],  # Порядок не меняется, так как все даты одинаковые
        ),
        (
            [
                {"id": "1", "state": "EXECUTED", "date": "invalid-date"},
                {"id": "2", "state": "CANCELED", "date": "2023-11-22"},
                {"id": "3", "state": "EXECUTED", "date": "2023-11-24"},
            ],
            True,
            ["3", "2", "1"],  # Должен быть помещен на последнее место, так как дата некорректна
        ),
    ]
)
def test_sort_by_date(records: List[Dict[str, str]], reverse: bool, expected_order: List[str]):
    """Тестирование сортировки по дате."""
    sorted_records = sort_by_date(records, reverse)
    sorted_ids = [record["id"] for record in sorted_records]
    assert sorted_ids == expected_order, f"Expected order {expected_order}, but got {sorted_ids}"


@pytest.mark.parametrize(
    "records, expected_exception",
    [
        ([
            {"id": "1", "state": "EXECUTED", "date": "2023-13-01"},  # Некорректный месяц
            {"id": "2", "state": "CANCELED", "date": "2023-11-22"},
        ], ValueError),  # Ожидаем ValueError, так как месяц некорректен
        ([
            {"id": "1", "state": "EXECUTED", "date": "invalid-date"},  # Некорректный формат даты
        ], ValueError),  # Ожидаем ValueError, так как дата не может быть распарсена
    ]
)
def test_sort_by_date_invalid(records: List[Dict[str, str]], expected_exception: type):
    """Тестирование обработки некорректных дат."""
    with pytest.raises(expected_exception):
        sort_by_date(records)


# Тестирование фильтрации и сортировки в связке
def test_filter_and_sort(sample_records: List[Dict[str, str]]):
    """Тестирование фильтрации и сортировки."""
    filtered_records = filter_by_state(sample_records, "EXECUTED")
    sorted_records = sort_by_date(filtered_records, reverse=True)
    sorted_ids = [record["id"] for record in sorted_records]
    assert sorted_ids == ["3", "1"], f"Expected sorted order ['3', '1'], but got {sorted_ids}"
