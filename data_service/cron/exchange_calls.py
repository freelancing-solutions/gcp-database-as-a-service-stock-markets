"""
    calls to exchanges to obtain financial information or data
    the calls will execute in certain dates and times in order to
    satisfy customer requirements

    calls read stock databases to get initial data, then goes to api's to obtain
    data for the day or time of day,
    if any missing data is detected its updated on the database
"""
import typing
from data_service.store.stocks import Stock
from data_service.store.settings import ExchangeDataModel


def stocks_by_exchange(exchange_id: str) -> typing.List[dict]:
    exchange_instance: ExchangeDataModel = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).get()
    if isinstance(exchange_instance, ExchangeDataModel):
        return exchange_instance.exchange_tickers_list
    else:
        return []


def ticker_found(tickers_list: typing.List[dict], stock_instance: dict) -> bool:
    for ticker in tickers_list:
        if ticker['symbol'] == stock_instance['symbol'] and ticker['stock_name'] == stock_instance['stock_name']:
            return True
    return False


def add_stock_to_exchange(exchange_id: str, stock_instance: dict) -> bool:
    exchange_instance: ExchangeDataModel = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).get()
    if isinstance(exchange_instance, ExchangeDataModel):
        tickers_list: typing.List[dict] = exchange_instance.exchange_tickers_list
        if not(ticker_found(tickers_list=tickers_list, stock_instance=stock_instance)):
            tickers_list.append(stock_instance)
            if exchange_instance.set_exchange_tickers_list(tickers_list=tickers_list):
                exchange_instance.put()
                return True
    return False


def cron_call_eod_api():
    pass


def cron_call_yahoo_api():
    pass


def cron_call_pse_api():
    pass


# Crypto Currencies API's
def cron_call_binance_api():
    pass

