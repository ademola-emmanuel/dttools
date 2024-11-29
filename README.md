# dttools

A simple library for common date and time manipulations.

## Installation

```bash
pip install dttools
```

## Usage

```py
# Adding Business Days
from dttools import add_business_days
from datetime import datetime

start_date = datetime(2023, 11, 10)
new_date = add_business_days(start_date, 5)
print(new_date)  # Output: A date 5 business days from the start_date, skipping weekends

```

```py
# Calculating Business Days Between Dates
from dttools import days_between_in_business_days
from datetime import datetime

start_date = datetime(2023, 11, 1)
end_date = datetime(2023, 11, 10)
business_days = days_between_in_business_days(start_date, end_date)
print(business_days)  # Output: The count of business days between the two dates

```

```py
# Formatting Relative Dates
from dttools import format_relative_date
from datetime import datetime, timedelta

some_date = datetime.now() - timedelta(days=3)
relative_format = format_relative_date(some_date)
print(relative_format)  # Output: "3 days ago"

```

```py
# Converting to a Specific Time Zone
from dttools import to_timezone
from datetime import datetime

utc_time = datetime.utcnow()
new_york_time = to_timezone(utc_time, "America/New_York")
print(new_york_time)  # Output: The datetime converted to New York time


```

```py
# Parse Natural Language Date Strings 
from dttools import parse_date

result = parse_date("tomorrow")
print(result)  # Outputs: 2024-11-29 00:00:00


```


```py
# Parse Dates in Specific Languages
from dttools import parse_in_language

result = parse_in_language("hoy", ["es"])  # "hoy" means "today" in Spanish
print(result)  # Outputs: 2024-11-28 00:00:00


```


```py
# Parse Dates with Specific Formats
from dttools import parse_with_format


result = parse_with_format("25/12/2024", date_order="DMY")
print(result)  # Outputs: 2024-12-25 00:00:00

```