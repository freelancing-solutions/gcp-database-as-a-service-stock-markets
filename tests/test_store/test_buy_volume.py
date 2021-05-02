import datetime
from google.cloud.ndb.exceptions import BadValueError
from pytest import raises
from data_service.store.stocks import BuyVolumeModel
from data_service.utils.utils import create_id, today
from .. import app

buy_volume_instance: BuyVolumeModel = BuyVolumeModel()

def test_buy_volume_instance():
    assert isinstance(buy_volume_instance, BuyVolumeModel), "buy volume not instantiating correctly"


def test_transaction_id():
    assert buy_volume_instance.transaction_id is not None, "Buy volume transaction_id initial value invalid"
    assert isinstance(buy_volume_instance.transaction_id, str), "Buy volume default value is a wrong type"

    with raises(BadValueError):
        buy_volume_instance.transaction_id = 0


def test_stock_id():
    assert buy_volume_instance.stock_id is None, "Buy volume stock_id initial value invalid"
    stock_id = create_id()
    buy_volume_instance.stock_id = stock_id
    assert buy_volume_instance.stock_id == stock_id, "Buy_volume stock_id is not being set correctly"

    with raises(TypeError):
        buy_volume_instance.stock_id = 25

    with raises(ValueError):
        buy_volume_instance.stock_id = ""

def test_date_created():
    message: str = "Buy_volume date_created is not being set correctly"
    buy_volume_instance.date_created = today()
    assert isinstance(buy_volume_instance.date_created, datetime.date), message
    with raises(TypeError):
        buy_volume_instance.date_created = "this is not a date"
    assert buy_volume_instance.date_created != "this is not a date"


def test_currency():

    with app.app_context():
        def_currency: str = app.config.get("CURRENCY")
        assert buy_volume_instance.currency == def_currency, "Buy Volume currency initial value invalid"
        buy_volume_instance.currency = "USD"
        assert buy_volume_instance.currency == "USD", "Currency is not being set correctly"
        with raises(TypeError):
            buy_volume_instance.currency = "XXX"
        assert buy_volume_instance.currency != "XXX", "False Currency Symbols are being accepted"

def test_buy_volume():
    assert buy_volume_instance.buy_volume == 0, "Buy Volume initial volume is invalid"
    buy_volume_instance.buy_volume = 1000
    assert buy_volume_instance.buy_volume == 1000, "Buy volume not being set correctly"
    with raises(ValueError):
        buy_volume_instance.buy_volume = -1000
    assert buy_volume_instance.buy_volume != -1000, "Buy volume not being set correctly"

def test_buy_value():
    assert buy_volume_instance.buy_value == 0, "Buy_volume buy value defaul invalid"
    buy_volume_instance.buy_value = 1000
    assert buy_volume_instance.buy_value == 1000, "Buy_volume buy_value is not being set correctly"
    with raises(TypeError):
        buy_volume_instance.buy_value = "12"
    with raises(ValueError):
        buy_volume_instance.buy_value = ""
    with raises(ValueError):
        buy_volume_instance.buy_value = -1000

def test_buy_ave_price():
    assert buy_volume_instance.buy_ave_price == 0, "Buy_volume default not being set"
    buy_volume_instance.buy_volume = 100
    assert buy_volume_instance.buy_volume == 100, "Buy Volumen is not being set correctly"
    with raises(TypeError):
        buy_volume_instance.buy_volume = "ABC"
    with raises(ValueError):
        buy_volume_instance.buy_volume = -1


def test_buy_market_val_percent():
    assert buy_volume_instance.buy_market_val_percent == 0, "Buy_volume default not being set correctly"
    buy_volume_instance.buy_market_val_percent = 100
    assert buy_volume_instance.buy_market_val_percent == 100, "Buy_volume buy market is not being set correctly"
    with raises(TypeError):
        buy_volume_instance.buy_market_val_percent = "ABC"
    with raises(ValueError):
        buy_volume_instance.buy_market_val_percent = -10


def buy_trade_count():
    assert buy_volume_instance.buy_trade_count == 0, "Buy_volume default not being set correctly"
    buy_volume_instance.buy_trade_count = 100
    assert buy_volume_instance.buy_trade_count == 100, "Buy_volume trade account is not being set correctly"
    with raises(TypeError):
        buy_volume_instance.buy_trade_count = "ABC"
    with raises(ValueError):
        buy_volume_instance.buy_trade_count = -10
