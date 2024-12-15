from unittest.mock import mock_open, patch

from src.financial_transactions import read_transactions_from_csv, read_transactions_from_excel


# Тесты для read_csv_transactions
def test_read_csv_transactions_success():
    """Тест для проверки корректного чтения данных из CSV-файла"""

    csv_data = "date,amount,description\n2023-10-01,100.0,Payment\n2023-10-02,-50.0,Refund"
    with patch("builtins.open", mock_open(read_data=csv_data)):
        with patch("pandas.read_csv") as mock_read_csv:
            expected_transactions = [
                {"date": "2023-10-01", "amount": 100.0, "description": "Payment"},
                {"date": "2023-10-02", "amount": -50.0, "description": "Refund"},
            ]
            mock_read_csv.return_value.to_dict.return_value = expected_transactions
            result = read_transactions_from_csv("fake_path.csv")
            assert result == expected_transactions


def test_read_csv_transactions_file_not_found():
    """Тест для проверки обработки ошибки, если файл не найден"""
    with patch("pandas.read_csv", side_effect=FileNotFoundError):
        result = read_transactions_from_csv("nonexistent_file.csv")
        assert result == []


def test_read_csv_transactions_invalid_format():
    """Тест для проверки обработки ошибки, если формат файла некорректен"""
    with patch("pandas.read_csv", side_effect=Exception("Invalid format")):
        result = read_transactions_from_csv("invalid_format.csv")
        assert result == []


# Тесты для read_excel_transactions
def test_read_excel_transactions_success():
    """Тест для проверки корректного чтения данных из Excel-файла"""
    # excel_data = "date,amount,description\n2023-10-01,100.0,Payment\n2023-10-02,-50.0,Refund"
    with patch("pandas.read_excel") as mock_read_excel:
        expected_transactions = [
            {"date": "2023-10-01", "amount": 100.0, "description": "Payment"},
            {"date": "2023-10-02", "amount": -50.0, "description": "Refund"},
        ]
        mock_read_excel.return_value.to_dict.return_value = expected_transactions
        result = read_transactions_from_excel("fake_path.xlsx")
        assert result == expected_transactions


def test_read_excel_transactions_file_not_found():
    """Тест для проверки обработки ошибки, если файл не найден"""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = read_transactions_from_excel("nonexistent_file.xlsx")
        assert result == []


def test_read_excel_transactions_invalid_format():
    """Тест для проверки обработки ошибки, если формат файла некорректен"""
    with patch("pandas.read_excel", side_effect=Exception("Invalid format")):
        result = read_transactions_from_excel("invalid_format.xlsx")
        assert result == []
