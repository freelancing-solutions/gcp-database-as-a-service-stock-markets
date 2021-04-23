import typing
from google.cloud import ndb
from datetime import date, datetime
from google.api_core.exceptions import RetryError, Aborted
from data_service.store.mixins import AmountMixin
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError


class AffiliatesValidators:
    def __init__(self):
        super(AffiliatesValidators, self).__init__()

    @staticmethod
    def affiliate_exist(affiliate_id: str) -> typing.Union[None, bool]:
        if not isinstance(affiliate_id, str) or affiliate_id == "":
            raise ValueError("Affiliate ID cannot be Null, and Should be a String")
        try:
            affiliates_list: typing.List[Affiliates] = Affiliates.query(Affiliates.affiliate_id == affiliate_id).fetch()
            if isinstance(affiliates_list, list) and len(affiliates_list) > 0:
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

    @staticmethod
    def user_already_registered(uid: str) -> typing.Union[None, bool]:
        if not isinstance(uid, str) or uid == "":
            raise ValueError("UID cannot be Null, and should be a string")
        try:
            affiliates_list: typing.List[Affiliates] = Affiliates.query(Affiliates.uid == uid).fetch()
            if isinstance(affiliates_list, list) and len(affiliates_list) > 0:
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

class RecruitsValidators:
    def __init__(self):
        super(RecruitsValidators, self).__init__()

    @staticmethod
    def user_already_recruited(uid: str) -> typing.Union[None, bool]:
        if not isinstance(uid, str) or uid == "":
            raise ValueError("UID cannot be Null, and can only be a string")
        try:
            recruits_list: typing.List[Recruits] = Recruits.query(Recruits.uid == uid).fetch()
            if isinstance(recruits_list, list) and len(recruits_list) > 0:
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

    @staticmethod
    def user_already_an_affiliate(uid: str) -> typing.Union[None, bool]:

        if not isinstance(uid, str) or (uid == ""):
            raise ValueError("UID cannot be Null, and can only be a string")
        try:
            affiliates_list: typing.List[Affiliates] = Affiliates.query(Affiliates.uid == uid).fetch()
            if isinstance(affiliates_list, list) and len(affiliates_list) > 0:
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

class EarningsValidators:
    def __init__(self):
        super(EarningsValidators, self).__init__()

    @staticmethod
    def unclosed_earnings_already_exist(affiliate_id: str) -> typing.Union[None, bool]:
        if not isinstance(affiliate_id, str) or affiliate_id == "":
            raise ValueError("Affiliate_id cannot be Null, and can only be a string")
        try:
            earnings_list: typing.List[EarningsData] = EarningsData.query(
                EarningsData.affiliate_id == affiliate_id).fetch()
            if isinstance(earnings_list, list) and len(earnings_list) > 0:
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

class ClassSetters:
    def __init__(self):
        super(ClassSetters, self).__init__()

    def set_id(self, value: str) -> str:
        if (value == "") or (value is None):
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(self.name))
        return value

    def set_number(self, value: int) -> int:
        if (value == "") or (value is None):
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, int):
            raise TypeError("{} can only be an integer".format(self.name))
        return value

    def set_date(self, value: datetime) -> datetime:
        if not isinstance(value, datetime):
            raise TypeError("{}, can only be a datetime".format(self.name))
        return value

    def set_bool(self, value: bool) -> bool:
        if not isinstance(value, bool):
            raise TypeError("{}, can only be a boolean".format(self.name))
        return value

    def set_percent(self, value: int) -> int:
        if (value == "") or (value is None):
            raise ValueError("{} cannot be Null".format(self.name))

        if not isinstance(value, int):
            raise TypeError("{}, can only be an integer".format(self.name))

        if 0 < value > 100:
            raise ValueError("{}, should be a percent". format(self.name))

        return value

    def set_amount(self, amount: AmountMixin) -> AmountMixin:
        if not isinstance(amount, AmountMixin):
            raise TypeError('{} is invalid'.format(self.name))
        return amount

