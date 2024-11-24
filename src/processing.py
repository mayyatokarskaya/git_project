from datetime import datetime
from typing import Dict, List


def filter_by_state(records: List[Dict[str, str]], state: str = "EXECUTED") -> List[Dict[str, str]]:
    """Фильтрует список словарей по значению ключа 'state'"""

    return [record for record in records if record.get("state") == state]


def sort_by_date(records: List[Dict[str, str]], reverse: bool = False) -> List[Dict[str, str]]:
    """Сортирует записи по дате. Выбрасывает ValueError, если дата имеет некорректный формат"""

    def parse_date(record: Dict[str, str]) -> datetime:
        """Парсит строку даты в объект datetime."""
        try:
            return datetime.strptime(record["date"], "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"Invalid date format in record: {record['date']}") from e

    return sorted(
        records,
        key=lambda record: (parse_date(record), record["amount"]),
        reverse=reverse,
    )
