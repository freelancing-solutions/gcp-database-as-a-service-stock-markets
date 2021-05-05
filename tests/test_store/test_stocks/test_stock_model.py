from data_service.store.stocks import StockModel
from data_service.store.stocks import Stock, Broker
from data_service.utils.utils import create_id
from pytest import raises
stock_model_instance: StockModel = StockModel()
stock_instance: Stock = Stock()
broker_instance: Broker = Broker()
# TODO add mocks for ndb.put calls

def test_stock_model_instance():
    assert isinstance(stock_model_instance, StockModel), "stock model instance not instatiating correctly"
    assert isinstance(stock_instance, Stock), "Stock not instantiating correctly"
    assert isinstance(broker_instance, Broker), "Broker not instanting correctly"
    with raises(TypeError):
        stock_model_instance.stock = "sds"
    with raises(TypeError):
        stock_model_instance.broker = "sds"
    with raises(TypeError):
        stock_model_instance.transaction_id = 2
    with raises(ValueError):
        stock_model_instance.transaction_id = str()
    with raises(ValueError):
        stock_model_instance.transaction_id = ""


def test_exchanged_id():
    assert stock_model_instance.exchange_id is None, "Exchange ID Initial value invalid"
    e_id: str = create_id()
    stock_model_instance.exchange_id = e_id
    assert stock_model_instance.exchange_id == e_id, "exchange id not being set correctly"
    with raises(TypeError):
        stock_model_instance.exchange_id = 3
    with raises(ValueError):
        stock_model_instance.exchange_id = str()
    with raises(ValueError):
        stock_model_instance.exchange_id = ""

def test_transaction_id():
    assert stock_model_instance.transaction_id is None, "transaction id initial value invalid"
    t_id: str = create_id()
    stock_model_instance.transaction_id = t_id
    assert stock_model_instance.transaction_id == t_id, "transaction id not being set correctly"
    with raises(TypeError):
        stock_model_instance.transaction_id = -56
    with raises(ValueError):
        stock_model_instance.transaction_id = ""
    with raises(ValueError):
        stock_model_instance.transaction_id = str()

def test_stock_instance():
    assert stock_model_instance.stock is None, "stock model instance initial instance incorrect"
    stock_model_instance.stock = stock_instance
    assert isinstance(stock_model_instance.stock, Stock), "Stock model not setting stock correctly"
    with raises(TypeError):
        # noinspection PyTypeChecker
        stock_model_instance.stock = "ABCD"
    with raises(TypeError):
        stock_model_instance.stock = str()


def test_broker_instance():
    assert stock_model_instance.broker is None, "Broker model instance initial value invalid"
    stock_model_instance.broker = broker_instance
    assert isinstance(stock_model_instance.broker, Broker), "Broker Model instance not being set correctly"
    with raises(TypeError):
        stock_model_instance.broker = ""
    with raises(TypeError):
        stock_model_instance.broker = {}

