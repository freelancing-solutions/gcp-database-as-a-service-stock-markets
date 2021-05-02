from pytest import raises
from data_service.store.stocks import Stock
from data_service.utils.utils import create_id

stock_instance: Stock = Stock()

# TODO add ndb put mock- in order to test more options such as error checking on the database level
def test_stock_instance():
    assert isinstance(stock_instance, Stock), "Stock not properly initialized"


def test_stock_id():
    sid = create_id()
    stock_instance.stock_id = sid
    assert stock_instance.stock_id == sid, "stock_id not set correctly"
    with raises(TypeError):
        stock_instance.stock_id = 34
    with raises(ValueError):
        stock_instance.stock_id = ""
    with raises(ValueError):
        stock_instance.stock_id = str()


def test_stock_code():
    s_code = "ABC"
    stock_instance.stock_code = s_code
    assert stock_instance.stock_code == s_code, "stock code is not set correctly"
    with raises(TypeError):
        stock_instance.stock_code = 70
    with raises(ValueError):
        stock_instance.stock_code = str()
    with raises(TypeError):
        stock_instance.stock_code = {}
    with raises(ValueError):
        stock_instance.stock_code = ""

def test_stock_name():
    stock_name = "ABCD"
    stock_instance.stock_name = stock_name
    assert stock_instance.stock_name == stock_name.lower(), "stock name is not set correctly"
    with raises(TypeError):
        stock_instance.stock_name = 123
    with raises(ValueError):
        stock_instance.stock_name = str()
    with raises(ValueError):
        stock_instance.stock_name = ""


def test_stock_symbol():
    s_symbol = "ABC"
    stock_instance.symbol = s_symbol
    assert stock_instance.symbol == s_symbol,  "stock symbol is not set correctly"
    with raises(TypeError):
        stock_instance.symbol = 0
    with raises(ValueError):
        stock_instance.symbol = str()
    with raises(ValueError):
        stock_instance.symbol = ""

def create_stock_mock(my_stock_instance: Stock) -> Stock:
    my_stock_instance.stock_id = "45345345"
    my_stock_instance.symbol = "SDF"
    my_stock_instance.stock_name = "HGTFR"
    my_stock_instance.stock_code = "X45T"
    return my_stock_instance

def test_stock_dunder_methods():
    first_stock: Stock = create_stock_mock(stock_instance)
    second_stock: Stock = create_stock_mock(stock_instance)
    assert first_stock == second_stock, "__eq__ not implemented correctly"
    assert str(first_stock) == str(second_stock), "__str__ not implemented correctly"

