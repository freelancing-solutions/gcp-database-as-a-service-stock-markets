from datetime import datetime
from random import choice

from pytest import raises

from data_service.config.stocks import currency_symbols
from data_service.store.mixins import AmountMixin
from data_service.utils.utils import create_id
from data_service.store.affiliates import AffiliateTransactionItems
from tests import int_positive

transaction_item_instance: AffiliateTransactionItems() = AffiliateTransactionItems()

def test_transaction_id():
    transaction_id: str = create_id()
    assert transaction_item_instance.transaction_id is None, "Transaction Id is not set correctly"
    transaction_item_instance.transaction_id = transaction_id
    assert transaction_item_instance.transaction_id == transaction_id, "transaction id is not being set correclty"
    with raises(TypeError):
        transaction_item_instance.transaction_id = 0
    with raises(ValueError):
        transaction_item_instance.transaction_id = ""

def test_amount():
    amount_instance: AmountMixin = AmountMixin()
    amount: int = int_positive()
    currency: str = choice(currency_symbols())
    assert transaction_item_instance.amount is None, "Amount default is not being set correctly"
    amount_instance.amount = amount
    amount_instance.currency = currency
    assert amount_instance.amount == amount, "amount is not being set correctly"
    assert amount_instance.currency == currency, "currency symbol is not being set correctly"
    transaction_item_instance.amount = amount_instance
    assert transaction_item_instance.amount == amount_instance, "amount instance is not being set correctly"
    with raises(TypeError):
        transaction_item_instance.amount = 0

def test_transaction_date():
    transaction_date: datetime = datetime.now()
    assert transaction_item_instance.transaction_date is None, "transaction_date default is not being set correctly"
    transaction_item_instance.transaction_date = transaction_date
    assert transaction_item_instance.transaction_date == transaction_date, "transaction_date is not being set correctly"
    with raises(TypeError):
        transaction_item_instance.transaction_date = 0

