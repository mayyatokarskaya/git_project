from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_numbers: str) -> str:
    """Маскируем номер карты или счета"""
    card_text = ""
    card_number = ""

    for char in card_numbers:
        if char.isalpha() or char.isspace():
            card_text += char
        elif char.isdigit():
            card_number += char

    if not card_number:  # Если нет цифр
        raise ValueError("Invalid card number")

    if len(card_number) > 16:
        return f"{card_text.strip()} {get_mask_account(card_number)}"
    elif len(card_number) >= 4:
        return f"{card_text.strip()} {get_mask_card_number(card_number)}"
    else:
        return f"{card_text.strip()} **"


def get_date(input_date: str) -> str:
    """Форматирование даты"""
    try:
        year, month, day = input_date.split("-")
        return f"{day}.{month}.{year}"
    except ValueError:
        raise ValueError("Некорректный формат даты. Ожидается YYYY-MM-DD.")
