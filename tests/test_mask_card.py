import pytest
from src.masks import get_mask_card_number


@pytest.fixture
def card_numbers():
    return [
        ("9876543210123456", "9876 54** **** 3456"),
        ("1234", ""),
        ("12345678901234567890", ""),
        ("", ""),
        ("abcd123456789012", ""),
        ("123456781234567X", ""),
    ]

