import unittest
from datetime import datetime
from dttools import add_business_days, days_between_in_business_days, format_relative_date, to_timezone

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

if __name__ == "__main__":
    unittest.main()
