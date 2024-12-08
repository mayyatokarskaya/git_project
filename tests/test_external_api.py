from unittest.mock import Mock, patch

import requests

from src.external_api import convert_transaction_to_rub, get_exchange_rate


def test_convert_transaction_to_rub_rub() -> None:
    """Тестирует конвертацию транзакции в рублях"""
    transaction = {"amount": 100, "currency": "RUB"}
    result = convert_transaction_to_rub(transaction)
    assert result == 100.0


@patch("src.external_api.get_exchange_rate")
def test_convert_transaction_to_rub_usd(mock_get_exchange_rate) -> None:
    """Тестирует конвертацию транзакции в долларах"""
    mock_get_exchange_rate.return_value = 70.0
    transaction = {"amount": 100, "currency": "USD"}
    result = convert_transaction_to_rub(transaction)
    assert result == 7000.0


def test_convert_transaction_to_rub_unsupported_currency() -> None:
    """Тестирует обработку неподдерживаемой валюты"""
    transaction = {"amount": 100, "currency": "GBP"}
    try:
        convert_transaction_to_rub(transaction)
    except ValueError as e:
        assert str(e) == "Неподдерживаемая валюта: GBP"
    else:
        assert False, "Ожидалось исключение ValueError"


def test_convert_transaction_to_rub_missing_key() -> None:
    """Тестирует обработку отсутствующего ключа в транзакции"""
    transaction = {"amount": 100}
    try:
        convert_transaction_to_rub(transaction)
    except ValueError as e:
        assert str(e) == "Отсутствует обязательный ключ в транзакции: 'currency'"
    else:
        assert False, "Ожидалось исключение ValueError"


@patch("src.external_api.requests.get")
def test_get_exchange_rate(mock_get) -> None:
    """тестирует получение курса валют"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 70.0}}
    mock_get.return_value = mock_response

    rate = get_exchange_rate("USD")
    assert rate == 70.0


@patch("src.external_api.requests.get")
def test_get_exchange_rate_error(mock_get) -> None:
    """Тестирует обработку ошибки при получении курса валюты"""
    mock_get.side_effect = requests.exceptions.RequestException("Network error")

    try:
        get_exchange_rate("USD")
    except Exception as e:
        assert str(e) == "Ошибка при получении курса валют: Network error"
    else:
        assert False, "Ожидалось исключение Exception"


if __name__ == "__main__":
    test_convert_transaction_to_rub_rub()
    test_convert_transaction_to_rub_usd()
    test_convert_transaction_to_rub_unsupported_currency()
    test_convert_transaction_to_rub_missing_key()
    test_get_exchange_rate()
    test_get_exchange_rate_error()
    print("Все тесты пройдены успешно.")
