import re
from datetime import datetime
from typing import Optional


def mask_account_card(account_info: Optional[str]) -> str:
    """Обрабатывает строку с информацией о карте или счете, маскирует номер в зависимости от типа."""
    if not account_info:  # Проверяем, что строка не пуста
        return "Информация отсутствует"

    parts = account_info.split()
    if len(parts) < 2:  # Проверяем, что есть минимум два элемента
        return f"Некорректный формат: {account_info}"

    card_type = " ".join(parts[:-1])
    card_number = parts[-1]

    known_card_types = ["Visa", "MasterCard", "Maestro", "Visa Platinum", "Visa Classic", "Visa Gold"]
    if card_type in known_card_types:
        if re.match(r"^\d{16}$", card_number):  # Проверка номера карты
            return f"{card_type} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        else:
            return f"Некорректный номер карты: {card_number}"

    if card_type == "Счет":
        if card_number.isdigit() and len(card_number) > 4:
            return f"{card_type} **{card_number[-4:]}"
        else:
            return f"Некорректный номер счета: {card_number}"

    return f"Неизвестный тип карты или счета: {card_type}"


def get_date(date_str: str) -> Optional[str]:
    """Преобразует строку с датой в формат 'ДД.ММ.ГГГГ'"""
    # Поддерживаем несколько форматов ISO 8601
    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]

    for fmt in formats:
        try:

            date_obj = datetime.strptime(date_str, fmt)

            return date_obj.strftime("%d.%m.%Y")
        except ValueError:

            continue

    return None


def format_transaction(transaction: dict) -> str:
    """Форматирует транзакцию для вывода."""
    date = get_date(transaction.get("date", "")) or "Неизвестная дата"
    description = transaction.get("description", "Неизвестная операция")
    from_account = mask_account_card(transaction.get("from"))  # Используем функцию для маскировки
    to_account = mask_account_card(transaction.get("to"))  # Используем функцию для маскировки
    amount = transaction.get("operationAmount", {}).get("amount", "Неизвестно")
    currency = transaction.get("operationAmount", {}).get("currency", {}).get("name", "Неизвестно")

    return f"{date} {description}\n{from_account} -> {to_account}\nСумма: {amount} {currency}"
