import re
import csv
import json
import pandas as pd
from pathlib import Path


def search_transactions(search_string):
    """Функция для поиска транзакций в трех файлах по заданной строке"""

    # Компиляция регулярного выражения для поиска
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Результирующий список транзакций
    result = []


    base_path = Path(__file__).resolve().parent.parent


    csv_file = base_path / "financial" / "transactions.csv"
    excel_file = base_path / "financial" / "transactions_excel.xlsx"
    json_file = base_path / "data" / "operation.json"

    # Чтение данных из CSV-файла
    try:
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if pattern.search(row.get("description", "")):
                    result.append(row)
    except FileNotFoundError:
        print(f"Файл {csv_file} не найден.")

    # Чтение данных из Excel-файла
    try:
        df = pd.read_excel(excel_file)
        for _, row in df.iterrows():
            description = str(row.get("description", ""))
            if pattern.search(description):
                result.append(row.to_dict())
    except FileNotFoundError:
        print(f"Файл {excel_file} не найден.")

    # Чтение данных из JSON-файла
    try:
        with open(json_file, mode="r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                if pattern.search(item.get("description", "")):
                    result.append(item)
    except FileNotFoundError:
        print(f"Файл {json_file} не найден.")

    return result
