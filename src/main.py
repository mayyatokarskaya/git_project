from pathlib import Path

from src.count_operations_by_category import count_operations_by_category
from src.search_tranzaction import filter_transactions_by_description
from search_tranzaction import load_transactions_from_json, load_transactions_from_csv, load_transactions_from_xlsx
from processing import filter_by_state, sort_transactions, filter_rub_transactions
from widget import format_transaction

# Используем BASE_DIR из load_transactions.py
BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    """Основная функция программы, связывающая все функциональности."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Ваш выбор: ").strip()

    if choice == "1":
        file_path = "data/operation.json"
        transactions = load_transactions_from_json(file_path)
    elif choice == "2":
        file_path = "financial/transactions.csv"
        transactions = load_transactions_from_csv(file_path)
    elif choice == "3":
        file_path = "financial/transactions_excel.xlsx"
        transactions = load_transactions_from_xlsx(file_path)
    else:
        print("Некорректный выбор. Завершение программы.")
        return

    transactions = filter_by_state(transactions)
    if input("Отсортировать операции по дате? Да/Нет: ").strip().lower() == "да":
        transactions = sort_transactions(transactions)

    if input("Отфильтровать по описанию? Да/Нет: ").strip().lower() == "да":
        keyword = input("Введите ключевое слово для фильтрации: ").strip()
        transactions = filter_transactions_by_description(transactions, keyword)

    if input("Выводить только рублевые транзакции? Да/Нет: ").strip().lower() == "да":
        transactions = filter_rub_transactions(transactions)

    operation_counts = count_operations_by_category(transactions, ["EXECUTED", "CANCELED", "PENDING"])
    print("Количество операций по категориям:", operation_counts)

    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}")
        for tx in transactions:
            print(format_transaction(tx))


if __name__ == "__main__":
    main()