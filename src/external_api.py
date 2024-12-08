import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(base_currency, target_currency="RUB"):
    """Получает текущий курс валюты base_currency к target_currency"""
    url = f"{BASE_URL}?base={base_currency}&symbols={target_currency}"
    headers = {"apikey": API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Выбрасывает исключение, если статус ответа не 200
        data = response.json()
        return data["rates"][target_currency]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при получении курса валют: {e}")


def convert_transaction_to_rub(transaction):
    """Конвертирует сумму транзакции в рубли"""
    try:
        amount = transaction["amount"]
        currency = transaction["currency"]

        if currency == "RUB":
            return float(amount)
        elif currency in ["USD", "EUR"]:
            exchange_rate = get_exchange_rate(currency)
            return float(amount) * exchange_rate
        else:
            raise ValueError(f"Неподдерживаемая валюта: {currency}")
    except KeyError as e:
        raise ValueError(f"Отсутствует обязательный ключ в транзакции: {e}")
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    transaction = {"amount": 100, "currency": "USD"}

    try:
        print(convert_transaction_to_rub(transaction))
    except Exception as e:
        print(f"Ошибка: {e}")
