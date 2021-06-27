import typing
from datetime import datetime
from google.cloud import ndb
from data_service.store.mixins import AmountMixin
from data_service.views.exception_handlers import handle_store_errors


class WalletValidator:
    def __init__(self):
        pass

    @staticmethod
    @handle_store_errors
    def wallet_exist(uid: str) -> typing.Union[bool, None]:
        wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
        return True if isinstance(wallet_instance, WalletModel) else False

    # TODO complete validations for all Wallet Models
    # TODO be sure to integrate all models to the view


class ClassSetters:
    def __init__(self):
        self.transaction_types = ['withdrawal', 'deposit']

    def set_id(self, value: str) -> str:
        if (value is None) or (value == ""):
            raise ValueError(" {} cannot be Null".format(str(self)))

        if not isinstance(value, str):
            raise ValueError(" {} can only be a string".format(str(self)))
        return value

    def set_funds(self, value: AmountMixin) -> AmountMixin:
        if not isinstance(value, AmountMixin):
            raise ValueError(" {} Invalid Argument Type".format(str(self)))
        return value

    def set_paypal(self, value: str) -> str:
        if (value is None) or (value == ""):
            raise ValueError(" {} cannot be Null".format(str(self)))

        if not isinstance(value, str):
            raise ValueError(" {} can only be a string".format(str(self)))
        return value

    def set_transaction_types(self, value: str) -> str:
        if value not in self.transaction_types:
            raise ValueError(" {} invalid transaction type".format(str(self)))
        return value

    def set_datetime(self, value: datetime) -> datetime:
        if not isinstance(value, datetime):
            raise ValueError("{} invalid argument".format(str(self)))
        return value

    def set_bool(self, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValueError("{} invalid argument".format(str(self)))
        return value


class WalletModel(ndb.Model):
    uid: str = ndb.StringProperty(validator=ClassSetters.set_id)
    available_funds: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_funds)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)
    last_transaction_time: datetime = ndb.DateTimeProperty(auto_now=True)
    paypal_address: str = ndb.StringProperty(validator=ClassSetters.set_paypal)

    def __str__(self) -> str:
        return "<Wallet {}{}{}{}".format(self.paypal_address, self.available_funds, self.time_created,
                                         self.last_transaction_time)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.uid != other.uid:
            return False
        if self.paypal_address != other.paypal_address:
            return False
        return True


class WalletTransactionsModel(ndb.Model):
    uid: str = ndb.StringProperty(validator=ClassSetters.set_id)
    transaction_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    transaction_type: str = ndb.StringProperty(validator=ClassSetters.set_transaction_types)
    transaction_date: str = ndb.DateTimeProperty(auto_now_add=True, validator=ClassSetters.set_datetime)

    def __str__(self) -> str:
        return "<Transactions {} {}".format(self.transaction_type, self.transaction_date)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_type != other.transaction_type:
            return False
        if self.transaction_date != other.transaction_date:
            return False
        return True


class WalletTransactionItemModel(ndb.Model):
    transaction_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    item_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    is_verified: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)

    def __str__(self) -> str:
        return "{}{}".format(self.amount, self.is_verified)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        if self.item_id != other.item_id:
            return False
        if self.amount != other.amount:
            return False
        return True

