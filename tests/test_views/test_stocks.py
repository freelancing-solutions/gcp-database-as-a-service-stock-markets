import typing
from datetime import datetime
from random import randint
from google.cloud import ndb
from data_service.views.stocks import StockView
from data_service.store.stocks import Stock
from data_service.utils.utils import create_id
from .. import test_app
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class StockQueryMock:
    stock_instance: Stock = Stock()
    results_range: int = randint(0, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[Stock]:
        return [self.stock_instance for _ in range(self.results_range)]

    def get(self) -> Stock:
        return self.stock_instance


# noinspection PyShadowingNames
def test_create_stock_data(mocker):
    pass


# noinspection PyShadowingNames
def test_create_broker_data(mocker):
    pass


# noinspection PyShadowingNames
def test_create_stock_model(mocker):
    pass


# noinspection PyShadowingNames
def test_create_buy_model(mocker):
    pass


# noinspection PyShadowingNames
def test_create_sell_model(mocker):
    pass



