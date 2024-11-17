from typing import List, Dict

def filter_by_state(records: List[Dict[str, str]], state: str = 'EXECUTED') -> List[Dict[str, str]]:
    """Фильтрует список словарей по значению ключа 'state' """

    return [record for record in records if record.get('state') == state]


from typing import List, Dict


def sort_by_date(records: List[Dict[str, str]], reverse: bool = True) -> List[Dict[str, str]]:
    """Сортирует список словарей по дате (ключ 'date') """

    return sorted(records, key=lambda record: record['date'], reverse=reverse)
