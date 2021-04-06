from google.cloud import ndb
import datetime
from flask import current_app, jsonify


class StockView:
    def __init__(self):
        self.client = ndb.Client(namespace="main", project=current_app.config.PROJECT)
        with current_app.app_context():
            self.timezone = datetime.timezone(current_app.config.UTC_OFFSET)

    def add_api_stock_data(self, stock_data: dict) -> tuple:
        with self.client.context():
            return jsonify({'status': True, 'message': 'successfully saved api stock data'}), 200

    def add_scrapped_stock_data(self, stock_data: dict) -> tuple:
        with self.client.context():
            return jsonify({'status': True, 'message': 'successfully saved scrapped stock data'}), 200

    def add_scrapped_pdf_data(self, stock_data: dict) -> tuple:
        with self.client.context():
            return jsonify({'status': True, 'message': 'successfully saved scrapped pdf stock data'}), 200
