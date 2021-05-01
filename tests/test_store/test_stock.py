from google.cloud import ndb
from data_service.store.stocks import Stock
from data_service.utils.utils import create_id

stock_instance: Stock = Stock()


def test_stock_instance():
    assert isinstance(stock_instance, Stock), "Stock not properly initialized"


def test_stock_id():
    stock_instance.stock_id = create_id()
    

def test_stock_code():
    pass

def test_stock_name():
    pass

def test_stock_symbol():
    pass

