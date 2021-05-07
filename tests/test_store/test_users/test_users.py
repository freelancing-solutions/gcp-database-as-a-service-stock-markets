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
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_names(names=0)

def test_surname():
    surname: str = "doe"
    assert user_instance.surname is None, "user instance surname default not initialized properly"
    user_instance.set_surname(surname=surname)
    assert user_instance.surname == surname, "user instance surnames not being set properly"
    with raises(ValueError):
        user_instance.set_surname(surname="")
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_surname(surname=0)

def test_cell():
    cell : str = "0761234567"
    assert user_instance.cell is None, "user instance cell default not initialized properly"
    user_instance.set_cell(cell=cell)
    assert user_instance.cell == cell, "user instance cell not being set properly"
    with raises(ValueError):
        user_instance.set_cell(cell="")
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_cell(cell=277627771)

def test_email():
    email: str = "mobiusndou@gmail.com"
    assert user_instance.email is None, "user instance email default not initialized properly"
    user_instance.set_email(email=email)
    assert user_instance.email == email, "user instance email not being set properly"
    with raises(ValueError):
        user_instance.set_email(email="")
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_email(email=277627771)


def test_password():
    password: str = "asidaosiduaosiduoaisd"
    assert user_instance.password is None, "user instance password default is not set properly"
    user_instance.set_password(password=password)
    assert user_instance.password == password, "user instance password not being set properly"
    with raises(ValueError):
        user_instance.set_password(password="")
    with raises(TypeError):
        user_instance.set_password(password=0)

def test_is_active():
    pass