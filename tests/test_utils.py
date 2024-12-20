from unittest.mock import patch
from src.utils import some_utils_function, logger_utils


def test_some_utils_function_success():
    data = [1, 2, 3, 4]
    with patch.object(logger_utils, 'info') as mock_info, patch.object(logger_utils, 'error') as mock_error:
        result = some_utils_function(data)
        assert result == [2, 4, 6, 8]
        mock_info.assert_called_once_with("Операция выполнена успешно.")
        mock_error.assert_not_called()


def test_some_utils_function_empty_data():
    data = []
    with patch.object(logger_utils, 'info') as mock_info, patch.object(logger_utils, 'error') as mock_error:
        result = some_utils_function(data)
        assert result == []
        mock_error.assert_called_once_with("Ошибка: данные пустые.")
        mock_info.assert_not_called()


def test_some_utils_function_exception():
    data = [1, 2, "three", 4]  # Пример данных, которые вызовут исключение
    with patch.object(logger_utils, 'info') as mock_info, patch.object(logger_utils, 'error') as mock_error:
        result = some_utils_function(data)
        assert result == []
        mock_error.assert_called_once()  # Проверяем, что была вызвана ошибка
        mock_info.assert_not_called()


if __name__ == "__main__":
    # Запускаем тесты и выводим результаты
    for test in [test_some_utils_function_success, test_some_utils_function_empty_data, test_some_utils_function_exception]:
        try:
            test()
            print(f"{test.__name__}: Passed")
        except AssertionError:
            print(f"{test.__name__}: Failed")