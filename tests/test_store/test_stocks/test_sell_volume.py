import datetime
from random import choice, randint
from google.cloud.ndb.exceptions import BadValueError
from pytest import raises
from data_service.config.stocks import currency_symbols
from data_service.store.stocks import SellVolumeModel
from data_service.utils.utils import create_id, today
from tests import test_app, int_positive, int_negative
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
    app = test_app()
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
        # noinspection PyTypeChecker
        sell_volume_instance.sell_value = "abed"
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
    assert sell_volume_instance.sell_ave_price == 0, "sell volume sell ave price is not being set correctly"
    with raises(TypeError):
        # noinspection PyTypeChecker
        sell_volume_instance.sell_volume = "abed"
    with raises(ValueError):
        sell_volume_instance.sell_volume = int_negative()
    with raises(TypeError):
        sell_volume_instance.sell_volume = "0"


def test_sell_volume_sell_market_val_percent():
    """
        test sell market value percent
    """

    # selecting an arbitrary percentage value
    # This test will sometimes fail
    sell_percent: int = randint(1, 100)
    assert (sell_volume_instance.sell_market_val_percent, int), "sell volume percent instance is not valid"
    assert sell_volume_instance.sell_market_val_percent == 0, "Sell volume percent default not valid"
    sell_volume_instance.sell_market_val_percent = sell_percent
    assert sell_volume_instance.sell_market_val_percent == sell_percent, "sell Volume sell market percent is not " \
                                                                         "set correctly"
    sell_volume_instance.sell_market_val_percent = 0
    assert sell_volume_instance.sell_market_val_percent == 0,  "sell Volume sell market percent is not set correctly"
    with raises(TypeError):
        sell_volume_instance.sell_market_val_percent = "abed"
    with raises(ValueError):
        # insuring the test succeed by substracting 150
        sell_volume_instance.sell_market_val_percent = sell_percent + 150
    with raises(ValueError):
        # insuring the test succeed by substracting 150
        sell_volume_instance.sell_market_val_percent = sell_percent - 150


def test_sell_volume_trade_account():
    """

    """
    temp_trade_account: int = int_positive()
    assert isinstance(sell_volume_instance.sell_trade_count, int), "sell volume instance initialized incorrectly"
    assert sell_volume_instance.sell_trade_count == 0, "sell volume instance initialized incorrectly"
    sell_volume_instance.sell_trade_count = temp_trade_account
    assert sell_volume_instance.sell_trade_count == temp_trade_account, "sell volume trade account not set correctly"
    sell_volume_instance.sell_trade_count = 0
    assert sell_volume_instance.sell_trade_count == 0, "sell volume trade account not set correctly"
    with raises(TypeError):
        sell_volume_instance.sell_volume = "abed"
    with raises(TypeError):
        sell_volume_instance.sell_volume = "0"
    with raises(ValueError):
        sell_volume_instance.sell_volume = int_negative()

def set_sell_volume_mock(sell_volume: SellVolumeModel) ->  SellVolumeModel:
    sell_volume.transaction_id = "abcde"
    sell_volume.currency = choice(currency_symbols())
    sell_volume.stock_id = "abdfgt"
    sell_volume.date_created = today()
    sell_volume.sell_volume = 100
    sell_volume.sell_value = 100
    sell_volume.sell_ave_price = 100
    return sell_volume


def test_sell_volume_test_dunder_methods():
    first_sell_volume: SellVolumeModel = set_sell_volume_mock(sell_volume=sell_volume_instance)
    second_sell_volume: SellVolumeModel = set_sell_volume_mock(sell_volume=sell_volume_instance)
    assert first_sell_volume == second_sell_volume, "__eq__ method not function correctly"
