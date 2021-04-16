import typing
from google.cloud import ndb
from flask import current_app, jsonify
from werkzeug.security import check_password_hash

from data_service.config.types import dict_list_type
from data_service.store.users import UserModel
from data_service.utils.utils import create_id

users_type = typing.List[UserModel]


class UserView:
    def __init__(self):
        self.client = ndb.Client(namespace="main", project=current_app.config.PROJECT)

    def add_user(self, names: str, surname: str, cell: str, email: str, password: str, uid: str = None) -> tuple:
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
                user_list: users_type = UserModel.query(UserModel.uid == uid).fetch()
                if len(user_list) > 0:
                    return jsonify({'status': False, 'message': 'user already exists'}), 500
            user_list: users_type = UserModel.query(UserModel.email == email).fetch()
            if len(user_list) > 0:
                message: str = '''
                the email you submitted is already attached to an account please login again or reset your password
                '''
                return jsonify({'status': False, 'message': message}), 500

            user_list: users_type = UserModel.query(UserModel.cell == cell).fetch()
            if len(user_list) > 0:
                message: str = '''
                the cell you submitted is already attached to an account please login again or reset your password
                '''
                return jsonify({'status': False, 'message': message}), 500
            try:
                user_instance: UserModel = UserModel()
                if uid:
                    user_instance.set_uid(uid=uid)
                else:
                    user_instance.set_uid(uid=create_id())

                user_instance.set_names(names=names)
                user_instance.set_surname(surname=surname)
                user_instance.set_cell(cell=cell)
                user_instance.set_email(email=email)
                user_instance.set_password(password=password)
                user_instance.set_is_active(is_active=True)
                user_instance.put()
                return jsonify({'status': True,
                                "message": "Successfully created new user",
                                "payload": user_instance.to_dict()
                                }), 200
            except ValueError as e:
                return jsonify({"status": False, "message": str(e)}), 500
            except TypeError as e:
                return jsonify({"status": False, "message": str(e)}), 500

    def update_user(self, uid: str, names: str, surname: str, cell: str, email: str) -> tuple:
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
                user_list: users_type = UserModel.query(UserModel.uid == uid).fetch()
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
                    return jsonify({"status": False, "message": str(e)}), 500
                except TypeError as e:
                    return jsonify({"status": False, "message": str(e)}), 500
            else:
                return jsonify({'status': False, 'message': 'user not found cannot update user details'}), 500

    def delete_user(self, uid: str = None, email: str = None, cell: str = None) -> tuple:
        """
            given either, uid, email or cell delete user
        :param uid:
        :param email:
        :param cell:
        :return:
        """
        with self.client.context():
            if uid != "" and (uid is not None):
                user_list: users_type = UserModel.query(UserModel.uid == uid).fetch()
                if len(user_list) > 0:
                    user_instance: UserModel = user_list[0]
                    user_instance.key.delete()
                    return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
            if email != "" and (email is not None):
                user_list: users_type = UserModel.query(UserModel.email == email).fetch()
                if len(user_list) > 0:
                    user_instance: UserModel = user_list[0]
                    user_instance.key.delete()
                    return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
            if cell != "" and (cell is not None):
                user_list: users_type = UserModel.query(UserModel.cell == cell).fetch()
                if len(user_list) > 0:
                    user_instance: UserModel = user_list[0]
                    user_instance.key.delete()
                    return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
            return jsonify({'status': False, 'message': 'user not found'}), 500

    def get_active_users(self) -> tuple:
        """
            return a list of all users
        :return:
        """
        with self.client.context():
            users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.is_active == True).fetch()]
            return jsonify(
                {'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

    def get_in_active_users(self) -> tuple:
        """
            return a list of non active users
        :return:
        """
        with self.client.context():
            users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.is_active == False).fetch()]
            return jsonify(
                {'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

    def get_all_users(self) -> tuple:
        """
            get a list of all users
        :return:
        """
        with self.client.context():
            users_list: dict_list_type = [user.to_dict() for user in UserModel.query().fetch()]
            message: str = 'successfully retrieved active users'
            return jsonify({'status': True, 'payload': users_list, 'message': message}), 200

    def get_user(self, uid: str = None, cell: str = None, email: str = None) -> tuple:
        """
            return a user either by uid, cell or email
        :param uid:
        :param cell:
        :param email:
        :return:
        """
        with self.client.context():
            if uid is not None:
                users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.uid == uid).fetch()]
                if len(users_list) > 0:
                    message: str = 'successfully retrieved user by uid'
                    return jsonify({'status': True, 'payload': users_list[0], 'message': message}), 200

            if cell is not None:
                users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.cell == cell).fetch()]
                if len(users_list) > 0:
                    message: str = 'successfully retrieved user by cell'
                    return jsonify({'status': True, 'payload': users_list[0], 'message': message}), 200

            if email is not None:
                users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.email == email).fetch()]
                if len(users_list) > 0:
                    message: str = 'successfully retrieved user by email'
                    return jsonify({'status': True, 'payload': users_list[0], 'message': message}), 200

            return jsonify(
                {'status': False, 'message': 'to retrieve a user either submit an email, cell or user id'}), 500

    def check_password(self, uid: str, password: str) -> tuple:
        with self.client.context():
            if uid is None:
                return jsonify({'status': False, 'message': 'please submit user id'}), 500
            if password is None:
                return jsonify({'status': False, 'message': 'please submit password'}), 500

            users_list: users_type = UserModel.query(UserModel.uid == uid).fetch()
            if len(users_list) > 0:
                user_instance: UserModel = users_list[0]
                if check_password_hash(password=password, pwhash=user_instance.password) is True:
                    return jsonify({'status': True, 'message': 'passwords match'}), 200
                else:
                    return jsonify({'status': False, 'message': 'passwords do not match'}), 200
            else:
                return jsonify({'status': False, 'message': 'user not found'}), 200

    def deactivate_user(self, uid: str) -> tuple:
        with self.client.context():
            if uid is None:
                return jsonify({'status': False, 'message': 'please submit user id'}), 500
            users_list: users_type = UserModel.query(UserModel.uid == uid).fetch()
            if len(users_list) > 0:
                user_instance: UserModel = users_list[0]
                if user_instance.set_is_active(is_active=False) is True:
                    user_instance.put()
                    return jsonify({'status': True, 'message': 'user deactivated'}), 200
                else:
                    return jsonify({'status': False, 'message': 'could not de-activate user'}), 200
            else:
                return jsonify({'status': False, 'message': 'user not found'}), 200

    def login(self, email: str, password: str) -> tuple:
        pass