import functools
import typing
import functools
from google.cloud import ndb
import datetime
from flask import current_app, jsonify
from data_service.store.stocks import Stock, Broker, StockModel, BuyVolumeModel, SellVolumeModel, NetVolumeModel
from data_service.utils.utils import date_string_to_date, create_id
from data_service.config import Config

stock_list_type = typing.List[Stock]

# NOTES: request wrappers for stock, broker, buy_volume sell_volume, and net_volume
def get_stock_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stock_data: dict = kwargs.get('stock_data')
        if 'stock_id' in stock_data and stock_data['stock_id'] != "":
            stock_id: str = stock_data.get('stock_id') or None
        else:
            stock_id = create_id(size=12)
        if 'stock_code' in stock_data and stock_data['stock_code'] != "":
            stock_code: str = stock_data.get('stock_code') or None
        else:
            return jsonify({'status': False, 'message': 'Stock Code is required'}), 500

        if 'stock_name' in stock_data and stock_data['stock_name'] != "":
            stock_name: str = stock_data.get('stock_name') or None
        else:
            return jsonify({'status': False, 'message': 'Stock Name is required'}), 500
        if 'symbol' in stock_data and stock_data['symbol'] != "":
            symbol: str = stock_data.get('symbol') or None
        else:
            return jsonify({'status': False, 'message': 'Stock Symbol is required'}), 500

        return func(stock_id=stock_id, stock_code=stock_code, stock_name=stock_name, symbol=symbol, *args)

    return wrapper

def get_broker_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        broker_data: dict = kwargs.get('broker_data')
        if "broker_id" in broker_data and broker_data['broker_id'] != "":
            broker_id: str = broker_data.get('broker_id') or None
        else:
            broker_id: str = create_id(size=12)
        if "broker_code" in broker_data and broker_data['broker_code'] != "":
            broker_code: str = broker_data.get('broker_code') or None
        else:
            return jsonify({'status': False, 'message': 'Broker Code is required'}), 500
        if "broker_name" in broker_data and broker_data['broker_name'] != "":
            broker_name: str = broker_data.get("broker_name")
        else:
            return jsonify({'status': False, 'message': 'Broker Name is required'}), 500

        return func(broker_id=broker_id, broker_code=broker_code, broker_name=broker_name, *args)

    return wrapper

def get_buy_volume_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        buy_data: dict = kwargs.get('buy_data')
        if not isinstance(buy_data, dict):
            return jsonify({'status': False, 'message': 'Please provide buy volume data'}), 500

        if "stock_id" in buy_data and buy_data['stock_id'] != "":
            stock_id: str = buy_data.get('stock_id') or None
        else:
            return jsonify({'status': False, 'message': "stock id is required"}), 500
        if "date" in buy_data and buy_data['date'] != "":
            # TODO- insure that FORMAT is DD_MM-YYYY
            try:
                date: object = date_string_to_date(buy_data.get('date'))
            except ValueError:
                date: object = datetime.date(datetime.datetime.now())
        else:
            return jsonify({'status': False, 'message': "date is required"}), 500

        if "buy_volume" in buy_data and buy_data['buy_volume'] != "":
            buy_volume: int = int(buy_data.get('buy_volume'))
        else:
            return jsonify({'status': False, 'message': "buy volume is required"}), 500

        if "buy_value" in buy_data and buy_data["buy_value"] != "":
            buy_value: int = int(buy_data.get("buy_value"))
        else:
            return jsonify({'status': False, 'message': "buy value is required"}), 500

        if "buy_ave_price" in buy_data and buy_data["buy_ave_price"] != "":
            buy_ave_price: int = int(buy_data.get("buy_ave_price"))
        else:
            return jsonify({'status': False, 'message': "buy average price is required"}), 500

        if "buy_market_val_percent" in buy_data and buy_data["buy_market_val_percent"] != "":
            buy_market_val_percent: int = int(buy_data.get("buy_market_val_percent"))
        else:
            return jsonify({'status': False, 'message': "buy market value percent is required"}), 500

        if "buy_trade_count" in buy_data and buy_data["buy_trade_count"] != "":
            buy_trade_count: int = int(buy_data.get("buy_trade_count"))
        else:
            return jsonify({'status': False, 'message': "buy trade account"}), 500

        if "transaction_id" in buy_data and buy_data["transaction_id"] != "":
            transaction_id: str = buy_data.get("transaction_id")

            return func(stock_id=stock_id, date=date, buy_volume=buy_volume,
                        buy_value=buy_value, buy_ave_price=buy_ave_price,
                        buy_market_val_percent=buy_market_val_percent, buy_trade_count=buy_trade_count,
                        transaction_id=transaction_id, *args)

        return func(stock_id=stock_id, date=date, buy_volume=buy_volume,
                    buy_value=buy_value, buy_ave_price=buy_ave_price,
                    buy_market_val_percent=buy_market_val_percent, buy_trade_count=buy_trade_count, *args)

    return wrapper

