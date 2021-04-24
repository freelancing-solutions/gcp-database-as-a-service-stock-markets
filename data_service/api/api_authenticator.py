import functools
import os
from flask import request
from werkzeug.exceptions import Unauthorized

def project_valid(project_name: str) -> bool:
    authorized_projects = os.getenv('AUTH_PROJECTS')
    if not isinstance(project_name, str):
        return False

    if project_name in authorized_projects:
        return True
    return False

def request_url_valid(url: str) -> bool:
    authorized_urls = os.getenv('AUTH_URLS')
    if not isinstance(url, str):
        return False

    if url in authorized_urls:
        return True
    return False

def handle_auth(func):
    @functools.wraps(func)
    def auth_wrapper(*args, **kwargs):
        is_cron = request.headers.get('X-Appengine-Cron')
        if is_cron is True:
            return func(*args, **kwargs)
            # this is a cron job authorize

        project_name = request.headers.get('X-PROJECT-NAME')

        if not project_valid(project_name=project_name):
            message: str = 'You are not authorized to use this resources'
            raise Unauthorized(message)

        if not request_url_valid(url=request.url):
            message: str = 'You are not authorized to use this resources'
            raise Unauthorized(message)

        secret_token = request.headers.get('x-auth-token')
        if secret_token is None:
            message: str = 'You are not authorized to use this resources'
            raise Unauthorized(message)
            # request not authorized reject
        if secret_token == os.getenv('SECRET'):

            return func(*args, **kwargs)
        else:
            message: str = 'You are not authorized to use this resources'
            raise Unauthorized(message)

    return auth_wrapper