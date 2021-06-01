import json

from flask import Blueprint, request, jsonify

from data_service.views.stocks import StockView

task_bp = Blueprint('tasks', __name__)


# NOTE: calls to this endpoints will come from pubsub messaging
# NOTE This works like data sinks for functions
@task_bp.route('/task/stock/<path:path>', methods=['POST'])
def stock_task_handler(path: str) -> tuple:
    """
        this task will be called by
        the function which retrieves data from api
        in order to submit data to be saved to database
    :return:
    """
    stock_view_instance: StockView = StockView()
    if path == "create-stock":
        stock_data: dict = request.get_json()
        return stock_view_instance.create_stock_data(stock_data=stock_data)
    elif path == "create-broker":
        broker_data: dict = request.get_json()
        return stock_view_instance.create_broker_data(broker_data=broker_data)
    elif path == "create-stock-model":
        json_data: dict = request.get_json()
        if "exchange_id" in json_data and json_data["exchange_id"] != "":
            exchange_id = json_data.get("exchange_id")
        else:
            return jsonify({"status": False, "message": "exchange id is required"}), 500
        if "sid" in json_data and json_data["sid"] != "":
            sid: str = json_data.get("sid")
        else:
            return jsonify({"status": False, "message": "sid is required"}), 500

        if "stock_id" in json_data and json_data["stock_id"] != "":
            stock_id: str = json_data.get("stock_id")
        else:
            return jsonify({"status": False, "message": "stock is required"}), 500
        if "broker_id" in json_data and json_data["broker_id"] != "":
            broker_id: str = json_data.get("broker_id")
        else:
            return jsonify({"status": False, "message": "stock is required"}), 500

        return stock_view_instance.create_stock_model(exchange_id=exchange_id, sid=sid, stock_id=stock_id,
                                                      broker_id=broker_id)

    elif path == "create-buy-volume":
        buy_data: dict = request.get_json()
        return stock_view_instance.create_buy_model(buy_data=buy_data)

    elif path == "create-sell-volume":
        sell_data: dict = request.get_json()
        return stock_view_instance.create_sell_volume(sell_data=sell_data)

    elif path == "create-net-volume":
        net_data: dict = request.get_json()
        return stock_view_instance.create_net_volume(net_volume_data=net_data)