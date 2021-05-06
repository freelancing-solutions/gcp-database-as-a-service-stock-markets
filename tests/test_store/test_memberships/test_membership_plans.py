from datetime import datetime
from random import choice

from google.cloud.ndb.exceptions import BadValueError
from pytest import raises

from data_service.config.stocks import currency_symbols
from data_service.store.mixins import AmountMixin
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

def set_schedule_term():
    schedule_term: str = "yearly"
    assert membership_plan_instance.schedule_term == "monthly", "membership_plan schedule term default is not " \
                                                                "set correctly"
    membership_plan_instance.schedule_term = schedule_term
    assert membership_plan_instance.schedule_term == schedule_term, "membership_plan schedule_term is not set correctly"
    schedule_term  = "quarterly"
    membership_plan_instance.schedule_term = schedule_term
    assert membership_plan_instance.schedule_term == schedule_term, "membership_plan schedule term is not set correctly"
    schedule_term  = "monthly"
    membership_plan_instance.schedule_term = schedule_term
    assert membership_plan_instance.schedule_term == schedule_term, "membership_plan schedule term is not set correctly"
    with raises(ValueError):
        membership_plan_instance.schedule_term = ""
    with raises(TypeError):
        membership_plan_instance.schedule_term = 0

def test_term_payment_amount():
    payment_amount: int = int_positive()
    currency: str = choice(currency_symbols())
    amount_instance: AmountMixin = AmountMixin(amount=payment_amount, currency=currency)
    assert membership_plan_instance.term_payment_amount is None, "membership_plan term_payment amount not set correctly"
    membership_plan_instance.term_payment_amount = amount_instance
    assert membership_plan_instance.term_payment_amount == amount_instance, "membership_plan term_payment amount not " \
                                                                            "set correctly"
    assert membership_plan_instance.term_payment_amount == amount_instance , "membership_plan term_amount not " \
                                                                             "set correctly"
    with raises(TypeError):
        membership_plan_instance.term_payment_amount = 0
    with raises(TypeError):
        membership_plan_instance.term_payment_amount = "o"

def test_registration_amount():
    payment_amount: int = int_positive()
    currency: str = choice(currency_symbols())
    amount_instance: AmountMixin = AmountMixin(amount=payment_amount, currency=currency)
    assert membership_plan_instance.registration_amount is None, "membership_plan registration not set correctly"
    membership_plan_instance.registration_amount = amount_instance
    assert membership_plan_instance.registration_amount == amount_instance, "membership_plan registration amount set " \
                                                                            "correctly"
    with raises(TypeError):
        membership_plan_instance.registration_amount = 0

    with raises(TypeError):
        membership_plan_instance.registration_amount = "0"

def test_is_active():
    is_active: bool = False
    assert not membership_plan_instance.is_active, "membership_pla is active not set correctly"
    membership_plan_instance.is_active = is_active
    assert membership_plan_instance.is_active == is_active, "membership_plan is_active not set correctly"
    with raises(TypeError):
        membership_plan_instance.is_active = 0
    with raises(TypeError):
        membership_plan_instance.is_active = "True"





