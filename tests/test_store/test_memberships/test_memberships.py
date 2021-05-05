from datetime import datetime
from pytest import raises
from data_service.utils.utils import create_id, datetime_now
from tests import int_positive, int_negative
from data_service.store.memberships import Memberships

membership_instance: Memberships = Memberships()

def test_uid():
    uid: str = create_id()
    assert membership_instance.uid is None, "membership uid default not properly set"
    membership_instance.uid = uid
    assert membership_instance.uid == uid, "membership uid default not properly set"
    with raises(TypeError):
        membership_instance.uid = 0
    with raises(ValueError):
        membership_instance.uid = ""

def test_plan_id():
    plan_id: str = create_id()
    assert membership_instance.plan_id is None, "membership plan_id default not properly set"
    membership_instance.plan_id = plan_id
    assert membership_instance.plan_id == plan_id, "membership plan_id is not being set properly"
    with raises(TypeError):
        membership_instance.plan_id = 0

    with raises(ValueError):
        membership_instance.plan_id = ""


def test_status():
    status: str = "paid"
    assert membership_instance.status == "unpaid", "membership status default not being set properly"
    membership_instance.status = status
    assert membership_instance.status == status, "membership status is not bein set properly"
    status = "unpaid"
    membership_instance.status = status
    assert membership_instance.status == status, "membership status is not bein set properly"
    with raises(TypeError):
        membership_instance.status = 0
    with raises(ValueError):
        membership_instance.status = ""


def test_date_created():
    date_created: datetime = datetime.now()
    assert membership_instance.date_created is None, "membership date_created default not set correctly"
    membership_instance.date_created = date_created
    assert membership_instance.date_created == date_created, "membership date_created is being set correctly"
    with raises(TypeError):
        membership_instance.date_created = 0
    with raises(TypeError):
        membership_instance.date_created =""

def test_plan_start_date():
    plan_start_date: datetime = datetime.now()
    assert membership_instance.plan_start_date is None, "membership plan_start_date default not set correctly"
    membership_instance.plan_start_date = plan_start_date
    assert membership_instance.plan_start_date == plan_start_date, "membership plan_start_date not being set correctly"
    with raises(TypeError):
        membership_instance.plan_start_date = 0
    with raises(TypeError):
        membership_instance.plan_start_date = "2017/09/09"
    with raises(TypeError):
        membership_instance.plan_start_date = ""





