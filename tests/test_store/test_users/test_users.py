from datetime import datetime
from random import choice
from google.cloud.ndb.exceptions import BadValueError
from pytest import raises
from data_service.config.stocks import currency_symbols
from data_service.store.mixins import AmountMixin, AddressMixin
from data_service.utils.utils import create_id, timestamp
from tests import int_positive
from data_service.store.users import UserModel
from werkzeug.security import check_password_hash

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
    cell: str = "0761234567"
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
    password: str = "1234567890"
    assert user_instance.password is None, "user instance password default is not set properly"
    user_instance.set_password(password=password)
    assert check_password_hash(user_instance.password, password), "user instance password not being set properly"
    with raises(ValueError):
        user_instance.set_password(password="")
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_password(password=0)


def test_is_active():
    is_active: bool = False
    assert user_instance.is_active, "user instance is_active default not properly set"
    user_instance.set_is_active(is_active=is_active)
    assert user_instance.is_active == is_active, "user instance is_active default not properly set"
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_is_active(is_active="")
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_is_active(is_active=0)


def test_time_registered():
    time_registered: int = timestamp()
    assert user_instance.time_registered, "user instance time_registered default not properly set"
    user_instance.set_time_registered(time_registered=time_registered)
    assert user_instance.time_registered == time_registered, "user instance time_registered default not set properly"
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_time_registered(time_registered="")
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_time_registered(time_registered="99")


def test_is_admin():
    is_admin: bool = True
    assert not user_instance.is_admin, "user instance is_admin default not properly set"
    user_instance.set_admin(is_admin=is_admin)
    assert user_instance.is_admin == is_admin, "user instance is_admin default not set properly"
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_admin(is_admin=0)
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_admin(is_admin="0")


def test_is_support():
    is_support: bool = False
    assert not user_instance.is_support, "user instance is_support default not properly set"
    user_instance.set_support(is_support=is_support)
    assert user_instance.is_support == is_support, "user instance is_suport default not set properly"
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_support(is_support=0)
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_support(is_support="0")


def test_address():
    address: AddressMixin = AddressMixin(line_1="joe slovo street", city="Johannesburg", zip_code="1000",
                                         province="gauteng")
    assert user_instance.address is None, "user instance address default not properly set"
    user_instance.set_address(address=address)
    assert user_instance.address == address, "user instance address not properly set"
    with raises(TypeError):
        # noinspection PyTypeChecker
        user_instance.set_address(address="joe slovo street johannesburg")
