def get_mask_card_number(card_number: str) -> str:
    """маскирует цифры номера карты, начиная с седьмой и до последних четырех"""
    card_number = card_number.replace(" ", "")
    if not card_number.isdigit() or len(card_number) not in (12, 16, 19):
        raise ValueError("Invalid card number")
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    return masked_number


def get_mask_account(current_account: str) -> str:
    """Маскирует номер счета"""
    if len(current_account) < 4:
        return "*" * len(current_account)
    last_four_digits = current_account[-4:]  # последние 4 цифры счета
    masked_account = "**" + last_four_digits  # формируем маску

    return masked_account
