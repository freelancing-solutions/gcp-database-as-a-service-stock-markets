import typing
from flask import current_app, jsonify
from google.cloud import ndb
from pinoydesk.store.settings import (UserSettingsModel, AdminSettingsModel, ExchangeDataModel,
                                      ScrappingPagesModel, StockAPIEndPointModel)


class UserSettingsView:
    pass


class AdminSettingsView:
    pass


class ExchangeDataView:

    def __init__(self):
        self.client = ndb.Client(namespace="main", project=current_app.config.PROJECT)

    def add_exchange(self, country: str, name: str) -> tuple:
        with self.client.context():
            exchange_instance: ExchangeDataModel = ExchangeDataModel()
            exchange_instance.set_exchange_country(country=country)
            exchange_instance.set_exchange_name(exchange=name)
            exchange_instance.set_exchange_id()
            exchange_instance.put()
            return jsonify({"status": True, "message": "successfully created an exchange",
                            "payload": exchange_instance.to_dict()}), 200

    def update_exchange(self, exchange_id: str, country: str, name: str) -> tuple:
        with self.client.context():
            exchanges_list: typing.List[ExchangeDataModel] = ExchangeDataModel.query(
                ExchangeDataModel.exchange_id == exchange_id).fetch()
            if len(exchanges_list) > 0:
                exchange_instance: ExchangeDataModel = exchanges_list[0]
                exchange_instance.set_exchange_country(country=country)
                exchange_instance.set_exchange_name(exchange=name)
                exchange_instance.put()
                return jsonify({'status': True, 'message': 'exchange updated'}), 200
            return jsonify({'status': False, 'message': 'exchange was not found'}), 500

    def add_complete_stock_tickers_list(self, exchange_id: str, tickers_list: list) -> tuple:
        with self.client.context():
            exchange_id: str = exchange_id.strip()
            exchange_list: typing.List[ExchangeDataModel] = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).fetch()

            if len(exchange_list) > 0:
                exchange_instance: ExchangeDataModel = exchange_list[0]
                if exchange_instance.set_exchange_tickers_list(tickers_list=tickers_list) is True:
                    exchange_instance.put()
                    return jsonify({'status': True, 'message': 'stock tickers added',
                                    'payload': exchange_instance.to_dict()}), 200
                else:
                    return jsonify({'status': False, 'message': 'error adding stock tickers'}), 500
            else:
                return jsonify({'status': False, 'message': 'unable to find the exchange please inform admin'}), 500

    def get_exchange_tickers(self, exchange_id: str) -> tuple:
        with self.client.context():
            exchange_id: str = exchange_id.strip()
            exchange_list: typing.List[ExchangeDataModel] = ExchangeDataModel.query(
                ExchangeDataModel.exchange_id == exchange_id).fetch()

            if len(exchange_list) > 0:
                exchange_instance: ExchangeDataModel = exchange_list[0]
                tickers_list: typing.List[ExchangeDataModel] = exchange_instance.exchange_tickers_list
                return jsonify({'status': True, 'message': 'successfully obtained exchange tickers',
                                'payload': tickers_list}), 200
            else:
                return jsonify({'status': False, 'message': 'Unable to locate exchange'}), 500

    def get_exchange(self, exchange_id: str) -> tuple:
        with self.client.context():
            exchange_id: str = exchange_id.strip()
            exchange_list: typing.List[ExchangeDataModel] = ExchangeDataModel.query(
                ExchangeDataModel.exchange_id == exchange_id).fetch()

            if len(exchange_list) > 0:
                exchange_instance: ExchangeDataModel = exchange_list[0]
                return jsonify({'status': True, 'message': 'successfully fetched an exchange',
                                'payload': exchange_instance.to_dict()}), 200
            return jsonify({'status': False, 'message': 'error unable to locate exchange'}), 500

    def return_all_exchanges(self) -> tuple:
        with self.client.context():
            exchange_list: typing.List[ExchangeDataModel] = ExchangeDataModel.query().fetch()
            payload: typing.List[dict] = [exchange.to_dict() for exchange in exchange_list]
            message: str = 'successfully retrieved Exchanges List'
            return jsonify({'status': True, 'message': message, 'payload': payload}), 200

    def return_exchange_errors(self, exchange_id: str) -> tuple:
        with self.client.context():
            exchange_list: typing.List[ExchangeDataModel] = ExchangeDataModel.query(
                ExchangeDataModel.exchange_id == exchange_id).fetch()
            if len(exchange_list) > 0:
                exchange_instance: ExchangeDataModel = exchange_list[0]
                payload: typing.List[str] = exchange_instance.exchange_tickers_list
                return jsonify({'status': True, 'message': 'successfully fetched exchange errors'}), 200

            return jsonify({'status': False, 'message': 'error unable to locate exchange'}), 500

    def delete_exchange(self, exchange_id: str) -> tuple:
        with self.client.context():
            exchange_id: str = exchange_id.strip()
            exchange_list: typing.List[ExchangeDataModel] = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).fetch()
            if len(exchange_list) > 0:
                exchange_instance: ExchangeDataModel = exchange_list[0]
                exchange_instance.key.delete()
                scrapping_pages_list: typing.List[ScrappingPagesModel] = ScrappingPagesModel.query(
                    ScrappingPagesModel.exchange_id == exchange_id).fetch()
                for page in scrapping_pages_list:
                    page.key.delete()

                api_list: typing.List[StockAPIEndPointModel] = StockAPIEndPointModel.query(StockAPIEndPointModel.exchange_id == exchange_id).fetch()
                for api in api_list:
                    api.key.delete()
                message: str = 'successfully deleted an exchange and all data related to it'
                return jsonify({'status': True, 'message': message}), 500
            return jsonify({'status': False, 'message': 'unable to delete the exchange may already have been deleted'}), 500


class ScrappingPagesView:
    pass


class StockAPIEndPointView:
    pass

