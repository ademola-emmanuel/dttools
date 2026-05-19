"""Tests for dttools."""

import unittest
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from dttools import (
    add_business_days,
    days_between_in_business_days,
    format_relative_date,
    is_business_day,
    is_weekend,
    to_timezone,
)


class TestAddBusinessDays(unittest.TestCase):
    def test_forward(self):
        # Wed Nov 8 + 3 business days -> Mon Nov 13
        result = add_business_days(datetime(2023, 11, 8), 3)
        self.assertEqual(result, datetime(2023, 11, 13))

    def test_skips_weekend(self):
        # Fri Nov 10 + 1 business day -> Mon Nov 13
        result = add_business_days(datetime(2023, 11, 10), 1)
        self.assertEqual(result, datetime(2023, 11, 13))

    def test_zero_returns_start(self):
        start = datetime(2023, 11, 10)
        self.assertEqual(add_business_days(start, 0), start)

    def test_negative(self):
        # Mon Nov 13 - 1 business day -> Fri Nov 10
        result = add_business_days(datetime(2023, 11, 13), -1)
        self.assertEqual(result, datetime(2023, 11, 10))

    def test_skips_holidays(self):
        # Wed Nov 22 + 1 business day with Thu Nov 23 as holiday -> Fri Nov 24
        holidays = {date(2023, 11, 23)}
        result = add_business_days(datetime(2023, 11, 22), 1, holidays=holidays)
        self.assertEqual(result, datetime(2023, 11, 24))


class TestDaysBetweenInBusinessDays(unittest.TestCase):
    def test_basic(self):
        # Wed Nov 1 to Wed Nov 8 (exclusive) -> 5 business days
        self.assertEqual(
            days_between_in_business_days(
                datetime(2023, 11, 1), datetime(2023, 11, 8)
            ),
            5,
        )

    def test_same_day_zero(self):
        d = datetime(2023, 11, 8)
        self.assertEqual(days_between_in_business_days(d, d), 0)

    def test_skips_holidays(self):
        # Same range but Fri Nov 3 is a holiday -> 4
        holidays = {date(2023, 11, 3)}
        self.assertEqual(
            days_between_in_business_days(
                datetime(2023, 11, 1), datetime(2023, 11, 8), holidays=holidays
            ),
            4,
        )


class TestIsBusinessDay(unittest.TestCase):
    def test_weekday(self):
        self.assertTrue(is_business_day(date(2023, 11, 10)))  # Friday

    def test_weekend(self):
        self.assertFalse(is_business_day(date(2023, 11, 11)))  # Saturday

    def test_holiday(self):
        self.assertFalse(
            is_business_day(date(2023, 11, 10), holidays={date(2023, 11, 10)})
        )


class TestIsWeekend(unittest.TestCase):
    def test_saturday(self):
        self.assertTrue(is_weekend(date(2023, 11, 11)))

    def test_monday(self):
        self.assertFalse(is_weekend(date(2023, 11, 13)))


class TestFormatRelativeDate(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2024, 6, 15, 12, 0, 0)

    def test_just_now(self):
        self.assertEqual(
            format_relative_date(self.now - timedelta(seconds=10), now=self.now),
            "Just now",
        )

    def test_minutes_ago(self):
        self.assertEqual(
            format_relative_date(self.now - timedelta(minutes=30), now=self.now),
            "30 minutes ago",
        )

    def test_hours_ago(self):
        self.assertEqual(
            format_relative_date(self.now - timedelta(hours=3), now=self.now),
            "3 hours ago",
        )

    def test_yesterday(self):
        self.assertEqual(
            format_relative_date(self.now - timedelta(days=1), now=self.now),
            "Yesterday",
        )

    def test_days_ago(self):
        self.assertEqual(
            format_relative_date(self.now - timedelta(days=3), now=self.now),
            "3 days ago",
        )

    def test_future_in_hours(self):
        self.assertEqual(
            format_relative_date(self.now + timedelta(hours=2), now=self.now),
            "In 2 hours",
        )

    def test_far_future_falls_back_to_date(self):
        result = format_relative_date(self.now + timedelta(days=60), now=self.now)
        self.assertEqual(result, "August 14, 2024")


class TestToTimezone(unittest.TestCase):
    def test_naive_assumed_utc(self):
        naive = datetime(2024, 6, 15, 12, 0)
        result = to_timezone(naive, "America/New_York")
        # June is EDT (UTC-4): 12:00 UTC -> 08:00 EDT
        self.assertEqual(result.hour, 8)
        self.assertEqual(result.tzinfo, ZoneInfo("America/New_York"))

    def test_aware(self):
        aware = datetime(2024, 6, 15, 12, 0, tzinfo=timezone.utc)
        result = to_timezone(aware, "America/New_York")
        self.assertEqual(result.tzinfo, ZoneInfo("America/New_York"))


if __name__ == "__main__":
    unittest.main()
