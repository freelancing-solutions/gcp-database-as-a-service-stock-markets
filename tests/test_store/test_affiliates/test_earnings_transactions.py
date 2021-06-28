from datetime import datetime
from random import choice

from google.cloud.ndb.exceptions import BadValueError
from pytest import raises
from data_service.config.stocks import currency_symbols
from data_service.store.mixins import AmountMixin
from data_service.utils.utils import create_id
from data_service.store.affiliates import AffiliateEarningsTransactions
from tests import int_positive

earnings_transactions_instance: AffiliateEarningsTransactions = AffiliateEarningsTransactions()


def test_transaction_id():
    """"""
    affiliate_id: str = create_id()
    assert earnings_transactions_instance.affiliate_id is None, "earning transaction affiliate_id  not set properly"
    earnings_transactions_instance.affiliate_id = affiliate_id
    assert earnings_transactions_instance.affiliate_id == affiliate_id, "earnings transaction affiliate id not " \
                                                                        "set properly"
    with raises(TypeError):
        earnings_transactions_instance.affiliate_id = 0
    with raises(ValueError):
        earnings_transactions_instance.affiliate_id = ""


def test_total_earned():
    total_earned: AmountMixin = AmountMixin()
    symbol: str = choice(currency_symbols())
    amount: int = int_positive()
    assert earnings_transactions_instance.total_earned is None, "Total earned has not been initialized correctly"
    total_earned.amount = amount
    total_earned.currency = symbol
    assert total_earned.amount == amount, "Total earned amount not being set correctly"
    assert total_earned.currency == symbol, "Total Earned Currency Symbol not being set correctly"
    earnings_transactions_instance.total_earned = total_earned
    assert earnings_transactions_instance.total_earned == total_earned, "Total earned is not be set properly"
    with raises(BadValueError):
        earnings_transactions_instance.total_earned = 0


def test_last_transaction_time():
    last_transaction_time: datetime = datetime.now()
    assert earnings_transactions_instance.last_transaction_time is None, "Last transaction time is not correctly set"
    earnings_transactions_instance.last_transaction_time = last_transaction_time
    assert earnings_transactions_instance.last_transaction_time == last_transaction_time
    with raises(TypeError):
        earnings_transactions_instance.last_transaction_time = 0

    with raises(TypeError):
        earnings_transactions_instance.last_transaction_time = ""
