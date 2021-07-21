import functools
from flask import jsonify
from google.api_core.exceptions import Aborted, RetryError
from google.cloud.ndb.exceptions import BadRequestError, BadQueryError
from data_service.config.exceptions import InputError, RequestError, DataServiceError


def handle_view_errors(func):
    """
        view error handler wrapper
    #     TODO - raise user related errors here
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            message: str = str(e)
            # IF debug please print debug messages
            # raise InputError(description='Bad input values, please check your input')
            return({'status': False, 'message': message}), 500
        except TypeError as e:
            message: str = str(e)
            raise InputError(description='Bad input values, please check your input')
        except BadRequestError as e:
            message: str = str(e)
            raise RequestError(description='Bad request while connecting to database')
        except BadQueryError as e:
            message: str = str(e)
            raise DataServiceError(description="Error creating database query please check your input")
        except ConnectionRefusedError as e:
            message: str = str(e)
            raise RequestError(description="database server is refusing connection please try again later")
        except RetryError as e:
            message: str = str(e)
            raise RequestError(description="database server is refusing connection please try again later")
        except Aborted as e:
            message: str = str(e.message or e)
            raise RequestError(description="database server is refusing connection please try again later")

    return wrapper


def handle_store_errors(func):
    """
        handle errors related to GCP datastore
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

    return wrapper
