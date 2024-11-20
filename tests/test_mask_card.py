import pytest

from src.masks import get_mask_card_number


@pytest.fixture
def card_numbers() -> list[tuple[str, str]]:
    """Фикстура для предоставления списка тестовых данных с номерами карт
    и ожидаемыми результатами маскирования"""

    return [
        ("9876543210123456", "9876 54** **** 3456"),
        ("1234", ""),
        ("12345678901234567890", ""),
        ("", ""),
        ("abcd123456789012", ""),
        ("123456781234567X", ""),
    ]


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234", ""),
        ("12345678901234567890", ""),
        ("", ""),
        ("abcd123456789012", ""),
        ("123456781234567X", ""),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Тестирование функции get_mask_card_number на различные входные данные"""

    result = get_mask_card_number(card_number)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_invalid_card_number() -> None:
    """Дополнительные тесты для проверки обработки некорректных входных данных"""

    assert get_mask_card_number("") == "", "Failed for empty string"

    assert get_mask_card_number("abcd123456789012") == "", "Failed for non-numeric string"

    assert get_mask_card_number("123456781234567X") == "", "Failed for non-digit characters in the middle"

    assert get_mask_card_number("1234") == "", "Failed for short number"
    assert get_mask_card_number("12345678901234567890") == "", "Failed for too long number"


def test_valid_card_numbers() -> None:
    """Дополнительные тесты для проверки корректной обработки валидных номеров карт"""

    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361", "Test case 1 failed"
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456", "Test case 2 failed"
    assert get_mask_card_number("9876543210123456") == "9876 54** **** 3456", "Test case 3 failed"
