"""
Date and Time Functions

Date/time manipulation, formatting, and calculations.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
import time


def current_timestamp() -> int:
    """
    Returns current Unix timestamp
    
    Returns:
        Current timestamp in seconds
        
    Example:
        >>> timestamp = current_timestamp()
        >>> timestamp > 1600000000
        True
    """
    return int(time.time())


def current_datetime() -> datetime:
    """
    Returns current datetime
    
    Returns:
        Current datetime object
        
    Example:
        >>> dt = current_datetime()
        >>> isinstance(dt, datetime)
        True
    """
    return datetime.now()


def timestamp_to_datetime(timestamp: int) -> datetime:
    """
    Converts Unix timestamp to datetime
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Datetime object
        
    Example:
        >>> dt = timestamp_to_datetime(1609459200)
        >>> dt.year
        2021
    """
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(dt: datetime) -> int:
    """
    Converts datetime to Unix timestamp
    
    Args:
        dt: Datetime object
        
    Returns:
        Unix timestamp
        
    Example:
        >>> dt = datetime(2021, 1, 1)
        >>> timestamp_to_datetime(datetime_to_timestamp(dt)).year
        2021
    """
    return int(dt.timestamp())


def format_datetime(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Formats datetime as string
    
    Args:
        dt: Datetime object
        format_string: Format string
        
    Returns:
        Formatted string
        
    Example:
        >>> dt = datetime(2021, 1, 1, 12, 0, 0)
        >>> format_datetime(dt)
        '2021-01-01 12:00:00'
    """
    return dt.strftime(format_string)


def parse_datetime(date_string: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parses datetime from string
    
    Args:
        date_string: Date string
        format_string: Format string
        
    Returns:
        Datetime object
        
    Example:
        >>> dt = parse_datetime("2021-01-01 12:00:00")
        >>> dt.year
        2021
    """
    return datetime.strptime(date_string, format_string)


def add_days(dt: datetime, days: int) -> datetime:
    """
    Adds days to datetime
    
    Args:
        dt: Datetime object
        days: Number of days to add
        
    Returns:
        New datetime
        
    Example:
        >>> dt = datetime(2021, 1, 1)
        >>> new_dt = add_days(dt, 5)
        >>> new_dt.day
        6
    """
    return dt + timedelta(days=days)


def add_hours(dt: datetime, hours: int) -> datetime:
    """
    Adds hours to datetime
    
    Args:
        dt: Datetime object
        hours: Number of hours to add
        
    Returns:
        New datetime
        
    Example:
        >>> dt = datetime(2021, 1, 1, 10)
        >>> new_dt = add_hours(dt, 5)
        >>> new_dt.hour
        15
    """
    return dt + timedelta(hours=hours)


def add_minutes(dt: datetime, minutes: int) -> datetime:
    """
    Adds minutes to datetime
    
    Args:
        dt: Datetime object
        minutes: Number of minutes to add
        
    Returns:
        New datetime
        
    Example:
        >>> dt = datetime(2021, 1, 1, 10, 30)
        >>> new_dt = add_minutes(dt, 45)
        >>> new_dt.minute
        15
    """
    return dt + timedelta(minutes=minutes)


def difference_in_days(dt1: datetime, dt2: datetime) -> int:
    """
    Calculates difference between two dates in days
    
    Args:
        dt1: First datetime
        dt2: Second datetime
        
    Returns:
        Number of days (absolute value)
        
    Example:
        >>> dt1 = datetime(2021, 1, 1)
        >>> dt2 = datetime(2021, 1, 10)
        >>> difference_in_days(dt1, dt2)
        9
    """
    return abs((dt2 - dt1).days)


def difference_in_hours(dt1: datetime, dt2: datetime) -> float:
    """
    Calculates difference between two datetimes in hours
    
    Args:
        dt1: First datetime
        dt2: Second datetime
        
    Returns:
        Number of hours (absolute value)
        
    Example:
        >>> dt1 = datetime(2021, 1, 1, 10)
        >>> dt2 = datetime(2021, 1, 1, 15)
        >>> difference_in_hours(dt1, dt2)
        5.0
    """
    return abs((dt2 - dt1).total_seconds() / 3600)


def difference_in_minutes(dt1: datetime, dt2: datetime) -> float:
    """
    Calculates difference between two datetimes in minutes
    
    Args:
        dt1: First datetime
        dt2: Second datetime
        
    Returns:
        Number of minutes (absolute value)
        
    Example:
        >>> dt1 = datetime(2021, 1, 1, 10, 30)
        >>> dt2 = datetime(2021, 1, 1, 11, 15)
        >>> difference_in_minutes(dt1, dt2)
        45.0
    """
    return abs((dt2 - dt1).total_seconds() / 60)


def is_leap_year(year: int) -> bool:
    """
    Checks if year is a leap year
    
    Args:
        year: Year to check
        
    Returns:
        True if leap year
        
    Example:
        >>> is_leap_year(2020)
        True
        >>> is_leap_year(2021)
        False
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def days_in_month(year: int, month: int) -> int:
    """
    Returns number of days in a month
    
    Args:
        year: Year
        month: Month (1-12)
        
    Returns:
        Number of days
        
    Example:
        >>> days_in_month(2021, 2)
        28
        >>> days_in_month(2020, 2)
        29
    """
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    else:  # February
        return 29 if is_leap_year(year) else 28


def start_of_day(dt: datetime) -> datetime:
    """
    Returns start of day (00:00:00)
    
    Args:
        dt: Datetime object
        
    Returns:
        Start of day
        
    Example:
        >>> dt = datetime(2021, 1, 1, 15, 30)
        >>> start = start_of_day(dt)
        >>> start.hour
        0
    """
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def end_of_day(dt: datetime) -> datetime:
    """
    Returns end of day (23:59:59)
    
    Args:
        dt: Datetime object
        
    Returns:
        End of day
        
    Example:
        >>> dt = datetime(2021, 1, 1, 15, 30)
        >>> end = end_of_day(dt)
        >>> end.hour
        23
    """
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)


