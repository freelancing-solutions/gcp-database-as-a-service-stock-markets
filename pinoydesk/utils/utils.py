import os, random, string, time
char_set = string.ascii_lowercase + string.digits


def is_development() -> bool:
    return True if os.environ['SERVER_SOFTWARE'].lower().startswith('development') else False


def create_id(size: int = 64, chars: str = char_set) -> str: return ''.join(random.choice(chars) for x in range(size))


def timestamp() -> int: return int(float(time.time()) * 1000)


def timestamp_difference(stamp1, stamp2) -> int: return int(stamp1 - stamp2)




