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


def test_count_operations_with_empty_data():
    """
    Тест проверяет, что функция возвращает пустой словарь, если данные отсутствуют.
    """
    empty_data = []
    categories = ["Перевод организации", "Открытие вклада"]
    result = count_operations_by_category(empty_data, categories)

    # Ожидаемый результат
    expected = {}

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_no_description_key():
    """
    Тест проверяет, что функция корректно обрабатывает данные, где ключ description отсутствует.
    """
    test_data_with_no_description_key = [
        {
            "id": 1,
            "state": "EXECUTED",
        },
        {
            "id": 2,
            "state": "EXECUTED",
        },
    ]

    categories = ["Перевод организации"]
    result = count_operations_by_category(test_data_with_no_description_key, categories)

    # Ожидаемый результат
    expected = {}

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_some_categories_missing():
    """
    Тест проверяет, что функция корректно обрабатывает данные, где не все категории присутствуют.
    """
    test_data_with_some_categories_missing = [
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
    ]

    categories = ["Перевод организации", "Открытие вклада", "Перевод с карты на карту"]
    result = count_operations_by_category(test_data_with_some_categories_missing, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 1,
        "Открытие вклада": 1,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_single_occurrence():
    """
    Тест проверяет, что функция корректно обрабатывает категорию, которая встречается только один раз.
    """
    test_data_with_single_occurrence = [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
    ]

    categories = ["Перевод организации"]
    result = count_operations_by_category(test_data_with_single_occurrence, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 1,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_multiple_occurrences():
    """
    Тест проверяет, что функция корректно обрабатывает категорию, которая встречается много раз.
    """
    test_data_with_multiple_occurrences = [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
    ]

    categories = ["Перевод организации"]
    result = count_operations_by_category(test_data_with_multiple_occurrences, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 3,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_empty_operations():
    """
    Тест проверяет, что функция возвращает пустой словарь, если список операций пуст.
    """
    operations = []
    categories = ["Перевод организации", "Открытие вклада"]
    result = count_operations_by_category(operations, categories)

    # Ожидаемый результат
    expected = {}

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_empty_description():
    """
    Тест проверяет, что функция корректно обрабатывает операции с пустым описанием.
    """
    operations = [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
    ]
    categories = ["Перевод организации"]
    result = count_operations_by_category(operations, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 1,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_missing_description_key():
    """
    Тест проверяет, что функция корректно обрабатывает операции без ключа description.
    """
    operations = [
        {
            "id": 1,
            "state": "EXECUTED",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
    ]
    categories = ["Перевод организации"]
    result = count_operations_by_category(operations, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 1,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"


def test_count_operations_with_non_matching_categories():
    """
    Тест проверяет, что функция корректно обрабатывает операции, у которых description не совпадает с категориями.
    """
    operations = [
        {
            "id": 1,
            "state": "EXECUTED",
            "description": "Неизвестная категория",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "description": "Перевод организации",
        },
    ]
    categories = ["Перевод организации"]
    result = count_operations_by_category(operations, categories)

    # Ожидаемый результат
    expected = {
        "Перевод организации": 1,
    }

    assert result == expected, f"Ожидалось {expected}, но получено {result}"
