import typing
from datetime import datetime
from random import randint, choice
from google.cloud import ndb
from data_service.config.stocks import currency_symbols
from data_service.views.stocks import StockView
from data_service.store.stocks import NetVolumeModel
from data_service.utils.utils import create_id
from .. import test_app, int_positive
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class NetVolumeQueryMock:
    net_volume_instance: NetVolumeModel = NetVolumeModel()
    results_status: int = randint(1, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[NetVolumeModel]:
        return [self.net_volume_instance for _ in range(self.results_status)]

    def get(self) -> NetVolumeModel:
        return self.net_volume_instance


net_volume_data_mock: dict = {
    'stock_id': create_id(),
    'transaction_id': create_id(),
    'date_created': datetime.now().date(),
    'currency': choice(currency_symbols()),
    'net_volume': int_positive(),
    'net_value': int_positive(),
    'total_volume': int_positive(),
    'total_value': int_positive()
}


# noinspection PyShadowingNames
def test_net_volume(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=NetVolumeQueryMock())

    with test_app().app_context():
        stock_view_instance: StockView = StockView()
        response, status = stock_view_instance.create_net_volume(net_volume_data=net_volume_data_mock)
        response_data: dict = response.get_json()
        assert status == 200, response_data['message']



