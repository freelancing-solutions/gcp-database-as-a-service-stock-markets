from datetime import datetime
from pytest import raises
from data_service.utils.utils import create_id
from data_service.store.affiliates import Recruits


recruit_instance: Recruits = Recruits()

def test_recruit_affiliate_id():
    rec_id: str = create_id()

    assert recruit_instance.affiliate_id is None, "recruits affilite id is not being set correctly"
    recruit_instance.affiliate_id = rec_id
    assert recruit_instance.affiliate_id == rec_id, "recruits affiliate id is not being set correctly"
    with raises(TypeError):
        recruit_instance.affiliate_id = 1
    with raises(ValueError):
        recruit_instance.affiliate_id = ""

def test_recruit_referrer_uid():
    referrer_uid: str = create_id()

    assert recruit_instance.referrer_uid is None, "recruits referrer_uid is not being set correctly"
    recruit_instance.referrer_uid = referrer_uid
    assert recruit_instance.referrer_uid == referrer_uid, "recruits referrer_uid is not being set correctly"
    with raises(TypeError):
        recruit_instance.referrer_uid = 1
    with raises(ValueError):
        recruit_instance.referrer_uid = ""

def test_datetime_recruited():
    datetime_recruited: datetime = datetime.now()

    assert recruit_instance.datetime_recruited is None, "recruits date recruited default not being set correctly"
    recruit_instance.datetime_recruited = datetime_recruited
    assert recruit_instance.datetime_recruited == datetime_recruited, "recruits date recruited not being set correctly"
    with raises(TypeError):
        recruit_instance.datetime_recruited = 0
    with raises(TypeError):
        recruit_instance.datetime_recruited = "date"

def test_datetime_updated():
    datetime_updated: datetime = datetime.now()

    assert recruit_instance.datetime_updated is None, "recruits datetime_updated default not being set correctly"
    recruit_instance.datetime_updated = datetime_updated
    assert recruit_instance.datetime_updated == datetime_updated, "recruits datetime_updated not being set correctly"
    with raises(TypeError):
        recruit_instance.datetime_updated = 0
    with raises(TypeError):
        recruit_instance.datetime_updated = "date"


def test_is_member():
    is_member: bool = True

    assert not recruit_instance.is_member, "recruits is member default not being set correctly"
    recruit_instance.is_member = is_member
    assert recruit_instance.is_member, "recruits is member not being set correctly"
    with raises(TypeError):
        recruit_instance.is_member = 0
    with raises(TypeError):
        recruit_instance.is_member = 1
    with raises(TypeError):
        recruit_instance.is_member = "None"


def test_plan_id():
    plan_id: str = create_id()
    assert not recruit_instance.plan_id, "recruits plan id not being set correctly"
    recruit_instance.plan_id = plan_id
    assert recruit_instance.plan_id == plan_id, "recruits plan id not being set correctly"
    with raises(TypeError):
        recruit_instance.plan_id = 0
    with raises(ValueError):
        recruit_instance.plan_id = ""

def test_is_active():
    is_active: bool = False
    assert recruit_instance.is_active, "recruit is active is not being set correctly"
    recruit_instance.is_active = is_active
    assert recruit_instance.is_active == is_active, "recruit is active is not being set correctly"
    with raises(TypeError):
        recruit_instance.is_active = 0
    with raises(TypeError):
        recruit_instance.is_active = 1

def test_is_deleted():
    is_deleted: bool = True
    assert not recruit_instance.is_deleted, "recruit is_deleted is not being set correctly"
    recruit_instance.is_deleted = is_deleted
    assert recruit_instance.is_deleted == is_deleted, "recruit is_deleted is not being set correctly"
    with raises(TypeError):
        recruit_instance.is_deleted = 0
    with raises(TypeError):
        recruit_instance.is_deleted = 1