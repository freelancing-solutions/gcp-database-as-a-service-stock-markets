from google.cloud import ndb
import datetime
from pinoydesk.config import Config
from pinoydesk.utils.utils import create_id


class Stock(ndb.Model):
    stock_id: str = ndb.StringProperty(required=True, indexed=True)
    stock_code: str = ndb.StringProperty(required=True, indexed=True)
    stock_name: str = ndb.StringProperty(required=True)
    symbol: str = ndb.StringProperty(required=True, indexed=True)

    def set_stock_id(self, stock_id: str) -> bool:
        stock_id: str = stock_id.strip()
        if stock_id is None or stock_id == "":
            raise ValueError('Stock Id cannot be Null')
        if not isinstance(stock_id, str):
            raise TypeError("Stock Id can only be a string")

        self.stock_id = stock_id
        return True

    def set_stock_code(self, stock_code: str) -> bool:
        stock_code = stock_code.strip()
        if stock_code is None or stock_code == "":
            raise ValueError("Stock Code cannot be Null")
        if not isinstance(stock_code, str):
            raise TypeError("stock_code may only be a string")
        self.stock_code = stock_code
        return True

    def set_stock_name(self, stock_name: str) -> bool:
        stock_name = stock_name.strip()
        if stock_name is None or stock_name == "":
            raise ValueError("Stock Name cannot be Null")
        if not isinstance(stock_name, str):
            raise TypeError("Stock Name may only be a string")
        self.stock_name = stock_name
        return True

    def set_symbol(self, symbol: str) -> bool:
        symbol: str = symbol.strip()
        if symbol is None or symbol == "":
            raise ValueError("Symbol cannot be Null")
        if not isinstance(symbol, str):
            raise TypeError("Symbol can only be a string")
        self.symbol = symbol
        return True


class Broker(ndb.Model):
    broker_id: str = ndb.StringProperty(required=True)
    broker_code: str = ndb.StringProperty(required=True)

    def set_broker_id(self, broker_id: str) -> bool:
        broker_id = broker_id.strip()
        if broker_id is None or broker_id == "":
            raise ValueError("Broker ID  cannot be Null")
        if not isinstance(broker_id, str):
            raise TypeError("Broker ID can only be a string")
        self.broker_id = broker_id
        return True

    def set_broker_code(self, broker_code: str) -> bool:
        broker_code = broker_code.strip()
        if broker_code is None or broker_code == "":
            raise ValueError("Broker Code cannot be Null")
        if not isinstance(broker_code, str):
            raise TypeError("Broker Code can only be a string")
        self.broker_code = broker_code
        return True


class StockModel(ndb.Model):
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
    exchange_id: str = ndb.StringProperty(required=True, indexed=True)
    sid: str = ndb.StringProperty()
    stock = ndb.StructuredProperty(Stock)
    broker = ndb.StructuredProperty(Broker)

    def set_exchange_id(self, exchange_id: str) -> bool:
        exchange_id: str = exchange_id.strip()
        if exchange_id is None or exchange_id == "":
            raise ValueError('exchange id cannot be null')
        if not isinstance(exchange_id, str):
            raise TypeError('exchange id may only be a string')
        self.exchange_id = exchange_id
        return True

    def set_id(self, sid: str) -> bool:
        if sid is None or sid == "":
            raise ValueError("id cannot be null")

        if not isinstance(sid, str):
            raise TypeError("id can only be a string")
        self.sid = sid
        return True

    def set_stock(self, stock: Stock) -> bool:
        if not isinstance(stock, Stock):
            raise TypeError('Invalid Stock argument, needs to be an instance of Stock')
        self.stock = stock
        return True

    def set_broker(self, broker: Broker) -> bool:
        if not isinstance(broker, Broker):
            raise TypeError("Invalid Broker argument, needs to be an instance of Broker")
        self.broker = broker
        return True


class BuyModel(ndb.Model):
    stock_id: str = ndb.StringProperty()
    transaction_id: str = ndb.StringProperty()
    date: object = ndb.DateTimeProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    buy_volume: int = ndb.IntegerProperty(default=0)
    buy_value: int = ndb.IntegerProperty(default=0)
    buy_ave_price: int = ndb.IntegerProperty(default=0)
    buy_market_val_percent: int = ndb.IntegerProperty(default=0)
    buy_trade_count: int = ndb.IntegerProperty(default=0)

    def set_transaction_id(self):
        """
            an id to match buy volume sell volume and net volume
        :return:
        """
        self.transaction_id = create_id()


class SellVolumeModel(ndb.Model):
    stock_id: str = ndb.StringProperty()
    transaction_id: str = ndb.StringProperty()
    date: object = ndb.DateTimeProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    sell_volume: int = ndb.IntegerProperty(default=0)
    sell_value: int = ndb.IntegerProperty(default=0)
    sell_ave_price: int = ndb.IntegerProperty(default=0)
    sell_market_val_percent: int = ndb.IntegerProperty(default=0)
    sell_trade_count: int = ndb.IntegerProperty(default=0)


class NetVolumeModel(ndb.Model):
    stock_id: str = ndb.StringProperty()
    transaction_id: str = ndb.StringProperty()
    date: object = ndb.DateTimeProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    net_volume: int = ndb.IntegerProperty(default=0)
    net_value: int = ndb.IntegerProperty(default=0)
    total_volume: int = ndb.IntegerProperty(default=0)
    total_value: int = ndb.IntegerProperty(default=0)
