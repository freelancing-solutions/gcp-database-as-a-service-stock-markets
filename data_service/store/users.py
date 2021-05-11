import typing

from google.api_core.exceptions import RetryError
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError
from werkzeug.security import generate_password_hash

from data_service.store.mixins import AddressMixin
from data_service.utils.utils import timestamp


class UserValidators:
    # Which ever module calls this validators it will provide its own context

    @staticmethod
    def is_user_valid(uid: str) -> typing.Union[None, bool]:
        if not isinstance(uid, str):
            return False
        try:
            user_instance: typing.List[UserModel] = UserModel.query(
                UserModel.uid == uid).get()
        except ConnectionRefusedError:
            return None
        except RetryError:
            return None
        if isinstance(user_instance, UserModel):
            return True
        return False


class UserModel(ndb.Model):
    uid: str = ndb.StringProperty(required=True, indexed=True)
    names: str = ndb.StringProperty()
    surname: str = ndb.StringProperty()
    cell: str = ndb.StringProperty(indexed=True)
    email: str = ndb.StringProperty(indexed=True)
    password: str = ndb.StringProperty()
    is_active: bool = ndb.BooleanProperty(default=True)
    time_registered: int = ndb.IntegerProperty(default=timestamp())
    is_admin: bool = ndb.BooleanProperty(default=False)
    is_support: bool = ndb.BooleanProperty(default=False)
    address: AddressMixin = ndb.StructuredProperty(AddressMixin)

    def set_uid(self, uid: str) -> bool:
        if uid is None or uid == "":
            raise ValueError('UID cannot be Null')
        if not isinstance(uid, str):
            raise TypeError('uid can only be a string')

        self.uid = uid
        return True

    def set_names(self, names: str) -> bool:
        if names is None or names == "":
            raise ValueError('names cannot be Null')
        if not isinstance(names, str):
            raise TypeError('names can only be a string')

        self.names = names
        return True

    def set_surname(self, surname: str) -> bool:
        if surname is None or surname == "":
            raise ValueError('surname cannot be Null')
        if not isinstance(surname, str):
            raise TypeError('surname can only be a string')

        self.surname = surname
        return True

    def set_cell(self, cell: str) -> bool:
        # TODO find a way to better check for Cell Number
        #  a regex can work best here
        if cell is None or cell == "":
            raise ValueError('cell cannot be Null')
        if not isinstance(cell, str):
            raise TypeError('cell can only be a string')

        self.cell = cell
        return True

    def set_email(self, email: str) -> bool:
        if email is None or email == "":
            raise ValueError('email cannot be Null')
        if not isinstance(email, str):
            raise TypeError('email can only be a string')

        self.email = email
        return True

    def set_password(self, password: str) -> bool:
        if password is None or password == "":
            raise ValueError('password cannot be Null')
        if not isinstance(password, str):
            raise TypeError('password can only be a string')

        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        return True

    def set_is_active(self, is_active: bool) -> bool:
        if not isinstance(is_active, bool):
            raise TypeError('invalid Type is_active is bool')
        self.is_active = is_active
        return True

    def set_time_registered(self, time_registered: int) -> bool:
        if not isinstance(time_registered, int):
            raise TypeError('time registered can only be an integer')
        self.time_registered = time_registered
        return True

    def set_admin(self, is_admin: bool) -> bool:
        if not isinstance(is_admin, bool):
            raise TypeError("invalid argument")
        self.is_admin = is_admin
        return True

    def set_support(self, is_support: bool) -> bool:
        if not isinstance(is_support, bool):
            raise TypeError("invalid argument")
        self.is_support = is_support
        return True

    def set_address(self, address: AddressMixin) -> bool:
        if not isinstance(address, AddressMixin):
            raise TypeError('Invalid Argument')
        self.address = address
        return True
