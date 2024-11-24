import pytest

from src.widget import get_date, mask_account_card


# Фикстуры
@pytest.fixture
def card_data():
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ]


@pytest.fixture
def date_data():
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-25T00:00:00.000000", "25.12.2023"),
        ("2021-01-01T12:00:00.000000", "01.01.2021"),
        ("invalid_date", None),
        ("", None),
    ]


# Тесты для mask_account_card
@pytest.mark.parametrize(
    "account_info, expected_output",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa 123", "Неизвестный тип карты: Visa"),  # Некорректная карта
        ("InvalidType 1234567890123456", "Неизвестный тип карты: InvalidType"),  # Неизвестный тип карты
        ("Счет invalid_account", "Неизвестный тип карты: Счет"),  # Некорректный счет
    ],
)
def test_mask_account_card(account_info, expected_output):
    """Проверка маскировки номеров карт и счетов"""
    assert mask_account_card(account_info) == expected_output


# Тестирование get_date
@pytest.mark.parametrize(
    "date_str, expected_output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-25T00:00:00.000000", "25.12.2023"),
        ("2021-01-01T12:00:00.000000", "01.01.2021"),
        ("invalid_date", None),
        ("", None),
    ],
)
def test_get_date(date_str, expected_output):
    """Проверка преобразования строки в формат даты"""
    assert get_date(date_str) == expected_output


# Тестирование на фикстурах
def test_mask_account_card_with_fixture(card_data):
    """Тестирование функции mask_account_card с использованием фикстуры card_data"""
    for account_info, expected in card_data:
        assert mask_account_card(account_info) == expected


def test_get_date_with_fixture(date_data):
    """Тестирование функции get_date с использованием фикстуры date_data"""
    for date_str, expected in date_data:
        assert get_date(date_str) == expected


# Тестирование обработки некорректных входных данных для mask_account_card
@pytest.mark.parametrize(
    "account_info",
    [
        "Visa 123",  # слишком короткий номер карты
        "InvalidType 1234567890123456",  # неизвестный тип карты
        "Счет invalid_account",  # некорректный номер счета
        "1234 5678",  # отсутствие типа
    ],
)
def test_invalid_mask_account_card(account_info):
    """Проверка корректности обработки некорректных входных данных"""
    assert mask_account_card(account_info) == "Неизвестный тип карты: 1234"


# Тестирование обработки некорректных данных в get_date
@pytest.mark.parametrize(
    "date_str",
    [
        "2024-13-11T02:26:18.671407",  # некорректный месяц
        "2024-03-32T02:26:18.671407",  # некорректный день
        "not_a_date",  # строка не является датой
        "2024-03-11T25:00:00.000000",  # некорректное время
    ],
)
def test_invalid_get_date(date_str):
    """Проверка обработки некорректных данных даты"""
    assert get_date(date_str) is None
