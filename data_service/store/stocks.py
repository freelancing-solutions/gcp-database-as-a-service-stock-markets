import typing
from google.cloud import ndb
import datetime
from data_service.config import Config
from data_service.utils.utils import create_id
from data_service.config.stocks import currency_symbols


class Setters:
    def __init__(self):
        pass

    @staticmethod
    def set_string(prop, value: typing.Union[str, None]) -> str:
        """
            takes in string input verifies and returns the same string
            input: value: str
            output str
        """
        if (value is None) or (value == ""):
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not(isinstance(value, str)):
            raise TypeError("{} can only be a string".format(str(prop)))
        return value.strip()

    @staticmethod
    def set_stock_name(prop, value: typing.Union[str, None]) -> str:
        """
            verify stock_name
        """
        if (value is None) or (value == ""):
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not(isinstance(value, str)):
            raise TypeError("{} can only be a string".format(str(prop)))
        return value.strip().lower()

    @staticmethod
    def set_id(prop, value: str) -> str:
        if (value is None) or (value == ""):
            raise ValueError("{} can only accept a string".format(str(prop)))
        if not(isinstance(value, str)):
            raise TypeError("{} can only be a string".format(str(prop)))
        return value.strip()

    @staticmethod
    def set_broker_code(prop, broker_code: str) -> str:
        if (broker_code is None) or (broker_code == ""):
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not(isinstance(broker_code, str)):
            raise TypeError("{} can only be a string".format(str(prop)))
        return broker_code.strip()

    @staticmethod
    def set_broker_name(prop, broker_name: str) -> str:
        if (broker_name is None) or (broker_name == ""):
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not(isinstance(broker_name, str)):
            raise TypeError("{} can only be a string".format(str(prop)))
        return broker_name.strip().lower()

    @staticmethod
    def set_bool(prop, value: bool) -> bool:
        if not(isinstance(value, bool)):
            raise TypeError("{} Invalid type".format(str(prop)))
        return value


setters: Setters = Setters()


class Stock(ndb.Model):
    """
        A Model for keeping stock code, stored separately on datastore
        but also a sub model of StockModel
    """
    stock_id: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_string)
    stock_code: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_string)
    stock_name: str = ndb.StringProperty(required=True, validator=setters.set_stock_name)
    symbol: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_string)
    is_crypto: bool = ndb.BooleanProperty(validator=setters.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.stock_id != other.stock_id:
            return False
        if self.stock_code != other.stock_code:
            return False
        if self.symbol != other.symbol:
            return False
        return True

    def __str__(self) -> str:
        return "<Stock stock_code: {}, symbol: {}".format(self.stock_code, self.symbol)

    def __repr__(self) -> str:
        return "<Stock: {}{}{}{}".format(self.stock_id, self.stock_code, self.symbol, self.stock_name)


class Broker(ndb.Model):
    """
        a model for storing broker data
    """
    broker_id: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_id)
    broker_code: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_broker_code)
    broker_name: str = ndb.StringProperty(required=True, validator=setters.set_broker_name)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.broker_id != other.broker_id:
            return False
        if self.broker_code != other.broker_code:
            return False
        return True

    def __str__(self) -> str:
        return "<Broker broker_code: {} {}".format(self.broker_code, self.broker_name)

    def __repr__(self) -> str:
        return "<Broker: {} {} {}".format(self.broker_id, self.broker_code, self.broker_name)


class StockModelSetters:
    def __init__(self):
        pass

    @staticmethod
    def set_stock(prop, stock: Stock) -> Stock:
        if not(isinstance(stock, Stock)):
            raise TypeError('{}, needs to be an instance of Stock'.format(str(prop)))
        return stock

    @staticmethod
    def set_broker(prop, broker: Broker) -> Broker:
        if not(isinstance(broker, Broker)):
            raise TypeError("{}, Needs to be an instance of Broker".format(str(prop)))
        return broker

    @staticmethod
    def set_stock_id(prop, value: str) -> str:
        if (value is None) or (value == ""):
            raise ValueError('{} cannot be Null'.format(str(prop)))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(str(prop)))

        return value.strip()

    @staticmethod
    def set_date(prop, value: datetime.date) -> datetime.date:
        if isinstance(value, datetime.date):
            return value
        raise TypeError('{} can only be an object of datetime'.format(str(prop)))

    @staticmethod
    def set_int(prop, value: int) -> int:
        if (value is None) or (value == ""):
            raise ValueError("{} can not be Null".format(str(prop)))

        if not(isinstance(value, int)):
            raise TypeError("{} can only be an Integer".format(str(prop)))
        if value < 0:
            raise ValueError("{} can only be a positive integer".format(str(prop)))
        return value

    @staticmethod
    def set_float(prop, value: float) -> float:
        if (value is None) or (value == ""):
            raise ValueError("{} can not be Null".format(str(prop)))

        if not(isinstance(value, float)):
            raise TypeError("{} can only be a float".format(str(prop)))
        if value < 0:
            raise ValueError("{} can only be a positive float".format(str(prop)))
        return value

    @staticmethod
    def set_currency(prop, value: str) -> str:
        if value not in currency_symbols():
            raise TypeError("{} not a valid currency".format(str(prop)))
        return value

    @staticmethod
    def set_percent(prop, value: int) -> int:
        if (value is None) or (value == ""):
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not(isinstance(value, int)):
            raise TypeError("{} can only be an integer".format(str(prop)))
        if (value < 0) or (value > 100):
            raise ValueError("{} should be a percentage".format(str(prop)))
        return value


stock_setters: StockModelSetters = StockModelSetters()


