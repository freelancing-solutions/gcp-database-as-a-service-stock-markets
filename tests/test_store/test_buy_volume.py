import datetime

from flask import current_app

from data_service.store.stocks import BuyVolumeModel
from data_service.utils.utils import create_id, today
from .. import app

buy_volume_instance: BuyVolumeModel = BuyVolumeModel()

def test_buy_volume_instance():
    assert isinstance(buy_volume_instance, BuyVolumeModel), "buy volume not instantiating correctly"


def test_transaction_id():
    assert buy_volume_instance.transaction_id is not None, "Buy volume transaction_id initial value invalid"
    assert isinstance(buy_volume_instance.transaction_id, str), "Buy volume default value is a wrong type"

def test_stock_id():
    assert buy_volume_instance.stock_id is None, "Buy volume stock_id initial value invalid"
    stock_id = create_id()
    buy_volume_instance.stock_id = stock_id
    assert buy_volume_instance.stock_id == stock_id, "Buy_volume stock_id is not being set correctly"


def test_date_created():
    message: str = "Buy_volume date_created is not being set correctly"
    buy_volume_instance.date_created = today()
    assert isinstance(buy_volume_instance.date_created, datetime.date), message

def test_currency():

    with app.app_context():
        def_currency: str = app.config.get("CURRENCY")
        assert buy_volume_instance.currency == def_currency, "Buy Volume currency initial value invalid"
        buy_volume_instance.currency = "USD"
        assert buy_volume_instance.currency == "USD", "Currency is not being set correctly"

def test_buy_volume():
    assert buy_volume_instance.buy_volume == 0, "Buy Volume initial volume is invalid"
    buy_volume_instance.buy_volume = 1000
    assert buy_volume_instance.buy_volume == 1000, "Buy volume not being set correctly"

    assert buy_volume_instance.buy_volume != -1000, "Buy volume not being set correctly"

def test_buy_value():
    pass

def test_buy_ave_price():
    pass

def test_buy_market_val_percent():
    pass

def buy_trade_count():
    pass
