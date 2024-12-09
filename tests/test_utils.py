from unittest.mock import mock_open, patch

from src.utils import read_transactions


def test_read_transactions_success():
    with patch("os.path.exists") as mock_exists:
        with patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]'):
            mock_exists.return_value = True  # Симулируем существование файла

            result = read_transactions("dummy_path.json")

            assert len(result) == 1
            assert result[0]["id"] == 1
            assert result[0]["amount"] == 100


def test_file_not_found():
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False  # Симулируем отсутствие файла

        result = read_transactions("dummy_path.json")

        assert result == []


def test_invalid_json():
    with patch("os.path.exists") as mock_exists:
        with patch("builtins.open", new_callable=mock_open, read_data="not a json"):
            mock_exists.return_value = True  # Симулируем существование файла

            result = read_transactions("dummy_path.json")

            assert result == []


def test_not_a_list():
    with patch("os.path.exists") as mock_exists:
        with patch("builtins.open", new_callable=mock_open, read_data="{}"):  # Не список
            mock_exists.return_value = True  # Симулируем существование файла

            result = read_transactions("dummy_path.json")

            assert result == []


if __name__ == "__main__":
    # Запускаем тесты и выводим результаты
    for test in [test_read_transactions_success, test_file_not_found, test_invalid_json, test_not_a_list]:
        try:
            test()
            print(f"{test.__name__}: Passed")
        except AssertionError:
            print(f"{test.__name__}: Failed")
