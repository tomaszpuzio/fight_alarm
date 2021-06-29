import unittest
from data_manager import DataManager

data_manager = DataManager()


class TestDataManager(unittest.TestCase):

    def test_city_as_number(self):
        self.assertFalse(data_manager.does_city_exist(123412))
        self.assertFalse(data_manager.does_city_exist("12345"))

    def test_city_as_imaginary_number(self):
        self.assertFalse(data_manager.does_city_exist(5 + 1j))

    def test_city_as_random_text(self):
        self.assertFalse(data_manager.does_city_exist("dkahbdaajbdka"))

    def test_city_as_close_to_existing_city(self):
        self.assertFalse(data_manager.does_city_exist("New Yoark"))

    def test_city_as_existing_city(self):
        self.assertTrue(data_manager.does_city_exist("New York"))
