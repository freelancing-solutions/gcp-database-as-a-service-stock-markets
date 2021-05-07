import functools
from flask import current_app
from data_service.main import create_app
from data_service.config import Config
from google.cloud import ndb
import os
credential_path = "C:\\gcp_credentials\\pinoydesk.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def use_context(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        if not current_app:
            app = create_app(config_class=Config)
            app.app_context().push()
        else:
            app = current_app

        client = ndb.Client(namespace="main", project=app.config.get('PROJECT'))
        # TODO - setup everything related to cache policy and all else here

        with client.context():
            return func(*args, **kwargs)

    return wrapper
