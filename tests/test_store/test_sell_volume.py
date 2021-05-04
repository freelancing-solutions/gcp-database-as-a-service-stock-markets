import datetime
from google.cloud.ndb.exceptions import BadValueError
from pytest import raises
from data_service.store.stocks import SellVolumeModel
from data_service.utils.utils import create_id, today
from .. import app

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
        sell_volume_instance.date_created = 123
    with raises(BadValueError):
        sell_volume_instance.date_created = {}