def get_sell_volume_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        sell_data: dict = kwargs.get('sell_data')
        if sell_data is None:
            return jsonify({'status': False, 'message': 'Unable to get sell volume data'}), 500

        if "stock_id" in sell_data and sell_data['stock_id'] != "":
            stock_id: str = sell_data.get('stock_id') or None
        else:
            return jsonify({'status': False, 'message': "stock id is required"}), 500

        if "date" in sell_data and sell_data["date"] != "":
            try:
                date: object = date_string_to_date(sell_data.get('date'))
            except ValueError:
                date: object = datetime.datetime.date(datetime.datetime.now())
        else:
            return jsonify({'status': False, 'message': "date is required"}), 500

        if "sell_volume" in sell_data and sell_data["sell_volume"] != "":
            sell_volume: int = int(sell_data.get("sell_volume"))
        else:
            return jsonify({"status": False, "message": "sell volume is required"}), 500

        if "sell_value" in sell_data and sell_data["sell_value"] != "":
            sell_value: int = int(sell_data.get("sell_value"))
        else:
            return jsonify({"status": False, "message": "sell value is required"}), 500

        if "sell_ave_price" in sell_data and sell_data["sell_ave_price"] != "":
            sell_ave_price: int = int(sell_data.get("sell_ave_price"))
        else:
            return jsonify({"status": False, "message": "sell ave price is required"}), 500

        if "sell_market_val_percent" in sell_data and sell_data["sell_market_val_percent"] != "":
            sell_market_val_percent: int = int(sell_data.get("sell_market_val_percent"))
        else:
            return jsonify({"status": False, "message": "sell market value percent price is required"}), 500

        if "sell_trade_count" in sell_data and sell_data["sell_trade_count"] != "":
            sell_trade_count: int = int(sell_data.get("sell_trade_count"))
        else:
            return jsonify({"status": False, "message": "sell trade account percent price is required"}), 500
        if 'transaction_id' in sell_data and sell_data['transaction_id'] != "":
            transaction_id: str = sell_data['transaction_id']

            return func(stock_id=stock_id, date=date, sell_volume=sell_volume, sell_value=sell_value,
                        sell_ave_price=sell_ave_price, sell_market_val_percent=sell_market_val_percent,
                        sell_trade_count=sell_trade_count, transaction_id=transaction_id, *args)

        return func(stock_id=stock_id, date=date, sell_volume=sell_volume, sell_value=sell_value,
                    sell_ave_price=sell_ave_price, sell_market_val_percent=sell_market_val_percent,
                    sell_trade_count=sell_trade_count, *args)

    return wrapper

