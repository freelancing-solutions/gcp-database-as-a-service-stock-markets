from data_service.config import Config
from binance.client import Client


class Binance:
    def __init__(self, app):
        api_key = ""
        api_secret = ""
        self.client = Client(api_key, api_secret)


