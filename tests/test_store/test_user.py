from data_service.utils.utils import create_id
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







