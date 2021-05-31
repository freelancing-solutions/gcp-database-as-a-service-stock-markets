import typing
import functools
from datetime import date as date_class
from datetime import datetime, timezone
from google.api_core.exceptions import RetryError, Aborted
from flask import current_app, jsonify
from google.cloud import ndb
from google.cloud.ndb import Future
from google.cloud.ndb.exceptions import BadRequestError, BadQueryError
from google.cloud.ndb.tasklets import _TaskletFuture

from data_service.main import cache_stocks
from data_service.config.exceptions import DataServiceError
from data_service.store.stocks import Stock, Broker, StockModel, BuyVolumeModel, SellVolumeModel, NetVolumeModel
from data_service.utils.utils import date_string_to_date, create_id, return_ttl, end_of_month
from data_service.config import Config
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context

stock_list_type = typing.List[Stock]


class StockDataWrappers:
    """
        # NOTES: request wrappers for stock, broker, buy_volume sell_volume, and net_volume
    """

    def __init__(self):
        pass

    @staticmethod
    def get_stock_data(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            stock_data: dict = kwargs.get('stock_data')
            if 'stock_id' in stock_data and stock_data['stock_id'] != "":
                stock_id: typing.Union[str, None] = stock_data.get('stock_id')
            else:
                stock_id = create_id(size=12)
            if 'stock_code' in stock_data and stock_data['stock_code'] != "":
                stock_code: typing.Union[str, None] = stock_data.get('stock_code')
            else:
                return jsonify({'status': False, 'message': 'Stock Code is required'}), 500

            if 'stock_name' in stock_data and stock_data['stock_name'] != "":
                stock_name: typing.Union[str, None] = stock_data.get('stock_name')
            else:
                return jsonify({'status': False, 'message': 'Stock Name is required'}), 500
            if 'symbol' in stock_data and stock_data['symbol'] != "":
                symbol: typing.Union[str, None] = stock_data.get('symbol')
            else:
                return jsonify({'status': False, 'message': 'Stock Symbol is required'}), 500

            return func(stock_id=stock_id, stock_code=stock_code, stock_name=stock_name, symbol=symbol, *args)

        return wrapper

    @staticmethod
    def get_broker_data(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            broker_data: dict = kwargs.get('broker_data')
            if "broker_id" in broker_data and broker_data['broker_id'] != "":
                broker_id: typing.Union[str, None] = broker_data.get('broker_id')
            else:
                broker_id: str = create_id(size=12)
            if "broker_code" in broker_data and broker_data['broker_code'] != "":
                broker_code: typing.Union[str, None] = broker_data.get('broker_code')
            else:
                return jsonify({'status': False, 'message': 'Broker Code is required'}), 500
            if "broker_name" in broker_data and broker_data['broker_name'] != "":
                broker_name: typing.Union[str, None] = broker_data.get("broker_name")
            else:
                return jsonify({'status': False, 'message': 'Broker Name is required'}), 500

            return func(broker_id=broker_id, broker_code=broker_code, broker_name=broker_name, *args)

        return wrapper

    @staticmethod
    def get_buy_volume_data(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            buy_data: dict = kwargs.get('buy_data')
            if not isinstance(buy_data, dict):
                return jsonify({'status': False, 'message': 'Please provide buy volume data'}), 500

            if "stock_id" in buy_data and buy_data['stock_id'] != "":
                stock_id: typing.Union[str, None] = buy_data.get('stock_id')
            else:
                return jsonify({'status': False, 'message': "stock id is required"}), 500
            if "date_created" in buy_data and buy_data['date_created'] != "":
                try:
                    date_created: date_class = date_string_to_date(buy_data.get('date_created'))
                except ValueError:
                    date_created: date_class = datetime.now().date()
            else:
                return jsonify({'status': False, 'message': "date_created is required"}), 500

            if "buy_volume" in buy_data and buy_data['buy_volume'] != "":
                buy_volume: typing.Union[int, None] = int(buy_data.get('buy_volume'))
            else:
                return jsonify({'status': False, 'message': "buy volume is required"}), 500

            if "buy_value" in buy_data and buy_data["buy_value"] != "":
                buy_value: typing.Union[int, None] = int(buy_data.get("buy_value"))
            else:
                return jsonify({'status': False, 'message': "buy value is required"}), 500

            if "buy_ave_price" in buy_data and buy_data["buy_ave_price"] != "":
                buy_ave_price: typing.Union[int, None] = int(buy_data.get("buy_ave_price"))
            else:
                return jsonify({'status': False, 'message': "buy average price is required"}), 500

            if "buy_market_val_percent" in buy_data and buy_data["buy_market_val_percent"] != "":
                buy_market_val_percent: typing.Union[int, None] = int(buy_data.get("buy_market_val_percent"))
            else:
                return jsonify({'status': False, 'message': "buy market value percent is required"}), 500

            if "buy_trade_count" in buy_data and buy_data["buy_trade_count"] != "":
                buy_trade_count: typing.Union[int, None] = int(buy_data.get("buy_trade_count"))
            else:
                return jsonify({'status': False, 'message': "buy trade account"}), 500

            if "transaction_id" in buy_data and buy_data["transaction_id"] != "":
                transaction_id: typing.Union[str, None] = buy_data.get("transaction_id")

                return func(stock_id=stock_id, date_created=date_created, buy_volume=buy_volume,
                            buy_value=buy_value, buy_ave_price=buy_ave_price,
                            buy_market_val_percent=buy_market_val_percent, buy_trade_count=buy_trade_count,
                            transaction_id=transaction_id, *args)

            return func(stock_id=stock_id, date_created=date_created, buy_volume=buy_volume,
                        buy_value=buy_value, buy_ave_price=buy_ave_price,
                        buy_market_val_percent=buy_market_val_percent, buy_trade_count=buy_trade_count, *args)

        return wrapper

    @staticmethod
    def get_sell_volume_data(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sell_data: dict = kwargs.get('sell_data')
            if sell_data is None:
                return jsonify({'status': False, 'message': 'Unable to get sell volume data'}), 500

            if "stock_id" in sell_data and sell_data['stock_id'] != "":
                stock_id: typing.Union[str, None] = sell_data.get('stock_id')
            else:
                return jsonify({'status': False, 'message': "stock id is required"}), 500

            if "date_created" in sell_data and sell_data["date_created"] != "":
                try:
                    date_created: date_class = date_string_to_date(sell_data.get('date_created'))
                except ValueError:
                    date_created: date_class = datetime.date(datetime.now())
            else:
                return jsonify({'status': False, 'message': "date_class is required"}), 500

            if "sell_volume" in sell_data and sell_data["sell_volume"] != "":
                sell_volume: typing.Union[int, None] = int(sell_data.get("sell_volume"))
            else:
                return jsonify({"status": False, "message": "sell volume is required"}), 500

            if "sell_value" in sell_data and sell_data["sell_value"] != "":
                sell_value: typing.Union[int, None] = int(sell_data.get("sell_value"))
            else:
                return jsonify({"status": False, "message": "sell value is required"}), 500

            if "sell_ave_price" in sell_data and sell_data["sell_ave_price"] != "":
                sell_ave_price: typing.Union[int, None] = int(sell_data.get("sell_ave_price"))
            else:
                return jsonify({"status": False, "message": "sell ave price is required"}), 500

            if "sell_market_val_percent" in sell_data and sell_data["sell_market_val_percent"] != "":
                sell_market_val_percent: typing.Union[int, None] = int(sell_data.get("sell_market_val_percent"))
            else:
                return jsonify({"status": False, "message": "sell market value percent price is required"}), 500

            if "sell_trade_count" in sell_data and sell_data["sell_trade_count"] != "":
                sell_trade_count: typing.Union[int, None] = int(sell_data.get("sell_trade_count"))
            else:
                return jsonify({"status": False, "message": "sell trade account percent price is required"}), 500
            if 'transaction_id' in sell_data and sell_data['transaction_id'] != "":
                transaction_id: typing.Union[str, None] = sell_data['transaction_id']

                return func(stock_id=stock_id, date_created=date_created, sell_volume=sell_volume,
                            sell_value=sell_value,
                            sell_ave_price=sell_ave_price, sell_market_val_percent=sell_market_val_percent,
                            sell_trade_count=sell_trade_count, transaction_id=transaction_id, *args)

            return func(stock_id=stock_id, date_created=date_created, sell_volume=sell_volume, sell_value=sell_value,
                        sell_ave_price=sell_ave_price, sell_market_val_percent=sell_market_val_percent,
                        sell_trade_count=sell_trade_count, *args)

        return wrapper

    @staticmethod
    def get_net_volume_data(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            net_volume_data: dict = kwargs.get('net_volume_data')

            if net_volume_data is None:
                return jsonify({'status': False, 'message': 'please define net volume data'}), 500

            if "stock_id" in net_volume_data and net_volume_data["stock_id"] != "":
                stock_id: typing.Union[str, None] = net_volume_data.get("stock_id")
            else:
                return jsonify({'status': False, 'message': "stock id is required"}), 500
            if "date_created" in net_volume_data and net_volume_data['date_created'] != "":
                # assumed format DD/MM/YYYY
                date_created: date_class = date_string_to_date(net_volume_data['date_created'])
            else:
                return jsonify({'status': False, 'message': "date_created is required"}), 500

            if "transaction_id" in net_volume_data and net_volume_data["transaction_id"] != "":
                transaction_id: typing.Union[str, None] = net_volume_data.get("transaction_id")
            else:
                return jsonify({'status': False, 'message': "transaction id is required"}), 500

            if "net_volume" in net_volume_data and net_volume_data["net_volume"] != "":
                net_volume: typing.Union[int, None] = int(net_volume_data.get("net_volume"))
            else:
                return jsonify({'status': False, 'message': "net volume is required"}), 500

            if "net_value" in net_volume_data and net_volume_data["net_value"] != "":
                net_value: typing.Union[int, None] = int(net_volume_data.get("net_value"))
            else:
                return jsonify({'status': False, 'message': "net value is required"}), 500

            if "total_value" in net_volume_data and net_volume_data["total_value"] != "":
                total_value:typing.Union[int, None] = int(net_volume_data.get("total_value"))
            else:
                return jsonify({'status': False, 'message': "total value is required"}), 500

            if "total_volume" in net_volume_data and net_volume_data["total_volume"] != "":
                total_volume: typing.Union[int, None] = int(net_volume_data.get('total_volume'))
            else:
                return jsonify({'status': False, 'message': "total volume is required"}), 500

            return func(stock_id=stock_id, date_created=date_created, transaction_id=transaction_id,
                        net_volume=net_volume, net_value=net_value, total_value=total_value,
                        total_volume=total_volume, *args)
        return wrapper


data_wrappers: StockDataWrappers = StockDataWrappers()


class StockViewContext:
    """
        add common variables here
    """
    def __int__(self):
        pass


# noinspection DuplicatedCode
class CatchStockErrors(StockViewContext):
    def __int__(self):
        super(CatchStockErrors, self).__int__()

    @staticmethod
    def symbol_exist(symbol: typing.Union[str, None]) -> typing.Union[None, bool]:
        # noinspection DuplicatedCode
        try:
            if not isinstance(symbol, str):
                return None
            stock_instance: Stock = Stock.query(Stock.symbol == symbol).get()
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
        if isinstance(stock_instance, Stock):
            return True
        return False

    @staticmethod
    def stock_code_exist(stock_code: typing.Union[str, None]) -> typing.Union[None, bool]:
        try:
            if not isinstance(stock_code, str):
                return None
            stock_list: stock_list_type = Stock.query(Stock.stock_code == stock_code).get()
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

        if isinstance(stock_list, list) and len(stock_list) > 0:
            return True
        return False

    @staticmethod
    def stock_id_exist(stock_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        try:
            if not isinstance(stock_id, str):
                return None
            stock_list: stock_list_type = Stock.query(Stock.stock_id == stock_id).get()
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
        if isinstance(stock_list, list) and len(stock_list) > 0:
            return True
        return False

    def can_add_stock(self, stock_code: typing.Union[str, None] = None, symbol: typing.Union[str, None] = None,
                      stock_id: typing.Union[str, None] = None) -> bool:
        stock_id_exist: bool = self.stock_id_exist(stock_id=stock_id)
        stock_code_exist: bool = self.stock_code_exist(stock_code=stock_code)
        symbol_exist: bool = self.symbol_exist(symbol=symbol)
        if isinstance(stock_id_exist, bool) and isinstance(stock_code_exist, bool) and isinstance(symbol_exist, bool):
            return not (stock_id_exist or stock_code_exist or symbol_exist)

        message: str = "Unable to verify input data, Due to database error please try again later"
        raise DataServiceError(message)


# noinspection DuplicatedCode
class CatchBrokerErrors(StockViewContext):

    def __int__(self):
        super(CatchBrokerErrors, self).__init__()

    @staticmethod
    def broker_id_exist(broker_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        try:
            if not isinstance(broker_id, str):
                return None
            broker_instance: Broker = Broker.query(Broker.broker_id == broker_id).get()
            if isinstance(broker_instance, Broker):
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

    # noinspection DuplicatedCode
    @staticmethod
    def broker_code_exist(broker_code: typing.Union[str, None]) -> typing.Union[None, bool]:
        try:
            if not isinstance(broker_code, str):
                return None
            broker_instance: Broker = Broker.query(Broker.broker_code == broker_code).get()
            if isinstance(broker_instance, Broker):
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

    def can_add_broker(self, broker_id: typing.Union[str, None], broker_code: typing.Union[str, None]) -> bool:
        broker_id_exist: bool = self.broker_id_exist(broker_id=broker_id)
        broker_code_exist: bool = self.broker_code_exist(broker_code=broker_code)
        if isinstance(broker_id_exist, bool) and isinstance(broker_code_exist, bool):
            return not (broker_id_exist or broker_code_exist)
        message: str = "Unable to verify broker data due to database errors please try again later"
        raise DataServiceError(message)


class StockView(CatchStockErrors, CatchBrokerErrors):
    def __init__(self):
        super(StockView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')
        with current_app.app_context():
            self.timezone = timezone(Config.UTC_OFFSET)

    @use_context
    def fetch_stock(self, stock_id: str) -> typing.Union[Stock, None]:
        if not isinstance(stock_id, str):
            return None
        stock: Stock = Stock.query(Stock.stock_id == stock_id).get()
        return stock

    @use_context
    def fetch_broker(self, broker_id: str) -> typing.Union[Broker, None]:
        if not isinstance(broker_id, str):
            return None
        broker: Broker = Broker.query(Broker.broker_id == broker_id).get()
        return broker

    @data_wrappers.get_stock_data
    @use_context
    @handle_view_errors
    def create_stock_data(self, stock_id: str, stock_code: str, stock_name: str, symbol: str) -> tuple:
        if self.can_add_stock(stock_code=stock_code, stock_id=stock_id, symbol=symbol) is True:
            stock_instance: Stock = Stock(stock_id=stock_id, stock_code=stock_code, stock_name=stock_name,
                                          symbol=symbol)
            key = stock_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "For some strange reason we could not save your data to database"
                raise DataServiceError(message)
        else:
            message: str = "Stock Duplicate detected, you cannot add duplicate stock in here"
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True,
                        'message': 'successfully saved stock data',
                        "payload": {"stock_instance": stock_instance.to_dict()}}), 200

    @data_wrappers.get_broker_data
    @use_context
    @handle_view_errors
    def create_broker_data(self, broker_id: str, broker_code: str, broker_name: str) -> tuple:
        if self.can_add_broker(broker_id=broker_id, broker_code=broker_code) is True:
            broker_instance: Broker = Broker(broker_id=broker_id, broker_code=broker_code,
                                             broker_name=broker_name)
            key = broker_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "For some strange reason we could not save your data to database"
                raise DataServiceError(message)
        else:
            message: str = "cannot create broker data, duplicates would be created"
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True, 'message': 'successfully saved broker data',
                        'payload': broker_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    def create_stock_model(self, exchange_id: str, sid: str, stock_id: str, broker_id: str) -> tuple:

        stock: typing.Union[Stock, None] = self.fetch_stock(stock_id=stock_id)
        broker: typing.Union[Broker, None] = self.fetch_broker(broker_id=broker_id)
        if not isinstance(stock, Stock):
            return jsonify({'status': False, 'message': 'A stock with that ID was not found'}), 500
        if not isinstance(broker, Broker):
            return jsonify({'status': False, 'message': 'A broker with that ID was not found'}), 500

        stock_model_instance: StockModel = StockModel(exchange_id=exchange_id,
                                                      sid=sid, stock=stock, broker=broker)
        key = stock_model_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if key is None:
            message: str = "For some strange reason we could not save your data to database"
            raise DataServiceError(message)
        return jsonify({'status': True, 'message': 'Stock Model Successfully created',
                        'payload': stock_model_instance.to_dict()}), 200

    @data_wrappers.get_buy_volume_data
    @use_context
    @handle_view_errors
    def create_buy_model(self, stock_id: str, date_created: date_class, buy_volume: int, buy_value: int,
                         buy_ave_price: int, buy_market_val_percent: int,
                         buy_trade_count: int) -> tuple:

        buy_volume_instance: BuyVolumeModel = BuyVolumeModel(stock_id=stock_id, date_created=date_created,
                                                             buy_volume=buy_volume, buy_value=buy_value,
                                                             buy_ave_price=buy_ave_price,
                                                             buy_market_val_percent=buy_market_val_percent,
                                                             buy_trade_count=buy_trade_count)
        key = buy_volume_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if key is None:
            message: str = "For some strange reason we could not save your data to database"
            raise DataServiceError(message)

        message: str = "Buy volume successfully created"
        return jsonify({'status': True, 'message': message, 'payload': buy_volume_instance.to_dict()}), 200

    @data_wrappers.get_sell_volume_data
    @use_context
    @handle_view_errors
    def create_sell_volume(self, stock_id: str, date_created: date_class, sell_volume: int, sell_value: int,
                           sell_ave_price: int, sell_market_val_percent: int,
                           sell_trade_count: int) -> tuple:
        sell_volume_instance: SellVolumeModel = SellVolumeModel(stock_id=stock_id,
                                                                date_created=date_created,
                                                                sell_volume=sell_volume,
                                                                sell_value=sell_value,
                                                                sell_ave_price=sell_ave_price,
                                                                sell_market_val_percent=sell_market_val_percent,
                                                                sell_trade_count=sell_trade_count)
        key = sell_volume_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if key is None:
            message: str = "For some strange reason we could not save your data to database"
            raise DataServiceError(message)
        return jsonify({'status': True, 'message': 'Sell Volume Successfully created',
                        'payload': sell_volume_instance.to_dict()}), 200

    # noinspection DuplicatedCode
    @data_wrappers.get_net_volume_data
    @use_context
    @handle_view_errors
    def create_net_volume(self, stock_id: str, date_created: date_class, transaction_id: str, net_volume: str,
                          net_value: str, total_value: str, total_volume: str) -> tuple:
        """
            if net volume already exist update net volume
        """
        net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
            NetVolumeModel.transaction_id == transaction_id).fetch()
        if isinstance(net_volume_list, list) and len(net_volume_list) > 0:
            net_volume_instance: NetVolumeModel = net_volume_list[0]
        else:
            net_volume_instance: NetVolumeModel = NetVolumeModel()

        net_volume_instance.stock_id = stock_id
        net_volume_instance.transaction_id = transaction_id
        net_volume_instance.date_created = date_created
        net_volume_instance.net_volume = net_volume
        net_volume_instance.net_value = net_value
        net_volume_instance.total_value = total_value
        net_volume_instance.total_volume = total_volume

        key = net_volume_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if key is None:
            message: str = "For some strange reason we could not save your data to database"
            raise DataServiceError(message)
        message: str = 'Net Volume Successfully created'
        return jsonify({'status': True, 'message': message,
                        'payload': net_volume_instance.to_dict()}), 200

    @data_wrappers.get_stock_data
    @use_context
    @handle_view_errors
    def update_stock_data(self, stock_id: str, stock_code: str, stock_name: str, symbol: str) -> tuple:
        stock_instance_list: typing.List[Stock] = Stock.query(Stock.stock_id == stock_id).fetch()
        if len(stock_instance_list) > 0:
            stock_instance: Stock = stock_instance_list[0]
            stock_instance.stock_id = stock_id
            stock_instance.stock_code = stock_code
            stock_instance.stock_name = stock_name
            stock_instance.symbol = symbol
            key = stock_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is not None:
                return jsonify({'status': True, 'payload': stock_instance.to_dict(),
                                'message': 'successfully updated stock'}), 200
            else:
                message: str = "Unable to update stock data due to database erros"
                raise DataServiceError(message)
        else:
            message: str = "Could not find stock please try again later"
            return jsonify({'status': False, 'message': message}), 500

    @data_wrappers.get_broker_data
    @use_context
    @handle_view_errors
    def update_broker_data(self, broker_id: str, broker_code: str, broker_name: str) -> tuple:
        broker_instance_list: typing.List[Broker] = Broker.query(Broker.broker_id == broker_id).fetch()
        if isinstance(broker_instance_list, list) and len(broker_instance_list) > 0:
            broker_instance: Broker = broker_instance_list[0]
            broker_instance.broker_id = broker_id
            broker_instance.broker_code = broker_code
            broker_instance.broker_name = broker_name
            key = broker_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is not None:
                return jsonify({'status': True, 'payload': broker_instance.to_dict(),
                                'message': 'broker instance updated successfully'}), 200
            else:
                message: str = 'while updating broker something snapped'
                raise DataServiceError(message)

    @use_context
    @handle_view_errors
    def update_stock_model(self, stock_model: dict) -> tuple:
        if 'transaction_id' in stock_model and stock_model['transaction_id'] != "":
            transaction_id: typing.Union[str, None] = stock_model.get('transaction_id')
        else:
            return jsonify({'status': False, 'message': 'transaction_id is required'}), 500

        if 'exchange_id' in stock_model and stock_model['exchange_id'] != "":
            exchange_id: typing.Union[str, None] = stock_model.get('exchange_id')
        else:
            return jsonify({'status': False, 'message': 'exchange_id is required'}), 500

        if 'stock' in stock_model and stock_model['stock'] != "":
            stock: typing.Union[Stock, None] = stock_model.get('stock')
        else:
            return jsonify({'status': False, 'message': 'stock is required'}), 500

        if 'broker' in stock_model and stock_model['broker'] != "":
            broker: typing.Union[Broker, None] = stock_model.get('broker')
        else:
            return jsonify({'status': False, 'message': 'Broker is required'}), 500
        # TODO fix bug Stock and Broker would Dicts not Instances of Stock and Broker
        stock_model_instance: StockModel = StockModel.query(StockModel.transaction_id == transaction_id).get()

        if stock is not None:
            stock_instance: Stock = Stock.query(Stock.stock_code == stock['stock_code']).get()
        else:
            return jsonify({'status': False, 'message': 'stock is required'}), 500

        if broker is not None:
            broker_instance: Broker = Broker.query(Broker.broker_code == broker['broker_code']).get()
        else:
            return jsonify({'status': False, 'message': 'Broker is required'}), 500

        if isinstance(stock_model_instance, StockModel):
            stock_model = stock_model_instance
            stock_model.transaction_id = transaction_id
            stock_model.exchange_id = exchange_id
            stock_model.stock = stock_instance
            stock_model.broker = broker_instance
            key = stock_model.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is not None:
                return jsonify({'status': True, 'payload': stock_model.to_dict(),
                                'message': 'stock model is update'}), 200
            else:
                message: str = 'Something snapped while updating stock model'
                raise DataServiceError(message)
        else:
            return jsonify({'status': False, 'message': 'Stock Model not found'}), 500

    @data_wrappers.get_buy_volume_data
    @use_context
    @handle_view_errors
    def update_buy_volume(self, stock_id: str, date_created: date_class, buy_volume: int, buy_value: int,
                          buy_ave_price: int, buy_market_val_percent: int,
                          buy_trade_count: int, transaction_id: str) -> tuple:
        buy_transactions_list: typing.List[BuyVolumeModel] = BuyVolumeModel.query(
            BuyVolumeModel.transaction_id == transaction_id).fetch()
        if isinstance(buy_transactions_list, list) > 0:
            buy_instance: BuyVolumeModel = buy_transactions_list[0]
            buy_instance.stock_id = stock_id
            buy_instance.date_created = date_created
            buy_instance.buy_volume = buy_volume
            buy_instance.buy_value = buy_value
            buy_instance.buy_ave_price = buy_ave_price
            buy_instance.buy_market_val_percent = buy_market_val_percent
            buy_instance.buy_trade_count = buy_trade_count
            key = buy_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "For some strange reason we could not save your data to database"
                raise DataServiceError(message)
        else:
            return jsonify({'status': False, 'message': 'buy volume not found'}), 500

        return jsonify({"status": True, "message": "successfully updated buy volume",
                        "payload": buy_instance.to_dict()})

    @data_wrappers.get_sell_volume_data
    @use_context
    @handle_view_errors
    def update_sell_volume(self, stock_id: str, date_created: date_class, sell_volume: int, sell_value: int,
                           sell_ave_price: int, sell_market_val_percent: int,
                           sell_trade_count: int, transaction_id: str) -> tuple:
        sell_volume_instance: SellVolumeModel = SellVolumeModel.query(
            SellVolumeModel.transaction_id == transaction_id).get()

        if isinstance(sell_volume_instance, SellVolumeModel):
            sell_volume_instance.stock_id = stock_id
            sell_volume_instance.date_created = date_created
            sell_volume_instance.sell_volume = sell_volume
            sell_volume_instance.sell_value = sell_value
            sell_volume_instance.sell_ave_price = sell_ave_price
            sell_volume_instance.sell_market_val_percent = sell_market_val_percent
            sell_volume_instance.sell_trade_count = sell_trade_count
            sell_volume_instance.transaction_id = transaction_id
            key = sell_volume_instance.put(retries=self._max_retries, timeout=self._max_timeout)

            if key is not None:
                return jsonify({'status': True, 'payload': sell_volume_instance.to_dict(),
                                'message': 'sell volume successfully updated'}), 200
            else:
                message: str = "something snapped updating sell volume"
                raise DataServiceError(message)

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_stock_data(self, stock_id: typing.Union[str, None] = None, stock_code: typing.Union[str, None] = None,
                       symbol: typing.Union[str, None] = None) -> tuple:
        """
            with either stock_id or stock_code or symbol return stock_data
        """
        if stock_id is not None:
            stock_instance: Stock = Stock.query(Stock.stock_id == stock_id).get()
        elif stock_code is not None:
            stock_instance: Stock = Stock.query(Stock.stock_code == stock_code).get()
        elif symbol is not None:
            stock_instance: Stock = Stock.query(Stock.symbol == symbol).get()
        else:
            return jsonify({"status": False, "message": "Stock not found", }), 500

        if isinstance(stock_instance, Stock):
            return jsonify({"status": True, "payload": stock_instance.to_dict(),
                            "message": "successfully fetched stock data with stock_id"}), 200

        return jsonify({"status": False, "message": "Stock not found", }), 500

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_all_stocks(self) -> tuple:
        stock_list: typing.List[dict] = [stock.to_dict() for stock in Stock.query().fetch()]
        return jsonify({"status": True, "payload": stock_list, "message": "stocks returns"}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_broker_data(self, broker_id: str = None, broker_code: str = None) -> tuple:
        """
            with either broker_id or broker_code return broker data
        """
        if broker_id is not None:
            broker_instance: Broker = Broker.query(Broker.broker_id == broker_id).get()
        elif broker_code is not None:
            broker_instance: Broker = Broker.query(Broker.broker_code == broker_code).get()
        else:
            return jsonify({"status": False, "message": "Broker not found"}), 500
        return jsonify({"status": True, "payload": broker_instance.to_dict(),
                        "message": "successfully fetched broker data"}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_all_brokers(self) -> tuple:
        brokers_list: typing.List[dict] = [broker.to_dict() for broker in Broker.query().fetch()]
        return jsonify({
            "status": True,
            "payload": brokers_list,
            "message": "successfully fetched all brokers"}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_stock_model(self, transaction_id: str = None) -> tuple:
        if transaction_id is None:
            return jsonify({"status": False, "message": "transaction id is required"}), 500

        stock_model: StockModel = StockModel.query(StockModel.transaction_id == transaction_id).get()
        if isinstance(stock_model, StockModel):
            return jsonify({"status": False, "message": "stock found", "payload": stock_model.to_dict()}), 200

        return jsonify({"status": False, "message": "that transaction does not exist"}), 500

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_all_stock_models(self) -> tuple:
        """
            return stock models
        """
        stock_model_list: typing.List[dict] = [stock_model.to_dict() for stock_model in StockModel.query().fetch()]
        return jsonify({
            "status": True,
            "payload": stock_model_list,
            "message": "successfully fetched all stock model data"}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_buy_volume(self, transaction_id: str = None, date_created: date_class = None,
                       stock_id: str = None) -> tuple:
        """
            get a specific buy volume filtered by transaction_id or
            by date_class and stock_id
        """
        if transaction_id is not None:
            buy_volume: BuyVolumeModel = BuyVolumeModel.query(BuyVolumeModel.transaction_id == transaction_id).get()
        elif date_created is not None:
            # for a specific date_class buy volume should be filtered by stock
            buy_volume: BuyVolumeModel = BuyVolumeModel.query(
                BuyVolumeModel.date_created == date_created, BuyVolumeModel.stock_id == stock_id).get()
        else:
            message: str = "transaction id or transaction date_class need to be specified"
            return jsonify({"status": False, "message": message}), 500
        message: str = "buy volume data successfully found"
        return jsonify({"status": True, "payload": buy_volume.to_dict(), "message": message}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_day_buy_volumes(self, date_created: typing.Union[date_class, None] = None) -> tuple:
        """
            return buy volumes for all stocks for a specific date_class
        """
        if date_created is None:
            return jsonify({'status': True, 'message': 'date is required'}), 500

        buy_volume_list: typing.List[BuyVolumeModel] = BuyVolumeModel.query(
            BuyVolumeModel.date_created == date_created).fetch()
        payload: typing.List[dict] = [buy_volume.to_dict() for buy_volume in buy_volume_list]
        message: str = "successfully fetched day buy volume data"
        return jsonify({"status": True, "payload": payload, "message": message}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_daily_buy_volumes_by_stock(self, stock_id: typing.Union[str, None] = None) -> tuple:
        """
            for a specific stock return daily buy volumes
        """
        if stock_id is None:
            return jsonify({'status': False, 'message': 'Stock ID cannot be None'}), 500

        buy_volume_list: typing.List[BuyVolumeModel] = BuyVolumeModel.query(
            BuyVolumeModel.stock_id == stock_id).fetch()
        payload: typing.List[dict] = [buy_volume.to_dict() for buy_volume in buy_volume_list]
        message: str = "successfully daily buy volumes by stock"
        return jsonify({"status": True, "payload": payload, "message": message}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_sell_volume(self, transaction_id: typing.Union[str, None] = None,
                        date_created: typing.Union[None, date_class] = None,
                        stock_id: typing.Union[str, None] = None) -> tuple:
        """
            for a specific transaction_id return the related transaction_id
            or for date_class and stock_id return a specific sell_volume
        """
        if transaction_id is not None:
            sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(
                SellVolumeModel.transaction_id == transaction_id).fetch()

        elif (date_class is not None) and (stock_id is not None):
            sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(
                SellVolumeModel.date_created == date_created, SellVolumeModel.stock_id == stock_id).fetch()
        else:
            return jsonify({"status": False, "message": "sell volume not found"}), 500

        if len(sell_volume_list) > 0:
            sell_volume_instance: SellVolumeModel = sell_volume_list[0]
            message: str = "successfully found sell volume"
            return jsonify({"status": True,
                            "payload": sell_volume_instance.to_dict(),
                            "message": message}), 200

        return jsonify({"status": False, "message": "sell volume not found"}), 500

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_day_sell_volumes(self, date_created: date_class) -> tuple:
        """
            fetch all daily sell volumes
        """
        sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(
            SellVolumeModel.date_created == date_created).fetch()
        sell_volumes: typing.List[dict] = [sell_volume.to_dict() for sell_volume in sell_volume_list]
        message: str = "day sell volumes returned"
        return jsonify({"status": False, "payload": sell_volumes, "message": message}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_daily_sell_volumes_by_stock(self, stock_id: typing.Union[str, None] = None) -> tuple:
        if stock_id is None:
            return jsonify({'status': False, "message": "stock_id cannot be None"}), 500

        sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(
            SellVolumeModel.stock_id == stock_id).fetch()

        payload: typing.List[dict] = [sell_volume.to_dict() for sell_volume in sell_volume_list]
        message: str = "successfully fetched sell volume by stock"
        return jsonify({'status': False, "payload": payload, "message": message}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_net_volume(self, transaction_id: typing.Union[str, None] = None,
                       date_created: typing.Union[date_class, None] = None,
                       stock_id: typing.Union[str, None] = None) -> tuple:

        if transaction_id is not None:
            net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                NetVolumeModel.transaction_id == transaction_id).fetch()
        elif date_class and stock_id:
            net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                NetVolumeModel.date_created == date_created, NetVolumeModel.stock_id == stock_id).fetch()
        else:
            message: str = "net volume data not found"
            return jsonify({"status": False, "message": message}), 500

        payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
        message: str = "successfully fetched net volume"
        return jsonify({"status": True, "payload": payload, "message": message}), 200

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_day_net_volumes(self, date_created: typing.Union[date_class, None] = None) -> tuple:
        if date_class is not None:
            net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                NetVolumeModel.date_created == date_created).fetch()

            payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
        else:
            message: str = "day net volume data not found"
            return jsonify({"status": False, "message": message}), 500

        message: str = "day net volume data not found"
        return jsonify({"status": True, "payload": payload, "message": message}), 500

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_daily_net_volumes_by_stock(self, stock_id: typing.Union[str, None] = None) -> tuple:
        if stock_id is not None:
            net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                NetVolumeModel.stock_id == stock_id).fetch()
            payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
        else:
            message: str = "daily net volume data not found"
            return jsonify({"status": False, "message": message}), 500

        message: str = "daily net volume data not found"
        return jsonify({"status": True, "payload": payload, "message": message}), 500
