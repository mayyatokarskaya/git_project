import pytest
from src.search_tranzaction import filter_transactions_by_description  # Импортируем функцию

# Примеры данных для тестов
@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 2,
            "description": "Открытие вклада",
            "state": "EXECUTED",
            "date": "2018-03-23T10:45:06.972075",
            "operationAmount": {"amount": "48223.05", "currency": {"name": "руб.", "code": "RUB"}},
            "to": "Счет 41421565395219882431"
        },
        {
            "id": 3,
            "description": "Перевод с карты на счет",
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 4,
            "description": 12345,  # Некорректное значение (число вместо строки)
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 5,
            "description": None,  # Пустое значение
            "state": "EXECUTED",
            "date": "2018-12-20T16:43:26.929246",
            "operationAmount": {"amount": "70946.18", "currency": {"name": "USD", "code": "USD"}},
            "from": "Счет 10848359769870775355",
            "to": "Счет 21969751544412966366"
        }
    ]

# Тесты для функции filter_transactions_by_description
def test_filter_transactions_by_description_positive(sample_transactions):
    """
    Тест на корректную работу функции с валидными данными.
    """
    search_string = "перевод"
    result = filter_transactions_by_description(sample_transactions, search_string)
    assert len(result) == 2  # Должно найти 2 транзакции с описанием "перевод"
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3

def test_filter_transactions_by_description_empty_description(sample_transactions):
    """
    Тест на обработку транзакций с пустым описанием.
    """
    search_string = "перевод"
    result = filter_transactions_by_description(sample_transactions, search_string)
    assert len(result) == 2  # Транзакция с пустым описанием не должна попасть в результат

def test_filter_transactions_by_description_invalid_description(sample_transactions):
    """
    Тест на обработку транзакций с некорректным типом описания (например, число).
    """
    search_string = "перевод"
    result = filter_transactions_by_description(sample_transactions, search_string)
    assert len(result) == 2  # Транзакция с некорректным описанием не должна попасть в результат

def test_filter_transactions_by_description_no_matches(sample_transactions):
    """
    Тест на случай, когда нет совпадений.
    """
    search_string = "нет такого описания"
    result = filter_transactions_by_description(sample_transactions, search_string)
    assert len(result) == 0  # Результат должен быть пустым

def test_filter_transactions_by_description_case_insensitive(sample_transactions):
    """
    Тест на регистронезависимый поиск.
    """
    search_string = "Перевод"
    result = filter_transactions_by_description(sample_transactions, search_string)
    assert len(result) == 2  # Поиск должен быть регистронезависимым

def test_filter_transactions_by_description_empty_transactions():
    """
    Тест на обработку пустого списка транзакций.
    """
    search_string = "перевод"
    result = filter_transactions_by_description([], search_string)
    assert len(result) == 0  # Результат должен быть пустым

def test_filter_transactions_by_description_missing_description(sample_transactions):
    """
    Тест на обработку транзакций без ключа 'description'.
    """
    # Удаляем ключ 'description' из одной из транзакций
    sample_transactions[0].pop("description")
    search_string = "перевод"
    result = filter_transactions_by_description(sample_transactions, search_string)
    assert len(result) == 1  # Транзакция без 'description' не должна попасть в результат