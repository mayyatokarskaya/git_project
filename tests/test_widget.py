import pytest


from src.widget import mask_account_card, get_date
from typing import List, Dict


@pytest.fixture
def account_card_data() -> List[Dict[str, str]]:
    """Фикстура, возвращающая тестовые данные для номеров карт и счетов."""
    return [
        {"input": "Visa Platinum 7000792289606361", "expected": "Visa Platinum **6361"},
        {"input": "MasterCard 1234567890123456", "expected": "MasterCard **3456"},
        {"input": "Счет 987654321012345678901234", "expected": "Счет **234"},
        {"input": "Счет 12", "expected": "Счет **"},
        {"input": "  1  ", "expected": "  *  "},
        {"input": "Account 1", "expected": "Account *"},
    ]


@pytest.mark.parametrize(
    "data",
    [
        {"input": "Visa Platinum 7000792289606361", "expected": "Visa Platinum **6361"},
        {"input": "MasterCard 1234567890123456", "expected": "MasterCard **3456"},
        {"input": "Счет 987654321012345678901234", "expected": "Счет **234"},
        {"input": "Счет 12", "expected": "Счет **"},
        {"input": "  1  ", "expected": "  *  "},
        {"input": "Account 1", "expected": "Account *"},
    ],
)
def test_mask_account_card(data: Dict[str, str]) -> None:
    """Тестирование функции mask_account_card с различными картами и счетами."""
    result = mask_account_card(data["input"])
    assert result == data["expected"], f"Expected {data['expected']} but got {result}"


@pytest.mark.parametrize(
    "data",
    [
        {"input": "123456", "expected": "123456"},
        {"input": " ", "expected": " "},
        {"input": "Visa 12345", "expected": "Visa **5"},
    ],
)
def test_mask_account_card_invalid(data: Dict[str, str]) -> None:
    """Тестирование обработки некорректных данных в mask_account_card."""
    result = mask_account_card(data["input"])
    assert result == data["expected"], f"Expected {data['expected']} but got {result}"


@pytest.fixture
def date_data() -> List[Dict[str, str]]:
    """Фикстура c тестовыми данными для дат"""
    return [
        {"input": "2024-03-11T02:26:18.671407", "expected": "11.03.2024"},
        {"input": "2020-12-31T23:59:59.999999", "expected": "31.12.2020"},
        {"input": "2024-01-01T00:00:00.000000", "expected": "01.01.2024"},
        {"input": "2024-03-11", "expected": "11.03.2024"},
        {"input": "invalid-date", "expected": "Неверный формат даты"},
        {"input": "", "expected": "Неверный формат даты"},
    ]


@pytest.mark.parametrize(
    "data",
    [
        {"input": "2024-03-11T02:26:18.671407", "expected": "11.03.2024"},
        {"input": "2020-12-31T23:59:59.999999", "expected": "31.12.2020"},
        {"input": "2024-01-01T00:00:00.000000", "expected": "01.01.2024"},
        {"input": "2024-03-11", "expected": "11.03.2024"},
        {"input": "invalid-date", "expected": "Неверный формат даты"},
        {"input": "", "expected": "Неверный формат даты"},
    ],
)
def test_get_date(data: Dict[str, str]) -> None:
    """Тестирование функции get_date на различных входных данных."""
    result = get_date(data["input"])
    assert result == data["expected"], f"Expected {data['expected']} but got {result}"


@pytest.mark.parametrize(
    "input_data", ["InvalidInput", "12-12-2024", "Account"]  # Неверные данные  # Неверный формат даты  # Нет цифр
)
def test_mask_account_card_invalid(input_data):
    with pytest.raises(ValueError, match="Invalid card number"):
        mask_account_card(input_data)
