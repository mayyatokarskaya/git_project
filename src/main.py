import csv
import json

import pandas as pd

from src.count_operations_by_category import count_operations_by_category
from src.search_tranzaction import filter_transactions_by_description


def load_transactions_from_json():
    """Загружает транзакции из JSON-файла."""
    filename = "C:\\Users\\КГА ПОУ ЛИК\\PycharmProjects\\My_project\\data\\operation.json"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return []


def load_transactions_from_csv():
    """Загружает транзакции из CSV-файла."""
    filename = "C:\\Users\\КГА ПОУ ЛИК\\PycharmProjects\\My_project\\financial\\transactions.csv"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return []


def load_transactions_from_xlsx():
    """Загружает транзакции из XLSX-файла."""
    filename = "C:\\Users\\КГА ПОУ ЛИК\\PycharmProjects\\My_project\\financial\\transactions_excel.xlsx"
    try:
        df = pd.read_excel(filename)
        return df.to_dict("records")
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return []


def filter_transactions_by_status(transactions):
    """Фильтрует транзакции по заданному статусу."""
    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        status = input("Введите статус для фильтрации (EXECUTED, CANCELED, PENDING): ").strip().upper()
        if status in valid_statuses:
            return [tx for tx in transactions if tx.get("state", "").upper() == status]
        print(f'Статус операции "{status}" недоступен.')


def sort_transactions(transactions):
    """Сортирует транзакции по дате в заданном порядке."""
    sort_order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
    reverse_sort = sort_order == "по убыванию"
    return sorted(transactions, key=lambda tx: tx.get("date", ""), reverse=reverse_sort)


def main():
    """Основная функция программы, связывающая все функциональности."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()
    if choice == "1":
        transactions = load_transactions_from_json()
    elif choice == "2":
        transactions = load_transactions_from_csv()
    elif choice == "3":
        transactions = load_transactions_from_xlsx()
    else:
        print("Некорректный выбор. Завершение программы.")
        return

    transactions = filter_transactions_by_status(transactions)
    if input("Отсортировать операции по дате? Да/Нет: ").strip().lower() == "да":
        transactions = sort_transactions(transactions)

    if input("Отфильтровать по описанию? Да/Нет: ").strip().lower() == "да":
        keyword = input("Введите ключевое слово для фильтрации: ").strip()
        transactions = filter_transactions_by_description(transactions, keyword)

    operation_counts = count_operations_by_category(transactions, ["EXECUTED", "CANCELED", "PENDING"])
    print("Количество операций по категориям:", operation_counts)

    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}")
        for tx in transactions:
            # Исправлено: получаем данные о сумме и валюте из вложенных структур
            amount = tx.get("operationAmount", {}).get("amount", "Неизвестно")
            currency = tx.get("operationAmount", {}).get("currency", {}).get("name", "Неизвестно")
            print(
                f"{tx.get('date')} {tx.get('description')}\nСумма: {amount} {currency}"
            )


if __name__ == "__main__":
    main()