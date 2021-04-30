import typing
from flask import jsonify, current_app
from data_service.config.types import dict_list_type, tickers_type
from data_service.main import cache_stocks
from data_service.store.settings import (UserSettingsModel, AdminSettingsModel, ExchangeDataModel,
                                         ScrappingPagesModel, StockAPIEndPointModel)
from data_service.utils.utils import return_ttl, end_of_month
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context

exc_list_type = typing.List[ExchangeDataModel]
scrape_list_type = typing.List[ScrappingPagesModel]
api_list_type = typing.List[StockAPIEndPointModel]

# TODO Refactor Settings View and Write Test Cases and Documentation
class UserSettingsView:
    def __init__(self):
        pass


class AdminSettingsView:
    def __init__(self):
        pass


class ExchangeDataView:

    def __init__(self):
        pass

    @use_context
    @handle_view_errors
    def add_exchange(self, country: str = None, name: str = None) -> tuple:
        exchange_instance: ExchangeDataModel = ExchangeDataModel()
        exchange_instance.set_exchange_country(country=country)
        exchange_instance.set_exchange_name(exchange=name)
        exchange_instance.set_exchange_id()
        exchange_instance.put()
        return jsonify({"status": True, "message": "successfully created an exchange",
                        "payload": exchange_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    def update_exchange(self, exchange_id: str = None, country: str = None, name: str = None) -> tuple:
        exchanges_list: exc_list_type = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).fetch()
        if len(exchanges_list) > 0:
            exchange_instance: ExchangeDataModel = exchanges_list[0]
            exchange_instance.set_exchange_country(country=country)
            exchange_instance.set_exchange_name(exchange=name)
            exchange_instance.put()
            return jsonify({'status': True, 'message': 'exchange updated'}), 200
        return jsonify({'status': False, 'message': 'exchange was not found'}), 500

    @use_context
    @handle_view_errors
    def add_complete_stock_tickers_list(self, exchange_id: str, tickers_list: list) -> tuple:
        exchange_id: str = exchange_id.strip()
        exchange_list: exc_list_type = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).fetch()

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

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_exchange_tickers(self, exchange_id: str) -> tuple:
        exchange_id: str = exchange_id.strip()
        exchange_list: exc_list_type = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).fetch()

        if len(exchange_list) > 0:
            exchange_instance: ExchangeDataModel = exchange_list[0]
            tickers_list: tickers_type = exchange_instance.exchange_tickers_list
            return jsonify({'status': True, 'message': 'successfully obtained exchange tickers',
                            'payload': tickers_list}), 200
        else:
            return jsonify({'status': False, 'message': 'Unable to locate exchange'}), 500

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_exchange(self, exchange_id: str) -> tuple:
        exchange_id: str = exchange_id.strip()
        exchange_list: exc_list_type = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).fetch()

        if len(exchange_list) > 0:
            exchange_instance: ExchangeDataModel = exchange_list[0]
            return jsonify({'status': True, 'message': 'successfully fetched an exchange',
                            'payload': exchange_instance.to_dict()}), 200
        return jsonify({'status': False, 'message': 'error unable to locate exchange'}), 500

    @cache_stocks.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def return_all_exchanges(self) -> tuple:
        exchange_list: exc_list_type = ExchangeDataModel.query().fetch()
        payload: dict_list_type = [exchange.to_dict() for exchange in exchange_list]
        message: str = 'successfully retrieved Exchanges List'
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200

    @cache_stocks.cached(timeout=return_ttl(name='short'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def return_exchange_errors(self, exchange_id: str) -> tuple:
        exchange_list: exc_list_type = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).fetch()
        if len(exchange_list) > 0:
            exchange_instance: ExchangeDataModel = exchange_list[0]
            payload: tickers_type = exchange_instance.exchange_tickers_list
            return jsonify({'status': True,
                            'message': 'successfully fetched exchange errors',
                            'payload': payload}), 200

        return jsonify({'status': False, 'message': 'error unable to locate exchange'}), 500

    @use_context
    @handle_view_errors
    def delete_exchange(self, exchange_id: str) -> tuple:
        exchange_id: str = exchange_id.strip()
        exchange_list: exc_list_type = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).fetch()
        if len(exchange_list) > 0:
            exchange_instance: ExchangeDataModel = exchange_list[0]
            exchange_instance.key.delete()
            pages_list: scrape_list_type = ScrappingPagesModel.query(
                ScrappingPagesModel.exchange_id == exchange_id).fetch()
            for page in pages_list:
                page.key.delete()

            api_list: api_list_type = StockAPIEndPointModel.query(
                StockAPIEndPointModel.exchange_id == exchange_id).fetch()
            for api in api_list:
                api.key.delete()
            message: str = 'successfully deleted an exchange and all data related to it'
            return jsonify({'status': True, 'message': message}), 500
        message: str = "unable to delete the exchange may already have been deleted"
        return jsonify({'status': False, 'message': message}), 500


