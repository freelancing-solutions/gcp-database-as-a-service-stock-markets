import datetime
import typing
import functools
from google.api_core.exceptions import RetryError, Aborted
from flask import current_app, jsonify
from google.cloud.ndb.exceptions import BadRequestError, BadQueryError
from data_service.main import cache_stocks
from data_service.config.exceptions import DataServiceError
from data_service.store.stocks import StockPriceData, Stock
from datetime import date
from data_service.utils.utils import create_id, return_ttl, end_of_month, timestamp, get_days, date_days_ago
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context


def get_stock_price_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stock_price_data: dict = kwargs.get('stock_price_data')
        if 'stock_id' in stock_price_data and stock_price_data['stock_id'] != "":
            stock_id: typing.Union[str, None] = stock_price_data.get('stock_id')
        else:
            stock_id = create_id(size=12)
        if 'date_created' in stock_price_data and stock_price_data['date_created'] != "":
            date_created: typing.Union[date, None] = stock_price_data.get('date_created')
        else:
            return jsonify({'status': False, 'message': 'date_created required'}), 500

        if 'price_open' in stock_price_data and stock_price_data['price_open'] != "":
            price_open: typing.Union[int, None] = stock_price_data.get('price_open')
        else:
            return jsonify({'status': False, 'message': 'price_open is required'}), 500
        if 'price_high' in stock_price_data and stock_price_data['price_high'] != "":
            price_high: typing.Union[int, None] = stock_price_data.get('price_high')
        else:
            return jsonify({'status': False, 'message': 'price_high is required'}), 500

        if 'price_low' in stock_price_data and stock_price_data['price_low'] != "":
            price_low: typing.Union[int, None] = stock_price_data.get('price_low')
        else:
            return jsonify({'status': False, 'message': 'price low is required'}), 500

        if 'price_close' in stock_price_data and stock_price_data['price_close'] != "":
            price_close: typing.Union[int, None] = stock_price_data.get('price_close')
        else:
            return jsonify({'status': False, 'message': 'price_close is required'}), 500

        if 'adjusted_close' in stock_price_data and stock_price_data['adjusted_close'] != "":
            adjusted_close: typing.Union[int, None] = stock_price_data.get('adjusted_close')
        else:
            return jsonify({'status': False, 'message': 'adjusted_close is required'}), 500

        if 'volume' in stock_price_data and stock_price_data['volume'] != "":
            volume: typing.Union[int, None] = stock_price_data.get('volume')
        else:
            return jsonify({'status': False, 'message': 'volume is required'}), 500

        return func(stock_id=stock_id, date_created=date_created, price_open=price_open, price_high=price_high,
                    price_low=price_low, price_close=price_close, adjusted_close=adjusted_close,
                    volume=volume, *args)

    return wrapper


class CatchStockPriceDataErrors:
    def __init__(self):
        super(CatchStockPriceDataErrors, self).__init__()

    @staticmethod
    def stock_exist(stock_id: typing.Union[str, None]) -> typing.Union[bool, None]:
        try:
            if not isinstance(stock_id, str):
                return None
            stock_instance: Stock = Stock.query(Stock.stock_id == stock_id).get()
            if isinstance(stock_instance, Stock):
                return True
            return False
        except BadRequestError:
            return None
        except BadQueryError:
            return None
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

    @staticmethod
    async def stock_exist_async(stock_id: typing.Union[str, None]) -> typing.Union[bool, None]:
        try:
            if not isinstance(stock_id, str):
                return None
            stock_instance: Stock = Stock.query(Stock.stock_id == stock_id).get_async().results()
            if isinstance(stock_instance, Stock):
                return True
            return False
        except BadRequestError:
            return None
        except BadQueryError:
            return None
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None


    @staticmethod
    def price_data_exist(stock_id: typing.Union[str, None], date_created: typing.Union[date, None]) -> \
            typing.Union[bool, None]:
        try:
            if not (isinstance(stock_id, str)):
                return None
            if not (isinstance(date_created, date)):
                return None
            stock_price_data: StockPriceData = StockPriceData.query(StockPriceData.stock_id == stock_id,
                                                                    StockPriceData.date_created == date_created).get()
            if isinstance(stock_price_data, StockPriceData):
                return True
            return False

        except BadRequestError:
            return None
        except BadQueryError:
            return None
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

    def can_add_price_data(self, stock_id: typing.Union[str, None],
                           date_created: typing.Union[date, None]) -> bool:
        is_stock_exist = self.stock_exist(stock_id=stock_id)
        is_price_data_exist = self.price_data_exist(stock_id=stock_id, date_created=date_created)
        if isinstance(is_stock_exist, bool) and isinstance(is_price_data_exist, bool):
            return is_stock_exist and not is_price_data_exist
        raise DataServiceError(description="Unable to read database")

    async def can_add_price_data_async(self, stock_id: typing.Union[str, None],
                                       date_created: typing.Union[date, None]) -> bool:
        is_stock_exist = self.stock_exist(stock_id=stock_id)

