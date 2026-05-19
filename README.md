# dttools

A simple Python library for common date and time manipulations.

## Installation

```bash
pip install dttools
```

Requires Python 3.10+. Uses the standard library's `zoneinfo` for timezones
(no `pytz`). On Windows, `tzdata` is pulled in automatically.

## Usage

### Adding (or subtracting) business days

```python
from dttools import add_business_days
from datetime import datetime, date

start_date = datetime(2023, 11, 10)
add_business_days(start_date, 5)   # 5 business days forward, skipping weekends
add_business_days(start_date, -3)  # 3 business days backward

# Optionally skip holidays too
add_business_days(start_date, 5, holidays={date(2023, 11, 23)})
```

### Counting business days between two dates

```python
from dttools import days_between_in_business_days
from datetime import datetime

days_between_in_business_days(datetime(2023, 11, 1), datetime(2023, 11, 10))
# Counts weekdays from start (inclusive) up to end (exclusive).
```

### Checking business days and weekends

```python
from dttools import is_business_day, is_weekend
from datetime import date

is_business_day(date(2023, 11, 10))  # True  (Friday)
is_business_day(date(2023, 11, 11))  # False (Saturday)
is_weekend(date(2023, 11, 11))       # True
```

### Human-readable relative dates

```python
from dttools import format_relative_date
from datetime import datetime, timedelta

now = datetime.now()
format_relative_date(now - timedelta(minutes=30))  # "30 minutes ago"
format_relative_date(now - timedelta(hours=2))     # "2 hours ago"
format_relative_date(now - timedelta(days=3))      # "3 days ago"
format_relative_date(now + timedelta(days=1))      # "Tomorrow"
```

### Converting to a specific timezone

```python
from dttools import to_timezone
from datetime import datetime, timezone

utc_now = datetime.now(timezone.utc)
to_timezone(utc_now, "America/New_York")
```

Naive datetimes are treated as UTC.

## License

MIT - see [LICENSE](https://github.com/ademola-emmanuel/dttools/blob/master/LICENSE).
