from datetime import datetime, timedelta
import pytz

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
