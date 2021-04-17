import typing
from datetime import datetime
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError

class MembershipValidators:

    @staticmethod
    def start_date_valid(start_date: datetime) -> bool:
        """
            check if date is from today and falls within normal parameters
        """
        now = datetime.now().date()
        if isinstance(start_date, datetime) and start_date > now:
            return True
        return False


class PlanValidators:

    @staticmethod
    def plan_exist(plan_id: str) -> bool:
        if not isinstance(plan_id, str):
            return False
        plan_id = plan_id.strip()
        if plan_id == "":
            return False
        plan_instance_list: typing.List[MembershipPlans] = MembershipPlans.query(
            MembershipPlans.plan_id == plan_id).fetch()
        if isinstance(plan_instance_list, list) and len(plan_instance_list) > 0:
            return True
        return False

    @staticmethod
    def plan_name_exist(plan_name: str) -> bool:
        if not isinstance(plan_name, str):
            return False
        plan_name = plan_name.strip().lower()
        if plan_name == "":
            return False
        plan_instance_list: typing.List[MembershipPlans] = MembershipPlans.query(MembershipPlans.plan_name == plan_name)
        if isinstance(plan_instance_list, list) and len(plan_instance_list) > 0:
            return True
        return False

class Memberships(ndb.Model):
    """
        TODO - add validators
    """
    uid = ndb.StringProperty()
    plan_id = ndb.StringProperty()
    status = ndb.StringProperty()  # Paid/ Unpaid
    date_created = ndb.DateTimeProperty()  # the date and time this plan was created
    plan_start_date = ndb.DateProperty()  # the date this plan will become active


class MembershipPlans(ndb.Model):
    """
        contains a definition of all membership plans
        TODO - add validators

    """
    def set_plan_id(self, value: str) -> str:
        if value is None or value == "":
            raise ValueError("{} cannot be Null".format(self.name))
        if not isinstance(value, str):
            raise TypeError("{} can only be a string ".format(self.name))
        if len(value) > 64:
            raise ValueError("Invalid format for ID")
        return value.strip()

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
        if not value in [1,2,3,4,5]:
            raise ValueError('{} can only be between 1 -> 5 of every month'.format(self.name))
        return value

    def set_number(self, value):
        if not isinstance(value, int):
            raise TypeError('{} can only be an integer'.format(self.name))

        if value < 0:
            raise TypeError("{} no negative numbers".format(self.name))

        return value

    plan_id = ndb.StringProperty(validator=set_plan_id)
    plan_name = ndb.StringProperty(validator=set_string)
    description = ndb.StringProperty(validator=set_string)
    total_members = ndb.IntegerProperty(validator=set_number)
    schedule_day = ndb.IntegerProperty(validator=set_schedule_day)  # 1 or 2 or 3 of every month or week, or three months
    schedule_term = ndb.StringProperty(validator=set_schedule_term)  # Monthly, Quarterly, Annually
    term_payment_amount = ndb.IntegerProperty(validator=set_number)
    registration_amount = ndb.IntegerProperty(validator=set_number)
    is_active = ndb.BooleanProperty(default=False)
    date_created = ndb.DateProperty(auto_now_add=True)


class AccessRights(ndb.Model):
    """
        TODO - add validators
    """
    plan_id = ndb.StringProperty()
    access_rights_list = ndb.StringProperty(repeated=True)  # a list containing the rights of users
