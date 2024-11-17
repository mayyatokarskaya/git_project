from masks import get_mask_account, get_mask_card_number


def mask_account_card(card_numbers: str) -> str:
    """маскируем цифры карты"""
    card_text = ""
    card_number = ""
    for char in card_numbers:
        if char.isalpha() or char.isspace():
            card_text += char
        if char.isdigit():
            card_number += char
    if len(card_number) > 16:
        return f"{card_text} {get_mask_account(card_number)}"
    else:
        return f"{card_text} {get_mask_card_number(card_number)}"


card_numbers = input("Введите номер карты/ счета в формате Visa Platinum/Счет 7000792289606361 \n")
masked = mask_account_card(card_numbers)
print(masked)


def get_date(input_date: str) -> str:
    """форматирование даты"""
    year = input_date[0:4]
    month = input_date[5:7]
    day = input_date[8:10]

    return f"{day}.{month}.{year}"


input_date = get_date("2024-03-11T02:26:18.671407")
print(input_date)
