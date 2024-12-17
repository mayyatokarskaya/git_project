import re
import csv
import json
import pandas as pd
from pathlib import Path
from collections import Counter


def count_operations_by_category(search_string, categories, csv_file=None, excel_file=None, json_file=None):
    """
    Функция для подсчета количества банковских операций определенного типа.

    :param search_string: Строка для поиска в описании транзакций.
    :param categories: Список категорий операций.
    :param csv_file: Путь к CSV-файлу с транзакциями (по умолчанию None).
    :param excel_file: Путь к Excel-файлу с транзакциями (по умолчанию None).
    :param json_file: Путь к JSON-файлу с транзакциями (по умолчанию None).
    :return: Словарь, в котором ключи — это названия категорий, а значения — количество операций в каждой категории.
    """
    # Компиляция регулярного выражения для поиска
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    # Создаем счетчик для подсчета операций
    counter = Counter()

    # Определение корневой папки проекта
    base_path = Path(__file__).resolve().parent.parent  # Переходим на уровень выше (корневая папка проекта)

    # Определение путей к файлам, если они не переданы
    if csv_file is None:
        csv_file = base_path / 'financial' / 'transactions.csv'
    if excel_file is None:
        excel_file = base_path / 'financial' / 'transactions_excel.xlsx'
    if json_file is None:
        json_file = base_path / 'data' / 'operation.json'

    # Чтение данных из CSV-файла
    if csv_file:
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')  # Указываем разделитель ';'
                for row in reader:
                    description = row.get('description', '').strip()
                    if pattern.search(description):
                        for category in categories:
                            if category.lower() in description.lower():
                                counter[category] += 1
                                break
        except FileNotFoundError:
            print(f"Файл {csv_file} не найден.")

    # Чтение данных из Excel-файла
    if excel_file:
        try:
            df = pd.read_excel(excel_file)
            for _, row in df.iterrows():
                description = str(row.get('description', '')).strip()
                if pattern.search(description):
                    for category in categories:
                        if category.lower() in description.lower():
                            counter[category] += 1
                            break
        except FileNotFoundError:
            print(f"Файл {excel_file} не найден.")

    # Чтение данных из JSON-файла
    if json_file:
        try:
            with open(json_file, mode='r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    description = item.get('description', '').strip()
                    if pattern.search(description):
                        for category in categories:
                            if category.lower() in description.lower():
                                counter[category] += 1
                                break
        except FileNotFoundError:
            print(f"Файл {json_file} не найден.")

    # Возвращаем словарь с результатами
    return dict(counter)

search_string = 'Открытие вклада'
categories = ["Перевод", "Открытие вклада", "Перевод со счета на счет"]
result = count_operations_by_category(search_string, categories)
print(result)