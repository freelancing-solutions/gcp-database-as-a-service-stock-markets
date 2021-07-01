import base64
import json
from flask import Blueprint, request, jsonify, current_app
from data_service.views.users import UserView
from data_service.views.stocks import StockView
pubsub_bp = Blueprint('pubsub', __name__)


# noinspection DuplicatedCode
@pubsub_bp.route('/pubsub/<path:path>', methods=["POST", "GET"])
def pubsub(path):
    """
        get messages from pubsub topics
        :param path:
        :return:
    """
    stock_view_instance: StockView = StockView()
    if (request.args.get('token', '') !=
            current_app.config['PUBSUB_VERIFICATION_TOKEN']):
        return 'Invalid request', 400

    if path == "stock-data":
        envelope = json.loads(request.data.decode('utf-8'))
        payload = base64.b64decode(envelope['message']['data'])
        print(payload)
        stock_data: dict = json.loads(payload['fields'][0])
        return stock_view_instance.create_stock_data(stock_data=stock_data)
    elif path == "broker-data":
        envelope = json.loads(request.data.decode('utf-8'))
        payload = base64.b64decode(envelope['message']['data'])
        print(payload)
        broker_data: dict = json.loads(payload['fields'][0])
        return stock_view_instance.create_broker_data(broker_data=broker_data)
    elif path == "sell-volume-data":
        envelope = json.loads(request.data.decode('utf-8'))
        payload = base64.b64decode(envelope['message']['data'])
        print(payload)
        sell_data: dict = json.loads(payload['fields'][0])
        return stock_view_instance.create_sell_volume(sell_data=sell_data)
    elif path == "buy-volume-data":
        envelope = json.loads(request.data.decode('utf-8'))
        payload = base64.b64decode(envelope['message']['data'])
        print(payload)
        buy_volume_data: dict = json.loads(payload['fields'][0])
        return stock_view_instance.create_buy_model(buy_data=buy_volume_data)
    elif path == "net-volume-data":
        envelope = json.loads(request.data.decode('utf-8'))
        payload = base64.b64decode(envelope['message']['data'])
        print(payload)
        net_volume_data: dict = json.loads(payload['fields'][0])
        return stock_view_instance.create_buy_model(buy_data=net_volume_data)
    else:
        return "Failure", 500
