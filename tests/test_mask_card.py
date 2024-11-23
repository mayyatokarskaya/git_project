import pytest
from src.masks import get_mask_card_number


@pytest.fixture
def valid_card_numbers():
    """Фикстура с корректными номерами карт"""
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ]


@pytest.fixture
def invalid_card_numbers():
    """Фикстура с некорректными номерами карт"""
    return [
        ("12345", "Invalid card number"),
        ("abcd1234efgh5678", "Invalid card number"),
        ("", "Invalid card number"),
        ("123456781234567", "Invalid card number"),
    ]


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567812345678", "1234 56** **** 5678"),
        ("1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected: str):
    """Тестирование функции get_mask_card_number с корректными номерами карт"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number",
    [
        "12345",
        "abcd1234efgh5678",
        "",
        "123456781234561",
    ],
)
def test_get_mask_card_number_invalid(card_number: str):
    """Тестирование функции get_mask_card_number с некорректными номерами карт"""
    with pytest.raises(ValueError, match="Invalid card number"):
        get_mask_card_number(card_number)
