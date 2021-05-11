import typing
from datetime import datetime
from random import randint

from google.cloud import ndb

from data_service.views.stocks import StockView
from data_service.store.stocks import Stock
from data_service.utils.utils import create_id
from .. import test_app
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker

