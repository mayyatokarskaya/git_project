from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования выполнения функции, Callable: Обёртка для декорируемой функции"""

    def decorator(func: Callable) -> Callable:
        """Декоратор для логирования конкретной функции, выполняет вызов функции и логирует её выполнение или ошибки"""

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обёртка для функции, выполняющая логирование и обработку исключений"""
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok. Result: {result}\n"
                return result
            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}. " f"Inputs: {args}, {kwargs}\n"
                raise
            finally:
                (open(filename, "a").write(message) if filename else print(message, end=""))

        return wrapper

    return decorator


@log(filename="mylog.txt")
def divide(x: float, y: float) -> float:
    """Функция деления для примера"""
    return x / y


divide(4, 2)
try:
    divide(4, 0)
except ZeroDivisionError:
    pass
