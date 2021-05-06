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

coupon_instance: Coupons = Coupons()
def test_code():
    code: str = create_id()
    assert coupon_instance.code is None, "coupon code not initialized properly"
    coupon_instance.code = code
    assert coupon_instance.code == code, "coupon code not set properly"

    with raises(TypeError):
        coupon_instance.code = 0


def test_discount():
    discount: AmountMixin = AmountMixin(amount=int_positive(), currency=choice(currency_symbols()))
    assert coupon_instance.discount is None, "coupon discount not initialized properly"
    coupon_instance.discount = discount
    assert coupon_instance.discount == discount, "coupon discount not set properly"
    with raises(BadValueError):
        coupon_instance.discount = 0
    with raises(BadValueError):
        coupon_instance.discount = "0"

def test_is_valid():
    is_valid: bool = False
    assert coupon_instance.is_valid, "coupon is_valid not initialized properly"
    coupon_instance.is_valid = is_valid
    assert coupon_instance.is_valid == is_valid, "coupon is_valid not set properly"
    is_valid = True
    coupon_instance.is_valid = is_valid
    assert coupon_instance.is_valid == is_valid, "coupon is_valid not set properly"
    with raises(TypeError):
        coupon_instance.is_valid = 0


def test_date_created():
    pass

def test_expiration_date():
    pass

