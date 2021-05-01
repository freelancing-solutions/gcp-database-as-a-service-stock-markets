from google.cloud import ndb
from data_service.store.stocks import Stock
from data_service.utils.utils import create_id

stock_instance: Stock = Stock()


def test_stock_instance():
    assert isinstance(stock_instance, Stock), "Stock not properly initialized"


def test_stock_id():
    sid = create_id()
    stock_instance.stock_id = sid
    assert stock_instance.stock_id == sid, "stock_id not set correctly"


def test_stock_code():
    s_code = "ABC"
    stock_instance.stock_code = s_code
    assert stock_instance.stock_code == s_code, "stock code is not set correctly"


def test_stock_name():
    stock_name = "ABCD"
    stock_instance.stock_name = stock_name
    assert stock_instance.stock_name == stock_name, "stock name is not set correctly"


def test_stock_symbol():
    s_symbol = "ABC"
    stock_instance.symbol = s_symbol
    assert stock_instance.symbol == s_symbol,  "stock symbol is not set correctly"

