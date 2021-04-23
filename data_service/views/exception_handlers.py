import functools

from flask import jsonify
from google.api_core.exceptions import Aborted
from google.cloud.ndb.exceptions import BadRequestError, BadQueryError
from requests.exceptions import RetryError


def handle_ndb_errors(func):
    functools.wraps(func)

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            message: str = str(e)
            return jsonify({'status': False, 'message': message}), 500
        except TypeError as e:
            message: str = str(e)
            return jsonify({'status': False, 'message': message}), 500
        except BadRequestError as e:
            message: str = str(e)
            return jsonify({'status': False, 'message': message}), 500
        except BadQueryError as e:
            message: str = str(e)
            return jsonify({'status': False, 'message': message}), 500
        except ConnectionRefusedError as e:
            message: str = str(e)
            return jsonify({'status': False, 'message': message}), 500
        except RetryError as e:
            message: str = str(e.message or e)
            return jsonify({'status': False, 'message': message}), 500
        except Aborted as e:
            message: str = str(e.message or e)
            return jsonify({'status': False, 'message': message}), 500

    return wrapper