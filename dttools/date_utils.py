"""Date and time utilities."""

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def _to_date(dt: date | datetime) -> date:
    return dt.date() if isinstance(dt, datetime) else dt


def is_weekend(dt: date | datetime) -> bool:
    """Return True if ``dt`` falls on a Saturday or Sunday."""
    return _to_date(dt).weekday() >= 5


def is_business_day(dt: date | datetime, holidays: set[date] | None = None) -> bool:
    """Return True if ``dt`` is a weekday and not in ``holidays``."""
    d = _to_date(dt)
    if d.weekday() >= 5:
        return False
    return holidays is None or d not in holidays


def add_business_days(
    start_date: datetime,
    days: int,
    holidays: set[date] | None = None,
) -> datetime:
    """Add business days to ``start_date``, skipping weekends and holidays.

    Pass a negative ``days`` to subtract business days. Zero returns ``start_date``.
    """
    if days == 0:
        return start_date
    step = timedelta(days=1 if days > 0 else -1)
    remaining = abs(days)
    current = start_date
    while remaining > 0:
        current += step
        if is_business_day(current, holidays):
            remaining -= 1
    return current


def days_between_in_business_days(
    start_date: datetime,
    end_date: datetime,
    holidays: set[date] | None = None,
) -> int:
    """Count business days from ``start_date`` (inclusive) up to ``end_date`` (exclusive).

    Returns 0 if ``start_date`` is on or after ``end_date``.
    """
    count = 0
    current = start_date
    while current < end_date:
        if is_business_day(current, holidays):
            count += 1
        current += timedelta(days=1)
    return count


def format_relative_date(dt: datetime, *, now: datetime | None = None) -> str:
    """Return a human-readable string for ``dt`` relative to ``now``.

    Handles minutes, hours and days. Falls back to ``"Month DD, YYYY"`` for
    differences beyond a week. ``now`` defaults to the current time, using the
    same timezone as ``dt`` when ``dt`` is timezone-aware.
    """
    if now is None:
        now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()

    seconds = int((dt - now).total_seconds())
    future = seconds > 0
    seconds = abs(seconds)

    if seconds < 45:
        return "Just now"

    minutes = seconds // 60
    if minutes < 60:
        unit = "minute" if minutes == 1 else "minutes"
        return f"In {minutes} {unit}" if future else f"{minutes} {unit} ago"

    hours = minutes // 60
    if hours < 24:
        unit = "hour" if hours == 1 else "hours"
        return f"In {hours} {unit}" if future else f"{hours} {unit} ago"

    delta_days = (dt.date() - now.date()).days
    if delta_days == 1:
        return "Tomorrow"
    if delta_days == -1:
        return "Yesterday"
    if -7 <= delta_days <= -2:
        return f"{-delta_days} days ago"
    if 2 <= delta_days <= 7:
        return f"In {delta_days} days"
    return dt.strftime("%B %d, %Y")


def to_timezone(dt: datetime, timezone_str: str) -> datetime:
    """Convert ``dt`` to the IANA timezone named ``timezone_str``.

    Naive datetimes are assumed to be in UTC.
    """
    tz = ZoneInfo(timezone_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(tz)
