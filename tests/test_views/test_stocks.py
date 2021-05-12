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


stock_data_mock: dict = {
    "stock_id": create_id(),
    "stock_code": "TSLA",
    "stock_name": "TESLA",
    "symbol": "TSLA"
}
broker_data_mock: dict = {
    "broker_id": create_id(),
    "broker_code": "ASD",
    "broker_name": "ASD"
}


# noinspection PyShadowingNames
def test_create_stock_data(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=StockQueryMock())

    with test_app().app_context():
        stock_view_instance: StockView = StockView()
        mocker.patch('data_service.views.stocks.StockView.stock_id_exist', return_value=False)
        mocker.patch('data_service.views.stocks.StockView.stock_code_exist', return_value=False)
        mocker.patch('data_service.views.stocks.StockView.symbol_exist', return_value=False)
        response, status = stock_view_instance.create_stock_data(stock_data=stock_data_mock)
        response_data: dict = response.get_json()
        assert status == 200, response_data['message']

    mocker.stopall()
