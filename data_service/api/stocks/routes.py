from flask import Blueprint, request, jsonify
from data_service.main import cache_stock_buys_sells, default_timeout
from data_service.utils.utils import date_string_to_date
from data_service.views.stocks import StockView

stocks_bp = Blueprint('stocks_bp', __name__)


@stocks_bp.route('/api/v1/stocks/create/<path:path>', methods=['POST'])
def stocks(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    if path == "stock":
        stock_data: dict = request.get_json()
        return stock_view_instance.create_stock_data(stock_data=stock_data)
    elif path == "broker":
        broker_data: dict = request.get_json()
        return stock_view_instance.create_broker_data(broker_data=broker_data)
    elif path == "stock-model":
        stock_model_data: dict = request.get_json()
        if "exchange_id" in stock_model_data and stock_model_data["exchange_id"] != "":
            exchange_id = stock_model_data.get("exchange_id") or None
        else:
            return jsonify({"status": False, "message": "exchange id is required"}), 500
        if "sid" in stock_model_data and stock_model_data["sid"] != "":
            sid: str = stock_model_data.get("sid") or None
        else:
            return jsonify({"status": False, "message": "sid is required"}), 500

        if "stock_id" in stock_model_data and stock_model_data["stock_id"] != "":
            stock_id: str = stock_model_data.get("stock_id") or None
        else:
            return jsonify({"status": False, "message": "stock is required"}), 500
        if "broker_id" in stock_model_data and stock_model_data["broker_id"] != "":
            broker_id: str = stock_model_data.get("broker_id") or None
        else:
            return jsonify({"status": False, "message": "stock is required"}), 500

        return stock_view_instance.create_stock_model(exchange_id=exchange_id, sid=sid, stock_id=stock_id,
                                                      broker_id=broker_id)

    elif path == "buy-volume":
        buy_volume_data: dict = request.get_json()
        # Date and transaction id are created here
        return stock_view_instance.create_buy_model(buy_data=buy_volume_data)

    elif path == "sell-volume":
        sell_volume_data: dict = request.get_json()
        return stock_view_instance.create_sell_volume(sell_data=sell_volume_data)
    elif path == "net-volume":
        net_volume_data: dict = request.get_json()
        return stock_view_instance.create_net_volume(net_volume_data=net_volume_data)
    else:
        # if error the error handlers will handle it
        pass


@stocks_bp.route('/api/v1/stocks/all/<path:path>', methods=['POST'])
@cache_stock_buys_sells.cached(timeout=3600)
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
@cache_stock_buys_sells.cached(timeout=default_timeout)
def daily_stocks(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    if path == "buy-volumes":
        json_data: dict = request.get_json()
        return stock_view_instance.get_daily_buy_volumes_by_stock(stock_id=json_data['stock_id'])
    elif path == "sell-volumes":
        json_data: dict = request.get_json()
        return stock_view_instance.get_daily_sell_volumes_by_stock(stock_id=json_data['stock_id'])
    elif path == "net-volumes":
        json_data: dict = request.get_json()
        return stock_view_instance.get_daily_net_volumes_by_stock(stock_id=json_data['stock_id'])
    else:
        pass


@stocks_bp.route('/api/v1/stocks/item/<path:path>', methods=['POST'])
@cache_stock_buys_sells.cached(timeout=default_timeout)
def stock_item(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    if path == "stock":
        json_data: dict = request.get_json()
        stock_id: str = json_data.get('stock_id') or None
        stock_code: str = json_data.get('stock_code') or None
        symbol: str = json_data.get('symbol') or None
        return stock_view_instance.get_stock_data(stock_id=stock_id, stock_code=stock_code, symbol=symbol)
    elif path == "broker":
        json_data: dict = request.get_json()
        broker_id: str = json_data.get('broker_id') or None
        broker_code: str = json_data.get('broker_code') or None
        return stock_view_instance.get_broker_data(broker_id=broker_id, broker_code=broker_code)
    elif path == "stock-model":
        json_data: dict = request.get_json()
        transaction_id: str = json_data.get('transaction_id') or None
        return stock_view_instance.get_stock_model(transaction_id=transaction_id)
    elif path == "buy-volume":
        json_data: dict = request.get_json()
        transaction_id: str = json_data.get('transaction_id') or None
        # Date format :  DD-MM-YYYY
        date: object = date_string_to_date(json_data.get('date')) or None
        stock_id: str = json_data.get('stock_id') or None
        return stock_view_instance.get_buy_volume(transaction_id=transaction_id, date=date, stock_id=stock_id)
    elif path == "sell-volume":
        json_data: dict = request.get_json()
        transaction_id: str = json_data.get('transaction_id') or None
        # Date format :  DD-MM-YYYY
        date: object = date_string_to_date(json_data.get('date')) or None
        stock_id: str = json_data['stock_id'] or None
        return stock_view_instance.get_sell_volume(transaction_id=transaction_id, date=date, stock_id=stock_id)
    elif path == "net-volume":
        json_data: dict = request.get_json()
        transaction_id: str = json_data.get('transaction_id') or None
        date: object = date_string_to_date(json_data.get('date')) or None
        stock_id: str = json_data.get('stock_id') or None
        return stock_view_instance.get_net_volume(transaction_id=transaction_id, date=date, stock_id=stock_id)
    else:
        pass


@stocks_bp.route('/api/v1/stocks/day-volumes/<path:path>', methods=['POST'])
@cache_stock_buys_sells.cached(timeout=default_timeout)
def day_volumes(path: str) -> tuple:
    stock_view_instance: StockView = StockView()
    if path == "buy-volumes":
        json_data: dict = request.get_json()
        date: object = date_string_to_date(json_data.get('date')) or None
        return stock_view_instance.get_day_buy_volumes(date=date)
    elif path == "sell-volumes":
        json_data: dict = request.get_json()
        date: object = date_string_to_date(json_data.get('date')) or None
        return stock_view_instance.get_day_sell_volumes(date=date)
    elif path == "net-volumes":
        json_data: dict = request.get_json()
        date: object = date_string_to_date(json_data.get('date')) or None
        return stock_view_instance.get_day_net_volumes(date=date)
    else:
        pass










        


