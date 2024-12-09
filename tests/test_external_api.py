from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import convert_transaction_to_rub, get_exchange_rate


@pytest.fixture
def mock_getenv():
    with patch("os.getenv") as mock:
        mock.return_value = "test_api_key"
        yield mock


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock:
        yield mock


def test_get_exchange_rate_success(mock_getenv, mock_requests_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 75.0}}
    mock_requests_get.return_value = mock_response

    rate = get_exchange_rate("USD")

    assert rate == 75.0
    mock_requests_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": "test_api_key"},
        params={"base": "USD", "symbols": "RUB"},
    )


def test_get_exchange_rate_error(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.RequestException("Network error")

    with pytest.raises(requests.exceptions.RequestException) as exc_info:
        get_exchange_rate("USD")

    assert str(exc_info.value) == "Network error"


def test_convert_transaction_to_rub_usd():
    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "USD"}}, "id": 1}

    with patch("src.external_api.get_exchange_rate") as mock_get_exchange_rate:
        mock_get_exchange_rate.return_value = 75.0

        rub_amount = convert_transaction_to_rub(transaction)

        assert rub_amount == 7500.0


def test_convert_transaction_to_rub_eur():
    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "EUR"}}, "id": 2}

    with patch("src.external_api.get_exchange_rate") as mock_get_exchange_rate:
        mock_get_exchange_rate.return_value = 80.0

        rub_amount = convert_transaction_to_rub(transaction)

        assert rub_amount == 8000.0


def test_convert_transaction_to_rub_already_in_rub():
    transaction = {"operationAmount": {"amount": 100, "currency": {"code": "RUB"}}, "id": 3}

    rub_amount = convert_transaction_to_rub(transaction)

    assert rub_amount == 100.0


def test_convert_transaction_to_rub_unsupported_currency():
    transaction_invalid = {"operationAmount": {"amount": 100, "currency": {"code": "GBP"}}, "id": 4}

    with pytest.raises(ValueError) as exc_info:
        convert_transaction_to_rub(transaction_invalid)

    assert str(exc_info.value) == "Unsupported currency: GBP"


def test_convert_transaction_to_rub_empty_transaction():
    result = convert_transaction_to_rub(None)

    assert result is None
