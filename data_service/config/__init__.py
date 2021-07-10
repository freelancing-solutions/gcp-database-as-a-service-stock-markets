import os
from decouple import config
import datetime


class Config:
    PROJECT = os.environ.get("PROJECT") or config("PROJECT")
    APP_NAME = os.environ.get("APP_NAME") or config("APP_NAME")
    DEFAULT_MEMBERSHIP_LIST = ["member"]
    DEFAULT_ACCESS_RIGHTS = ["visitor", "user", "super_user", "admin"]
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL") or config("ADMIN_EMAIL")
    UTC_OFFSET = datetime.timedelta(hours=4)
    DATA_SOURCE_TYPES = ['api', 'scrape']
    PUBSUB_VERIFICATION_TOKEN = os.environ.get("PUBSUB_VERIFICATION_TOKEN") or config("PUBSUB_VERIFICATION_TOKEN")
    DATASTORE_TIMEOUT: int = 3600  # seconds
    DATASTORE_RETRIES: int = 10  # total retries when saving to datastore
    CURRENCY: str = "PHP"
    BINANCE_API_KEY: str = os.environ.get("BINANCE_API_KEY") or config("BINANCE_API_KEY")
    BINANCE_SECRET: str = os.environ.get("BINANCE_SECRET_KEY") or config("BINANCE_SECRET_KEY")



