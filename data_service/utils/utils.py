import os, random, string, time, datetime

import typing

char_set = string.ascii_lowercase + string.digits


def is_development() -> bool:
    return True if os.environ['SERVER_SOFTWARE'].lower().startswith('development') else False


def create_id(size: int = 64, chars: str = char_set) -> str: return ''.join(random.choice(chars) for x in range(size))


def timestamp() -> int: return int(float(time.time()) * 1000)


def timestamp_difference(stamp1, stamp2) -> int: return int(stamp1 - stamp2)


def date_string_to_date(date: str) -> object:
    if isinstance(date, str):
        if "/" in date:
            date_list: typing.List[str] = date.split("/")
        elif "-" in date:
            date_list: typing.List[str] = date.split("-")
        else:
            raise ValueError('Date format invalid')
        try:
            year: int = int(date_list[2])
            month: int = int(date_list[1])
            day: int = int(date_list[0])
        except KeyError as e:
            raise ValueError("Date Format invalid")

        if 0 < month > 12:
            raise ValueError("Date Format Invalid")

        if 0 < day > 31:
            raise ValueError("Date Format invalid")

        if 2000 < year > datetime.datetime.now().year:
            raise ValueError("Date Format invalid")

        return datetime.date(year=year, month=month, day=day)

    elif isinstance(date, object):
        return date

    else:
        raise ValueError('Date format invalid')



