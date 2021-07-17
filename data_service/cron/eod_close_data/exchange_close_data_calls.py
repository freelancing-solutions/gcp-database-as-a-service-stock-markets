"""
    calls to exchanges to obtain financial information or data
    the calls will execute in certain dates and times in order to
    satisfy customer requirements

    calls read stock databases to get initial data, then goes to api's to obtain
    data for the day or time of day,
    if any missing data is detected its updated on the database
"""
import datetime
import typing
from unittest.mock import sentinel
from google.cloud import ndb
from data_service.sdks.eod.eod_historical_data._utils import RemoteDataError
from data_service.store.settings import ExchangeDataModel
from data_service.utils.utils import create_id, date_string_to_date
from data_service.views.settings import ExchangeDataView
from data_service.views.stock_price import StockPriceDataView
from data_service.sdks.eod.eod_historical_data.data import get_eod_data_async
import asyncio
import aiohttp


def stocks_by_exchange(exchange_id: str) -> typing.List[dict]:
    exchange_view_instance: ExchangeDataView = ExchangeDataView()
    response, status = exchange_view_instance.get_exchange_tickers(exchange_id=exchange_id)
    response_data: dict = response.get_json()
    if response_data['status']:
        return response_data['payload']
    else:
        return []


def ticker_found(tickers_list: typing.List[dict], stock_instance: dict) -> bool:
    for ticker in tickers_list:
        if (ticker['symbol'] == stock_instance['symbol']) and (ticker['stock_name'] == stock_instance['stock_name']):
            return True
    return False


async def add_stock_to_exchange(exchange_id: str, stock_instance: dict) -> bool:
    exchange_instance: ExchangeDataModel = ExchangeDataModel.query(
        ExchangeDataModel.exchange_id == exchange_id).get_async().result()
    if isinstance(exchange_instance, ExchangeDataModel):
        tickers_list: typing.List[dict] = exchange_instance.exchange_tickers_list
        if not (ticker_found(tickers_list=tickers_list, stock_instance=stock_instance)):
            tickers_list.append(stock_instance)
            if exchange_instance.set_exchange_tickers_list(tickers_list=tickers_list):
                key = exchange_instance.put_async().result()
                return True
    return False


async def get_stock_close_data_from_pse(ticker: dict, exchange: dict) -> bool:
    """
        get stock data from pse ana save into the database
        # net_volumes, sell_volumes, buy_volumes
        if unable to get the data for the stock try eod
        TODO- complete this
        ticker: dict
        exchange: dict
    """
    pse_stock_endpoint: str = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(pse_stock_endpoint) as response:
            response_data = await response.json()
            # TODO get net volume
            # TODO get sell volume
            # TODO get buy volume
            # If cant obtain data use create task to use eod instead
            # TODO - send net , sell and buy for the stock to save to database
            pass
    return True


def convert_eod_stock_price_data(data) -> dict:
    """
        format:
            {
                "stock_id": "",
                "date_created": "",
                "price_open": 0,
                "price_high": 0,
                "price_low": 0,
                "price_close": 0,
                "adjusted_close": 0,
                "volume": 0
            }
    """
    def convert_to_int(num: float) -> int:
        return int(num * 100)

    return {
        "stock_id": create_id(),
        "date_created": date_string_to_date(date_str=data[0]),
        "price_open": convert_to_int(num=data[1]),
        "price_high": convert_to_int(num=data[2]),
        "price_low": convert_to_int(num=data[3]),
        "price_close": convert_to_int(num=data[4]),
        "adjusted_close": convert_to_int(num=data[5]),
        "volume": convert_to_int(num=data[6])
    }


