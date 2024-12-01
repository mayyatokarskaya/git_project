import functools
import traceback

def log(filename=None):
    def decorator(func):
        @functools.wraps(func)  # Сохраняет метаданные оригинальной функции
        def wrapper(*args, **kwargs):
            log_message = ""
            try:
                # Попытка выполнения функции
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok. Result: {result}\n"
                return result
            except Exception as e:
                # Логирование ошибки
                error_type = type(e).__name__
                log_message = (
                    f"{func.__name__} error: {error_type}. "
                    f"Inputs: {args}, {kwargs}\n"
                )
                traceback.print_exc()  # Отображение стека вызовов (опционально)
            finally:
                # Логирование в файл или консоль
                if filename:
                    with open(filename, "a") as log_file:
                        log_file.write(log_message)
                else:
                    print(log_message, end="")
        return wrapper
    return decorator

# Пример использования
@log(filename="mylog.txt")
def my_function(x, y):
    return x / y  # Демонстрация: можно вызвать с делением на 0 для тестирования ошибок.

my_function(4, 2)  # Успешный вызов
my_function(4, 0)  # Ошибка деления на 0
