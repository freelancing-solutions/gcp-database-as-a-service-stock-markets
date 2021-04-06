from google.cloud import ndb
import datetime
from pinoydesk.config import Config


class Stock(ndb.Model):
    """
        remember to set timezone info when saving date
        id,
        stock_id,
        broker_id,
        stock_code,
        stock_name,
        broker_code,
        date,
        buy_volume,
        buy_value,
        buy_ave_price,
        buy_market_val_percent,
        buy_trade_count,
        sell_volume,
        sell_value,
        sell_ave_price,
        sell_market_val_percent,
        sell_trade_count,
        net_volume,
        net_value,
        total_volume,
        total_value
    """
    exchange_id: str = ndb.StringProperty()
    id: str = ndb.StringProperty()
    stock_id: str = ndb.StringProperty()
    broker_id: str = ndb.StringProperty()
    stock_code: str = ndb.StringProperty()
    stock_name: str = ndb.StringProperty()
    broker_code: str = ndb.StringProperty()
    symbol: str = ndb.StringProperty()
    date_created: object = ndb.DateTimeProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))

    def set_exchange_name(self, exchange) -> bool:
        if exchange == "":
            raise ValueError('exchange name cannot be null')

        if not isinstance(exchange, str):
            raise TypeError('Exchange can only be a String')

        self.exchange_name = exchange
        return True


class Buys(ndb.Model):
    stock_id: str = ndb.StringProperty()
    date: object = ndb.DateTimeProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    buy_volume: int = ndb.IntegerProperty(default=0)
    buy_value: int = ndb.IntegerProperty(default=0)
    buy_ave_price: int = ndb.IntegerProperty(default=0)
    buy_market_val_percent: int = ndb.IntegerProperty(default=0)
    buy_trade_count: int = ndb.IntegerProperty(default=0)


class Sell(ndb.Model):
    stock_id: str = ndb.StringProperty()
    date: object = ndb.DateTimeProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    sell_volume: int = ndb.IntegerProperty(default=0)
    sell_value: int = ndb.IntegerProperty(default=0)
    sell_ave_price: int = ndb.IntegerProperty(default=0)
    sell_market_val_percent: int = ndb.IntegerProperty(default=0)
    sell_trade_count: int = ndb.IntegerProperty(default=0)


class NetVolumeModel(ndb.Model):
    stock_id: str = ndb.StringProperty()
    date: object = ndb.DateTimeProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    net_volume: int = ndb.IntegerProperty(default=0)
    net_value: int = ndb.IntegerProperty(default=0)
    total_volume: int = ndb.IntegerProperty(default=0)
    total_value: int = ndb.IntegerProperty(default=0)
    