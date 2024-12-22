from datetime import datetime
from typing import Dict, List


def filter_by_state(transactions):
    """Фильтрует транзакции по заданному статусу."""
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        status = input("Введите статус для фильтрации (EXECUTED, CANCELED, PENDING): ").strip().upper()
        if status in valid_statuses:
            return [tx for tx in transactions if tx.get("state", "").upper() == status]
        print(f'Статус операции "{status}" недоступен.')


def parse_date(record: Dict[str, str]) -> datetime:
    """Парсит строку даты в объект datetime."""
    try:
        # Поддерживаем формат даты с временем и миллисекундами
        return datetime.strptime(record["date"], "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError as e:
        raise ValueError(f"Invalid date format in record: {record['date']}") from e


def sort_by_date(records: List[Dict[str, str]], reverse: bool = False) -> List[Dict[str, str]]:
    """Сортирует записи по дате. Выбрасывает ValueError, если дата имеет некорректный формат."""
    return sorted(
        records,
        key=lambda record: (parse_date(record), record["amount"]),
        reverse=reverse,
    )


def sort_transactions(transactions: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Сортирует транзакции по дате в заданном порядке."""
    sort_order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
    reverse_sort = sort_order == "по убыванию"

    # Используем sort_by_date для сортировки с учетом reverse_sort
    return sort_by_date(transactions, reverse=reverse_sort)


def filter_rub_transactions(transactions):
    """Фильтрует транзакции, оставляя только рублевые."""
    return [tx for tx in transactions if tx.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]