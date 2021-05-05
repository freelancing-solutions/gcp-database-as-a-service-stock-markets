from datetime import datetime
from pytest import raises
from data_service.utils.utils import create_id, today, datetime_now
from data_service.store.affiliates import Recruits
from tests import int_positive, int_negative

recruitment_instance: Recruits = Recruits()

def test_recruit_affiliate_id():
    affiliate_id: int = create_id()
    assert recruitment_instance.affiliate_id is None, "recruits affiliate_id default was not set correctly"
    recruitment_instance.affiliate_id = affiliate_id
    assert recruitment_instance.affiliate_id == affiliate_id, "recruits affilite_id is not being set correctly"
    with raises(TypeError):
        recruitment_instance.affiliate_id = 0
    with raises(ValueError):
        recruitment_instance.affiliate_id = ""


def test_recruit_referrer_uid():
    referrer_uid: int = create_id()
    assert recruitment_instance.referrer_uid is None, "recruits referrer_uid default was not set correctly"
    recruitment_instance.referrer_uid = referrer_uid
    assert recruitment_instance.referrer_uid == referrer_uid, "recruits referrer_uid is not being set correctly"
    with raises(TypeError):
        recruitment_instance.referrer_uid = 0
    with raises(ValueError):
        recruitment_instance.referrer_uid = ""

def test_datetime_recruited():
    datetime_recruited: datetime = datetime.now()
    assert recruitment_instance.datetime_recruited is None, "recruits recruited_datetime was not set correctly"
    recruitment_instance.datetime_recruited = datetime_recruited
    assert recruitment_instance.datetime_recruited, "recruits recruited_datetime is not set correctly"
    with raises(TypeError):
        recruitment_instance.datetime_recruited = 0
    with raises(TypeError):
        recruitment_instance.datetime_recruited = ""


def test_datetime_updated():
    datetime_updated: datetime = datetime.now()
    assert recruitment_instance.datetime_updated is None, "recruits datetime_updated was not set correctly"
    recruitment_instance.datetime_updated = datetime_updated
    assert recruitment_instance.datetime_updated, "recruits datetime_updated is not set correctly"
    with raises(TypeError):
        recruitment_instance.datetime_updated = 0
    with raises(TypeError):
        recruitment_instance.datetime_updated = ""

def test_is_member():
    is_member: bool = True
    assert not recruitment_instance.is_member, "recruits is_member default not set correctly"
    recruitment_instance.is_member = is_member
    assert recruitment_instance.is_member == is_member, "recruits is_member default not set correctly"
    with raises(TypeError):
        recruitment_instance.is_member = 0
    with raises(TypeError):
        recruitment_instance.is_member = "0"


def test_plan_id():
    plan_id: str = create_id()
    assert not recruitment_instance.plan_id, "recruits plan_id default not set correctly"
    recruitment_instance.plan_id = plan_id
    assert recruitment_instance.plan_id == plan_id, "recruits plan_id not set correctly"
    with raises(TypeError):
        recruitment_instance.plan_id = 0
    with raises(ValueError):
        recruitment_instance.plan_id = ""


def test_is_active():
    is_active: bool = False
    assert recruitment_instance.is_active, "recruits is_active default not set correctly"
    recruitment_instance.is_active = is_active
    assert recruitment_instance.is_active == is_active, "recruits is_active default not set correctly"
    with raises(TypeError):
        recruitment_instance.is_active = 0
    with raises(TypeError):
        recruitment_instance.is_active = ""

def test_is_deleted():
    is_deleted: bool = True
    assert not recruitment_instance.is_deleted, "recruits is_deleted default not set correctly"
    recruitment_instance.is_deleted = is_deleted
    assert recruitment_instance.is_deleted == is_deleted, "recruits is_deleted default not set correctly"
    with raises(TypeError):
        recruitment_instance.is_deleted = 0
    with raises(TypeError):
        recruitment_instance.is_deleted = ""

