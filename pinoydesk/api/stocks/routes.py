from flask import Blueprint, request, jsonify
from pinoydesk.views.stocks import StockView
from pinoydesk.store.stocks import Stock, Broker

stocks_bp = Blueprint('stocks_bp', __name__)


@stocks_bp.route('/api/v1/stocks/create/<path:path>', methods=['POST'])
def stocks(path):
    stock_view_instance = StockView()
    if path == "stock":
        stock_data: dict = request.get_json()
        return stock_view_instance.create_stock_data(stock_data=stock_data)
    elif path == "broker":
        broker_data: dict = request.get_json()
        return stock_view_instance.create_broker_data(broker_data=broker_data)
    elif path == "stock-model":
        stock_model_data: dict = request.get_json()
        if "exchange_id" in stock_model_data and stock_model_data["exchange_id"] != "":
            exchange_id = stock_model_data["exchange_id"]
        else:
            return jsonify({"status": False, "message": "exchange id is required"}), 500
        if "sid" in stock_model_data and stock_model_data["sid"] != "":
            sid: str = stock_model_data["sid"]
        else:
            return jsonify({"status": False, "message": "sid is required"}), 500

        if "stock_id" in stock_model_data and stock_model_data["stock_id"] != "":
            stock_id: str = stock_model_data["stock_id"]
        else:
            return jsonify({"status": False, "message": "stock is required"}), 500

        if "broker_id" in stock_model_data and stock_model_data["broker_id"] != "":
            broker_id: str = stock_model_data["broker_id"]
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


