import json

from src.count_operations_by_category import count_operations_by_category
from src.main import filter_transactions_by_status, load_transactions_from_json, sort_transactions
from src.search_tranzaction import filter_transactions_by_description

# Тестовые данные для JSON
test_json_data = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "description": "Перевод организации",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
    },
    {
        "id": 2,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "description": "Перевод организации",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
    },
    {
        "id": 3,
        "state": "PENDING",
        "date": "2020-06-07T11:11:36.000000",
        "description": "Перевод с карты на карту",
        "operationAmount": {"amount": "30731.00", "currency": {"name": "руб.", "code": "RUB"}},
    },
]


# Тесты для функции load_transactions_from_json
def test_load_transactions_from_json(mocker):
    """Тест проверяет, что функция load_transactions_from_json корректно загружает данные из JSON-файла"""
    mocker.patch("builtins.open", mocker.mock_open(read_data=json.dumps(test_json_data)))
    transactions = load_transactions_from_json()
    assert len(transactions) == 3
    assert transactions[0]["state"] == "EXECUTED"
    assert transactions[1]["state"] == "CANCELED"


# Тесты для функции filter_transactions_by_status
def test_filter_transactions_by_status():
    """Тест проверяет, что функция filter_transactions_by_status корректно фильтрует транзакции по статусу"""
    transactions = [
        {"state": "EXECUTED", "date": "2019-08-26T10:50:58.294041", "description": "Перевод организации"},
        {"state": "CANCELED", "date": "2018-09-12T21:27:25.241689", "description": "Перевод организации"},
        {"state": "PENDING", "date": "2020-06-07T11:11:36.000000", "description": "Перевод с карты на карту"},
    ]

    # Фильтрация по EXECUTED
    filtered = filter_transactions_by_status(transactions)
    assert len(filtered) == 1
    assert filtered[0]["state"] == "EXECUTED"

    # Фильтрация по CANCELED
    filtered = filter_transactions_by_status(transactions)
    assert len(filtered) == 1
    assert filtered[0]["state"] == "CANCELED"


# Тесты для функции sort_transactions
def test_sort_transactions():
    """Тест проверяет, что функция sort_transactions корректно сортирует транзакции по дате"""
    transactions = [
        {"date": "2019-08-26T10:50:58.294041", "description": "Перевод организации"},
        {"date": "2018-09-12T21:27:25.241689", "description": "Перевод организации"},
        {"date": "2020-06-07T11:11:36.000000", "description": "Перевод с карты на карту"},
    ]

    # Сортировка по возрастанию
    sorted_asc = sort_transactions(transactions)
    assert sorted_asc[0]["date"] == "2018-09-12T21:27:25.241689"
    assert sorted_asc[-1]["date"] == "2020-06-07T11:11:36.000000"

    # Сортировка по убыванию
    sorted_desc = sort_transactions(transactions)
    assert sorted_desc[0]["date"] == "2020-06-07T11:11:36.000000"
    assert sorted_desc[-1]["date"] == "2018-09-12T21:27:25.241689"


# Тесты для функции filter_transactions_by_description
def test_filter_transactions_by_description():
    """Тест проверяет, что функция filter_transactions_by_description корректно фильтрует транзакции по описанию"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты на карту"},
        {"description": "Открытие вклада"},
    ]

    # Фильтрация по ключевому слову "Перевод"
    filtered = filter_transactions_by_description(transactions, "Перевод")
    assert len(filtered) == 2
    assert filtered[0]["description"] == "Перевод организации"
    assert filtered[1]["description"] == "Перевод с карты на карту"

    # Фильтрация по ключевому слову "Открытие"
    filtered = filter_transactions_by_description(transactions, "Открытие")
    assert len(filtered) == 1
    assert filtered[0]["description"] == "Открытие вклада"


def test_count_operations_by_category():
    """Тест проверяет, что функция count_operations_by_category корректно подсчитывает операции по категориям"""
    transactions = [
        {"state": "EXECUTED"},
        {"state": "CANCELED"},
        {"state": "EXECUTED"},
        {"state": "PENDING"},
    ]

    result = count_operations_by_category(transactions, ["EXECUTED", "CANCELED", "PENDING"])
    assert result == {"EXECUTED": 2, "CANCELED": 1, "PENDING": 1}
