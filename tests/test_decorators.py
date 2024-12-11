import pytest

from src.decorators import log


@log()
def add(x: int, y: int) -> int:
    """Функция сложения"""
    return x + y


def test_add_success(capsys):
    """Тестирование успешного выполнения функции add"""
    add(2, 3)
    captured = capsys.readouterr()
    assert "add ok. Result: 5" in captured.out


@log()
def divide(x: int, y: int) -> float:
    """Функция деления"""
    return x / y


def test_divide_by_zero(capsys):
    """Тестирование обработки ошибки деления на ноль"""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out


def test_add_to_file(tmp_path):
    """Тестирование логирования в файл"""
    log_file = tmp_path / "src/mylog.txt"

    @log(filename=str(log_file))
    def add(x: int, y: int) -> int:
        """Функция для сложения двух чисел, используется для логирования в файл"""
        return x + y

    add(2, 3)
    with open(log_file, "r") as f:
        log_content = f.read()
    assert "add ok. Result: 5" in log_content
