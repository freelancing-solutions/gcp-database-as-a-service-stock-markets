from datetime import datetime
from pytest import raises
from data_service.utils.utils import create_id, today, datetime_now
from data_service.store.affiliates import AffiliateEarningsTransactions
from tests import int_positive, int_negative

earnings_transactions_instance: AffiliateEarningsTransactions = AffiliateEarningsTransactions()

def test_transaction_id():
    """"""
    affiliate_id: str = create_id()
    assert earnings_transactions_instance.affiliate_id is None, "earning transaction affiliate_id  not set properly"
    earnings_transactions_instance.affiliate_id = affiliate_id
    assert earnings_transactions_instance.affiliate_id == affiliate_id, "earnings transaction affiliate id not set properly"
    with raises(TypeError):
        earnings_transactions_instance.affiliate_id = 0
    with raises(ValueError):
        earnings_transactions_instance.affiliate_id = ""


def test_amount():
    pass

def test_transaction_date():
    pass

