import re
from datetime import datetime
from typing import Optional


def mask_account_card(account_info: str) -> str:
    """Обрабатывает строку с информацией о карте или счете, маскирует номер в зависимости от типа"""
    parts = account_info.split()

    if len(parts) < 2:
        return f"Неизвестный тип карты: {parts[0]}"

    card_type = " ".join(parts[:-1])
    card_number = parts[-1]

    known_card_types = ["Visa", "MasterCard", "Maestro", "Visa Platinum", "Visa Classic", "Visa Gold"]
    if card_type in known_card_types:
        if re.match(r"^\d{16}$", card_number):
            return f"{card_type} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        else:
            return f"Неизвестный тип карты: {card_type}"

    if card_type == "Счет":
        if card_number.isdigit() and len(card_number) > 4:
            return f"{card_type} **{card_number[-4:]}"
        else:
            return f"Неизвестный тип карты: {card_type}"

    return f"Неизвестный тип карты: {card_type}"


def get_date(date_str: str) -> Optional[str]:
    """Преобразует строку с датой в формат "ДД.ММ.ГГГГ" """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return None
