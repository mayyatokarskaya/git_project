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

    try:
        # Некоторые операции с данными
        result = [x * 2 for x in data]  # Просто пример обработки данных
        logger_utils.info("Операция выполнена успешно.")  # Логируем успешное выполнение
        return result
    except Exception as e:
        logger_utils.error(f"Ошибка при обработке данных: {e}")  # Логируем ошибку
        return []


if __name__ == "__main__":
    # Пример использования функции
    data = [1, 2, 3, 4]
    result = some_utils_function(data)
    print(result)

    # Пример с ошибкой
    data = []
    result = some_utils_function(data)
    print(result)
