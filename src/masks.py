def get_mask_card_number(card_number: str) -> str:
    """маскирует цифры номера карты, начиная с седьмой и до последних четырех"""
    card_number = card_number.replace(" ", "")
    masked_number = f"{card_number[:4]} {card_number[4:6]} ** **** {card_number[-4:]}"

    return masked_number


input_card_number = input("Введите номер карты \n")
masked_card_number = get_mask_card_number(input_card_number)
print(masked_card_number)


def get_mask_account(current_account: str) -> str:
    """Маскирует номер счета"""
    last_four_digits = current_account[-4:]  # последние 4 цифры счета
    masked_account = "**" + last_four_digits  # формируем маску

    return masked_account


current_account = input("Введите номер счета \n")
masked = get_mask_account(current_account)
print(masked)
