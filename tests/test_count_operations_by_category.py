from src.count_operations_by_category import count_operations_by_category

# Тестовые данные
test_data = [
    {
        "id": 1,
        "state": "EXECUTED",
        "description": "Перевод организации",
    },
    {
        "id": 2,
        "state": "EXECUTED",
        "description": "Открытие вклада",
    },
    {
        "id": 3,
        "state": "EXECUTED",
        "description": "Перевод со счета на счет",
    },
    {
        "id": 4,
        "state": "EXECUTED",
        "description": "Перевод организации",
    },
    {
        "id": 5,
        "state": "EXECUTED",
        "description": "Открытие вклада",
    },
    {
        "id": 6,
        "state": "EXECUTED",
        "description": "Перевод с карты на карту",
    },
]


# Тесты для функции count_operations_by_category
def test_count_operations_by_category():
    """
    Тест проверяет, что функция корректно подсчитывает операции по категориям.
    """
    categories = ["Перевод организации", "Открытие вклада", "Перевод со счета на счет", "Перевод с карты на карту"]
    result = count_operations_by_category(test_data, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 2,
        "Открытие вклада": 2,
        "Перевод со счета на счет": 1,
        "Перевод с карты на карту": 1,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_empty_categories():
    """
    Тест проверяет, что функция возвращает пустой словарь, если категории отсутствуют.
    """
    categories = []
    result = count_operations_by_category(test_data, categories)

    # Ожидаемый результат
    expected = {}

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_missing_description():
    """
    Тест проверяет, что функция корректно обрабатывает операции без категории (description отсутствует).
    """
    test_data_with_missing_description = [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "state": "EXECUTED",
        },
    ]

    categories = ["Перевод организации"]
    result = count_operations_by_category(test_data_with_missing_description, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 1,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_duplicates():
    """
    Тест проверяет, что функция корректно обрабатывает дубликаты операций.
    """
    test_data_with_duplicates = [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
    ]

    categories = ["Перевод организации"]
    result = count_operations_by_category(test_data_with_duplicates, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 2,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"
