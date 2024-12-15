import pandas as pd
from typing import List, Dict
import os


def read_transactions_from_csv(file_path: str) -> List[Dict[str, any]]:
    """Считывает финансовые операции из CSV-файла"""
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict(orient="records")
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении CSV-файла: {e}")
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict[str, any]]:
    """Считывает финансовые операции из Excel-файла"""
    try:
        df = pd.read_excel(file_path)
        transactions = df.to_dict(orient="records")
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении Excel-файла: {e}")
        return []



# Определение базовой директории как родителя текущего файла
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Пути к файлам
csv_file_path = os.path.join(base_dir, "financial", "transactions.csv")
excel_file_path = os.path.join(base_dir, "financial", "transactions_excel.xlsx")

# Пример вызова функций
csv_transactions = read_transactions_from_csv(csv_file_path)
excel_transactions = read_transactions_from_excel(excel_file_path)

# Вывод первых 5 транзакций для проверки
print("CSV Transactions:", csv_transactions[:5])
print("Excel Transactions:", excel_transactions[:5])