def get_net_volume_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        net_volume_data: dict = kwargs.get('net_volume_data')

        if net_volume_data is None:
            return jsonify({'status': False, 'message': 'please define net volume data'}), 500

        if "stock_id" in net_volume_data and net_volume_data["stock_id"] != "":
            stock_id: str = net_volume_data.get("stock_id") or None
        else:
            return jsonify({'status': False, 'message': "stock id is required"}), 500
        if "date" in net_volume_data and net_volume_data['date'] != "":
            # assumed format DD/MM/YYYY
            date: object = date_string_to_date(net_volume_data['date'])
        else:
            return jsonify({'status': False, 'message': "date is required"}), 500

        if "transaction_id" in net_volume_data and net_volume_data["transaction_id"] != "":
            transaction_id: str = net_volume_data.get("transaction_id") or None
        else:
            return jsonify({'status': False, 'message': "transaction id is required"}), 500

        if "net_volume" in net_volume_data and net_volume_data["net_volume"] != "":
            net_volume: int = int(net_volume_data.get("net_volume"))
        else:
            return jsonify({'status': False, 'message': "net volume is required"}), 500

        if "net_value" in net_volume_data and net_volume_data["net_value"] != "":
            net_value: int = int(net_volume_data.get("net_value"))
        else:
            return jsonify({'status': False, 'message': "net value is required"}), 500

        if "total_value" in net_volume_data and net_volume_data["total_value"] != "":
            total_value: int = int(net_volume_data.get("total_value"))
        else:
            return jsonify({'status': False, 'message': "total value is required"}), 500

        if "total_volume" in net_volume_data and net_volume_data["total_volume"] != "":
            total_volume: int = int(net_volume_data.get('total_volume'))
        else:
            return jsonify({'status': False, 'message': "total volume is required"}), 500

        return func(stock_id=stock_id, date=date, transaction_id=transaction_id, net_volume=net_volume,
                    net_value=net_value,
                    total_value=total_value, total_volume=total_volume, *args)

    return wrapper


class StockViewContext:
    """
        add common variables here
    """

    def __int__(self):
        pass


class CatchStockErrors(StockViewContext):
    def __int__(self):
        super(CatchStockErrors, self).__int__()

    @staticmethod
    def symbol_exist(symbol: str) -> bool:
        stock_list: stock_list_type = Stock.query(Stock.symbol == symbol).fetch()
        if isinstance(stock_list, list) and len(stock_list) > 0:
            return True
        return False

    @staticmethod
    def stock_code_exist(stock_code: str) -> bool:
        stock_list: stock_list_type = Stock.query(Stock.stock_code == stock_code).fetch()
        if isinstance(stock_list, list) and len(stock_list) > 0:
            return True
        return False

    @staticmethod
    def stock_id_exist(stock_id: str) -> bool:
        stock_list: stock_list_type = Stock.query(Stock.stock_id == stock_id).fetch()
        if isinstance(stock_list, list) and len(stock_list) > 0:
            return True
        return False

    def can_add_stock(self, stock_code: str, symbol: str, stock_id: str = None) -> bool:
        if stock_id is None or stock_id == "":
            return False

        if stock_code is None or stock_code == "":
            return False

        if symbol is None or symbol == "":
            return False

        if self.stock_id_exist(stock_id=stock_id):
            return False

        if self.stock_code_exist(stock_code=stock_code):
            return False
        if self.symbol_exist(symbol=symbol):
            return False

        return True


class CatchBrokerErrors(StockViewContext):
    def __int__(self):
        super(CatchBrokerErrors, self).__init__()

    @staticmethod
    def broker_id_exist(broker_id: str) -> bool:
        broker_list: typing.List[Broker] = Broker.query(Broker.broker_id == broker_id).fetch()
        if isinstance(broker_list, list) and len(broker_list) > 0:
            return True
        return False

    @staticmethod
    def broker_code_exist(broker_code: str) -> bool:
        broker_list: typing.List[Broker] = Broker.query(Broker.broker_code == broker_code).fetch()
        if isinstance(broker_list, list) and len(broker_list) > 0:
            return True
        return False

    def can_add_broker(self, broker_id: str, broker_code: str) -> bool:
        if self.broker_id_exist(broker_id=broker_id) or self.broker_code_exist(broker_code=broker_code):
            return False
        return True


