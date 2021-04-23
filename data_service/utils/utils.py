import os, random, string, time, datetime
from datetime import datetime, date
import typing

char_set = string.ascii_lowercase + string.digits


def is_development() -> bool:
    return True if os.environ['SERVER_SOFTWARE'].lower().startswith('development') else False


def create_id(size: int = 64, chars: str = char_set) -> str: return ''.join(random.choice(chars) for x in range(size))


def timestamp() -> int: return int(float(time.time()) * 1000)


def timestamp_difference(stamp1, stamp2) -> int: return int(stamp1 - stamp2)


def date_string_to_date(date_str: str) -> date:
    """
        date form dd/mm/yyyy
    """
    if isinstance(date_str, str):
        if "/" in date_str:
            date_list: typing.List[str] = date_str.split("/")
        elif "-" in date_str:
            date_list: typing.List[str] = date_str.split("-")
        else:
            raise ValueError('Date format invalid')
        try:
            year: int = int(date_list[2])
            month: int = int(date_list[1])
            day: int = int(date_list[0])
        except KeyError:
            raise ValueError("Date Format invalid")

        if 0 < month > 12:
            raise ValueError("Date Format Invalid")

        if 0 < day > 31:
            raise ValueError("Date Format invalid")

        if year < 1990:
            raise ValueError("Date Format invalid")

        return date(year=year, month=month, day=day)

    elif isinstance(date_str, date):
        return date_str
    else:
        raise ValueError('Date format invalid')


# cache functions

def end_of_month() -> bool:
    now: date = datetime.now().date()
    if now.day in [30, 31, 1]:
        return True
    return False

def return_ttl(name) -> int:
    cache_ttl_short: int = 60 * 60 * 3  # 3 hours
    cache_ttl_medium: int = 60 * 60 * 6  # 6 hours
    cache_ttl_long: int = 60 * 60 * 12  # 24 hours

    if name == "long":
        return cache_ttl_long
    elif name == "short":
        return cache_ttl_short
    elif name == "medium":
        return cache_ttl_medium
    return cache_ttl_short
