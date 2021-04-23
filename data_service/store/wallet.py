import typing

from google.api_core.exceptions import RetryError
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError
from werkzeug.security import generate_password_hash
from data_service.utils.utils import timestamp


class WalletModel(ndb.Model):
    pass