class Affiliates(ndb.Model):
    """
        class used to track affiliates registered
    """
    affiliate_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    uid: str = ndb.StringProperty(validator=ClassSetters.set_id)
    last_updated: datetime = ndb.DateTimeProperty(auto_now=True)
    datetime_recruited: datetime = ndb.DateTimeProperty(auto_now_add=True)
    total_recruits: int = ndb.IntegerProperty(default=0, validator=ClassSetters.set_number)
    is_active: bool = ndb.BooleanProperty(default=True, validator=ClassSetters.set_bool)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.uid != other.uid:
            return False
        return True

    def __str__(self):
        return "<Affiliates: date_recruited: {}, total_recruits: {}".format(self.datetime_recruited,
                                                                            self.total_recruits)

    def __repr__(self):
        return "<Affiliates: {}{}".format(self.affiliate_id, self.uid)

class Recruits(ndb.Model):
    """
        class used to track recruited affiliates
    """
    affiliate_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    referrer_uid: str = ndb.StringProperty(validator=ClassSetters.set_id)
    datetime_recruited: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=ClassSetters.set_date)
    datetime_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=ClassSetters.set_date)
    is_member: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)
    plan_id: str = ndb.StringProperty(validator=ClassSetters.set_id)  # Membership plan id allows to get payment fees
    is_active: bool = ndb.BooleanProperty(default=True, validator=ClassSetters.set_bool)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.referrer_uid != other.referrer_uid:
            return False
        return True

    def __str__(self) -> str:
        return "<Recruits: {}{}{}".format(self.affiliate_id, self.referrer_uid, self.datetime_recruited)

    def __repr__(self) -> str:
        return self.__str__()

class EarningsData(ndb.Model):
    """
        class used to track periodical earnings per affiliate
        #
    """
    def set_date(self, value) -> date:
        if not isinstance(value, date):
            raise ValueError("{} is invalid".format(self.name))
        return value

    affiliate_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    start_date: date = ndb.DateProperty(auto_now_add=True)
    last_updated: date = ndb.DateProperty(validator=set_date)
    total_earned: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    is_paid: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)
    on_hold: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.start_date != other.start_date:
            return False
        return True

    def __str__(self) -> str:
        return "<EarningsClass start_date: {}, end_date: {}, total_earned: {}, is_paid: {}, on_hold: {}".format(
            self.start_date, self.last_updated, self.total_earned, self.is_paid, self.on_hold)

    def __repr__(self) -> str:
        return self.__str__()


class AffiliateEarningsTransactions(ndb.Model):
    """
        keeps track of amounts paid from earningsData
    """
    affiliate_id: str = ndb.StringProperty()
    total_earned: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    transaction_id_list: typing.List[str] = ndb.StringProperty(repeated=True)
    last_transaction_time: datetime = ndb.DateTimeProperty(auto_now=True)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.total_earned != other.total_earned:
            return False
        return True

    def __str__(self) -> str:
        return "total_earned: {} ".format(str(self.total_earned))

    def __repr__(self) -> str:
        return self.__str__()


class AffiliateTransactionItems(ndb.Model):
    """
        keeps track of singular transaction items
    """
    transaction_id: str = ndb.StringProperty()
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    transaction_date: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=ClassSetters.set_date)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.amount != other.amount:
            return False
        if self.transaction_id != other.transaction_id:
            return False
        return True

    def __str__(self) -> str:
        return "<AffiliateTransactionItem Amount: {}, date: {}".format(str(self.amount), str(self.transaction_date))

    def __repr__(self) -> str:
        return self.__str__()


class AffiliateSettingsStats(ndb.Model):
    """
        if earnings are recurring then an affiliate will continue to earn income
        on their down-line , if not then income will be earned once off when a recruited user becomes a member.
    """
    earnings_percent: int = ndb.IntegerProperty(validator=ClassSetters.set_percent)
    recurring_earnings: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)
    total_affiliates_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    total_affiliates: int = ndb.IntegerProperty(default=0, validator=ClassSetters.set_number)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.earnings_percent != other.earnings_percent:
            return False
        if self.total_affiliates_earnings != other.total_affiliates_earnings:
            return False
        if self.total_affiliates != other.total_affiliates:
            return False
        return True

    def __str__(self) -> str:
        return "Earnings Percent: {}, Recurring Earnings: {}, Total Affiliates Earnings: {}, " \
               "Total Affiliates: {}".format(str(self.earnings_percent), str(self.recurring_earnings),
                                             str(self.total_affiliates_earnings), str(self.total_affiliates))

    def __repr__(self) -> str:
        return self.__str__()