class StockModel(ndb.Model):

    exchange_id: str = ndb.StringProperty(required=True, indexed=True, validator=setters.set_id)
    transaction_id: str = ndb.StringProperty(validator=setters.set_id)
    stock = ndb.StructuredProperty(Stock, validator=stock_setters.set_stock)
    broker = ndb.StructuredProperty(Broker, validator=stock_setters.set_broker)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        if self.stock != other.stock:
            return False
        if self.broker != other.broker:
            return False
        return True

    def __str__(self) -> str:
        return "<Stock_Model: Stock : {} , Broker {}".format(str(self.stock), str(self.broker))

    def __repr__(self) -> str:
        return "<Stock_Model: {}{}{}".format(self.transaction_id, self.stock.stock_id, self.broker.broker_id)


class BuyVolumeModel(ndb.Model):
    """
        daily buy volumes
    """
    transaction_id: str = ndb.StringProperty(indexed=True, required=True, default=create_id())
    stock_id: str = ndb.StringProperty(validator=stock_setters.set_stock_id)
    date_created: datetime.date = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET),
                                                   validator=stock_setters.set_date)
    currency: str = ndb.StringProperty(default=Config.CURRENCY, validator=stock_setters.set_currency)
    buy_volume: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    buy_value: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    buy_ave_price: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    buy_market_val_percent: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    buy_trade_count: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        if self.stock_id != other.stock_id:
            return False
        if self.date_created != other.date_created:
            return False
        return True

    def __str__(self) -> str:
        return "<Buy_Volume: date_created: {} buy volume: {} , buy value: {}, buy ave price: {}, " \
               "buy market value percent: {}, buy trade account: {}".format(self.date_created, self.buy_volume,
                                                                            self.buy_value, self.buy_ave_price,
                                                                            self.buy_market_val_percent,
                                                                            self.buy_trade_count)

    def __repr__(self) -> str:
        return "<Buy_Volume: {}{}{}".format(self.transaction_id, self.stock_id, self.date_created)


class SellVolumeModel(ndb.Model):
    """
        daily sell volumes
    """
    transaction_id: str = ndb.StringProperty(indexed=True, validator=setters.set_id)
    stock_id: str = ndb.StringProperty(validator=setters.set_id)
    # Auto now add can be over written
    date_created: datetime.date = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET))
    currency: str = ndb.StringProperty(default=Config.CURRENCY, validator=stock_setters.set_currency)
    sell_volume: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    sell_value: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    sell_ave_price: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    sell_market_val_percent: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_percent)
    sell_trade_count: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        if self.stock_id != other.stock_id:
            return False
        if self.date_created != other.date_created:
            return False
        return True

    def __str__(self) -> str:
        return "<Sell_Volume: Date_Created : {} , sell_volume: {}, sell_value: {}, sell_ave_price: {}, " \
               "sell_market_val_percent: {}, sell_trade_account: {}".format(self.date_created, self.sell_volume,
                                                                            self.sell_value, self.sell_ave_price,
                                                                            self.sell_market_val_percent,
                                                                            self.sell_trade_count)

    def __repr__(self) -> str:
        return "Sell_Volume: {} {} {}".format(self.transaction_id, self.stock_id, self.date_created)


class NetVolumeModel(ndb.Model):
    """
        daily net volume
    """
    stock_id: str = ndb.StringProperty(validator=setters.set_id)
    transaction_id: str = ndb.StringProperty(validator=setters.set_id)
    date_created: datetime.date = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET),
                                                   validator=stock_setters.set_date)
    currency: str = ndb.StringProperty(default=Config.CURRENCY, validator=stock_setters.set_currency)
    net_volume: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    net_value: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    total_volume: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)
    total_value: int = ndb.IntegerProperty(default=0, validator=stock_setters.set_int)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        if self.stock_id != other.stock_id:
            return False
        if self.date_created != other.date_created:
            return False
        return True

    def __str__(self) -> str:
        return "<Net_Volume: date_created: {}, net_volume: {}, net_value: {}, total_volume: {}, total_value: {}".format(
            self.date_created, self.net_volume, self.net_value, self.total_volume, self.total_value)

    def __repr__(self) -> str:
        return "<Net_Volume: {}{}{}".format(self.date_created, self.transaction_id, self.stock_id)


class StockPriceData(ndb.Model):
    """
        used to capture daily lows and highs for each stock
    """
    stock_id: str = ndb.StringProperty(validator=setters.set_id)
    date: datetime.date = ndb.DateProperty(auto_now_add=True, tzinfo=datetime.timezone(Config.UTC_OFFSET), validator=stock_setters.set_date)
    open: float == ndb.FloatProperty(default=0, validator=stock_setters.set_int)
    high: float == ndb.FloatProperty(default=0, validator=stock_setters.set_int)
    low: float == ndb.FloatProperty(default=0, validator=stock_setters.set_int)
    close: float == ndb.FloatProperty(default=0, validator=stock_setters.set_int)
    adjusted_close: float == ndb.FloatProperty(default=0, validator=stock_setters.set_int)
    volume: float == ndb.FloatProperty(default=0, validator=stock_setters.set_int)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class:
            return False
        if self.stock_id != other.stock_id:
            return False
        if self.date != other.date:
            return False
        return True

    def __str__(self) -> str:
        return "<StockPriceData stock_id: {} , date: {} , open: {}, high: {}, low: {}".format(self.stock_id, self.date,
                                                                                              self.open, self.high,
                                                                                              self.low)

    def __repr__(self) -> str:
        return self.__str__()

