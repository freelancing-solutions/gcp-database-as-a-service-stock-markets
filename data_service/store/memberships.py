import typing
from datetime import datetime, date
from google.api_core.exceptions import RetryError, Aborted
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError

from data_service.store.mixins import AmountMixin


class MembershipValidators:

    @staticmethod
    def start_date_valid(start_date: date) -> bool:
        """
            check if date is from today and falls within normal parameters
        """
        now = datetime.now().date()
        if isinstance(start_date, date) and start_date > now:
            return True
        return False


class PlanValidators:

    @staticmethod
    def plan_exist(plan_id: str) -> typing.Union[None, bool]:
        """
            return True or False
            return None if Error
        """
        if not isinstance(plan_id, str):
            return False
        plan_id = plan_id.strip()
        if plan_id == "":
            return False
        try:
            plan_instance_list: typing.List[MembershipPlans] = MembershipPlans.query(
                MembershipPlans.plan_id == plan_id).fetch()
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        except Aborted:
            return None
        if isinstance(plan_instance_list, list) and len(plan_instance_list) > 0:
            return True
        return False

    @staticmethod
    def plan_name_exist(plan_name: str) -> typing.Union[None, bool]:
        """
            returns True or False if plan exist or dont exist
            returns None if an error occured
        """
        if not isinstance(plan_name, str):
            return False
        plan_name = plan_name.strip().lower()
        if plan_name == "":
            return False
        try:
            plan_instance_list: typing.List[MembershipPlans] = MembershipPlans.query(
                MembershipPlans.plan_name == plan_name)
            if isinstance(plan_instance_list, list) and len(plan_instance_list) > 0:
                return True

        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        return False


class ClassSetters:
    def set_id(self, value: str) -> str:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string ".format(self.name))
        if len(value) > 64:
            raise ValueError("Invalid format for ID")
        return value.strip()

    def set_status(self, value: str) -> str:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        value = value.strip().lower()
        if value not in ['paid', 'upaid']:
            raise TypeError("{} invalid status".format(self.name))
        return value

    def set_datetime(self, value: date) -> object:
        if not isinstance(value, date):
            raise TypeError("{}, invalid datetime".format(self.name))
        return value

    def set_string(self, value: str) -> str:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string ".format(self.name))
        return value.strip()

    def set_schedule_term(self, value: str) -> str:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string ".format(self.name))
        value = value.strip().lower()
        if value in ["monthly", "quarterly", "annually"]:
            return value
        raise ValueError("Invalid scheduled term")

    def set_schedule_day(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError('{} can only be an integer'.format(self.name))
        if value not in [1, 2, 3, 4, 5]:
            raise ValueError('{} can only be between 1 -> 5 of every month'.format(self.name))
        return value

    def set_number(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError('{} can only be an integer'.format(self.name))

        if value < 0:
            raise TypeError("{} no negative numbers".format(self.name))

        return value

    def set_bool(self, value: bool) -> bool:
        if not isinstance(value, bool):
            raise TypeError("{}, should be boolean".format(self.name))
        return value

    def set_amount(self, value: AmountMixin) -> AmountMixin:
        if not isinstance(value, AmountMixin):
            raise TypeError("{}, Amount Invalid".format(self.name))
        return value


class Memberships(ndb.Model):
    """
        TODO - add validators
    """
    uid: str = ndb.StringProperty(validator=ClassSetters.set_id)
    plan_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    status: str = ndb.StringProperty(validator=ClassSetters.set_status)  # Paid/ Unpaid
    date_created: date = ndb.DateTimeProperty(auto_now_add=True,
                                              validator=ClassSetters.set_datetime)
    plan_start_date: date = ndb.DateProperty(validator=ClassSetters.set_datetime)  # the date this plan will become active

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.uid != other.uid:
            return False

        if self.plan_id != other.plan_id:
            return False
        return True

    def __str__(self) -> str:
        return "<Memberships: status: {}, date_created: {}, start_date: {}".format(self.status, str(self.date_created),
                                                                                   str(self.plan_start_date))

    def __repr__(self) -> str:
        return "Memberships: {}{}{}".format(self.uid, self.plan_id, self.status)


class MembershipPlans(ndb.Model):
    """
        contains a definition of all membership plans
        TODO - add validators
    """
    plan_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    plan_name: str = ndb.StringProperty(validator=ClassSetters.set_string)
    description: str = ndb.StringProperty(validator=ClassSetters.set_string)
    total_members: int = ndb.IntegerProperty(validator=ClassSetters.set_number)
    schedule_day: int = ndb.IntegerProperty(validator=ClassSetters.set_schedule_day)  # 1 or 2 or 3 of every month or week, or three months
    schedule_term: str = ndb.StringProperty(validator=ClassSetters.set_schedule_term)  # Monthly, Quarterly, Annually
    term_payment_amount: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    registration_amount: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    is_active: bool = ndb.BooleanProperty(default=False, validator=ClassSetters.set_bool)
    date_created: int = ndb.DateProperty(auto_now_add=True, validator=ClassSetters.set_datetime)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.plan_id != other.__class__:
            return False
        return True

    def __str__(self) -> str:
        return "<MembershipPlans: plan_name: {}, description: {}, total_members: {}, schedule_day: {}, " \
               "term : {}".format(self.plan_name, self.description, self.total_members,
                                   self.schedule_day, self.schedule_term)

    def __repr__(self) -> str:
        return "<Memberships: {}{}".format(self.plan_id, self.plan_name)


class AccessRights(ndb.Model):
    """
        # TODO - add validators
        # TODO - use access rights to protect routes on the client app
        # There should be a route that the client app can call to get permission for a route,
        #  the route should accept route and uid and then respond with True or False
        # of all the routes he or she can access
    """
    plan_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    access_rights_list = ndb.StringProperty(repeated=True)  # a list containing the rights of users


class MembershipDailyStats(ndb.Model):
    """
        provides information and settings pertaining to paying members

        run update stats task against this class daily
    """
    daily_id: str = ndb.StringProperty(validator=ClassSetters.set_id)
    total_users: int = ndb.IntegerProperty(default=0)
    total_members: int = ndb.IntegerProperty(default=0)
    expected_monthly_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    expected_quarterly_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    expected_annual_earnings: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    expected_earnings_this_month: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)
    total_earned_so_far: AmountMixin = ndb.StructuredProperty(AmountMixin, validator=ClassSetters.set_amount)

