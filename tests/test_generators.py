from typing import Any, Dict, Iterator, List
import pytest
from src.generators import filter_by_currency, transaction_descriptions

# Фикстура для транзакций
@pytest.fixture
def sample_transactions()-> List[Dict[str, Any]]:
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
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]], currency_code: str, expected_count: int)-> None:
    generator = filter_by_currency(sample_transactions, currency_code)
    filtered_transactions = list(generator)  # Собираем все результаты
    assert len(filtered_transactions) == expected_count
    if expected_count > 0:
        assert all(
            transaction["operationAmount"]["currency"]["code"] == currency_code
            for transaction in filtered_transactions
        )

# Тест на обработку пустого списка
def test_filter_by_currency_empty_list() -> None:
    generator = filter_by_currency([], "USD")
    assert list(generator) == []

# Тест на отсутствие соответствующих операций
def test_filter_by_currency_no_matching_transactions(sample_transactions: List[Dict[str, Any]])-> None:
    generator = filter_by_currency(sample_transactions, "GBP")
    assert list(generator) == []



# Фикстура для примеров транзакций
@pytest.fixture
def sample_transactions() -> List[Dict[str,Any]]:
    return [
        {"id": 1, "description": "Описание транзакции 1"},
        {"id": 2, "description": "Описание транзакции 2"},
        {"id": 3, "description": "Описание транзакции 3"},
    ]

@pytest.fixture
def transactions_without_descriptions() -> List[Dict[str,Any]]:
    return [
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 5, "state": "EXECUTED"}
    ]

# Тесты для генератора описаний
@pytest.mark.parametrize(
    "transactions, expected_descriptions",
    [
        (  # Набор с тремя транзакциями
            [{"id": 1, "description": "Перевод A"}, {"id": 2, "description": "Перевод B"}],
            ["Перевод A", "Перевод B"]
        ),
        ([], []),  # Пустой список
    ]
)
def test_transaction_descriptions(transactions: List[Dict[str,Any]], expected_descriptions: List[str]) -> None:
    descriptions = transaction_descriptions(transactions)
    assert list(descriptions) == expected_descriptions

# Тест на обработку транзакций без описаний
def test_transaction_descriptions_missing_fields(transactions_without_descriptions: List[Dict[str,Any]]) -> None:
    descriptions = transaction_descriptions(transactions_without_descriptions)
    assert list(descriptions) == []  # Ожидаем пустой список, так как описания отсутствуют


