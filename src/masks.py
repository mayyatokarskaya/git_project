import logging
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Корень проекта
log_file_path = os.path.join(base_dir, "logs", "masks.log")


logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)


file_handler = logging.FileHandler(log_file_path, mode="w")
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """маскирует цифры номера карты, начиная с седьмой и до последних четырех"""
    try:
        card_number = card_number.replace(" ", "")
        if not card_number.isdigit() or len(card_number) not in (12, 16, 19):
            raise ValueError("Invalid card number")

        masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

        logger.info(f"Successfully masked card number: {card_number}")  # Успешный случай
        return masked_number
    except Exception as e:
        logger.error(f"Error in get_mask_card_number: {str(e)}")  # Ошибка
        raise


def get_mask_account(current_account: str) -> str:
    """Маскирует номер счета"""
    try:
        if len(current_account) < 4:
            masked_account = "*" * len(current_account)
        else:
            last_four_digits = current_account[-4:]
            masked_account = "**" + last_four_digits

        logger.info(f"Successfully masked account number: {current_account}")  # Успешный случай
        return masked_account
    except Exception as e:
        logger.error(f"Error in get_mask_account: {str(e)}")  # Ошибка
        raise
