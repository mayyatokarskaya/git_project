import pytest
from unittest import mock
import json
import pandas as pd
from io import StringIO


from src.search_tranzaction import (
    load_transactions_from_json,
    load_transactions_from_csv,
    load_transactions_from_xlsx,
    filter_transactions_by_description,
)


# Фикстуры для тестирования загрузки данных

@pytest.fixture
def mock_json_file():
    return [
        {"id": 1, "state": "completed", "date": "2024-01-01",
         "operationAmount": {"amount": 100, "currency": {"name": "USD", "code": "USD"}}, "from": "Alice", "to": "Bob",
         "description": "exchange"},
        {"id": 2, "state": "completed", "date": "2024-01-02",
         "operationAmount": {"amount": 200, "currency": {"name": "EUR", "code": "EUR"}}, "from": "Charlie",
         "to": "David", "description": "payment"},
    ]


@pytest.fixture
def mock_csv_file():
    csv_data = StringIO(
        "id;state;date;amount;currency_name;currency_code;from;to;description\n"
        "1;completed;2024-01-01;100;USD;USD;Alice;Bob;exchange\n"
        "2;completed;2024-01-02;200;EUR;EUR;Charlie;David;payment\n"
    )
    return csv_data


@pytest.fixture
def mock_xlsx_file():
    data = {
        "id": [1, 2],
        "state": ["completed", "completed"],
        "date": ["2024-01-01", "2024-01-02"],
        "amount": [100, 200],
        "currency_name": ["USD", "EUR"],
        "currency_code": ["USD", "EUR"],
        "from": ["Alice", "Charlie"],
        "to": ["Bob", "David"],
        "description": ["exchange", "payment"]
    }
    return pd.DataFrame(data)


# Тестируем load_transactions_from_json
def test_load_transactions_from_json(mock_json_file):
    with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(mock_json_file))):
        result = load_transactions_from_json("mock_file.json")
    assert len(result) == 2
    assert result[0]["description"] == "exchange"


# Тестируем load_transactions_from_csv
def test_load_transactions_from_csv(mock_csv_file):
    with mock.patch("builtins.open", mock.mock_open(read_data=mock_csv_file.getvalue())):
        result = load_transactions_from_csv("mock_file.csv")
    assert len(result) == 2
    assert result[0]["description"] == "exchange"


# Тестируем load_transactions_from_xlsx
def test_load_transactions_from_xlsx(mock_xlsx_file):
    with mock.patch("pandas.read_excel", return_value=mock_xlsx_file):
        result = load_transactions_from_xlsx("mock_file.xlsx")
    assert len(result) == 2
    assert result[0]["description"] == "exchange"


# Тестируем filter_transactions_by_description
@pytest.mark.parametrize(
    "search_string, expected_count",
    [
        ("exchange", 2),
        ("payment", 2),
        ("non-existent", 0),
    ],
)
def test_filter_transactions_by_description(search_string, expected_count, mock_json_file, mock_csv_file,
                                            mock_xlsx_file):
    # Собираем все транзакции
    all_transactions = mock_json_file + load_transactions_from_csv("mock_file.csv") + mock_xlsx_file.to_dict(
        orient="records")

    # Применяем фильтрацию
    result = filter_transactions_by_description(all_transactions, search_string)

    # Проверяем, что количество найденных транзакций соответствует ожидаемому
    assert len(result) == expected_count
