from google.cloud import ndb
import datetime
from pinoydesk.config import Config


class Stock(ndb.Model):
    """
        remember to set timezone info when saving date
    """
    exchange_name: str = ndb.StringProperty()
    stock_name: str = ndb.StringProperty()
    symbol: str = ndb.StringProperty()
    low: int = ndb.IntegerProperty(default=0)
    high: int = ndb.IntegerProperty(default=0)
    date_created = ndb.DateTimeProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))

    def set_exchange_name(self, exchange):
        if exchange == "":
            raise ValueError('exchange name cannot be null')

        if not isinstance(exchange, str):
            raise TypeError('Exchange can only be a String')

        self.exchange_name = exchange


