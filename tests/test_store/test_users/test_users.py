from datetime import datetime
from random import choice
from google.cloud.ndb.exceptions import BadValueError
from pytest import raises
from data_service.config.stocks import currency_symbols
from data_service.store.mixins import AmountMixin
from data_service.utils.utils import create_id, timestamp
from tests import int_positive
from data_service.store.users import UserModel

user_instance: UserModel = UserModel()

def test_uid():
    uid: str = create_id()
    assert user_instance.uid is None, "user instance uid default not initialized properly"
    user_instance.set_uid(uid)
    assert user_instance.uid == uid, "user instance uid not set properly"
    with raises(ValueError):
        user_instance.set_uid(uid="")

def test_names():
    names: str = "john"
    assert user_instance.names is None, "user instance names default not initialized properlu"
    user_instance.set_names(names=names)
    assert user_instance.names == names, "user instance names not being set properly"
    with raises(ValueError):
        user_instance.set_names(names="")

def test_surname():
    surname: str = "doe"
    assert user_instance.surname is None, "user instance surname default not initialized properly"
    user_instance.set_surname(surname=surname)
    assert user_instance.surname == surname, "user instance surnames not being set properly"
    with raises(ValueError):
        user_instance.set_surname(surname="")
    with raises(TypeError):
        user_instance.set_surname(surname=0)
