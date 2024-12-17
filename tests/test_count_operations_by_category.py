import unittest
from collections import Counter
from src.count_operations_by_category import count_operations_by_category

class TestCountOperationsByCategory(unittest.TestCase):

    def test_count_operations_by_category(self):
        search_string = 'Перевод'
        categories = ["Перевод", "Открытие вклада", "Покупка"]
        result = count_operations_by_category(search_string, categories)
        expected = {'Перевод': 7, 'Открытие вклада': 4, 'Покупка': 0}
        self.assertEqual(result, expected)

    def test_empty_transactions(self):
        search_string = 'Перевод'
        categories = ["Перевод", "Открытие вклада", "Покупка"]
        result = count_operations_by_category(search_string, categories, csv_file="empty.csv", excel_file="empty.xlsx", json_file="empty.json")
        expected = {'Перевод': 0, 'Открытие вклада': 0, 'Покупка': 0}
        self.assertEqual(result, expected)

    def test_case_insensitive(self):
        search_string = 'перевод'
        categories = ["Перевод", "Открытие вклада", "Покупка"]
        result = count_operations_by_category(search_string, categories)
        expected = {'Перевод': 7, 'Открытие вклада': 4, 'Покупка': 0}
        self.assertEqual(result, expected)

    def test_no_matching_categories(self):
        search_string = 'Перевод'
        categories = ["Покупка"]
        result = count_operations_by_category(search_string, categories)
        expected = {'Покупка': 0}
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()