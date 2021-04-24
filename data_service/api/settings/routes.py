from flask import Blueprint, request, jsonify

from data_service.api.api_authenticator import handle_auth
from data_service.views.settings import ExchangeDataView, ScrappingPagesView

settings_bp = Blueprint('settings_bp', __name__)


@settings_bp.route('/api/v1/settings/<path:path>', methods=['GET', 'POST'])
@handle_auth
def settings(path):

    if request.method == "GET":
        if path == "scrapper":
            # TODO- load scrapper settings
            scrapper_instances: ScrappingPagesView = ScrappingPagesView()
            return scrapper_instances.return_scrappers_settings()
        elif path == "parser":
            # TODO- load parser settings
            pass

        elif path == "data-service":
            # TODO - load data-service settings
            pass
        else:
            pass
    else:
        # TODO - save settings files
        pass


@settings_bp.route('/api/v1/exchange/<path:path>', methods=['POST', 'GET'])
@handle_auth
def exchange_data(path: str) -> tuple:
    exchange_data_instance = ExchangeDataView()
    if request.method == "GET":
        pass
    if request.method == "POST":
        if path == "add":
            json_data = request.get_json()
            if 'country' in json_data and json_data['country'] != "":
                country: str = json_data.get('country') or None
            else:
                return jsonify({"status": False, "message": "Country is required"}), 500

            if "name" in json_data and json_data['name'] != "":
                name: str = json_data.get('name') or None
            else:
                return jsonify({"status": False, "message": "Name is required"}), 500
            return exchange_data_instance.add_exchange(country=country, name=name)

        elif path == "update":
            json_data = request.get_json()
            if 'exchange_id' in json_data and json_data['exchange_id'] != "":
                exchange_id: str = json_data.get('exchange_id') or None
            else:
                return jsonify({"status": False, "message": "Exchange ID is required"}), 500
            if 'country' in json_data and json_data['country'] != "":
                country: str = json_data.get('country') or None
            else:
                return jsonify({"status": False, "message": "Country is required"}), 500

            if 'name' in json_data and json_data['name'] != "":
                name: str = json_data.get('name') or None
            else:
                return jsonify({"status": False, "message": "Name is required"}), 500

            return exchange_data_instance.update_exchange(exchange_id=exchange_id, country=country, name=name)
        elif path == "add-tickers":
            json_data = request.get_json()
            if 'exchange_id' in json_data and json_data['exchange_id'] != "":
                exchange_id: str = json_data.get('exchange_id') or None
            else:
                return jsonify({"status": False, "message": "Exchange ID is required"}), 500
            if 'tickers' in json_data and json_data['tickers'] != "":
                tickers: list = json_data.get('tickers') or []
            else:
                return jsonify({"status": False, "message": "Tickers is required"}), 500

            return exchange_data_instance.add_complete_stock_tickers_list(exchange_id=exchange_id, tickers_list=tickers)

        elif path == "get-tickers":
            json_data = request.get_json()
            if 'exchange_id' in json_data and json_data['exchange_id'] != "":
                exchange_id: str = json_data.get('exchange_id') or None
            else:
                return jsonify({"status": False, "message": "Exchange ID is required"}), 500

            return exchange_data_instance.get_exchange_tickers(exchange_id=exchange_id)

        elif path == "get-exchange":
            json_data = request.get_json()
            if 'exchange_id' in json_data and json_data['exchange_id'] != "":
                exchange_id: str = json_data.get('exchange_id') or None
            else:
                return jsonify({"status": False, "message": "Exchange ID is required"}), 500

            return exchange_data_instance.get_exchange(exchange_id=exchange_id)

        elif path == "get-all-exchanges":
            return exchange_data_instance.return_all_exchanges()

        elif path == "exchange-errors":
            json_data = request.get_json()
            if 'exchange_id' in json_data and json_data['exchange_id'] != "":
                exchange_id: str = json_data.get('exchange_id') or None
            else:
                return jsonify({"status": False, "message": "Exchange ID is required"}), 500

            return exchange_data_instance.return_exchange_errors(exchange_id=exchange_id)

        elif path == "delete-exchange":
            json_data = request.get_json()
            if 'exchange_id' in json_data and json_data['exchange_id'] != "":
                exchange_id: str = json_data.get('exchange_id') or None
            else:
                return jsonify({"status": False, "message": "Exchange ID is required"}), 500

            return exchange_data_instance.delete_exchange(exchange_id=exchange_id)
        else:
            pass