class ScrappingPagesView:
    def __init__(self):
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @cache_stocks.cached(timeout=return_ttl(name='long'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def return_scrappers_settings(self) -> tuple:
        scrapping_instance_list: scrape_list_type = ScrappingPagesModel.query().fetch()
        payload: dict_list_type = [scrapping_instance.to_dict() for scrapping_instance in scrapping_instance_list]
        return jsonify({'status': True,
                        'payload': payload,
                        'message': 'scrapping settings fetched successfully'})

    @use_context
    @handle_view_errors
    def add_scrapper_settings(self, scrapper_settings: dict) -> tuple:
        if "exchange_id" in scrapper_settings and scrapper_settings['exchange_id'] != "":
            exchange_id: str = scrapper_settings.get('exchange_id') or None
        else:
            return jsonify({"status": False, "message": "exchange id is required"}), 500

        if "target_url" in scrapper_settings and scrapper_settings["target_url"] != "":
            target_url: str = scrapper_settings.get("target_url") or None
        else:
            return jsonify({"status": False, "message": "target url is required"}), 500

        if "access_timestamps" in scrapper_settings and scrapper_settings["access_timestamps"] != "":
            access_timestamps: typing.List[int] = scrapper_settings.get('access_timestamps') or None
        else:
            return jsonify({"status": False, "message": "access timestamps is required"}), 500

        if "require_login" in scrapper_settings and scrapper_settings["require_login"] != "":
            require_login: bool = scrapper_settings.get("require_login") or None
            scrapper_settings_instance: ScrappingPagesModel = ScrappingPagesModel()
            if require_login:
                if "login_page_url" in scrapper_settings and scrapper_settings["login_page_url"] != "":
                    login_page_url: str = scrapper_settings.get("login_page_url") or None
                else:
                    return jsonify({"status": False, "message": "login page url is required"}), 500

                if "username" in scrapper_settings and scrapper_settings["username"] != "":
                    username: str = scrapper_settings.get("username") or None
                else:
                    return jsonify({"status": False, "message": "login_name is required"}), 500

                if "password" in scrapper_settings and scrapper_settings["password"] != "":
                    password: str = scrapper_settings.get('password') or None
                else:
                    return jsonify({"status": False, "message": "password is required"}), 500
                try:
                    scrapper_settings_instance.set_login_page_url(login_page_url=login_page_url)
                    scrapper_settings_instance.set_username(username=username)
                    scrapper_settings_instance.set_password(password=password)
                except ValueError as e:
                    return jsonify({'status': False, 'message': str(e)})
                except TypeError as e:
                    return jsonify({'status': False, 'message': str(e)})
            else:
                return jsonify({"status": False, "message": "require_login is required"}), 500
            scrapper_settings_instance.set_exchange_id(exchange_id=exchange_id)
            scrapper_settings_instance.set_page_id()
            scrapper_settings_instance.set_target_url(target_url=target_url)
            scrapper_settings_instance.set_access_timestamps(access_timestamps=access_timestamps)
            scrapper_settings_instance.set_require_login(require_login=require_login)

            key = scrapper_settings_instance.put()
            return jsonify({'status': True, 'message': "successfully created new scrapper settings",
                            'payload': scrapper_settings_instance.to_dict()})



class StockAPIEndPointView:
    def __init__(self):
        pass




