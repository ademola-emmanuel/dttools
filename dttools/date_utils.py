from datetime import datetime, timedelta
import pytz
import dateparser

def add_business_days(start_date: datetime, days: int) -> datetime:
    """Add business days to a start date, skipping weekends."""
    current_date = start_date
    while days > 0:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday to Friday are business days
            days -= 1
    return current_date

def days_between_in_business_days(start_date: datetime, end_date: datetime) -> int:
    """Calculate the number of business days between two dates."""
    days = 0
    current_date = start_date
    while current_date < end_date:
        if current_date.weekday() < 5:
            days += 1
        current_date += timedelta(days=1)
    return days

def format_relative_date(date: datetime) -> str:
    """Return a human-readable string for a date relative to today."""
    today = datetime.now().date()
    delta = (date.date() - today).days
    if delta == 0:
        return "Today"
    elif delta == 1:
        return "Tomorrow"
    elif delta == -1:
        return "Yesterday"
    elif delta < -1 and delta >= -7:
        return f"{-delta} days ago"
    elif delta > 1 and delta <= 7:
        return f"In {delta} days"
    else:
        return date.strftime("%B %d, %Y")

def to_timezone(date: datetime, timezone_str: str) -> datetime:
    """Convert a datetime object to a specified timezone."""
    timezone = pytz.timezone(timezone_str)
    return date.astimezone(timezone)



def parse_date(text: str, settings: dict = None, langs: list = None):
    """
    Parse a single natural language date/time string.
    """
    if not text:
        raise ValueError("Input cannot be empty.")
    
    settings = settings or {
        "PREFER_DATES_FROM": "current_period",
        "TIMEZONE": "UTC",
        "RETURN_AS_TIMEZONE_AWARE": True,
    }
    parsed = dateparser.parse(text, settings=settings, languages=langs)
    if not parsed:
        raise ValueError(f"Could not parse: '{text}'")
    return parsed



def parse_in_language(text: str, langs: list, settings: dict = None):
    """
    Parse a natural language date/time string with specific language support.
    """
    if not langs:
        raise ValueError("Languages list cannot be empty.")
    return parse_date(text, settings, langs)


def parse_with_format(text: str, date_order: str = "DMY" , settings: dict = None):
    """
    Parse date/time strings using a specific date format (e.g., DMY, MDY, YMD).
    """
    # Ensure only allowed formats are used
    allowed_formats = {"DMY", "MDY", "YMD"}
    if date_order not in allowed_formats:
        raise ValueError(f"Invalid date_order. Choose from {allowed_formats}.")

    # Update settings with the specified date order
    settings = settings or {}
    settings["DATE_ORDER"] = date_order

    return parse_date(text, settings)