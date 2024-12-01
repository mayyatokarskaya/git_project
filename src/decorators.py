def log(filename=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
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


# Пример использования
@log(filename="mylog.txt")
def divide(x, y):
    return x / y


divide(4, 2)
try:
    divide(4, 0)
except ZeroDivisionError:
    pass
