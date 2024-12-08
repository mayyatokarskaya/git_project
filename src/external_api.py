import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env файла

API_URL = "https://api.apilayer.com/exchangerates_data/latest"
API_KEY = os.getenv("API_KEY")


def get_exchange_rate(currency):
    """Получает курс валюты к рублю"""
    headers = {
        "apikey": API_KEY
    }
    params = {
        "base": currency,
        "symbols": "RUB"
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['rates']['RUB']
    else:
        raise Exception(f"Error fetching exchange rate: {response.status_code} - {response.text}")


def convert_to_rubles(transaction):
    """Конвертирует сумму транзакции в рубли"""

    amount = transaction.get('amount', 0)
    currency = transaction.get('currency')

    if currency == 'RUB':
        return float(amount)  # Если уже в рублях, просто возвращаем

    if currency in ['USD', 'EUR']:
        exchange_rate = get_exchange_rate(currency)
        return float(amount) * exchange_rate

    raise ValueError("Unsupported currency")



if __name__ == "__main__":
    transaction_usd = {'amount': 100, 'currency': 'USD'}
    transaction_eur = {'amount': 100, 'currency': 'EUR'}
    transaction_rub = {'amount': 100, 'currency': 'RUB'}

    print(convert_to_rubles(transaction_usd))  # Конвертирует USD в RUB
    print(convert_to_rubles(transaction_eur))  # Конвертирует EUR в RUB
    print(convert_to_rubles(transaction_rub))  # Вернет 100.0
