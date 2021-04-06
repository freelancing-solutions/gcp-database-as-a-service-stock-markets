from google.cloud import ndb
from werkzeug.security import generate_password_hash
from flask import current_app, jsonify


class UserView:
    def __init__(self):
        self.client = ndb.Client(namespace="main", project=current_app.config.PROJECT)

    def add_user(self, names, surname, cell, email, password, uid=None) -> tuple:
        """
            create new user
        :param names:
        :param surname:
        :param cell:
        :param email:
        :param password:
        :param uid:
        :return:
        """
        with self.client.context():
            if uid is not None:
                user_list: list = UserModel.query(UserModel.uid == uid).fetch()
                if len(user_list) > 0:
                    return jsonify({'status': False, 'message': 'user already exists'}), 500
            user_list: list = UserModel.query(UserModel.email == email).fetch()
            if len(user_list) > 0:
                message: str = '''
                the email you submitted is already attached to an account please login again or reset your password
                '''
                return jsonify({'status': False, 'message': message}), 500

            user_list: list = UserModel.query(UserModel.cell == cell).fetch()
            if len(user_list) > 0:
                message: str = '''
                the cell you submitted is already attached to an account please login again or reset your password
                '''
                return jsonify({'status': False, 'message': message}), 500
            try:
                user_instance = UserModel()
                if uid:
                    user_instance.set_uid(uid=uid)
                user_instance.set_names(names=names)
                user_instance.set_surname(surname=surname)
                user_instance.set_cell(cell=cell)
                user_instance.set_email(email=email)
                user_instance.set_password(password=password)
                user_instance.put()
                return jsonify({'status': True, "message": "Successfully created new user"}), 200
            except ValueError as e:
                return jsonify({"status": False, "message": e}), 500
            except TypeError as e:
                return jsonify({"status": False, "message": e}), 500

    def update_user(self, uid, names, surname, cell, email) -> tuple:
        """
            update user details
        :param uid:
        :param names:
        :param surname:
        :param cell:
        :param email:
        :param password:
        :return:
        """
        with self.client.context():
            if uid is not None:
                user_list: list = UserModel.query(UserModel.uid == uid).fetch()
            if len(user_list) > 0:
                user_instance: UserModel = user_list[0]
                try:
                    user_instance.set_names(names=names)
                    user_instance.set_surname(surname=surname)
                    user_instance.set_cell(cell=cell)
                    user_instance.set_email(email=email)
                    user_instance.put()
                    return jsonify({'status': True, 'message': 'successfully updated user details'}), 200
                except ValueError as e:
                    return jsonify({"status": False, "message": e}), 500
                except TypeError as e:
                    return jsonify({"status": False, "message": e}), 500
            else:
                return jsonify({'status': False, 'message': 'user not found cannot update user details'}), 500

    def delete_user(self, uid=None, email=None, cell=None):
        """
            given either, uid, email or cell delete user
        :param uid:
        :param email:
        :param cell:
        :return:
        """
        with self.client.context():
            if uid is not None:
                user_list: list = UserModel.query(UserModel.uid == uid).fetch()
                if len(user_list) > 0:
                    user_instance: UserModel = user_list[0]
                    user_instance.key.delete()
                    return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
            if email is not None:
                user_list: list = UserModel.query(UserModel.email == email).fetch()
                if len(user_list) > 0:
                    user_instance: UserModel = user_list[0]
                    user_instance.key.delete()
                    return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
            if cell is not None:
                user_list: list = UserModel.query(UserModel.cell == cell).fetch()
                if len(user_list) > 0:
                    user_instance: UserModel = user_list[0]
                    user_instance.key.delete()
                    return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
            return jsonify({'status': False, 'message': 'user not found'}), 500

    def get_active_users(self):
        """
            return a list of all users
        :return:
        """
        with self.client.context():
            users_list: list = [user.to_dict() for user in UserModel.query(UserModel.is_active == True).fetch()]
            return jsonify(
                {'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

    def get_in_active_users(self):
        """
            return a list of non active users
        :return:
        """
        with self.client.context():
            users_list: list = [user.to_dict() for user in UserModel.query(UserModel.is_active == False).fetch()]
            return jsonify(
                {'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

    def get_all_users(self):
        """
            get a list of all users
        :return:
        """
        with self.client.context():
            users_list: list = [user.to_dict() for user in UserModel.query().fetch()]
            message: str = 'successfully retrieved active users'
            return jsonify({'status': True, 'payload': users_list, 'message': message}), 200

    def get_user(self, uid=None, cell=None, email=None):
        """
            return a user either by uid, cell or email
        :param uid:
        :param cell:
        :param email:
        :return:
        """
        with self.client.context():
            if uid is not None:
                users_list: list = [user.to_dict() for user in UserModel.query(UserModel.uid == uid).fetch()]
                if len(users_list) > 0:
                    message: str = 'successfully retrieved user by uid'
                    return jsonify({'status': True, 'payload': users_list[0], 'message': message}), 200

            if cell is not None:
                users_list: list = [user.to_dict() for user in UserModel.query(UserModel.cell == cell).fetch()]
                if len(users_list) > 0:
                    message: str = 'successfully retrieved user by cell'
                    return jsonify({'status': True, 'payload': users_list[0], 'message': message}), 200

            if email is not None:
                users_list: list = [user.to_dict() for user in UserModel.query(UserModel.email == email).fetch()]
                if len(users_list) > 0:
                    message: str = 'successfully retrieved user by email'
                    return jsonify({'status': True, 'payload': users_list[0], 'message': message}), 200

            return jsonify({'status': False, 'message': 'to retrieve a user either submit an email, cell or user id'}), 500


class UserModel(ndb.Model):
    uid = ndb.StringProperty()
    names = ndb.StringProperty()
    surname = ndb.StringProperty()
    cell = ndb.StringProperty()
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    membership_list = ndb.StringProperty()
    access_rights = ndb.StringProperty()
    is_active = ndb.StringProperty()
    time_registered = ndb.IntegerProperty()

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
        if not membership in current_app.config.DEFAULT_MEMBERSHIP_LIST:
            raise ValueError('invalid membership')

        self.membership_list += "," + membership
        return True

    def remove_membership(self, membership) -> bool:
        if not membership in current_app.config.DEFAULT_MEMBERSHIP_LIST:
            raise ValueError('invalid membership')

        if membership in self.membership_list:
            membership_list: list = self.membership_list.split(sep=",")
            membership_list.remove(membership)
            self.membership_list = ",".join(membership_list)
        return False

    def get_membership(self) -> list:
        return self.membership_list.split(",")

    def set_access_rights(self, access_right) -> bool:
        if not access_right in current_app.config.DEFAULT_ACCESS_RIGHTS:
            raise ValueError('invalid access right')

        self.access_rights += "," + access_right
        return True

    def remove_access_right(self, access_right) -> bool:
        if not access_right in current_app.config.DEFAULT_ACCESS_RIGHTS:
            raise ValueError('invalid access right')

        if access_right in self.access_rights:
            access_list: list = self.access_rights.split(",")
            access_list.remove(access_right)
            self.access_rights = ",".join(access_list)
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