class StockView(CatchStockErrors, CatchBrokerErrors):
    def __init__(self):
        super(StockView, self).__init__()
        self.client = ndb.Client(namespace="main", project="pinoydesk")
        with current_app.app_context():
            self.timezone = datetime.timezone(Config.UTC_OFFSET)

    @get_stock_data
    def create_stock_data(self, stock_id, stock_code, stock_name, symbol) -> tuple:
        with self.client.context():
            try:
                if self.can_add_stock(stock_code=stock_code, stock_id=stock_id, symbol=symbol):
                    stock_instance: Stock = Stock(stock_id=stock_id, stock_code=stock_code, stock_name=stock_name,
                                                  symbol=symbol)
                    key = stock_instance.put()
                    if key is None:
                        message: str = "For some strange reason we could not save your data to database"
                        return jsonify({'status': False, 'message': message}), 500

                else:
                    message: str = "Stock Duplicate detected, you cannot add duplicate stock in here"
                    return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except TypeError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

            return jsonify({'status': True,
                            'message': 'successfully saved stock data',
                            "payload": {"stock_instance": stock_instance.to_dict()}}), 200

    @get_broker_data
    def create_broker_data(self, broker_id: str, broker_code: str, broker_name: str) -> tuple:
        with self.client.context():
            try:
                if self.can_add_broker(broker_id=broker_id, broker_code=broker_code):
                    broker_instance: Broker = Broker(broker_id=broker_id, broker_code=broker_code,
                                                     broker_name=broker_name)
                    key = broker_instance.put()
                    if key is None:
                        message: str = "For some strange reason we could not save your data to database"
                        return jsonify({'status': False, 'message': message}), 500

                else:
                    message: str = "cannot create broker data, duplicates would be created"
                    return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except TypeError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

            return jsonify({'status': True, 'message': 'successfully saved broker data',
                            'payload': broker_instance.to_dict()}), 200

    def create_stock_model(self, exchange_id: str, sid: str, stock_id: str, broker_id: str) -> tuple:
        with self.client.context():
            try:
                stock_list: typing.List[Stock] = Stock.query(Stock.stock_id == stock_id).fetch()
                stock: Stock = stock_list[0]
                broker_list: typing.List[Broker] = Broker.query(Broker.broker_id == broker_id).fetch()
                broker: Broker = broker_list[0]
                stock_model_instance: StockModel = StockModel(exchange_id=exchange_id,
                                                              sid=sid, stock=stock, broker=broker)
                key = stock_model_instance.put()
                if key is None:
                    message: str = "For some strange reason we could not save your data to database"
                    return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except KeyError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            return jsonify({'status': True, 'message': 'Stock Model Successfully created',
                            'payload': stock_model_instance.to_dict()}), 200

    @get_buy_volume_data
    def create_buy_model(self, stock_id: str, date: object, buy_volume: int, buy_value: int,
                         buy_ave_price: int, buy_market_val_percent: int,
                         buy_trade_count: int) -> tuple:

        with self.client.context():
            try:
                buy_volume_instance: BuyVolumeModel = BuyVolumeModel(stock_id=stock_id, date=date,
                                                                     buy_volume=buy_volume, buy_value=buy_value,
                                                                     buy_ave_price=buy_ave_price,
                                                                     buy_market_val_percent=buy_market_val_percent,
                                                                     buy_trade_count=buy_trade_count)
                key = buy_volume_instance.put()
                if key is None:
                    message: str = "For some strange reason we could not save your data to database"
                    return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

            message: str = "Buy volume successfully created"
            return jsonify({'status': True, 'message': message, 'payload': buy_volume_instance.to_dict()}), 200

    @get_sell_volume_data
    def create_sell_volume(self, stock_id: str, date: object, sell_volume: int, sell_value: int,
                           sell_ave_price: int, sell_market_val_percent: int,
                           sell_trade_count: int) -> tuple:
        with self.client.context():
            try:
                sell_volume_instance: SellVolumeModel = SellVolumeModel(stock_id=stock_id,
                                                                        date=date,
                                                                        sell_volume=sell_volume,
                                                                        sell_value=sell_value,
                                                                        sell_ave_price=sell_ave_price,
                                                                        sell_market_val_percent=sell_market_val_percent,
                                                                        sell_trade_count=sell_trade_count)
                key = sell_volume_instance.put()
                if key is None:
                    message: str = "For some strange reason we could not save your data to database"
                    return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

            return jsonify({'status': True, 'message': 'Sell Volume Successfully created',
                            'payload': sell_volume_instance.to_dict()}), 200

    # noinspection DuplicatedCode
    @get_net_volume_data
    def create_net_volume(self, stock_id: str, date: object, transaction_id: str, net_volume: str, net_value: str,
                          total_value: str, total_volume: str) -> tuple:
        """
            if net volume already exist update net volume
        """

        with self.client.context():
            try:
                net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                    NetVolumeModel.transaction_id == transaction_id).fetch()
                if isinstance(net_volume_list, list) and len(net_volume_list) > 0:
                    net_volume_instance: NetVolumeModel = net_volume_list[0]
                else:
                    net_volume_instance: NetVolumeModel = NetVolumeModel()

                net_volume_instance.stock_id = stock_id
                net_volume_instance.transaction_id = transaction_id
                net_volume_instance.date = date
                net_volume_instance.net_volume = net_volume
                net_volume_instance.net_value = net_value
                net_volume_instance.total_value = total_value
                net_volume_instance.total_volume = total_volume

                key = net_volume_instance.put()
                if key is None:
                    message: str = "For some strange reason we could not save your data to database"
                    return jsonify({'status': False, 'message': message}), 500
            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

            message: str = 'Net Volume Successfully created'
            return jsonify({'status': True, 'message': message,
                            'payload': net_volume_instance.to_dict()}), 200

    @get_stock_data
    def update_stock_data(self, stock_id, stock_code, stock_name, symbol) -> tuple:
        with self.client.context():
            try:
                stock_instance_list: typing.List[Stock] = Stock.query(Stock.stock_id == stock_id).fetch()
                if len(stock_instance_list) > 0:
                    stock_instance: Stock = stock_instance_list[0]
                    stock_instance.stock_id = stock_id
                    stock_instance.stock_code = stock_code
                    stock_instance.stock_name = stock_name
                    stock_instance.symbol = symbol
                    key = stock_instance.put()
                    if key is not None:
                        return jsonify({'status': True, 'payload': stock_instance.to_dict(),
                                        'message': 'successfully updated stock'}), 200
                    else:
                        return jsonify({'status': False, 'message': 'Something snapped'}), 500
                else:
                    message: str = "Could not find stock please try again later"
                    return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except KeyError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

    @get_broker_data
    def update_broker_data(self, broker_id: str, broker_code: str, broker_name: str) -> tuple:
        with self.client.context():
            try:
                broker_instance_list: typing.List[Broker] = Broker.query(Broker.broker_id == broker_id).fetch()
                if isinstance(broker_instance_list, list) and len(broker_instance_list) > 0:
                    broker_instance: Broker = broker_instance_list[0]
                    broker_instance.broker_id = broker_id
                    broker_instance.broker_code = broker_code
                    broker_instance.broker_name = broker_name
                    key = broker_instance.put()
                    if key is not None:
                        return jsonify({'status': True, 'payload': broker_instance.to_dict(),
                                        'message': 'broker instance updated successfully'}), 200
                    else:
                        return jsonify({'status': False, 'message': 'while updating broker something snapped'}), 500

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except KeyError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

    def update_stock_model(self, stock_model: dict) -> tuple:
        with self.client.context():
            if 'transaction_id' in stock_model and stock_model['transaction_id'] != "":
                transaction_id: str = stock_model['transaction_id']
            else:
                return jsonify({'status': False, 'message': 'transaction_id is required'}), 500

            if 'exchange_id' in stock_model and stock_model['exchange_id'] != "":
                exchange_id: str = stock_model['exchange_id']
            else:
                return jsonify({'status': False, 'message': 'exchange_id is required'}), 500

            if 'stock' in stock_model and stock_model['stock'] != "":
                stock: Stock = stock_model['stock']
            else:
                return jsonify({'status': False, 'message': 'stock is required'}), 500

            if 'broker' in stock_model and stock_model['broker'] != "":
                broker: Broker = stock_model['broker']
            else:
                return jsonify({'status': False, 'message': 'Broker is required'}), 500
            try:
                stock_model_list: typing.List[StockModel] = StockModel.query(
                    StockModel.transaction_id == transaction_id).fetch()

                if isinstance(stock_model_list, list) and len(stock_model_list) > 0:
                    stock_model = stock_model_list[0]
                    stock_model.transaction_id = transaction_id
                    stock_model.exchange_id = exchange_id
                    stock_model.stock = stock
                    stock_model.broker = broker
                    key = stock_model.put()
                    if key is not None:
                        return jsonify({'status': True, 'payload': stock_model.to_dict(),
                                        'message': 'stock model is update'}), 200
                    else:
                        return jsonify(
                            {'status': False, 'message': 'Something snapped while updating stock model'}), 500
                else:
                    return jsonify({'status': False, 'message': 'Stock Model not found'}), 500

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except KeyError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

    @get_buy_volume_data
    def update_buy_volume(self, stock_id: str, date: object, buy_volume: int, buy_value: int,
                          buy_ave_price: int, buy_market_val_percent: int,
                          buy_trade_count: int, transaction_id: str) -> tuple:

        with self.client.context():
            try:
                buy_transactions_list: typing.List[BuyVolumeModel] = BuyVolumeModel.query(
                    BuyVolumeModel.transaction_id == transaction_id).fetch()
                if isinstance(buy_transactions_list, list) > 0:
                    buy_instance: BuyVolumeModel = buy_transactions_list[0]
                    buy_instance.stock_id = stock_id
                    buy_instance.date = date
                    buy_instance.buy_volume = buy_volume
                    buy_instance.buy_value = buy_value
                    buy_instance.buy_ave_price = buy_ave_price
                    buy_instance.buy_market_val_percent = buy_market_val_percent
                    buy_instance.buy_trade_count = buy_trade_count
                    key = buy_instance.put()
                    if key is None:
                        message: str = "For some strange reason we could not save your data to database"
                        return jsonify({'status': False, 'message': message}), 500
                else:
                    return jsonify({'status': False, 'message': 'buy volume not found'}), 500

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except KeyError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

            return jsonify({"status": True, "message": "successfully updated buy volume",
                            "payload": buy_instance.to_dict()})

    @get_sell_volume_data
    def update_sell_volume(self, stock_id: str, date: object, sell_volume: int, sell_value: int,
                           sell_ave_price: int, sell_market_val_percent: int,
                           sell_trade_count: int, transaction_id: str) -> tuple:

        with self.client.context():

            try:
                sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(
                    SellVolumeModel.transaction_id == transaction_id).fetch()

                if isinstance(sell_volume_list, list) and len(sell_volume_list) > 0:
                    sell_volume_instance: SellVolumeModel = sell_volume_list[0]
                    sell_volume_instance.stock_id = stock_id
                    sell_volume_instance.date = date
                    sell_volume_instance.sell_volume = sell_volume
                    sell_volume_instance.sell_value = sell_value
                    sell_volume_instance.sell_ave_price = sell_ave_price
                    sell_volume_instance.sell_market_val_percent = sell_market_val_percent
                    sell_volume_instance.sell_trade_count = sell_trade_count
                    sell_volume_instance.transaction_id = transaction_id
                    key = sell_volume_instance.put()

                    if key is not None:
                        return jsonify({'status': True, 'payload': sell_volume_instance.to_dict(),
                                        'message': 'sell volume successfully updated'}), 200
                    else:
                        return jsonify({'status': False, 'message': 'something snapped updating sell volume'}), 500

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except KeyError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

    def get_stock_data(self, stock_id: str = None, stock_code: str = None, symbol: str = None) -> tuple:
        """
            with either stock_id or stock_code or symbol return stock_data
        """
        with self.client.context():
            if stock_id is not None:
                stock_list: typing.List[dict] = [stock.to_dict() for stock in
                                                 Stock.query(Stock.stock_id == stock_id).fetch()]
            elif stock_code is not None:
                stock_list: typing.List[dict] = [stock.to_dict() for stock in
                                                 Stock.query(Stock.stock_code == stock_code).fetch()]
            elif symbol is not None:
                stock_list: typing.List[dict] = [stock.to_dict() for stock in
                                                 Stock.query(Stock.symbol == symbol).fetch()]

            else:
                return jsonify({
                    "status": False,
                    "message": "Stock not found",
                }), 500

            if len(stock_list) > 0:
                return jsonify({
                    "status": True,
                    "payload": stock_list[0],
                    "message": "successfully fetched stock data with stock_id"
                }), 200

            return jsonify({
                "status": False,
                "message": "Stock not found",
            }), 500

    def get_all_stocks(self) -> tuple:
        with self.client.context():
            stock_list: typing.List[dict] = [stock.to_dict() for stock in Stock.query().fetch()]
            return jsonify({"status": True, "payload": stock_list, "message": "stocks returns"}), 200

    def get_broker_data(self, broker_id: str = None, broker_code: str = None) -> tuple:
        """
            with either broker_id or broker_code return broker data
        """
        with self.client.context():
            if broker_id is not None:
                broker_list: typing.List[dict] = [broker.to_dict() for broker in Broker.query(
                    Broker.broker_id == broker_id)]
            elif broker_code is not None:
                broker_list: typing.List[dict] = [broker.to_dict() for broker in Broker.query(
                    Broker.broker_code == broker_code)]
            else:
                return jsonify({
                    "status": False,
                    "message": "Broker not found"
                }), 500

            if len(broker_list) > 0:
                return jsonify({
                    "status": True,
                    "payload": broker_list[0],
                    "message": "successfully fetched broker data"
                }), 200

            return jsonify({
                "status": False,
                "message": "Broker not found"
            }), 500

    def get_all_brokers(self) -> tuple:
        with self.client.context():
            brokers_list: typing.List[dict] = [broker.to_dict() for broker in Broker.query().fetch()]
            return jsonify({
                "status": True,
                "payload": brokers_list,
                "message": "successfully fetched all brokers"}), 200

    def get_stock_model(self, transaction_id: str = None) -> tuple:
        with self.client.context():
            if transaction_id is not None:
                stock_model_list: typing.List[StockModel] = StockModel.query(
                    StockModel.transaction_id == transaction_id).fetch()

                if len(stock_model_list) > 0:
                    return jsonify({
                        "status": False, "message": "stock found",
                        "payload": stock_model_list[0].to_dict()
                    }), 200

                return jsonify({"status": False, "message": "that transaction does not exist"}), 500

            return jsonify({"status": False, "message": "transaction id is required"}), 500

    def get_all_stock_models(self) -> tuple:
        """
            retu
        """
        with self.client.context():
            stock_model_list: typing.List[dict] = [stock_model.to_dict() for stock_model in StockModel.query().fetch()]
            return jsonify({
                "status": True, "payload": stock_model_list,
                "message": "successfully fetched all stock model data"}), 200

    def get_buy_volume(self, transaction_id: str = None, date: object = None, stock_id: str = None) -> tuple:
        """
            get a specific buy volume filtered by transaction_id or
            by date and stock_id
        """
        with self.client.context():
            if transaction_id is not None:
                buy_volume_list: typing.List[BuyVolumeModel] = BuyVolumeModel.query(
                    BuyVolumeModel.transaction_id == transaction_id).fetch()
            elif date is not None:
                # for a specific date buy volume should be filtered by stock
                buy_volume_list: typing.List[BuyVolumeModel] = BuyVolumeModel.query(
                    BuyVolumeModel.date == date, BuyVolumeModel.stock_id == stock_id).fetch()
            else:
                message: str = "transaction id or transaction date need to be specified"
                return jsonify({"status": False, "message": message}), 500
            message: str = "buy volume data successfully found"
            return jsonify({"status": True, "payload": buy_volume_list[0].to_dict(), "message": message}), 200

    def get_day_buy_volumes(self, date: object = None) -> tuple:
        """
            return buy volumes for all stocks for a specific date
        """
        with self.client.context():
            if date is not None:
                buy_volume_list: typing.List[BuyVolumeModel] = BuyVolumeModel.query(
                    BuyVolumeModel.date == date).fetch()
                payload: typing.List[dict] = [buy_volume.to_dict() for buy_volume in buy_volume_list]

            message: str = "successfully fetched day buy volume data"
            return jsonify({"status": True, "payload": payload, "message": message}), 200

    def get_daily_buy_volumes_by_stock(self, stock_id: str = None) -> tuple:
        """
            for a specific stock return daily buy volumes
        """
        with self.client.context():
            buy_volume_list: typing.List[BuyVolumeModel] = BuyVolumeModel.query(
                BuyVolumeModel.stock_id == stock_id).fetch()
            payload: typing.List[dict] = [buy_volume.to_dict() for buy_volume in buy_volume_list]
            message: str = "successfully daily buy volumes by stock"
            return jsonify({"status": True, "payload": payload, "message": message}), 200

    def get_sell_volume(self, transaction_id: str = None, date: object = None, stock_id: str = None) -> tuple:
        """
            for a specific transaction_id return the related transaction_id
            or for date and stock_id return a specific sell_volume
        """
        with self.client.context():
            if transaction_id is not None:
                sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(
                    SellVolumeModel.transaction_id == transaction_id).fetch()

            elif date and stock_id:
                sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(
                    SellVolumeModel.date == date, SellVolumeModel.stock_id == stock_id).fetch()

            else:
                return jsonify({"status": False, "message": "sell volume not found"}), 500

            if len(sell_volume_list) > 0:
                sell_volume_instance: SellVolumeModel = sell_volume_list[0]
                message: str = "successfully found sell volume"
                return jsonify({"status": True,
                                "payload": sell_volume_instance.to_dict(),
                                "message": message}), 200

            return jsonify({"status": False, "message": "sell volume not found"}), 500

    def get_day_sell_volumes(self, date: object) -> tuple:
        """
            fetch all daily sell volumes
        """
        with self.client.context():
            sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(SellVolumeModel.date == date).fetch()
            sell_volumes: typing.List[dict] = [sell_volume.to_dict() for sell_volume in sell_volume_list]
            message: str = "day sell volumes returned"
            return jsonify({"status": False, "payload": sell_volumes, "message": message}), 200

    def get_daily_sell_volumes_by_stock(self, stock_id: str = None) -> tuple:
        with self.client.context():
            sell_volume_list: typing.List[SellVolumeModel] = SellVolumeModel.query(
                SellVolumeModel.stock_id == stock_id).fetch()

            payload: typing.List[dict] = [sell_volume.to_dict() for sell_volume in sell_volume_list]
            message: str = "successfully fetched sell volume by stock"
            return jsonify({'status': False, "payload": payload, "message": message}), 200

    def get_net_volume(self, transaction_id: str = None, date: object = None, stock_id: str = None) -> tuple:
        with self.client.context():

            if transaction_id is not None:
                net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                    NetVolumeModel.transaction_id == transaction_id).fetch()
            elif date and stock_id:
                net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                    NetVolumeModel.date == date, NetVolumeModel.stock_id == stock_id).fetch()
            else:
                message: str = "net volume data not found"
                return jsonify({"status": False, "message": message}), 500

            payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
            message: str = "successfully fetched net volume"
            return jsonify({"status": True, "payload": payload, "message": message}), 200

    def get_day_net_volumes(self, date: object = None) -> tuple:
        with self.client.context():
            if date is not None:
                net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(NetVolumeModel.date == date).fetch()
                payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
            else:
                message: str = "day net volume data not found"
                return jsonify({"status": False, "message": message}), 500

            message: str = "day net volume data not found"
            return jsonify({"status": True, "payload": payload, "message": message}), 500

    def get_daily_net_volumes_by_stock(self, stock_id: str = None) -> tuple:
        with self.client.context():
            if stock_id is not None:
                net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                    NetVolumeModel.stock_id == stock_id).fetch()
                payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
            else:
                message: str = "daily net volume data not found"
                return jsonify({"status": False, "message": message}), 500

            message: str = "daily net volume data not found"
            return jsonify({"status": True, "payload": payload, "message": message}), 500
