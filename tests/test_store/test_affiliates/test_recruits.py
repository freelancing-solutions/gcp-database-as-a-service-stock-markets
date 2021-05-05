from datetime import datetime
from pytest import raises
from data_service.utils.utils import create_id, today, datetime_now
from data_service.store.affiliates import Recruits
from tests import int_positive, int_negative

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