class StockPriceDataView(CatchStockPriceDataErrors):
    def __init__(self):
        super(StockPriceDataView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @get_stock_price_data
    @use_context
    @handle_view_errors
    def add_stock_price_data(self, stock_id: typing.Union[str, None],
                             date_created: typing.Union[date, None],
                             price_open: typing.Union[int, None],
                             price_high: typing.Union[int, None],
                             price_low: typing.Union[int, None],
                             price_close: typing.Union[int, None],
                             adjusted_close: typing.Union[int, None],
                             volume: typing.Union[int, None]
                             ) -> tuple:
        if self.can_add_price_data(stock_id=stock_id, date_created=date_created) is True:
            stock_price_data_instance: StockPriceData = StockPriceData(stock_id=stock_id, date_created=date_created,
                                                                       price_open=price_open, price_high=price_high,
                                                                       price_low=price_low, price_close=price_close,
                                                                       adjusted_close=adjusted_close, volume=volume)
            key = stock_price_data_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "Unable to write to database"
                raise DataServiceError(description=message)
        else:
            message: str = "Stock price data may already be added"
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True,
                        'message': 'successfully saved stock data',
                        "payload": stock_price_data_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    async def add_stock_price_data_async(self) -> tuple:
        """
            add stock price data asynchronously
        """
        pass

    @cache_stocks.cached(timeout=return_ttl(name='medium'))
    @use_context
    @handle_view_errors
    def get_stock_price_data_list_by_date(self, date_created: typing.Union[date, None]) -> tuple:

        stock_price_data_list: typing.List[StockPriceData] = StockPriceData.query(
            StockPriceData.date_created == date_created).fetch()
        payload: typing.List[dict] = [price_data.to_dict() for price_data in stock_price_data_list]
        return jsonify({'status': True, 'payload': payload, 'message': 'successfully fetched stock price data'}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'))
    @use_context
    @handle_view_errors
    def get_monthly_stock_price_data_list_by_stock_id(self, stock_id: typing.Union[str, None]) -> tuple:
        if not (isinstance(stock_id, str)):
            return jsonify({'status': False, 'message': 'stock id is required'}), 500
        one_month = date_days_ago(days=30)
        stock_price_list: typing.List[StockPriceData] = StockPriceData.query(StockPriceData.stock_id == stock_id,
                                                                             StockPriceData.date_created > one_month).fetch()
        payload: typing.List[dict] = [price_data.to_dict() for price_data in stock_price_list]
        message: str = 'successfully fetched monthly stock price data'
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'))
    @use_context
    @handle_view_errors
    def get_weekly_stock_price_data_list_by_stock_id(self, stock_id: typing.Union[str, None]) -> tuple:
        if not (isinstance(stock_id, str)):
            return jsonify({'status': False, 'message': 'stock id is required'}), 500

        week = date_days_ago(days=7)
        stock_price_list: typing.List[StockPriceData] = StockPriceData.query(StockPriceData.stock_id == stock_id,
                                                                             StockPriceData.date_created > week).fetch()
        payload: typing.List[dict] = [price_data.to_dict() for price_data in stock_price_list]
        message: str = 'successfully fetched weekly stock price data'
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'))
    @use_context
    @handle_view_errors
    def get_n_days_stock_price_data_list_by_stock_id(self, stock_id: typing.Union[str, None],
                                                     days: typing.Union[int, None]) -> tuple:

        if not (isinstance(days, int)) or (days < 0):
            return jsonify({'status': False, 'message': 'days is required and should be greater than 0'}), 500
        if not (isinstance(stock_id, str)):
            return jsonify({'status': False, 'message': 'stock id is required'}), 500

        n_days = date_days_ago(days=days)
        stock_price_list: typing.List[StockPriceData] = StockPriceData.query(StockPriceData.stock_id == stock_id,
                                                                             StockPriceData.date_created > n_days).fetch()
        payload: typing.List[dict] = [price_data.to_dict() for price_data in stock_price_list]
        message: str = 'successfully fetched weekly stock price data'
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200
