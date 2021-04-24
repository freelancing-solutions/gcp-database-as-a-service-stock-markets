import functools
import os
from flask import request
from data_service.config.exceptions import UnAuthenticatedError

def handle_auth(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        request_headers = request.headers.copy()
        is_cron = request_headers.get('X-Appengine-Cron')
        if is_cron:
            return func(*args, **kwargs)
            # this is a cron job authorize
        secret_token = request_headers.get('x-auth-token')
        if secret_token is None:
            message: str = 'You are not authorized to use this resources'
            raise UnAuthenticatedError(message)
            # request not authorized reject
        if secret_token == os.environ.get('SECRET'):
            return func(*args, **kwargs)
        else:
            message: str = 'You are not authorized to use this resources'
            raise UnAuthenticatedError(message)

    return auth_wrapper