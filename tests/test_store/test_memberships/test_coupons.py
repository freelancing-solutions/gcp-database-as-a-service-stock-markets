from datetime import datetime
from datetime import date as date_class
from random import choice
from google.cloud.ndb.exceptions import BadValueError
from pytest import raises

from data_service.config.stocks import currency_symbols
from data_service.store.mixins import AmountMixin
from data_service.utils.utils import create_id, datetime_now, today
from tests import int_positive, int_negative
from data_service.store.memberships import Coupons

def test_code():
    pass

def test_discount():
    pass

def test_is_valid():
    pass

def test_date_created():
    pass

def test_expiration_date():
    pass

