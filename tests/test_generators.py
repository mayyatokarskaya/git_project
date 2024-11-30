from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными о транзакциях."""
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Payment in USD"},
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}, "description": "Payment in EUR"},
        {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}, "description": "Оплата в рублях"},
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}, "description": "USD transfer"},
        {"id": 5, "operationAmount": {"currency": {}}, "description": "Missing currency"},
        {"id": 6, "operationAmount": {}, "description": "Empty operationAmount"},
        {"id": 7, "description": "Missing operationAmount"},
    ]


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [1, 4]),
        ("EUR", [2]),
        ("RUB", [3]),
        ("GBP", []),  # Невалидная валюта
    ],
)
def test_filter_by_currency(sample_transactions: List[Dict[str, Any]], currency: str, expected_ids: List[str]) -> None:
    """Тестирует функцию `filter_by_currency"""
    result = list(filter_by_currency(sample_transactions, currency))
    assert [transaction["id"] for transaction in result] == expected_ids


def test_transaction_descriptions(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тестирует функцию transaction_descriptions на корректное извлечение описания из списка транзакций"""
    result = list(transaction_descriptions(sample_transactions))
    expected_descriptions = [
        "Payment in USD",
        "Payment in EUR",
        "Оплата в рублях",
        "USD transfer",
        "Missing currency",
        "Empty operationAmount",
        "Missing operationAmount",
    ]
    assert result == expected_descriptions


@pytest.mark.parametrize(
    "start, end, expected_count, expected_first",
    [
        (1, 5, 5, "0000 0000 0000 0001"),
        (1234, 1234, 1, "0000 0000 0000 1234"),  # Один номер
        (0, 0, 1, "0000 0000 0000 0000"),  # Граничный случай
        (9999, 10002, 4, "0000 0000 0000 9999"),  # Несколько номеров
    ],
)
def test_card_number_generator(start: int, end: int, expected_count: int, expected_first: int) -> None:
    """Проверяет, что функция генерирует корректные номера карт в заданном диапазоне"""
    result = list(card_number_generator(start, end))
    assert len(result) == expected_count  # Проверяем количество номеров
    assert result[0] == expected_first  # Проверяем первый номер в списке
    assert all(len(card.replace(" ", "")) == 16 for card in result)  # Проверяем длину каждого номера


@pytest.mark.parametrize(
    "start, end",
    [
        (0, -1),  # Неверный диапазон
        (12345, 12340),  # Перевернутый диапазон
    ],
)
def test_card_number_generator_invalid_range(start: int, end: int) -> None:
    """Проверяет, что функция возвращает пустой результат для некорректных диапазонов"""
    result = list(card_number_generator(start, end))
    assert result == []
