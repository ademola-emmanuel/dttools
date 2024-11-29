import unittest
from datetime import datetime
from dttools import add_business_days, days_between_in_business_days, format_relative_date, to_timezone, parse_date, parse_in_language, parse_with_format

class TestDateUtils(unittest.TestCase):
    def test_add_business_days(self):
        start_date = datetime(2023, 11, 8)
        self.assertEqual(add_business_days(start_date, 3).strftime("%Y-%m-%d"), "2023-11-13")

    def test_days_between_in_business_days(self):
        start_date = datetime(2023, 11, 1)
        end_date = datetime(2023, 11, 8)
        self.assertEqual(days_between_in_business_days(start_date, end_date), 5)

    def test_format_relative_date(self):
        today = datetime.now()
        self.assertEqual(format_relative_date(today), "Today")

    def test_to_timezone(self):
        date = datetime(2023, 11, 8)
        converted_date = to_timezone(date, "America/New_York")
        self.assertEqual(converted_date.tzinfo.zone, "America/New_York")

    def test_parse_date(self):
        self.assertIsNotNone(parse_date("tomorrow"))
        self.assertIsNotNone(parse_date("3 days ago"))
        with self.assertRaises(ValueError):
            parse_date("")  # Empty input
        with self.assertRaises(ValueError):
            parse_date("invalid string")  # Unparseable input

    
    def test_parse_in_language(self):
        self.assertIsNotNone(parse_in_language("hoy", ["es"]))  # Spanish for "today"
        self.assertIsNotNone(parse_in_language("demain", ["fr"]))  # French for "tomorrow")
        with self.assertRaises(ValueError):
            parse_in_language("hoy", ["en"])  # Incorrect language list
        with self.assertRaises(ValueError):
            parse_in_language("today", [])  # Empty language list

    def test_parse_with_format(self):
        self.assertIsNotNone(parse_with_format("25/12/2024", date_order="DMY"))
        self.assertIsNotNone(parse_with_format("12/25/2024", date_order="MDY"))
        self.assertIsNotNone(parse_with_format("2024-12-25", date_order="YMD"))

    def test_parse_with_format_invalid_format(self):
        with self.assertRaises(ValueError):
            parse_with_format("25/12/2024", date_order="XYZ")

    def test_parse_with_format_invalid_date(self):
        with self.assertRaises(ValueError):
            parse_with_format("not a date", date_order="DMY")

if __name__ == "__main__":
    unittest.main()
