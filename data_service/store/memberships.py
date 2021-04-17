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
    plan_id = ndb.StringProperty()
    plan_name = ndb.StringProperty()
    description = ndb.StringProperty()
    total_members = ndb.IntegerProperty()
    schedule_day = ndb.IntegerProperty()  # 1 or 2 or 3 of every month or week, or three months
    schedule_term = ndb.StringProperty()  # Monthly, Quarterly, Annually
    term_payment_amount = ndb.IntegerProperty()
    registration_amount = ndb.IntegerProperty()
    is_active = ndb.BooleanProperty(default=False)
    date_created = ndb.DateProperty()


class AccessRights(ndb.Model):
    """
        TODO - add validators
    """
    plan_id = ndb.StringProperty()
    access_rights_list = ndb.StringProperty(repeated=True)  # a list containing the rights of users
