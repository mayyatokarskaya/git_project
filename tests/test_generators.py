from typing import Any, Dict, Iterator, List
import pytest
from src.generators import filter_by_currency

# Фикстура для транзакций
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод в USD"
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "EUR"}},
            "description": "Перевод в EUR"
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Еще один перевод в USD"
        },
        {
            "id": 4,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Перевод в RUB"
        },
    ]

# Тест для фильтрации по валюте
@pytest.mark.parametrize(
    "currency_code, expected_count",
    [("USD", 2), ("EUR", 1), ("RUB", 1), ("GBP", 0)]
)
def test_filter_by_currency(sample_transactions, currency_code, expected_count):
    generator = filter_by_currency(sample_transactions, currency_code)
    filtered_transactions = list(generator)  # Собираем все результаты
    assert len(filtered_transactions) == expected_count
    if expected_count > 0:
        assert all(
            transaction["operationAmount"]["currency"]["code"] == currency_code
            for transaction in filtered_transactions
        )

# Тест на обработку пустого списка
def test_filter_by_currency_empty_list():
    generator = filter_by_currency([], "USD")
    assert list(generator) == []

# Тест на отсутствие соответствующих операций
def test_filter_by_currency_no_matching_transactions(sample_transactions):
    generator = filter_by_currency(sample_transactions, "GBP")
    assert list(generator) == []
