import datetime
from random import choice

from google.cloud.ndb.exceptions import BadValueError
from pytest import raises

from data_service.config.stocks import currency_symbols
from data_service.store.stocks import SellVolumeModel
from data_service.utils.utils import create_id, today
from .. import app, int_positive, int_negative

sell_volume_instance: SellVolumeModel = SellVolumeModel()

def test_sell_sell_volume_instance():
    assert isinstance(sell_volume_instance, SellVolumeModel), "sell_volume_instance deploying correctly"

def test_sell_volume_transaction_id():
    temp_id: str = create_id()
    assert sell_volume_instance.transaction_id is None, "Sell Volume transaction id initial value is invalid"
    sell_volume_instance.transaction_id = temp_id
    assert sell_volume_instance.transaction_id == temp_id, "Sell volume transaction id not being set correctly"

    with raises(TypeError):
        sell_volume_instance.transaction_id = 0
    with raises(ValueError):
        sell_volume_instance.transaction_id = ""
    with raises(TypeError):
        sell_volume_instance.transaction_id = {}

def test_sell_volume_stock_id():
    temp_stock_id: str = create_id()
    assert sell_volume_instance.stock_id is None, "Sell Volume stock id initial value is invalid"
    sell_volume_instance.stock_id = temp_stock_id
    assert sell_volume_instance.stock_id == temp_stock_id, "Sell Volume stock id not being set correctly"
    with raises(TypeError):
        sell_volume_instance.stock_id = 0
    with raises(ValueError):
        sell_volume_instance.stock_id = ""
    with raises(TypeError):
        sell_volume_instance.transaction_id = {}

def test_sell_volume_date_created():
    t_date: datetime.date = today()
    assert sell_volume_instance.date_created is None, "Sell volume date_created initial value is invalid"
    sell_volume_instance.date_created = t_date
    assert sell_volume_instance.date_created == t_date, "Sell volume date_created is not being set correctly"
    with raises(BadValueError):
        sell_volume_instance.date_created = int_positive()
    with raises(BadValueError):
        sell_volume_instance.date_created = {}

def test_sell_volume_currency():
    """
        test if i can store any valid currency
    """
    t_currency: str = choice(currency_symbols())
    with app.app_context():
        assert sell_volume_instance.currency == app.config.get("CURRENCY"), "Sell Volume currency initial value invalid"
        sell_volume_instance.currency = t_currency
        assert sell_volume_instance.currency == t_currency, "Sell Volume currency is not being set correctly"
        with raises(TypeError):
            sell_volume_instance.currency = int_positive()


def test_sell_volume_sell_volume():
    """
        test if the initial value is integer
        test if the initial value is zero
        test if i can set any value greater than 0
        test if i can store a zero
        test if storing negative numbers will fail
        test if storing anything else other than a number will fail
    """

    sell_volume: int = int_positive()
    assert isinstance(sell_volume_instance.sell_volume, int), "Sell volume instance should be integer"
    assert sell_volume_instance.sell_volume == 0, "sell Volume default value set incorrectly"
    sell_volume_instance.sell_volume = sell_volume
    assert sell_volume_instance.sell_volume == sell_volume, "Sell Volume instance not being set correctly"
    sell_volume_instance.sell_volume = 0
    assert sell_volume_instance.sell_volume == 0, "Sell volument instance not being set correctly"
    with raises(ValueError):
        sell_volume_instance.sell_volume = int_negative()
    with raises(TypeError):
        sell_volume_instance.sell_value = str(int_positive())
    with raises(TypeError):
        sell_volume_instance.sell_volume = "abcd"

def test_sell_volume_sell_value():
    """
        test if the initial value is integer
        test if the initial value is zero
        test if i can set any value greater than 0
        test if i can store a zero
        test if storing negative numbers will fail
        test if storing anything else other than a number will fail
    """

    temp_sell_value: int = int_positive()
    assert isinstance(sell_volume_instance.sell_value, int), "Sell Volume sell value can only be an integer"
    assert sell_volume_instance.sell_value == 0, "Sell Volume sell value default invalid"
    sell_volume_instance.sell_value = temp_sell_value
    assert sell_volume_instance.sell_value == temp_sell_value, "Sell Volume sell value not being set correctly"
    sell_volume_instance.sell_value = 0
    assert sell_volume_instance.sell_value == 0, "Sell volume sell value not being set correctly"
    with raises(ValueError):
        sell_volume_instance.sell_value = int_negative()
    with raises(TypeError):
        sell_volume_instance.sell_value = "abcd"
    with raises(TypeError):
        sell_volume_instance.sell_value = "0"

def test_sell_volume_sell_ave_price():
    """
        test if the initial value is integer
        test if the initial value is zero
        test if i can set any value greater than 0
        test if i can store a zero
        test if storing negative numbers will fail
        test if storing anything else other than a number will fail
    """
    ave_price: int = int_positive()
    assert (sell_volume_instance.sell_volume, int), "sell volume instance not an integer"
    assert sell_volume_instance.sell_ave_price == 0, "sell volume sell value default invalid"
    sell_volume_instance.sell_ave_price = ave_price
    assert sell_volume_instance.sell_ave_price == ave_price, "sell volume sell value is not being set correctly"
    sell_volume_instance.sell_ave_price = 0



