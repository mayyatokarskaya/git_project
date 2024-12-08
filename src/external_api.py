import json
import os

import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(base_currency, target_currency="RUB"):
    """Получает текущий курс валюты"""
    headers = {"apikey": API_KEY}
    params = {"base": base_currency, "symbols": target_currency}
    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data["rates"][target_currency]


def convert_transaction_to_rub(transaction):
    """Конвертирует сумму транзакции в рубли"""
    if not transaction:  # Проверка на пустой словарь
        return None

    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]

    if currency_code == "RUB":
        return amount
    elif currency_code in ["USD", "EUR"]:
        exchange_rate = get_exchange_rate(currency_code)
        return amount * exchange_rate
    else:
        raise ValueError(f"Unsupported currency: {currency_code}")


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(root_dir, "data", "operation.json")

    with open(file_path, "r", encoding="utf-8") as file:
        transactions = json.load(file)

    for transaction in transactions:
        rub_amount = convert_transaction_to_rub(transaction)
        if rub_amount is not None:
            print(f"Transaction ID: {transaction['id']}, Amount in RUB: {rub_amount}")
