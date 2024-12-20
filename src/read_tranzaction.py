import re
import json
import csv
import pandas as pd
from pathlib import Path

# Определяем базовый путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent


def load_transactions_from_json(file_path):
    """
    Загружает данные из JSON файла.
    :param file_path: Путь к файлу JSON.
    :return: Список словарей с транзакциями.
    """
    full_path = BASE_DIR / file_path
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            transactions = json.load(file)
            print(f"Загружено транзакций из JSON: {len(transactions)}")
            return transactions
    except Exception as e:
        print(f"Ошибка при загрузке JSON: {e}")
        return []


def load_transactions_from_csv(file_path):
    """
    Загружает данные из CSV файла.
    :param file_path: Путь к файлу CSV.
    :return: Список словарей с транзакциями.
    """
    full_path = BASE_DIR / file_path
    transactions = []
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                try:
                    # Проверяем, что значение id не пустое
                    if row['id'].strip() == '':
                        row['id'] = 0  # Заменяем пустое значение на 0
                    else:
                        row['id'] = int(row['id'])

                    # Проверяем, что значение amount не пустое
                    if row['amount'].strip() == '':
                        row['amount'] = 0.0  # Заменяем пустое значение на 0.0
                    else:
                        row['amount'] = float(row['amount'])

                    transactions.append(row)
                except ValueError as e:
                    print(f"Ошибка преобразования данных: {e}, строка: {row}")
        print(f"Загружено транзакций из CSV: {len(transactions)}")
        return transactions
    except Exception as e:
        print(f"Ошибка при загрузке CSV: {e}")
        return []


def load_transactions_from_xlsx(file_path):
    """
    Загружает данные из XLSX файла.
    :param file_path: Путь к файлу XLSX.
    :return: Список словарей с транзакциями.
    """
    full_path = BASE_DIR / file_path
    try:
        df = pd.read_excel(full_path)

        # Заменяем пустые значения на NaN
        df.replace('', pd.NA, inplace=True)

        # Преобразуем столбцы в нужные типы
        try:
            df['id'] = df['id'].astype('Int64')  # Используем Int64 для обработки NaN
            df['amount'] = df['amount'].astype(float)
        except Exception as e:
            print(f"Ошибка преобразования данных в XLSX: {e}")

        transactions = df.to_dict('records')
        print(f"Загружено транзакций из XLSX: {len(transactions)}")
        return transactions
    except Exception as e:
        print(f"Ошибка при загрузке XLSX: {e}")
        return []


def filter_transactions_by_description(transactions, search_string):
    """
    Фильтрует список транзакций по описанию с использованием регулярных выражений.
    :param transactions: Список словарей с данными о транзакциях.
    :param search_string: Строка поиска для фильтрации.
    :return: Список словарей, у которых в описании есть данная строка.
    """
    # Компиляция регулярного выражения
    pattern = re.compile(search_string, re.IGNORECASE)

    # Фильтрация транзакций
    filtered_transactions = [
        transaction for transaction in transactions
        if isinstance(transaction.get('description'), str) and pattern.search(transaction['description'])
    ]

    return filtered_transactions


# Пример использования
if __name__ == "__main__":
    # Указываем относительные пути к файлам
    json_file = "data/operation.json"
    csv_file = "financial/transactions.csv"
    xlsx_file = "financial/transactions_excel.xlsx"

    # Загрузка данных из JSON
    transactions_json = load_transactions_from_json(json_file)

    # Загрузка данных из CSV
    transactions_csv = load_transactions_from_csv(csv_file)

    # Загрузка данных из XLSX
    transactions_xlsx = load_transactions_from_xlsx(xlsx_file)

    # Объединение всех транзакций
    all_transactions = transactions_json + transactions_csv + transactions_xlsx

    # Поиск по описанию
    search_string = "обмен"
    filtered_transactions = filter_transactions_by_description(all_transactions, search_string)
    print("Найдено транзакций по запросу:", len(filtered_transactions))
    print(filtered_transactions)