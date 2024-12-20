import csv
import json
from collections import Counter

import pandas as pd


def read_json(file_path):
    """Читает данные из JSON-файла и возвращает их в виде списка словарей"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def read_csv(file_path):
    """Читает данные из JSON-файла и возвращает их в виде списка словарей"""
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        data = [row for row in reader]
    return data


def read_excel(file_path):
    """Читает данные из Excel-файла и возвращает их в виде списка словарей"""
    df = pd.read_excel(file_path)
    data = df.to_dict(orient="records")
    return data


def extract_categories(operations):
    """Извлекает уникальные категории (описания) из списка операций"""
    categories = set()
    for operation in operations:
        description = operation.get("description")
        if description:
            categories.add(description)
    return list(categories)


def count_operations_by_category(operations, categories):
    """Подсчитывает количество банковских операций по каждой категории"""
    counter = Counter()

    for operation in operations:
        description = operation.get("description")
        if description in categories:
            counter[description] += 1

    return dict(counter)


def process_data():
    """Основная функция для чтения данных из файлов, извлечения категорий и подсчета операций"""
    json_data = read_json("../data/operation.json")
    csv_data = read_csv("../financial/transactions.csv")
    excel_data = read_excel("../financial/transactions_excel.xlsx")
    all_operations = json_data + csv_data + excel_data
    categories = extract_categories(all_operations)
    result = count_operations_by_category(all_operations, categories)
    print("Количество операций по категориям:")
    for category, count in result.items():
        print(f"{category}: {count}")


# Запуск обработки данных
if __name__ == "__main__":
    process_data()
