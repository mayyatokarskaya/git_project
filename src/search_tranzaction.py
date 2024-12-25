import csv
import json
import re
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent


def load_transactions_from_json(file_path):
    """Загружает данные из JSON файла"""
    full_path = BASE_DIR / file_path
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            transactions = json.load(file)
            print(f"Загружено транзакций из JSON: {len(transactions)}")
            return transactions
    except Exception as e:
        print(f"Ошибка при загрузке JSON: {e}")
        return []


def load_transactions_from_csv(file_path):
    """Загружает данные из CSV файла"""
    full_path = BASE_DIR / file_path
    transactions = []
    try:
        with open(full_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                try:
                    # Проверяем, что значение id не пустое
                    if row["id"].strip() == "":
                        row["id"] = 0
                    else:
                        row["id"] = int(row["id"])

                    # Проверяем, что значение amount не пустое
                    if row["amount"].strip() == "":
                        row["amount"] = 0.0
                    else:
                        row["amount"] = float(row["amount"])

                    # Преобразуем данные в формат, совместимый с JSON
                    transaction = {
                        "id": row["id"],
                        "state": row["state"],
                        "date": row["date"],
                        "operationAmount": {
                            "amount": row["amount"],
                            "currency": {"name": row["currency_name"], "code": row["currency_code"]},
                        },
                        "from": row["from"],
                        "to": row["to"],
                        "description": row["description"],
                    }
                    transactions.append(transaction)
                except ValueError as e:
                    print(f"Ошибка преобразования данных: {e}, строка: {row}")
        print(f"Загружено транзакций из CSV: {len(transactions)}")
        return transactions
    except Exception as e:
        print(f"Ошибка при загрузке CSV: {e}")
        return []


def load_transactions_from_xlsx(file_path):
    """Загружает данные из XLSX файла"""
    full_path = BASE_DIR / file_path
    try:
        df = pd.read_excel(full_path)

        # Заменяем пустые значения на NaN
        df.replace("", pd.NA, inplace=True)

        # Преобразуем столбцы в нужные типы
        try:
            df["id"] = df["id"].astype("Int64")
            df["amount"] = df["amount"].astype(float)
            # Приводим столбцы state, from и to к строкам и заменяем NaN на пустую строку
            df["state"] = df["state"].astype(str).fillna("")
            df["from"] = df["from"].astype(str).fillna("")
            df["to"] = df["to"].astype(str).fillna("")
        except Exception as e:
            print(f"Ошибка преобразования данных в XLSX: {e}")

        # Преобразуем данные в формат, совместимый с JSON
        transactions = []
        for _, row in df.iterrows():
            transaction = {
                "id": row["id"],
                "state": row["state"],
                "date": row["date"],
                "operationAmount": {
                    "amount": row["amount"],
                    "currency": {"name": row["currency_name"], "code": row["currency_code"]},
                },
                "from": row["from"],
                "to": row["to"],
                "description": row["description"],
            }
            transactions.append(transaction)

        print(f"Загружено транзакций из XLSX: {len(transactions)}")
        return transactions
    except Exception as e:
        print(f"Ошибка при загрузке XLSX: {e}")
        return []


def filter_transactions_by_description(transactions, search_string):
    """Фильтрует список транзакций по описанию с использованием регулярных выражений"""
    # Компиляция регулярного выражения
    pattern = re.compile(search_string, re.IGNORECASE)

    # Фильтрация транзакций
    filtered_transactions = [
        transaction
        for transaction in transactions
        if isinstance(transaction.get("description"), str) and pattern.search(transaction["description"])
    ]

    return filtered_transactions


if __name__ == "__main__":
    json_file = "data/operation.json"
    csv_file = "financial/transactions.csv"
    xlsx_file = "financial/transactions_excel.xlsx"

    transactions_json = load_transactions_from_json(json_file)

    transactions_csv = load_transactions_from_csv(csv_file)

    transactions_xlsx = load_transactions_from_xlsx(xlsx_file)

    all_transactions = transactions_json + transactions_csv + transactions_xlsx

    search_string = "обмен"
    filtered_transactions = filter_transactions_by_description(all_transactions, search_string)
    print("Найдено транзакций по запросу:", len(filtered_transactions))
    print(filtered_transactions)
