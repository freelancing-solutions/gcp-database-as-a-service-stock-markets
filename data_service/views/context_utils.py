import functools
from flask import current_app
from google.cloud import ndb

def use_context(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        client = ndb.Client(namespace="main", project=current_app.config.get('PROJECT'))
        # TODO - setup everything related to cache policy and all else here
        context = client.context()
        with context:
            return func(*args, **kwargs)

    return wrapper
