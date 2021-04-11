import os
from decouple import config
import datetime


class Config:
    PROJECT = os.environ.get("PROJECT") or config("PROJECT")
    APP_NAME = os.environ.get("APP_NAME") or config("APP_NAME")
    DEFAULT_MEMBERSHIP_LIST = ["member"]
    DEFAULT_ACCESS_RIGHTS = ["visitor", "user", "super_user", "admin"]
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL") or config("ADMIN_EMAIL")
    UTC_OFFSET = datetime.timedelta(hours=2)
    DATA_SOURCE_TYPES = ['api', 'scrape']
    PUBSUB_VERIFICATION_TOKEN=os.environ.get("os.environ.get") or config("PUBSUB_VERIFICATION_TOKEN")



