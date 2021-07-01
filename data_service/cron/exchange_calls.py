"""
    calls to exchanges to obtain financial information or data
    the calls will execute in certain dates and times in order to
    satisfy customer requirements

    calls read stock databases to get initial data, then goes to api's to obtain
    data for the day or time of day,
    if any missing data is detected its updated on the database
"""
import typing
from google.cloud import ndb
from data_service.store.stocks import Stock
from data_service.store.settings import ExchangeDataModel
from data_service.views.settings import ExchangeDataView


def stocks_by_exchange(exchange_id: str) -> typing.List[dict]:
    exchange_view_instance: ExchangeDataView = ExchangeDataView()
    response, status =  exchange_view_instance.get_exchange_tickers(exchange_id=exchange_id)
    response_data: dict = response.get_json()
    if response_data['status']:
        return response_data['payload']
    else:
        return []


def ticker_found(tickers_list: typing.List[dict], stock_instance: dict) -> bool:
    for ticker in tickers_list:
        if ticker['symbol'] == stock_instance['symbol'] and ticker['stock_name'] == stock_instance['stock_name']:
            return True
    return False


@ndb.tasklet
def add_stock_to_exchange(exchange_id: str, stock_instance: dict) -> bool:
    exchange_instance: ExchangeDataModel = ExchangeDataModel.query(ExchangeDataModel.exchange_id == exchange_id).get_async().result()
    if isinstance(exchange_instance, ExchangeDataModel):
        tickers_list: typing.List[dict] = exchange_instance.exchange_tickers_list
        if not(ticker_found(tickers_list=tickers_list, stock_instance=stock_instance)):
            tickers_list.append(stock_instance)
            if exchange_instance.set_exchange_tickers_list(tickers_list=tickers_list):
                key = exchange_instance.put_async().result()
                return True
    return False


async def get_stock_data_from_pse(symbol: str) -> dict:
    pass


def cron_call_eod_api():
    pass


def cron_call_yahoo_api():
    pass


def cron_call_pse_api():
    stock_exchanges_list: typing.List[dict] =


# Crypto Currencies API's
def cron_call_binance_api():
    pass

