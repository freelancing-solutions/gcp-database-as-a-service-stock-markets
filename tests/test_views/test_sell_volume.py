import typing
from datetime import datetime
from random import randint, choice
from google.cloud import ndb
from data_service.config.stocks import currency_symbols
from data_service.views.stocks import StockView
from data_service.store.stocks import SellVolumeModel
from data_service.utils.utils import create_id
from .. import test_app, int_positive
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class SellVolumeQueryMock:
    sell_volume_instance: SellVolumeModel = SellVolumeModel()
    results_range: int = randint(1, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[SellVolumeModel]:
        return [self.sell_volume_instance for _ in range(self.results_range)]

    def get(self) -> SellVolumeModel:
        return self.sell_volume_instance


sell_volume_mock_data: dict = {
    'stock_id': create_id(),
    'date_created': datetime.now().date(),
    'currency': choice(currency_symbols()),
    'sell_volume': int_positive(),
    'sell_value': int_positive(),
    'sell_ave_price': int_positive(),
    'sell_market_val_percent': int_positive(),
    'sell_trade_count': int_positive()
}


# noinspection PyShadowingNames
def test_sell_volume(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=SellVolumeQueryMock())

    with test_app().app_context():
        stock_view_instance: StockView = StockView()
        response, status = stock_view_instance.create_sell_volume(sell_data=sell_volume_mock_data)
        response_data: dict = response.get_json()
        assert status == 200, response_data['message']
