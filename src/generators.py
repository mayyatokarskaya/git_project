from typing import List, Dict, Any, Iterator


def filter_by_currency(transactions:List[Dict[str, Any]], currency:str)-> Iterator[Dict[str, Any]]:
    """возвращает итератор, который выдает транзакции с заданной валютой"""

    return (transaction for transaction in transactions if transaction.get("operationAmount",{}).get("currency",{}).get("code") ==currency)


