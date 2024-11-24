import re
from datetime import datetime


def mask_account_card(account_info: str) -> str:
    """
    Обрабатывает строку с информацией о карте или счете, маскирует номер в зависимости от типа.

    Принимает строку, разделяет ее на тип и номер, а затем вызывает соответствующую функцию
    для маскировки номера.

    Args:
        account_info (str): Строка с типом и номером карты или счета (например, "Visa Platinum 7000792289606361").

    Returns:
        str: Строка с замаскированным номером или сообщение об ошибке.
    """
    # Разделяем строку на части по пробелам
    parts = account_info.split()

    if len(parts) < 2:  # Обработка некорректных данных
        return f"Неизвестный тип карты: {parts[0]}"  # Ошибка с типом карты

    # Тип карты может содержать несколько слов
    card_type = " ".join(parts[:-1])  # Все части, кроме последней — это тип
    card_number = parts[-1]  # Последняя часть — это номер карты или счета

    # Проверка на известные типы карт
    known_card_types = ["Visa", "MasterCard", "Maestro", "Visa Platinum", "Visa Classic", "Visa Gold"]
    if card_type in known_card_types:
        if re.match(r"^\d{16}$", card_number):  # Проверка, что номер состоит из 16 цифр
            return f"{card_type} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        else:
            # Возвращаем сообщение об ошибке с типом карты
            return f"Неизвестный тип карты: {card_type}"

    # Обработка счета
    if card_type == "Счет":
        if card_number.isdigit() and len(card_number) > 4:  # Номер счета должен быть цифрами и более 4 символов
            return f"{card_type} **{card_number[-4:]}"
        else:
            # Возвращаем сообщение об ошибке с типом счета
            return f"Неизвестный тип карты: {card_type}"

    # Если тип не распознан, возвращаем ошибку с типом карты
    return f"Неизвестный тип карты: {card_type}"


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формате ISO в формат "ДД.ММ.ГГГГ".

    Args:
        date_str (str): Строка с датой в формате ISO (например, "2024-03-11T02:26:18.671407").

    Returns:
        str: Строка с датой в формате "ДД.ММ.ГГГГ" (например, "11.03.2024").
    """
    try:
        # Преобразуем строку в объект datetime
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        # Если произошла ошибка парсинга даты, возвращаем None
        return None
