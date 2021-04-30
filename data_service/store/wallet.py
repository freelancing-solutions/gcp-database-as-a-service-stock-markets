import typing
from datetime import datetime
from google.api_core.exceptions import RetryError
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError
from werkzeug.security import generate_password_hash
from data_service.store.mixins import AmountMixin
from data_service.utils.utils import timestamp


class WalletValidator:
    def __init__(self):
        pass

    @staticmethod
    def wallet_exist(uid: str) -> bool:
        wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
        return True if isinstance(wallet_instance, WalletModel) else False

class ClassSetters:
    def __init__(self):
        self.transaction_types = ['withdrawal', 'deposit']

    def set_id(self, value: str) -> str:
        if value is None or value == "":
            raise ValueError(" {} cannot be Null".format(self.name))

        if not isinstance(value, str):
            raise ValueError(" {} can only be a string".format(self.name))

        return value

    def set_funds(self, value: AmountMixin) -> AmountMixin:
        if not isinstance(value, AmountMixin):
            raise ValueError(" {} Invalid Argument Type".format(self.name))
        return value

    def set_paypal(self, value: str) -> str:
        if value is None or value == "":
            raise ValueError(" {} cannot be Null".format(self.name))

        if not isinstance(value, str):
            raise ValueError(" {} can only be a string".format(self.name))

        return value

    def set_transaction_types(self, value: str) -> str:
        if value not in self.transaction_types:
            raise ValueError(" {} invalid transaction type".format(self.name))
        return value

    def set_datetime(self, value: datetime) -> datetime:
        if not isinstance(value, datetime):
            raise ValueError("{} invalid argument".format(self.name))

        return value

    def set_bool(self, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValueError("{} invalid argument".format(self.name))
        return value

class WalletModel(ndb.Model):
    uid: str = ndb.StringProperty(validator=ClassSetters.set_id)
    available_funds: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_funds)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)
    last_transaction_time: datetime = ndb.DateTimeProperty(auto_now=True)
    paypal_address: str = ndb.StringProperty(validator=ClassSetters.set_paypal)

class WalletTransactionsModel(ndb.Model):
    uid: str = ndb.StringProperty(validator=ClassSetters.set_id)
    transaction_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    transaction_type: str = ndb.StringProperty(validator=ClassSetters.set_transaction_types)
    transaction_date: str = ndb.DateTimeProperty(auto_now_add=True, validator=ClassSetters.set_datetime)

class WalletTransactionItemModel(ndb.Model):
    transaction_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    item_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_verified: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)