async def get_stock_close_data_from_eod(ticker: dict, exchange: dict, today: bool = True) -> bool:
    """
        get stock data from eod ana save into the database
        # net_volumes, sell_volumes, buy_volumes
        if unable to get the data for the stock try yahoo
        TODO- Use python-eod sdk
    """
    try:
        stock_price_data: StockPriceDataView = StockPriceDataView()
        if today:
            response = await get_eod_data_async(symbol=ticker['symbol'],
                                                exchange=exchange['symbol'],
                                                start=str(datetime.datetime.now().date()),
                                                end=str(datetime.datetime.now().date()))
        else:
            response = await get_eod_data_async(symbol=ticker['symbol'],
                                                exchange=exchange['symbol'])

        if (response is not sentinel) and (response is not None):
            # this means response contains data as dataframe
            coro: list = []
            for data in response:
                stock_data: dict = convert_eod_stock_price_data(data=data)
                coro.append(stock_price_data.add_stock_price_data_async(stock_price_data=stock_data))

            if len(coro) > 0:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(asyncio.wait(coro))
    except RemoteDataError:
        pass
    return True


async def get_stock_close_data_from_yahoo(ticker: dict, exchange: dict) -> bool:
    """
        get stock data from yahoo finance ana save into the database
        # net_volumes, sell_volumes, buy_volumes
        if unable to get the data for the stock skip
        TODO- complete this
    """
    yahoo_stock_endpoint: str = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(yahoo_stock_endpoint) as response:
            response_data = await response.json()
            # TODO get net volume
            # TODO get sell volume
            # TODO get buy volume
            # If cant obtain data use create task to use eod instead
            # TODO - send net , sell and buy for the stock to save to database
            pass
    return True


async def get_crypto_close_data_from_binance(ticker: dict) -> bool:
    """
        get stock data from binance and save into database
        # net_volumes, sell_volumes, buy_volumes
        if unable to get the data for the stock try
            1. another exchange
            2. another one
        TODO- complete this
    """
    binance_stock_endpoint: str = ""
    async with aiohttp.ClientSession() as session:
        async with session.get(binance_stock_endpoint) as response:
            response_data = await response.json()
            # TODO get net volume
            # TODO get sell volume
            # TODO get buy volume
            # If cant obtain data use create task to use eod instead
            # TODO - send net , sell and buy for the stock to save to database
            pass
    return True


def cron_call_close_data_apis():
    exchange_view_instance: ExchangeDataView = ExchangeDataView()
    response, status = exchange_view_instance.return_all_exchanges()
    response_data: dict = response.get_json()
    coro: list = []
    if response_data['status']:
        exchange_list: typing.List[dict] = response_data['payload']
        for exchange in exchange_list:
            if exchange['exchange_type'] != 'crypto':
                response, status = exchange_view_instance.get_exchange_tickers(exchange_id=exchange['exchange_id'])
                response_data: dict = response.get_json()
                if response_data['status']:
                    exchange_tickers: typing.List[dict] = response_data['payload']
                    for ticker in exchange_tickers:
                        coro.append(get_stock_close_data_from_eod(ticker=ticker, exchange=exchange, today=True))
    if len(coro) > 0:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(asyncio.wait(coro))
    return 'OK', 200


def cron_call_crypto_close_data_api():
    exchange_view_instance: ExchangeDataView = ExchangeDataView()
    response, status = exchange_view_instance.return_all_exchanges()
    response_data: dict = response.get_json()
    coro: list = []
    if response_data['status']:
        exchange_list: typing.List[dict] = response_data['payload']
        for exchange in exchange_list:
            if exchange['exchange_type'] == 'crypto':
                if exchange['exchange_name'] == "binance":
                    response, status = exchange_view_instance.get_exchange_tickers(exchange_id=exchange['exchange_id'])
                    response_data: dict = response.get_json()
                    if response_data['status']:
                        exchange_tickers: typing.List[dict] = response_data['payload']
                        for ticker in exchange_tickers:
                            coro.append(get_crypto_close_data_from_binance(ticker=ticker))
    if len(coro) > 0:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(asyncio.wait(coro))
    return 'OK', 200


def cron_perform_net_calculations():
    pass

