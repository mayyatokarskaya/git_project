from typing import List, Dict, Any, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """возвращает итератор, который выдает транзакции с заданной валютой"""

    return (
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency
    )

def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """генератор, который возвращает описание каждой операции по очереди"""

    return (transaction["description"] for transaction in transactions if "description" in transaction)


# def card_number_generator(card_number: str) -> str:
#     pass


