from flask import Blueprint, request

from data_service.views.stocks import StockView

task_bp = Blueprint('tasks_input_pubsub_handlers', __name__)


# NOTE: calls to this endpoints will come from pubsub messaging
# NOTE This works like data sinks for functions
@task_bp.route('/task/stocks/api/save', methods=['POST'])
def save_api_stock_data() -> tuple:
    """
        this task will be called by
        the function which retrieves data from api
        in order to submit data to be saved to database


    :return:
    """
    stock_data: dict = request.get_json()
    stock_view_instance: StockView = StockView()
    return stock_view_instance.add_api_stock_data(stock_data=stock_data)


@task_bp.route('/task/stocks/scraped/save', methods=['POST'])
def save_scraped_stock_data() -> tuple:
    """
        this task will be called by
        the function which retrieves data by scrapping of the website
        in order to submit data to be saved to database
    :return:
    """
    stock_data: dict = request.get_json()
    stock_view_instance: StockView = StockView()
    return stock_view_instance.add_scrapped_stock_data(stock_data=stock_data)


@task_bp.route('/task/stocks/pdf/save', methods=['POST'])
def save_scraped_pdf_data() -> tuple:
    """
        this task will accept data from a function scrapping stock pdf data
    :return:
    """
    stock_data: dict = request.get_json()
    stock_view_instance: StockView = StockView()
    return stock_view_instance.add_scrapped_pdf_data(stock_data=stock_data)