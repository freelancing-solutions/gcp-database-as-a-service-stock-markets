from google.cloud import ndb
from flask import current_app
from werkzeug.security import generate_password_hash

from pinoydesk.utils.utils import timestamp


class UserModel(ndb.Model):
    uid: str = ndb.StringProperty()
    names: str = ndb.StringProperty()
    surname: str = ndb.StringProperty()
    cell: str = ndb.StringProperty()
    email: str = ndb.StringProperty()
    password: str = ndb.StringProperty()
    membership_list: str = ndb.StringProperty()
    access_rights_list: str = ndb.StringProperty()
    is_active: bool = ndb.BooleanProperty(default=True)
    time_registered: int = ndb.IntegerProperty(default=timestamp())

    def set_uid(self, uid: str) -> bool:
        if uid is None:
            raise ValueError('UID cannot be Null')
        if not isinstance(uid, str):
            raise TypeError('uid can only be a string')

        self.uid = uid
        return True

    def set_names(self, names: str) -> bool:
        if names is None:
            raise ValueError('names cannot be Null')
        if not isinstance(names, str):
            raise TypeError('names can only be a string')

        self.names = names
        return True

    def set_surname(self, surname: str) -> bool:
        if surname is None:
            raise ValueError('surname cannot be Null')
        if not isinstance(surname, str):
            raise TypeError('surname can only be a string')

        self.surname = surname
        return True

    def set_cell(self, cell: str) -> bool:
        if cell is None:
            raise ValueError('cell cannot be Null')
        if not isinstance(cell, str):
            raise TypeError('cell can only be a string')

        self.cell = cell
        return True

    def set_email(self, email: str) -> bool:
        if email is None:
            raise ValueError('email cannot be Null')
        if not isinstance(email, str):
            raise TypeError('email can only be a string')

        self.email = email
        return True

    def set_password(self, password: str) -> bool:
        if password is None:
            raise ValueError('password cannot be Null')
        if not isinstance(password, str):
            raise TypeError('password can only be a string')

        self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        return True

    def set_membership(self, membership: str) -> bool:
        if membership not in current_app.config.DEFAULT_MEMBERSHIP_LIST:
            raise ValueError('invalid membership')

        self.membership_list += "," + membership
        return True

    def remove_membership(self, membership: str) -> bool:
        if membership not in current_app.config.DEFAULT_MEMBERSHIP_LIST:
            raise ValueError('invalid membership')

        if membership in self.membership_list:
            membership_list: list = self.membership_list.split(sep=",")
            membership_list.remove(membership)
            self.membership_list = ",".join(membership_list)
        return False

    def get_membership(self) -> list:
        return self.membership_list.split(",")

    def set_access_rights(self, access_right: str) -> bool:
        if access_right not in current_app.config.DEFAULT_ACCESS_RIGHTS:
            raise ValueError('invalid access right')

        self.access_rights_list += "," + access_right
        return True

    def remove_access_right(self, access_right: str) -> bool:
        if access_right not in current_app.config.DEFAULT_ACCESS_RIGHTS:
            raise ValueError('invalid access right')

        if access_right in self.access_rights_list:
            access_list: list = self.access_rights_list.split(",")
            access_list.remove(access_right)
            self.access_rights_list = ",".join(access_list)
            return True

        return False

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
