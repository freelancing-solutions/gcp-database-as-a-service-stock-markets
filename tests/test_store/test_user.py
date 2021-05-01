from werkzeug.security import check_password_hash
from data_service.store.mixins import AddressMixin
from data_service.utils.utils import create_id, timestamp
from data_service.store.users import UserModel
user_model_instance: UserModel = UserModel()

uid: str = create_id()
assert isinstance(uid, str), "create_id not returning an ID"

def test_user_model():
    """
        test if user model can instantiate correctly
    """
    assert isinstance(user_model_instance, UserModel), "user model not correctly instatiating"

def test_user_uid():
    """
        test if user ID can be set correctly
    """

    result = user_model_instance.set_uid(uid=uid)
    assert isinstance(user_model_instance.uid, str), "Invalid uid Type"
    assert user_model_instance.uid == uid, "Invalid data set for UID"
    assert isinstance(result, bool), "result of uid should be bool"

def test_user_names():
    result = user_model_instance.set_names(names="steve")
    assert isinstance(user_model_instance.names, str), "invalid names type"
    assert user_model_instance.names == "steve", "Invalid name is being set on names field"
    assert isinstance(result, bool), "result of set_names should be bool"

def test_surname():
    result = user_model_instance.set_surname(surname="mantarakis")
    assert isinstance(user_model_instance.surname, str), "invalid surname type"
    assert user_model_instance.surname == "mantarakis", "invalid value for surname is being set"
    assert isinstance(result, bool), "invalid result for set_surname"

def test_cell():
    result = user_model_instance.set_cell(cell="0762777153")
    assert isinstance(user_model_instance.cell, str), "invalid cell type"
    assert user_model_instance.cell == "0762777153", "cell number is not being set correctly"
    assert isinstance(result, bool), "invalid result for set_cell"

def test_email():
    result = user_model_instance.set_email(email="mobiusndou@gmail.com")
    assert isinstance(user_model_instance.email, str), "invalid email type"
    assert user_model_instance.email == "mobiusndou@gmail.com", "email is not being set correctly"
    assert isinstance(result, bool), "set_email result should be bool"

def test_password():
    password: str = "1234567890"
    result = user_model_instance.set_password(password=password)
    assert isinstance(user_model_instance.password, str), "invalid password type"
    assert check_password_hash(user_model_instance.password, password), "password is not being set correctly"
    assert isinstance(result, bool), "set_email result should be bool"


def test_is_active():
    result = user_model_instance.set_is_active(is_active=True)
    assert isinstance(user_model_instance.is_active, bool), "invalid is_active type"
    assert user_model_instance.is_active == True, "is_active is not being set correctly"
    assert isinstance(result, bool), "set_is_active result should be bool"

def test_time_registered():
    time_stamp: int = timestamp()
    result = user_model_instance.set_time_registered(time_registered=time_stamp)
    assert isinstance(user_model_instance.time_registered, int), "invalid time_registered type"
    assert user_model_instance.time_registered == time_stamp, "time_registered is not being set correctly"
    assert isinstance(result, bool), "set_time_registered result should be bool"

def test_is_admin():
    result = user_model_instance.set_admin(is_admin=False)
    assert isinstance(user_model_instance.is_admin, bool), "invalid is_admin type"
    assert user_model_instance.is_admin == False, "is_admin is not being set correctly"
    assert isinstance(result, bool), "set_is_admin result should be bool"

def test_is_support():
    result = user_model_instance.set_support(is_support=False)
    assert isinstance(user_model_instance.is_support, bool), "invalid is_support type"
    assert user_model_instance.is_support == False, "is_support is not being set correctly"
    assert isinstance(result, bool), "set_is_support result should be bool"

def test_address():
    address: AddressMixin = AddressMixin()
    address.city = "new lands"
    address.line_1 = "street side"
    address.zip_code = "213"
    address.province = "Louis"

    result = user_model_instance.set_address(address=address)
    assert isinstance(user_model_instance.address, AddressMixin), "invalid address type"
    assert user_model_instance.address == address, "address is not being set correctly"
    assert isinstance(result, bool), "set_address result should be bool"







