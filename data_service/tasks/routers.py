import json

from flask import Blueprint, request

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
        stock_data: dict = json.loads(request.get_data(as_text=True))
        return stock_view_instance.create_stock_data(stock_data=stock_data)
    elif path == "create-broker":
        broker_data: dict = json.loads(request.get_data(as_text=True))
        return stock_view_instance.create_broker_data(broker_data=broker_data)


