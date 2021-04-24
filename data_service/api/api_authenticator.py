import functools
from flask import request

def handle_auth(func):
    functools.wraps(func)

    def wrapper(*args, **kwargs):
        # TODO - add JWT based authentication
        request_headers = request.headers.copy()

        return func(*args, **kwargs)

    return wrapper