import typing
from google.cloud import ndb
from datetime import date, datetime
from google.api_core.exceptions import RetryError, Aborted
from data_service.store.mixins import AmountMixin


class AffiliatesValidators:
    def __init__(self):
        super(AffiliatesValidators, self).__init__()

    @staticmethod
    def affiliate_exist(affiliate_id: typing.Union[str, None]) -> typing.Union[None, bool]:
        if not(isinstance(affiliate_id, str)) or (affiliate_id == ""):
            raise ValueError("Affiliate ID cannot be Null, and Should be a String")
        try:
            affiliate_instance: Affiliates = Affiliates.query(Affiliates.affiliate_id == affiliate_id).get()
            if isinstance(affiliate_instance, Affiliates):
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

    @staticmethod
    def user_already_registered(uid: typing.Union[str, None]) -> typing.Union[None, bool]:
        if not(isinstance(uid, str)) or (uid == ""):
            raise ValueError("UID cannot be Null, and should be a string")
        try:
            affiliate_instance: Affiliates = Affiliates.query(Affiliates.uid == uid).get()
            if isinstance(affiliate_instance, Affiliates):
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

    # noinspection DuplicatedCode
    @staticmethod
    def user_already_recruited(uid: typing.Union[str, None]) -> typing.Union[None, bool]:
        if not(isinstance(uid, str)) or (uid == ""):
            raise ValueError("UID cannot be Null, and can only be a string")
        try:
            recruit_instance: Recruits = Recruits.query(Recruits.uid == uid).get()
            if isinstance(recruit_instance, Recruits):
                return True
            return False
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None

    @staticmethod
    def user_already_an_affiliate(uid: typing.Union[str, None]) -> typing.Union[None, bool]:
        if not(isinstance(uid, str)) or (uid == ""):
            raise ValueError("UID cannot be Null, and can only be a string")
        try:
            affiliate_instance: Affiliates = Affiliates.query(Affiliates.uid == uid).get()
            if isinstance(affiliate_instance, Affiliates):
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
        if not(isinstance(affiliate_id, str)) or (affiliate_id == ""):
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
        pass

    @staticmethod
    def set_id(prop, value: typing.Union[str, None]) -> str:
        if value == "":
            raise ValueError("{} cannot be Null".format(str(prop)))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string".format(str(prop)))
        return value

    @staticmethod
    def set_number(prop, value: int) -> int:
        if not(isinstance(value, int)):
            raise TypeError("{} can only be an integer".format(str(prop)))
        if value < 0:
            raise ValueError('{} can only be positive integer'.format(str(prop)))
        return value

    @staticmethod
    def set_date(prop, value: datetime) -> datetime:
        if not(isinstance(value, datetime)):
            raise TypeError("{}, can only be a datetime".format(str(prop)))
        return value

    @staticmethod
    def set_bool(prop, value: bool) -> bool:
        if not(isinstance(value, bool)):
            raise TypeError("{}, can only be a boolean".format(str(prop)))
        return value

    @staticmethod
    def set_percent(prop, value: int) -> int:
        if not(isinstance(value, int)):
            raise TypeError("{}, can only be an integer".format(str(prop)))
        if 0 < value > 100:
            raise ValueError("{}, should be a percent".format(str(prop)))
        return value

    @staticmethod
    def set_amount(prop, amount: AmountMixin) -> AmountMixin:
        if not(isinstance(amount, AmountMixin)):
            raise TypeError('{} is invalid'.format(str(prop)))
        return amount


setters: ClassSetters = ClassSetters()


class Affiliates(ndb.Model):
    """
        class used to track affiliates registered
    """

    def set_date_time(self, value: datetime) -> datetime:
        if not(isinstance(value, datetime)):
            raise TypeError("{} can only be a datetime object".format(str(self)))
        return value

    affiliate_id: str = ndb.StringProperty(validator=setters.set_id)
    uid: str = ndb.StringProperty(validator=ClassSetters.set_id)
    last_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=set_date_time)
    datetime_recruited: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=set_date_time)
    total_recruits: int = ndb.IntegerProperty(default=0, validator=setters.set_number)
    is_active: bool = ndb.BooleanProperty(default=True, validator=setters.set_bool)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.uid != other.uid:
            return False
        return True

    def __str__(self) -> str:
        return "<Affiliates: date_recruited: {}, total_recruits: {}".format(self.datetime_recruited,
                                                                            self.total_recruits)

    def __repr__(self) -> str:
        return "<Affiliates: {}{}".format(self.affiliate_id, self.uid)


class Recruits(ndb.Model):
    """
        class used to track recruited affiliates
    """
    affiliate_id: str = ndb.StringProperty(validator=setters.set_id)
    referrer_uid: str = ndb.StringProperty(validator=setters.set_id)
    datetime_recruited: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_date)
    datetime_updated: datetime = ndb.DateTimeProperty(auto_now=True, validator=setters.set_date)
    is_member: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    plan_id: str = ndb.StringProperty(validator=setters.set_id)  # Membership plan id allows to get payment fees
    is_active: bool = ndb.BooleanProperty(default=True, validator=setters.set_bool)
    is_deleted: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)

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

    affiliate_id: str = ndb.StringProperty(validator=setters.set_id)
    start_date: date = ndb.DateProperty(auto_now_add=True)
    last_updated: date = ndb.DateProperty(validator=setters.set_date)
    total_earned: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=setters.set_amount)
    is_paid: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    on_hold: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.start_date != other.start_date:
            return False
        if self.total_earned != other.total_earned:
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
    affiliate_id: str = ndb.StringProperty(validator=setters.set_id)
    total_earned: AmountMixin = ndb.StructuredProperty(AmountMixin)
    transaction_id_list: typing.List[str] = ndb.StringProperty(repeated=True)
    last_transaction_time: datetime = ndb.DateTimeProperty(auto_now=True, validator=setters.set_date)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.affiliate_id != other.affiliate_id:
            return False
        if self.total_earned != other.total_earned:
            return False
        return True

    def __str__(self) -> str:
        return "<Total Earned: {} ".format(str(self.total_earned))

    def __repr__(self) -> str:
        return self.__str__()


class AffiliateTransactionItems(ndb.Model):
    """
        keeps track of singular transaction items
    """
    transaction_id: str = ndb.StringProperty(validator=setters.set_id)
    amount: AmountMixin = ndb.StructuredProperty(AmountMixin)
    transaction_date: datetime = ndb.DateTimeProperty(auto_now_add=True, validator=setters.set_date)

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
        on their down-line ,
        if not then income will be earned once off when a recruited
        user becomes a member.
    """
    earnings_percent: int = ndb.IntegerProperty(validator=setters.set_percent)
    recurring_earnings: bool = ndb.BooleanProperty(default=False, validator=setters.set_bool)
    total_affiliates_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin)
    total_affiliates: int = ndb.IntegerProperty(default=0, validator=setters.set_number)

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
