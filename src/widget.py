from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_numbers: str) -> str:
    """Маскируем цифры карты или заменяем недостающие символы"""
    card_text = ""
    card_number = ""

    # Разделяем текст и цифры
    for char in card_numbers:
        if char.isalpha() or char.isspace():
            card_text += char
        elif char.isdigit():
            card_number += char

    # Маскируем на основе длины числа
    if not card_number:
        # Если цифр нет, просто маскируем первый символ строки или заменяем на "*"
        return f"{card_text.strip()} *"

    if len(card_number) > 16:
        return f"{card_text} {get_mask_account(card_number)}"
    else:
        return f"{card_text} {get_mask_card_number(card_number)}"


from datetime import datetime


def get_date(input_date: str) -> str:
    """Форматирование даты в формат DD.MM.YYYY"""
    try:
        # Парсим дату, проверяя формат
        date_object = datetime.strptime(input_date, "%Y-%m-%d")
        return date_object.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Некорректный формат даты. Ожидается YYYY-MM-DD.")
