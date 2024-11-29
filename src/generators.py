from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """возвращает итератор, который выдает транзакции с заданной валютой"""

    return (
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency
    )


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """генератор, который возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        if "description" in transaction:
            yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """генератор банковских карт в формате ХХХХ ХХХХ ХХХХ ХХХХ"""

    for number in range(start, end + 1):
        card_number = f"{number:016d}"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
