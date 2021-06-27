from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError
from data_service.config.types import tickers_type, errors_type, timestamps_type
from data_service.utils.utils import create_id


class UserSettingsModel(ndb.Model):
    uid: str = ndb.StringProperty()
    #  TODO- complete this model
    #  TODO - complete the necessary d_under functions


class AdminSettingsModel(ndb.Model):
    uid: str = ndb.StringProperty()
    #  TODO- complete this model
    #  TODO - complete the necessary d_under functions


class ExchangeDataModel(ndb.Model):
    exchange_id: str = ndb.StringProperty()
    exchange_country: str = ndb.StringProperty()
    exchange_name: str = ndb.StringProperty()
    exchange_tickers_list: tickers_type = ndb.PickleProperty()  # an actual list datatype containing all
    # the available symbols
    last_accessed_timestamp: int = ndb.IntegerProperty(default=0)
    last_accessed_results: bool = ndb.BooleanProperty(default=True)  # if results where positive
    # true else false
    errors_list: errors_type = ndb.StringProperty(repeated=True)  # comma separated list containing last accessed

    def __str__(self) -> str:
        return "<Exchange {} {}".format(self.exchange_name, self.exchange_country)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.exchange_id != other.exchange_id:
            return False
        if self.exchange_name != other.exchange_name:
            return False
        if self.exchange_country != other.exchange_country:
            return False
        return True

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

    def set_exchange_tickers_list(self, tickers_list: tickers_type) -> bool:
        if not isinstance(tickers_list, tickers_type):
            raise TypeError("exchange tickers can only be a list")
        self.exchange_tickers_list = tickers_list
        return True
    # TODO - complete the necessary d_under functions


class ScrappingPagesModel(ndb.Model):
    """
        a model to store pages that needs to be scrapped with their access times
        and settings-

        GCP Functions must be able to retrieve this information and then create endpoint urls to call
        then submit the results through pubsub

        GCP Functions will be called using tasks once a function is created it will be scheduled to run
        at a specific time through the console
    """
    exchange_id: str = ndb.StringProperty(indexed=True)
    page_id: str = ndb.StringProperty(indexed=True)
    target_url: str = ndb.StringProperty()
    access_timestamps: timestamps_type = ndb.IntegerProperty(repeated=True)
    require_login: bool = ndb.BooleanProperty(default=False)
    login_page_url: str = ndb.StringProperty(default="")
    username: str = ndb.StringProperty(default="")
    password: str = ndb.StringProperty(default="")

    def __str__(self):
        return "<ScrappingPage {} {}".format(self.target_url, self.login_page_url)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.exchange_id != other.exchange_id:
            return False
        if self.page_id != other.page_id:
            return False
        if self.target_url != other.target_url:
            return False
        return True

    def set_exchange_id(self, exchange_id: str) -> bool:
        exchange_id = exchange_id.strip().lower()
        if exchange_id is None or exchange_id == "":
            raise ValueError('exchange_id can not be Null')
        if not isinstance(exchange_id, str):
            raise TypeError("exchange_id can only be a string")
        self.exchange_id = exchange_id
        return True

    def set_page_id(self) -> bool:
        self.page_id = create_id()
        return True

    def set_target_url(self, target_url: str) -> bool:
        target_url = target_url.strip().lower()
        if target_url is None or target_url == "":
            raise ValueError('Scrapping page url can not be Null')
        if not isinstance(target_url, str):
            raise TypeError("Scrapping Page URl can only be a string")
        self.target_url = target_url
        return True

    def set_access_timestamps(self, access_timestamps: timestamps_type) -> bool:
        if access_timestamps is None or access_timestamps == "":
            raise ValueError('Exchange access timestamps cannot be Null')
        if not isinstance(access_timestamps, timestamps_type):
            raise TypeError("Exchange access timestamps can only be list of stringed integers")
        self.access_timestamps = access_timestamps
        return True

    def read_exchange_access_timestamps(self) -> list:
        return self.access_timestamps

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

    def set_username(self, username: str) -> bool:
        username = username.strip()
        if username is None or username == "":
            raise ValueError("login name cannot be Null")
        if not isinstance(username, str):
            raise TypeError("login name can only be a string")
        self.username = username
        return True

    def set_password(self, password: str) -> bool:
        password = password.strip()
        if password is None or password == "":
            raise ValueError("password cannot be Null")
        if not isinstance(password, str):
            raise TypeError("password can only be a string")
        self.password = password
        return True
    # TODO - complete the necessary d_under functions


class StockAPIEndPointModel(ndb.Model):
    """
        the actual api to call and its method
    """
    exchange_id: str = ndb.StringProperty()
    api_id: str = ndb.StringProperty()
    stocks_api_endpoint: str = ndb.StringProperty()  # if api is available should be stored here
    exchange_access_timestamps: timestamps_type = ndb.IntegerProperty(repeated=True)
    method: str = ndb.StringProperty(default="GET")
    require_api_key: bool = ndb.BooleanProperty(default=False)
    api_key: str = ndb.StringProperty()

    def __str__(self):
        return "{}{}".format(self.stocks_api_endpoint, self.method)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.exchange_id != other.exchange_id:
            return False
        if self.api_id != other.api_id:
            return False
        if self.stocks_api_endpoint != other.stocks_api_endpoint:
            return False
        return True

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

    def set_exchange_access_timestamps(self, access_timestamps: timestamps_type) -> bool:
        if access_timestamps is None or access_timestamps == "":
            raise ValueError('Exchange access timestamps cannot be Null')
        if not isinstance(access_timestamps, timestamps_type):
            raise TypeError("Exchange access timestamps can only be list of stringed integers")
        self.exchange_access_timestamps = access_timestamps
        return True

    def read_exchange_access_timestamps(self) -> timestamps_type:
        return self.exchange_access_timestamps

    def set_method(self, method: str) -> bool:
        if not isinstance(method, str):
            raise TypeError('Invalid argument Type')

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

    # TODO - complete the necessary d_under functions
