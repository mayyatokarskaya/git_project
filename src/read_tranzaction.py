import re
import csv
import json
import pandas as pd
from pathlib import Path


def search_transactions(search_string, csv_file=None, excel_file=None, json_file=None):
    """Функция для поиска транзакций в трех файлах по заданной строке"""

    # Компиляция регулярного выражения для поиска
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    result = []

    base_path = Path(__file__).resolve().parent.parent  # Переходим на уровень выше (корневая папка проекта)

    # Определение путей к файлам, если они не переданы
    if csv_file is None:
        csv_file = base_path / "financial" / "transactions.csv"
    if excel_file is None:
        excel_file = base_path / "financial" / "transactions_excel.xlsx"
    if json_file is None:
        json_file = base_path / "data" / "operation.json"

    # Чтение данных из CSV-файла
    if csv_file:
        try:
            with open(csv_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file, delimiter=";")  # Указываем разделитель ';'
                for row in reader:
                    if pattern.search(row.get("description", "")):
                        result.append(row)
        except FileNotFoundError:
            print(f"Файл {csv_file} не найден.")

    # Чтение данных из Excel-файла
    if excel_file:
        try:
            df = pd.read_excel(excel_file)
            for _, row in df.iterrows():
                description = str(row.get("description", ""))
                if pattern.search(description):
                    result.append(row.to_dict())
        except FileNotFoundError:
            print(f"Файл {excel_file} не найден.")

    # Чтение данных из JSON-файла
    if json_file:
        try:
            with open(json_file, mode="r", encoding="utf-8") as file:
                data = json.load(file)
                for item in data:
                    if pattern.search(item.get("description", "")):
                        result.append(item)
        except FileNotFoundError:
            print(f"Файл {json_file} не найден.")

    return result

