import typing
from datetime import datetime
from random import randint
from google.cloud import ndb
from data_service.views.stocks import StockView
from data_service.store.stocks import Broker
from data_service.utils.utils import create_id
from .. import test_app
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class BrokerQueryMock:
    broker_instance: Broker = Broker()
    results_range: int = randint(0, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[Broker]:
        return [self.broker_instance for _ in range(self.results_range)]

    def get(self) -> Broker:
        return self.broker_instance


broker_data_mock: dict = {
    "broker_id": create_id(),
    "broker_code": "ASD",
    "broker_name": "ASD"
}


# noinspection PyShadowingNames
def test_create_broker(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=BrokerQueryMock())

    with test_app().app_context():
        stock_view_instance: StockView = StockView()
        mocker.patch('data_service.views.stocks.StockView.broker_id_exist', return_value=False)
        mocker.patch('data_service.views.stocks.StockView.broker_code_exist', return_value=False)
        response, status = stock_view_instance.create_broker_data(broker_data=broker_data_mock)
        assert status == 200, "Unable to create broker data"

        mocker.patch('data_service.views.stocks.StockView.broker_code_exist', return_value=True)
        response, status = stock_view_instance.create_broker_data(broker_data=broker_data_mock)
        assert status == 500, "Creating duplicate brokers"

        mocker.patch('data_service.views.stocks.StockView.broker_code_exist', return_value=False)
        mocker.patch('data_service.views.stocks.StockView.broker_id_exist', return_value=True)
        response, status = stock_view_instance.create_broker_data(broker_data=broker_data_mock)
        assert status == 500, "Creating duplicate brokers"

    mocker.stopall()