def start_of_month(dt: datetime) -> datetime:
    """
    Returns start of month
    
    Args:
        dt: Datetime object
        
    Returns:
        Start of month
        
    Example:
        >>> dt = datetime(2021, 1, 15)
        >>> start = start_of_month(dt)
        >>> start.day
        1
    """
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def end_of_month(dt: datetime) -> datetime:
    """
    Returns end of month
    
    Args:
        dt: Datetime object
        
    Returns:
        End of month
        
    Example:
        >>> dt = datetime(2021, 1, 15)
        >>> end = end_of_month(dt)
        >>> end.day
        31
    """
    last_day = days_in_month(dt.year, dt.month)
    return dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)


def age_in_years(birth_date: datetime, reference_date: Optional[datetime] = None) -> int:
    """
    Calculates age in years
    
    Args:
        birth_date: Date of birth
        reference_date: Reference date (default: today)
        
    Returns:
        Age in years
        
    Example:
        >>> birth = datetime(2000, 1, 1)
        >>> ref = datetime(2021, 6, 15)
        >>> age_in_years(birth, ref)
        21
    """
    if reference_date is None:
        reference_date = datetime.now()
    
    age = reference_date.year - birth_date.year
    
    if (reference_date.month, reference_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age


def is_weekend(dt: datetime) -> bool:
    """
    Checks if date is a weekend
    
    Args:
        dt: Datetime object
        
    Returns:
        True if Saturday or Sunday
        
    Example:
        >>> dt = datetime(2021, 1, 2)  # Saturday
        >>> is_weekend(dt)
        True
    """
    return dt.weekday() >= 5  # 5=Saturday, 6=Sunday


def is_weekday(dt: datetime) -> bool:
    """
    Checks if date is a weekday
    
    Args:
        dt: Datetime object
        
    Returns:
        True if Monday-Friday
        
    Example:
        >>> dt = datetime(2021, 1, 4)  # Monday
        >>> is_weekday(dt)
        True
    """
    return dt.weekday() < 5


def day_of_week(dt: datetime) -> str:
    """
    Returns day of week name
    
    Args:
        dt: Datetime object
        
    Returns:
        Day name
        
    Example:
        >>> dt = datetime(2021, 1, 1)  # Friday
        >>> day_of_week(dt)
        'Friday'
    """
    return dt.strftime("%A")


def month_name(dt: datetime) -> str:
    """
    Returns month name
    
    Args:
        dt: Datetime object
        
    Returns:
        Month name
        
    Example:
        >>> dt = datetime(2021, 1, 1)
        >>> month_name(dt)
        'January'
    """
    return dt.strftime("%B")


def time_ago(dt: datetime) -> str:
    """
    Returns human-readable time difference ("5 minutes ago")
    
    Args:
        dt: Past datetime
        
    Returns:
        Human-readable string
        
    Example:
        >>> past = datetime.now() - timedelta(hours=2)
        >>> 'ago' in time_ago(past)
        True
    """
    now = datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return f"{int(seconds)} seconds ago"
    elif seconds < 3600:
        return f"{int(seconds / 60)} minutes ago"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} hours ago"
    elif seconds < 604800:
        return f"{int(seconds / 86400)} days ago"
    elif seconds < 2592000:
        return f"{int(seconds / 604800)} weeks ago"
    elif seconds < 31536000:
        return f"{int(seconds / 2592000)} months ago"
    else:
        return f"{int(seconds / 31536000)} years ago"


# Export all functions
__all__ = [
    'current_timestamp', 'current_datetime',
    'timestamp_to_datetime', 'datetime_to_timestamp',
    'format_datetime', 'parse_datetime',
    'add_days', 'add_hours', 'add_minutes',
    'difference_in_days', 'difference_in_hours', 'difference_in_minutes',
    'is_leap_year', 'days_in_month',
    'start_of_day', 'end_of_day', 'start_of_month', 'end_of_month',
    'age_in_years', 'is_weekend', 'is_weekday',
    'day_of_week', 'month_name', 'time_ago',
]
