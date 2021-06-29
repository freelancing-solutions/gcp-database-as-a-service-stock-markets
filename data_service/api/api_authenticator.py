import functools
import os
from flask import request
from werkzeug.exceptions import Unauthorized
from data_service.utils.utils import is_development
from functools import lru_cache


def project_valid(project_name: str) -> bool:
    authorized_projects = os.environ.get('AUTH_PROJECTS').split(",")
    if not(isinstance(project_name, str)):
        return False
    if project_name in authorized_projects:
        return True
    return False


def request_url_valid(url: str) -> bool:
    authorized_urls = os.environ.get('AUTH_URLS').split(",")
    if not(isinstance(url, str)):
        return False
    if is_development():
        return True
    if url in authorized_urls:
        return True
    return False


@lru_cache(maxsize=1025)
def handle_auth(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        is_cron = request.headers.get('X-Appengine-Cron')
        if is_cron is True:
            return func(*args, **kwargs)
            # this is a cron job authorize
        project_name = request.headers.get('X-PROJECT-NAME')

        if not(project_valid(project_name=project_name)):
            message: str = 'You are not authorized to use this resources'
            raise Unauthorized(message)

        secret_token = request.headers.get('x-auth-token')
        if secret_token is None:
            message: str = 'You are not authorized to use this resources'
            raise Unauthorized(message)
            # request not authorized reject
        if secret_token == os.environ.get('SECRET'):
            return func(*args, **kwargs)
        else:
            message: str = 'You are not authorized to use this resources'
            raise Unauthorized(message)

    return auth_wrapper
