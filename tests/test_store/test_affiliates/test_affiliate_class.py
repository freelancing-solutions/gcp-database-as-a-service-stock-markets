from datetime import datetime
from pytest import raises
from data_service.utils.utils import create_id, datetime_now
from data_service.store.affiliates import Affiliates
from tests import int_positive, int_negative

affiliate_instance: Affiliates = Affiliates()


def test_affiliate_id():
    temp_affiliate_id: str = create_id()
    assert affiliate_instance.affiliate_id is None, 'Affiliate id default not correctly instantiated'
    affiliate_instance.affiliate_id = temp_affiliate_id
    assert affiliate_instance.affiliate_id == temp_affiliate_id, 'affiliate_id default not being set correctly'
    with raises(TypeError):
        affiliate_instance.affiliate_id = int_positive()
    with raises(ValueError):
        affiliate_instance.affiliate_id = ""


def test_uid():
    temp_uid: str = create_id()
    assert affiliate_instance.uid is None, "affiliate uid default not set correctly"
    affiliate_instance.uid = temp_uid
    assert affiliate_instance.uid == temp_uid, "affiliate uid not being set correctly"
    with raises(TypeError):
        affiliate_instance.uid = int_positive()
    with raises(ValueError):
        affiliate_instance.uid = ""


def test_last_updated():
    last_update: datetime = datetime_now()
    assert affiliate_instance.last_updated is None, "affiliate last updated default not set correctly"
    affiliate_instance.last_updated = last_update
    assert affiliate_instance.last_updated == last_update, "affiliate last updated not being set correctly"
    with raises(TypeError):
        affiliate_instance.last_updated = int_positive()
    with raises(TypeError):
        affiliate_instance.last_updated = ""


def test_date_recruited():
    date_recruited: datetime = datetime_now()
    assert affiliate_instance.datetime_recruited is None, "affiliate date recruited default not set correctly"
    affiliate_instance.datetime_recruited = date_recruited
    assert affiliate_instance.datetime_recruited == date_recruited, "affiliate date recruited not being set correctly"
    with raises(TypeError):
        affiliate_instance.datetime_recruited = int_positive()
    with raises(TypeError):
        affiliate_instance.datetime_recruited = ""


def test_total_recruits():
    total_recruits: int = int_positive()
    assert affiliate_instance.total_recruits == 0, "affiliate total recruits default not set correctly"
    affiliate_instance.total_recruits = total_recruits
    assert affiliate_instance.total_recruits == total_recruits, "affiliates total not being set correctly"
    with raises(ValueError):
        affiliate_instance.total_recruits = int_negative()
    with raises(TypeError):
        affiliate_instance.total_recruits = ""


def test_is_active():
    is_active: bool = False
    assert affiliate_instance.is_active, "affiliate is active default not set correctly"
    affiliate_instance.is_active = is_active
    assert not affiliate_instance.is_active, "affiliate is active not being set correctly"
    with raises(TypeError):
        affiliate_instance.is_active = 0
    with raises(TypeError):
        affiliate_instance.is_active = 1
    with raises(TypeError):
        affiliate_instance.is_active = "true"


def test_is_deleted():
    is_deleted: bool = True
    assert not affiliate_instance.is_deleted, "affiliate is deleted default not set correctly"
    affiliate_instance.is_deleted = is_deleted
    assert affiliate_instance.is_deleted, "affiliate is deleted not being set correctly"
    with raises(TypeError):
        affiliate_instance.is_deleted = 0
    with raises(TypeError):
        affiliate_instance.is_deleted = 1
    with raises(TypeError):
        affiliate_instance.is_deleted = "true"
