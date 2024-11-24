from datetime import datetime
from typing import Dict, List


def filter_by_state(records: List[Dict[str, str]], state: str = "EXECUTED") -> List[Dict[str, str]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    return [record for record in records if record.get("state") == state]


def sort_by_date(records: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """Сортирует список словарей по дате (ключ 'date') и проверяет формат даты."""
    for record in records:
        try:
            print(f"Checking date: {record['date']}")
            datetime.strptime(record["date"], "%Y-%m-%d")
        except ValueError:
            print(f"Invalid date format detected: {record['date']}")
            raise ValueError(f"Некорректный формат даты: {record['date']}")
    return sorted(records, key=lambda record: record["date"], reverse=reverse)
