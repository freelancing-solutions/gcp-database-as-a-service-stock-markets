from google.cloud import ndb
from pinoydesk.utils.utils import create_id


class UserSettingsModel(ndb.Model):
    uid: str = ndb.StringProperty()


class AdminSettingsModel(ndb.Model):
    uid: str = ndb.StringProperty()


class ExchangeDataModel(ndb.Model):
    exchange_id: str = ndb.StringProperty()
    exchange_country: str = ndb.StringProperty()
    exchange_name: str = ndb.StringProperty()
    exchange_tickers_list: list = ndb.PickleProperty()  # an actual list datatype containing all
    # the available symbols
    last_accessed_timestamp: int = ndb.IntegerProperty(default=0)
    last_accessed_results: bool = ndb.BooleanProperty(default=True)  # if results where positive
    # true else false
    errors_list: str = ndb.StringProperty()  # comma separated list containing last accessed

    # errors if available
    def set_exchange_id(self) -> bool:
        self.exchange_id = create_id()
        return True

    def set_exchange_country(self, country: str) -> bool:
        country = country.strip().lower()
        if country is None or country == "":
            raise ValueError("country name cannot be Null")

        if not isinstance(country, str):
            raise TypeError("Country can only be a string")
        self.exchange_country = country
        return True

    def set_exchange_name(self, exchange: str) -> bool:
        exchange = exchange.strip().lower()
        if exchange is None or exchange == "":
            raise ValueError("exchange name cannot be Null")
        if not isinstance(exchange, str):
            raise TypeError("Exchange can only be a string")
        self.exchange_name = exchange
        return True

    def set_exchange_tickers_list(self, tickers_list: list) -> bool:
        if not isinstance(tickers_list, list):
            raise TypeError("exchange tickers can only be a list")
        self.exchange_tickers_list = tickers_list
        return True


class ScrappingPagesModel(ndb.Model):
    """
        a model to store pages that needs to be scrapped with their access times
        and settings-

        GCP Functions must be able to retrieve this information and then create endpoint urls to call
        then submit the results through pubsub

        GCP Functions will be called using tasks once a function is created it will be scheduled to run
        at a specific time through the console
    """
    exchange_id: str = ndb.StringProperty()
    page_id: str = ndb.StringProperty()
    scrapping_page_url: str = ndb.StringProperty()
    exchange_access_timestamps: str = ndb.StringProperty()
    require_login: bool = ndb.BooleanProperty(default=False)
    login_page_url: str = ndb.StringProperty()
    login_name: str = ndb.StringProperty()
    password: str = ndb.StringProperty()

    def set_page_id(self) -> bool:
        self.page_id = create_id()
        return True

    def set_scrapping_page_url(self, scrapping_page_url: str) -> bool:
        scrapping_page_url = scrapping_page_url.strip().lower()
        if scrapping_page_url is None or scrapping_page_url == "":
            raise ValueError('Scrapping page url can not be Null')
        if not isinstance(scrapping_page_url, str):
            raise TypeError("Scrapping Page URl can only be a string")
        self.scrapping_page_url = scrapping_page_url
        return True

    def set_exchange_access_timestamps(self, access_timestamps: list) -> bool:
        if access_timestamps is None or access_timestamps == "":
            raise ValueError('Exchange access timestamps cannot be Null')
        if not isinstance(access_timestamps, list):
            raise TypeError("Exchange access timestamps can only be list of stringed integers")
        self.exchange_access_timestamps = ",".join(access_timestamps)
        return True

    def read_exchange_access_timestamps(self) -> list:
        return self.exchange_access_timestamps.split(sep=",")

    def set_require_login(self, require_login: bool) -> bool:
        if isinstance(require_login, bool):
            self.require_login = require_login
            return True
        raise TypeError('require login can only be a boolean')

    def set_login_page_url(self, login_page_url: str) -> bool:
        login_page_url = login_page_url.strip()
        if login_page_url is None or login_page_url == "":
            raise ValueError('Login page url cannot be Null')
        if not isinstance(login_page_url, str):
            raise TypeError('Login page url can only be a string')
        self.login_page_url = login_page_url
        return True

    def set_login_name(self, login_name: str) -> bool:
        login_name = login_name.strip()
        if login_name is None or login_name == "":
            raise ValueError("login name cannot be Null")
        if not isinstance(login_name, str):
            raise TypeError("login name can only be a string")
        self.login_name = login_name
        return True

    def set_password(self, password: str) -> bool:
        password = password.strip()
        if password is None or password == "":
            raise ValueError("password cannot be Null")
        if not isinstance(password, str):
            raise TypeError("password can only be a string")
        self.password = password
        return True


class StockAPIEndPointModel(ndb.Model):
    """
        the actual api to call and its method
    """
    exchange_id: str = ndb.StringProperty()
    api_id: str = ndb.StringProperty()
    stocks_api_endpoint: str = ndb.StringProperty()  # if api is available should be stored here
    exchange_access_timestamps: str = ndb.StringProperty()
    method: str = ndb.StringProperty(default="GET")
    require_api_key: bool = ndb.BooleanProperty(default=False)
    api_key: str = ndb.StringProperty()

    def set_api_id(self) -> bool:
        self.api_id = create_id()
        return True

    def set_api_endpoint(self, api_endpoint: str) -> bool:
        api_endpoint = api_endpoint.strip().lower()
        if api_endpoint is None or api_endpoint == "":
            raise ValueError('API Endpoint cannot be null')
        if not isinstance(api_endpoint, str):
            raise TypeError("API Endpoint can only be a string")
        self.stocks_api_endpoint = api_endpoint
        return True

    def set_exchange_access_timestamps(self, access_timestamps: list) -> bool:
        if access_timestamps is None or access_timestamps == "":
            raise ValueError('Exchange access timestamps cannot be Null')
        if not isinstance(access_timestamps, list):
            raise TypeError("Exchange access timestamps can only be list of stringed integers")
        self.exchange_access_timestamps = ",".join(access_timestamps)
        return True

    def read_exchange_access_timestamps(self) -> list:
        return self.exchange_access_timestamps.split(sep=",")

    def set_method(self, method: str) -> bool:
        method = method.strip().upper()
        if method in ["GET", "POST", "PUT"]:
            self.method = method
            return True
        raise ValueError('Invalid HTTP Method')

    def set_require_api_key(self, require_api_key: bool) -> bool:
        if not isinstance(require_api_key, bool):
            raise TypeError("require api key can only be a boolean")
        self.require_api_key = require_api_key
        return True

    def set_api_key(self, api_key: str) -> bool:
        api_key = api_key.strip()
        if api_key is None or api_key == "":
            raise ValueError("API Key cannot be null")
        self.api_key = api_key
        return True

