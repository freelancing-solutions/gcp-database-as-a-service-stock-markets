from datetime import datetime
from pytest import raises
from data_service.utils.utils import create_id, datetime_now
from tests import int_positive, int_negative
from data_service.store.memberships import MembershipPlans

membership_plan_instance: MembershipPlans = MembershipPlans()
def test_plan_id():
    plan_id: str = create_id()
    assert membership_plan_instance.plan_id is None, "plan_id membership_plan plan_id default not set properly"
    membership_plan_instance.plan_id = plan_id
    assert membership_plan_instance.plan_id == plan_id, "membership_plan plan_id is not being set correctly"
    with raises(TypeError):
        membership_plan_instance.plan_id = 0
    with raises(ValueError):
        membership_plan_instance.plan_id = ""


def test_plan_name():
    plan_name: str = "bronze"
    assert membership_plan_instance.plan_name is None, "membership_plans plan name is not being set correctly"
    membership_plan_instance.plan_name = plan_name
    assert membership_plan_instance.plan_name == plan_name, "membership plan_name is not being set correctly"
    with raises(TypeError):
        membership_plan_instance.plan_name = 0
    with raises(ValueError):
        membership_plan_instance.plan_name = ""

def test_description():
    description: str = "bronze plan"
    assert membership_plan_instance.description is None, "membership_plan description is not being set correctly"
    membership_plan_instance.description = description
    assert membership_plan_instance.description == description, "membership_plan is not being set correctly"
    with raises(TypeError):
        membership_plan_instance.description = 0
    with raises(ValueError):
        membership_plan_instance.description = ""

def set_total_members():
    total_members: int = 0
    assert membership_plan_instance.total_members == 0, "membership_plan total_members is not being set correctly"
    membership_plan_instance.total_members = total_members
    assert membership_plan_instance.total_members == total_members, "membership_plan total_members is not being set"
    with raises(TypeError):
        membership_plan_instance.total_members = "0"
    with raises(ValueError):
        membership_plan_instance.total_members = int_negative()

def set_schedule_day():
    schedule_day: int = 0
    assert membership_plan_instance.schedule_day is None, "membership_plan schedule_day default is not set correctly"
    membership_plan_instance.schedule_day = schedule_day
    assert membership_plan_instance.schedule_day == schedule_day, "membership_plan schedule_day is not set correctly"
    with raises(TypeError):
        membership_plan_instance.schedule_day = "0"
