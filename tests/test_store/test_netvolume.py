import datetime
from random import choice

from data_service.config.stocks import currency_symbols
from pytest import raises
from data_service.store.stocks import NetVolumeModel
from data_service.utils.utils import create_id, today
from .. import app, int_positive, int_negative

net_volume_instance: NetVolumeModel = NetVolumeModel()

def test_net_volume_instance():
    assert isinstance(net_volume_instance, NetVolumeModel), "net volume instance is instantiated incorrectly"

def test_net_volume_transaction_id():
    temp_t_id: str = create_id()
    assert net_volume_instance.transaction_id is None, "net volume transaction not initialized correctly"
    net_volume_instance.transaction_id = temp_t_id
    assert net_volume_instance.transaction_id == temp_t_id, "net volume transaction_id not set correctly"
    with raises(TypeError):
        net_volume_instance.transaction_id = int_positive()
    with raises(ValueError):
        net_volume_instance.transaction_id = str()


def test_net_volume_stock_id():
    stock_id: str = create_id()
    assert net_volume_instance.stock_id is None, "net volume stock_id not initialized correctly"
    net_volume_instance.stock_id = stock_id
    assert net_volume_instance.stock_id == stock_id, "net volume stock_id not set correctly"
    with raises(TypeError):
        net_volume_instance.stock_id = int_negative()
    with raises(ValueError):
        net_volume_instance.stock_id = ""
    with raises(ValueError):
        net_volume_instance.stock_id = str()

def test_net_volume_date_created():
    date_created: datetime.date = today()
    assert net_volume_instance.date_created is None, "net volume date_created not initialized"
    net_volume_instance.date_created = date_created
    assert net_volume_instance.date_created == date_created, "net volume date_created not being set correctly"
    with raises(TypeError):
        net_volume_instance.date_created = 0
    with raises(TypeError):
        net_volume_instance.date_created = {}


def test_net_volume_currency():
    currency: str = choice(currency_symbols())
    with app.app_context():
        assert net_volume_instance.currency is app.config.get('CURRENCY'), "net volume currency has not initialized correctly"
        net_volume_instance.currency = currency
        assert net_volume_instance.currency == currency, "net volume currency is not being set correctly"
        with raises(TypeError):
            net_volume_instance.currency = "A"


def test_net_volume_net_volume():
    net_volume: int = int_positive()
    assert isinstance(net_volume_instance.net_volume, int), "net volume default is not set correctly"
    assert net_volume_instance.net_volume == 0, "net volume default is not set correctly"
    net_volume_instance.net_volume = net_volume
