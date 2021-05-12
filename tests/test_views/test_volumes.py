import typing
from datetime import datetime
from random import randint, choice
from google.cloud import ndb
from data_service.config.stocks import currency_symbols
from data_service.views.stocks import StockView
from data_service.store.stocks import BuyVolumeModel
from data_service.utils.utils import create_id
from .. import test_app, int_positive
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class BuyVolumeQueryMock:
    buy_volume_instance: BuyVolumeModel = BuyVolumeModel()
    results_range: int = range(0, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[BuyVolumeModel]:
        return [self.buy_volume_instance for _ in range(self.results_range)]

    def get(self) -> BuyVolumeModel:
        return self.buy_volume_instance


buy_volume_mock_data: dict = {
    'transaction_id': create_id(),
    'stock_id': create_id(),
    'date_created': datetime.now().date(),
    'currency': choice(currency_symbols()),
    'buy_volume': int_positive(),
    'buy_value': int_positive(),
    'buy_ave_price': int_positive(),
    'buy_market_val_percent': int_positive(),
    'buy_trade_count': int_positive()
}


# noinspection PyShadowingNames
def test_buy_volume(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=BuyVolumeQueryMock())

    with test_app().app_context():
        stock_view_instance: StockView = StockView()
        response, status = stock_view_instance.create_buy_model(buy_data=buy_volume_mock_data)
        response_data: dict = response.get_json()
        assert status == 200, response_data['message']
