import typing
from google.cloud import ndb
import datetime
from flask import current_app, jsonify
from data_service.store.stocks import Stock, Broker, StockModel, BuyVolumeModel, SellVolumeModel, NetVolumeModel
from data_service.utils.utils import date_string_to_date, create_id
from data_service.config import Config
stock_list_type = typing.List[Stock]


class StockView:
    def __init__(self):
        self.client = ndb.Client(namespace="main", project="pinoydesk")
        with current_app.app_context():
            self.timezone = datetime.timezone(Config.UTC_OFFSET)

    def create_stock_data(self, stock_data: dict) -> tuple:
        with self.client.context():

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
            try:
                stock_instance: Stock = Stock(stock_id=stock_id, stock_code=stock_code, stock_name=stock_name,
                                              symbol=symbol)
                key = stock_instance.put()

            except ValueError as e:
                return jsonify({'status': False, 'message': e}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': e}), 500

            return jsonify({'status': True,
                            'message': 'successfully saved stock data',
                            "payload": {"stock_instance": stock_instance.to_dict()}}), 200

    def create_broker_data(self, broker_data: dict) -> tuple:
        with self.client.context():

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

            try:
                broker_instance: Broker = Broker(broker_id=broker_id, broker_code=broker_code, broker_name=broker_name)
                key = broker_instance.put()
            except ValueError as e:
                return jsonify({'status': False, 'message': e}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': e}), 500

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
            except ValueError as e:
                return jsonify({'status': False, 'message': e}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': e}), 500
            except KeyError as e:
                return jsonify({'status': False, 'message': e}), 500
            return jsonify({'status': True, 'message': 'Stock Model Successfully created',
                            'payload': stock_model_instance.to_dict()}), 200

    def create_buy_model(self, buy_data: dict) -> tuple:

        with self.client.context():
            if "stock_id" in buy_data and buy_data['stock_id'] != "":
                stock_id: str = buy_data.get('stock_id') or None
            else:
                return jsonify({'status': False, 'message': "stock id is required"}), 500
            if "date" in buy_data and buy_data['date'] != "":
                # TODO- insure that FORMAT is DD_MM-YYYY
                try:
                    date: object = date_string_to_date(buy_data.get('date'))
                except ValueError as e:
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
            try:
                buy_volume_instance: BuyVolumeModel = BuyVolumeModel(stock_id=stock_id, date=date,
                                                                     buy_volume=buy_volume, buy_value=buy_value,
                                                                     buy_ave_price=buy_ave_price,
                                                                     buy_market_val_percent=buy_market_val_percent,
                                                                     buy_trade_count=buy_trade_count)
                key = buy_volume_instance.put()
            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

            message: str = "Buy volume successfully created"
            return jsonify({'status': True, 'message': message, 'payload': buy_volume_instance.to_dict()}), 200

    def create_sell_volume(self, sell_data: dict) -> tuple:
        with self.client.context():
            if "stock_id" in sell_data and sell_data['stock_id'] != "":
                stock_id: str = sell_data.get('stock_id') or None
            else:
                return jsonify({'status': False, 'message': "stock id is required"}), 500

            if "date" in sell_data and sell_data["date"] != "":
                try:
                    date: object = date_string_to_date(sell_data.get('date'))
                except ValueError as e:
                    date: object = datetime.date(datetime.datetime.now())
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

            try:
                sell_volume_instance: SellVolumeModel = SellVolumeModel(stock_id=stock_id,
                                                                        date=date,
                                                                        sell_volume=sell_volume,
                                                                        sell_value=sell_value,
                                                                        sell_ave_price=sell_ave_price,
                                                                        sell_market_val_percent=sell_market_val_percent,
                                                                        sell_trade_count=sell_trade_count)
                key = sell_volume_instance.put()
            except ValueError as e:
                return jsonify({'status': False, 'message': e}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': e}), 500

            return jsonify({'status': True, 'message': 'Sell Volume Successfully created',
                            'payload': sell_volume_instance.to_dict()}), 200

    def create_net_volume(self, net_volume_data: dict) -> tuple:
        with self.client.context():
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
                transaction_id: str = net_volume_data.get("transaction_id")  or None
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

            try:
                net_volume_instance: NetVolumeModel = NetVolumeModel(stock_id=stock_id,
                                                                     transaction_id=transaction_id,
                                                                     date=date, net_volume=net_volume,
                                                                     net_value=net_value,
                                                                     total_value=total_value,
                                                                     total_volume=total_volume)
                key = net_volume_instance.put()

            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500

            message: str = 'Net Volume Successfully created'
            return jsonify({'status': True, 'message': message,
                            'payload': net_volume_instance.to_dict()}), 200

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
            return jsonify({"status": True, "payload": stock_list, "message": "stocks returns" }), 200

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
            sell_volumes: typing.List[dict] = [sell_volume.to_dict for sell_volume in sell_volume_list]
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
                return jsonify({"status": False,  "message": message}), 500

            payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
            message: str = "successfully fetched net volume"
            return jsonify({"status": True, "payload": payload, "message": message}), 200

    def get_day_net_volumes(self, date: object = None) -> tuple:
        with self.client.context():
            if date is not None:
                net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(NetVolumeModel.date == date).fetch()
                payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
            else:
                message: str = "net volume data not found"
                return jsonify({"status": False, "message": message}), 500

            message: str = "net volume data not found"
            return jsonify({"status": True, "payload": payload, "message": message}), 500

    def get_daily_net_volumes_by_stock(self, stock_id: str = None) -> tuple:
        with self.client.context():
            if stock_id is not None:
                net_volume_list: typing.List[NetVolumeModel] = NetVolumeModel.query(
                    NetVolumeModel.stock_id == stock_id).fetch()
                payload: typing.List[dict] = [net_volume.to_dict() for net_volume in net_volume_list]
            else:
                message: str = "net volume data not found"
                return jsonify({"status": False, "message": message}), 500

            message: str = "net volume data not found"
            return jsonify({"status": True, "payload": payload, "message": message}), 500

