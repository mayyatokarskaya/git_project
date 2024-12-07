import json
import os

def read_transactions(filepath):
    """Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях"""

    if not os.path.exists(filepath):
        print(f"Файл '{filepath}' не найден.")
        return []

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            print(f"Ошибка: содержимое файла '{filepath}' не является списком.")
            return []

        return data

    except json.JSONDecodeError:
        print(f"Ошибка: файл '{filepath}' содержит некорректный JSON.")
        return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Корень проекта
filepath = os.path.join(base_dir, "data", "operation.json")
# Получение данных о транзакциях
transactions = read_transactions(filepath)

# Вывод результата
if transactions:
    print("Транзакции успешно загружены:")
    print(transactions)
else:
    print("Файл пустой или содержит некорректные данные.")

print("Текущая рабочая директория:", os.getcwd())


