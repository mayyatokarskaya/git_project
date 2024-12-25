import logging
import os

log_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)  # Путь к папке logs относительно текущей рабочей директории
log_file_path_utils = os.path.join(log_dir, "logs", "utils.log")  # Путь к файлу лога для модуля utils

# Настройка логирования для модуля utils
logger_utils = logging.getLogger("utils")
logger_utils.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования DEBUG

# Создаем обработчик, который записывает логи в файл
file_handler_utils = logging.FileHandler(log_file_path_utils, encoding="utf-8", mode="w")
file_handler_utils.setLevel(logging.DEBUG)  # Записываем все логи, начиная с уровня DEBUG

# Настройка форматтера
file_formatter_utils = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler_utils.setFormatter(file_formatter_utils)

# Добавляем обработчик в логер
logger_utils.addHandler(file_handler_utils)


# Пример функции для модуля utils
def some_utils_function(data):
    """Пример функции, которая что-то делает с данными и логирует результат."""

    if not data:
        logger_utils.error("Ошибка: данные пустые.")  # Логируем ошибку
        return []

    result = []
    for item in data:
        if isinstance(item, (int, float)):  # Проверяем, что элемент - это число
            result.append(item * 2)  # Умножаем число на 2
        else:
            logger_utils.error(f"Ошибка: некорректные данные: {item}")  # Логируем ошибку
            return []  # Возвращаем пустой список, если встретили некорректные данные

    logger_utils.info("Операция выполнена успешно.")  # Логируем успешное выполнение
    return result



if __name__ == "__main__":
    # Пример использования функции
    data = [1, 2, 3, 4]
    result = some_utils_function(data)
    print(result)

    # Пример с ошибкой
    data = []
    result = some_utils_function(data)
    print(result)
