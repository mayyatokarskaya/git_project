import pytest
from pathlib import Path
from src.read_tranzaction import search_transactions  # Импортируем вашу функцию

# Тесты для функции search_transactions с использованием Excel-файла
TEST_EXCEL_FILE = Path(__file__).resolve().parent.parent / "test_transactions_excel.xlsx"


def test_search_in_excel():
    """Поиск по строке "Перевод организации"""
    result = search_transactions("Перевод организации", excel_file=TEST_EXCEL_FILE)
    assert len(result) == 157  # Должно найти 3 записи
    assert all("Перевод организации" in item["description"] for item in result)

def test_search_in_excel_case_insensitive():
    """Поиск по строке "перевод организации" (регистр не должен учитываться)"""
    result = search_transactions("перевод организации", excel_file=TEST_EXCEL_FILE)
    assert len(result) == 157  # Должно найти 3 записи
    assert all("Перевод организации" in item["description"] for item in result)

def test_search_in_excel_no_results():
    """Поиск по несуществующей строке"""
    result = search_transactions("nonexistent", excel_file=TEST_EXCEL_FILE)
    assert len(result) == 0  # Результат должен быть пустым

def test_search_in_excel_with_empty_string():
    """Поиск по пустой строке"""
    result = search_transactions("", excel_file=TEST_EXCEL_FILE)
    assert len(result) == 1101  # Результат должен быть пустым

def test_search_in_excel_with_multiple_keywords():
    """Поиск по нескольким ключевым словам"""
    result = search_transactions("карты", excel_file=TEST_EXCEL_FILE)
    assert len(result) == 622  # Должно найти 5 записей с "карты"
    assert all("карты" in item["description"] for item in result)

def test_search_in_excel_with_special_characters():
    """Поиск по строке с символами, которые могут быть экранированы в регулярных выражениях"""
    result = search_transactions("Visa", excel_file=TEST_EXCEL_FILE)
    assert len(result) == 0  # Должно найти 4 записи с "Visa"
    assert all("Visa" in item["description"] for item in result)

def test_search_in_excel_with_partial_match():
    """Поиск по частичному совпадению"""
    result = search_transactions("карт", excel_file=TEST_EXCEL_FILE)
    assert len(result) == 622  # Должно найти 5 записей с "карты"
    assert all("карт" in item["description"] for item in result)

# Тесты для функции search_transactions с использованием CSV-файла
TEST_CSV_FILE = Path(__file__).resolve().parent.parent / "test_transactions.csv"


def test_search_in_csv():
    """Поиск по строке "Перевод организации"""
    result = search_transactions("Перевод организации", csv_file=TEST_CSV_FILE)
    assert len(result) == 157  # Должно найти 2 записи
    assert all("Перевод организации" in item["description"] for item in result)

def test_search_in_csv_case_insensitive():
    """Поиск по строке "перевод организации" (регистр не должен учитываться)"""
    result = search_transactions("перевод организации", csv_file=TEST_CSV_FILE)
    assert len(result) == 157  # Должно найти 2 записи
    assert all("Перевод организации" in item["description"] for item in result)

def test_search_in_csv_no_results():
    """Поиск по несуществующей строке"""
    result = search_transactions("nonexistent", csv_file=TEST_CSV_FILE)
    assert len(result) == 0  # Результат должен быть пустым

def test_search_in_csv_with_empty_string():
    """Поиск по пустой строке"""
    result = search_transactions("", csv_file=TEST_CSV_FILE)
    assert len(result) == 1101

def test_search_in_csv_with_multiple_keywords():
    """Поиск по нескольким ключевым словам"""
    result = search_transactions("карты", csv_file=TEST_CSV_FILE)
    assert len(result) == 622
    assert all("карты" in item["description"] for item in result)

def test_search_in_csv_with_special_characters():
    """Поиск по строке с символами, которые могут быть экранированы в регулярных выражениях"""
    result = search_transactions("Visa", csv_file=TEST_CSV_FILE)
    assert len(result) == 0
    assert all("Visa" in item["description"] for item in result)

def test_search_in_csv_with_partial_match():
    """Поиск по частичному совпадению"""
    result = search_transactions("карт", csv_file=TEST_CSV_FILE)
    assert len(result) == 622
    assert all("карт" in item["description"] for item in result)

