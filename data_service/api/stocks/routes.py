from datetime import date as date_class
from flask import Blueprint, request, jsonify
from data_service.api.api_authenticator import handle_auth
from data_service.config.exceptions import InputError
from data_service.utils.utils import date_string_to_date
from data_service.views.stocks import StockView
from data_service.tasks.tasks import create_task
from functools import lru_cache

stocks_bp = Blueprint('stocks_bp', __name__)

task_time: int = 2
task_count: int = 1


@stocks_bp.route('/api/v1/stocks/create/<path:path>', methods=['POST'])
@handle_auth
@lru_cache(maxsize=1024)
def stocks(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    try:
        json_data: dict = request.get_json()
        assert isinstance(json_data, dict)
    except AssertionError:
        message: str = "cannot read json data"
        raise InputError(message)

    if path == "stock":
        task = create_task(uri='/task/stock/create-stock', payload=json_data, in_seconds=task_time)
        if task is None:
            return jsonify({'status': False,
                            'message': 'Unable to create task',
                            }), 500
        return jsonify({'status': True,
                        'message': 'Successfully added a stock task'}), 200

    elif path == "broker":
        task = create_task(uri='/task/stock/create-broker', payload=json_data, in_seconds=task_time)
        if task is None:
            return jsonify({'status': False,
                            'message': 'Unable to create task',
                            }), 500
        return jsonify({'status': True,
                        'message': 'Successfully added a broker task'}), 200

    elif path == "stock-model":
        task = create_task(uri='/task/stock/create-stock-model', payload=json_data, in_seconds=task_time)
        if task is None:
            return jsonify({'status': False,
                            'message': 'Unable to create task',
                            }), 500
        return jsonify({'status': True,
                        'message': 'Successfully added a broker task'}), 200

    elif path == "buy-volume":
        # Date and transaction id are created here
        # return stock_view_instance.create_buy_model(buy_data=json_data)
        task = create_task(uri='/task/stock/create-buy-volume', payload=json_data, in_seconds=task_time)
        if task is None:
            return jsonify({'status': False,
                            'message': 'Unable to create task',
                            }), 500
        return jsonify({'status': True,
                        'message': 'Successfully added a broker task'}), 200

    elif path == "sell-volume":
        task = create_task(uri='/task/stock/create-sell-volume', payload=json_data, in_seconds=task_time)
        if task is None:
            return jsonify({'status': False,
                            'message': 'Unable to create task',
                            }), 500
        return jsonify({'status': True,
                        'message': 'Successfully added a broker task'}), 200

    elif path == "net-volume":
        task = create_task(uri='/task/stock/create-net-volume', payload=json_data, in_seconds=task_time)
        if task is None:
            return jsonify({'status': False,
                            'message': 'Unable to create task',
                            }), 500
        return jsonify({'status': True,
                        'message': 'Successfully added a broker task'}), 200

    else:
        # if error the error handlers will handle it
        pass


@stocks_bp.route('/api/v1/stocks/all/<path:path>', methods=['POST'])
@handle_auth
def stocks_all(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    if path == "stocks":
        return stock_view_instance.get_all_stocks()
    elif path == "brokers":
        return stock_view_instance.get_all_brokers()
    elif path == "stock-models":
        return stock_view_instance.get_all_stock_models()
    else:
        pass


@stocks_bp.route('/api/v1/stocks/daily/<path:path>', methods=['POST'])
@handle_auth
def daily_stocks(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    try:
        json_data: dict = request.get_json()
        assert isinstance(json_data, dict)
    except AssertionError:
        message: str = "cannot read json data"
        raise InputError(message)
    if path == "buy-volumes":
        return stock_view_instance.get_daily_buy_volumes_by_stock(stock_id=json_data['stock_id'])
    elif path == "sell-volumes":
        return stock_view_instance.get_daily_sell_volumes_by_stock(stock_id=json_data['stock_id'])
    elif path == "net-volumes":
        return stock_view_instance.get_daily_net_volumes_by_stock(stock_id=json_data['stock_id'])
    else:
        pass


@stocks_bp.route('/api/v1/stocks/item/<path:path>', methods=['POST'])
@handle_auth
def stock_item(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    try:
        json_data: dict = request.get_json()
        assert isinstance(json_data, dict)
    except AssertionError:
        message: str = "cannot read json data"
        raise InputError(message)

    if path == "stock":
        stock_id: str = json_data.get('stock_id')
        stock_code: str = json_data.get('stock_code')
        symbol: str = json_data.get('symbol')
        return stock_view_instance.get_stock_data(stock_id=stock_id, stock_code=stock_code, symbol=symbol)
    elif path == "broker":
        broker_id: str = json_data.get('broker_id')
        broker_code: str = json_data.get('broker_code')
        return stock_view_instance.get_broker_data(broker_id=broker_id, broker_code=broker_code)
    elif path == "stock-model":
        transaction_id: str = json_data.get('transaction_id')
        return stock_view_instance.get_stock_model(transaction_id=transaction_id)
    elif path == "buy-volume":
        transaction_id: str = json_data.get('transaction_id')
        # Date format :  DD-MM-YYYY
        date_created: date_class = date_string_to_date(json_data.get('date'))
        stock_id: str = json_data.get('stock_id')
        return stock_view_instance.get_buy_volume(transaction_id=transaction_id, date_created=date_created,
                                                  stock_id=stock_id)
    elif path == "sell-volume":
        transaction_id: str = json_data.get('transaction_id')
        # Date format :  DD-MM-YYYY
        date_created: date_class = date_string_to_date(json_data.get('date'))
        stock_id: str = json_data['stock_id']
        return stock_view_instance.get_sell_volume(transaction_id=transaction_id, date_created=date_created,
                                                   stock_id=stock_id)
    elif path == "net-volume":
        transaction_id: str = json_data.get('transaction_id')
        date_created: date_class = date_string_to_date(json_data.get('date'))
        stock_id: str = json_data.get('stock_id')
        return stock_view_instance.get_net_volume(transaction_id=transaction_id, date_created=date_created,
                                                  stock_id=stock_id)
    else:
        pass


@stocks_bp.route('/api/v1/stocks/day-volumes/<path:path>', methods=['POST'])
@handle_auth
def day_volumes(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    try:
        message: str = "cannot read json data"
        content_type = request.headers.get('Content-Type')
        content_type = content_type.strip().lower()
        if content_type == "application/json":
            json_data: dict = request.get_json()
        else:
            raise InputError(message)
        assert isinstance(json_data, dict), "Unable to read json data"
    except AssertionError:
        raise InputError('Invalid Arguments')

    if path == "buy-volumes":
        date_created: date_class = date_string_to_date(json_data.get('date'))
        return stock_view_instance.get_day_buy_volumes(date_created=date_created)
    elif path == "sell-volumes":
        date_created: date_class = date_string_to_date(json_data.get('date'))
        return stock_view_instance.get_day_sell_volumes(date_created=date_created)
    elif path == "net-volumes":
        date_created: date_class = date_string_to_date(json_data.get('date'))
        return stock_view_instance.get_day_net_volumes(date_created=date_created)
    else:
        pass
