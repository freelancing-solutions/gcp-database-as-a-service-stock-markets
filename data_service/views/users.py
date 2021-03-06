import typing
from flask import jsonify, current_app
from werkzeug.security import check_password_hash
from data_service.config.types import dict_list_type
from data_service.main import cache_users
from data_service.store.users import UserModel
from data_service.utils.utils import create_id, return_ttl
from data_service.config.exception_handlers import handle_view_errors
from data_service.config.use_context import use_context

users_type = typing.List[UserModel]


# TODO create test cases for User View and Documentations
# noinspection DuplicatedCode
class UserView:
    def __init__(self):
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def add_user(self, names:  typing.Union[str, None], surname:  typing.Union[str, None],
                 cell:  typing.Union[str, None], email:  typing.Union[str, None],
                 password:  typing.Union[str, None], uid:  typing.Union[str, None] = None) -> tuple:
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
        if (uid is not None) and (uid != ""):
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
        user_instance: UserModel = UserModel()
        if (uid is not None) and (uid != ""):
            user_instance.set_uid(uid=uid)
        else:
            user_instance.set_uid(uid=create_id())

        user_instance.set_names(names=names)
        user_instance.set_surname(surname=surname)
        user_instance.set_cell(cell=cell)
        user_instance.set_email(email=email)
        user_instance.set_password(password=password)
        user_instance.set_is_active(is_active=True)
        user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        return jsonify({'status': True,
                        "message": "Successfully created new user",
                        "payload": user_instance.to_dict()
                        }), 200

    @use_context
    @handle_view_errors
    async def add_user_async(self, names:  typing.Union[str, None], surname:  typing.Union[str, None],
                             cell:  typing.Union[str, None], email:  typing.Union[str, None],
                             password:  typing.Union[str, None], uid:  typing.Union[str, None] = None) -> tuple:
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
        if (uid is not None) and (uid != ""):
            user_list: users_type = UserModel.query(UserModel.uid == uid).fetch_async().get_result()
            if len(user_list) > 0:
                return jsonify({'status': False, 'message': 'user already exists'}), 500
        user_list: users_type = UserModel.query(UserModel.email == email).fetch_async().get_result()
        if len(user_list) > 0:
            message: str = '''
            the email you submitted is already attached to an account please login again or reset your password
            '''
            return jsonify({'status': False, 'message': message}), 500

        user_list: users_type = UserModel.query(UserModel.cell == cell).fetch_async().get_result()
        if len(user_list) > 0:
            message: str = '''
            the cell you submitted is already attached to an account please login again or reset your password
            '''
            return jsonify({'status': False, 'message': message}), 500
        user_instance: UserModel = UserModel()
        if (uid is not None) and (uid != ""):
            user_instance.set_uid(uid=uid)
        else:
            user_instance.set_uid(uid=create_id())

        user_instance.set_names(names=names)
        user_instance.set_surname(surname=surname)
        user_instance.set_cell(cell=cell)
        user_instance.set_email(email=email)
        user_instance.set_password(password=password)
        user_instance.set_is_active(is_active=True)
        key = user_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
        return jsonify({'status': True,
                        "message": "Successfully created new user",
                        "payload": user_instance.to_dict()
                        }), 200

    @use_context
    @handle_view_errors
    def update_user(self, uid:  typing.Union[str, None], names:  typing.Union[str, None],
                    surname:  typing.Union[str, None], cell:  typing.Union[str, None],
                    email:  typing.Union[str, None], is_admin: bool, is_support: bool) -> tuple:
        """
            update user details
        """
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'User ID is required'}), 500

        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            user_instance.set_names(names=names)
            user_instance.set_surname(surname=surname)
            user_instance.set_cell(cell=cell)
            user_instance.set_email(email=email)
            user_instance.set_admin(is_admin=is_admin)
            user_instance.set_support(is_support=is_support)
            user_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            return jsonify({'status': True, 'message': 'successfully updated user details',
                            'payload': user_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found cannot update user details'}), 500

    @use_context
    @handle_view_errors
    async def update_user_async(self, uid:  typing.Union[str, None], names:  typing.Union[str, None],
                                surname:  typing.Union[str, None], cell:  typing.Union[str, None],
                                email:  typing.Union[str, None], is_admin: bool, is_support: bool) -> tuple:
        """
            update user details
        """
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'User ID is required'}), 500

        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
        if isinstance(user_instance, UserModel):
            user_instance.set_names(names=names)
            user_instance.set_surname(surname=surname)
            user_instance.set_cell(cell=cell)
            user_instance.set_email(email=email)
            user_instance.set_admin(is_admin=is_admin)
            user_instance.set_support(is_support=is_support)
            key = user_instance.put_async(retries=self._max_retries, timeout=self._max_timeout).get_result()
            return jsonify({'status': True, 'message': 'successfully updated user details',
                            'payload': user_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found cannot update user details'}), 500

    @use_context
    @handle_view_errors
    def delete_user(self, uid: typing.Union[str, None] = None, email: typing.Union[str, None] = None,
                    cell:  typing.Union[str, None] = None) -> tuple:
        """
            given either, uid, email or cell delete user
        :param uid:
        :param email:
        :param cell:
        :return:
        """
        if (uid != "") and (uid is not None):
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        elif (email != "") and (email is not None):
            user_instance: UserModel = UserModel.query(UserModel.email == email).get()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        elif (cell != "") and (cell is not None):
            user_instance: UserModel = UserModel.query(UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel):
                # TODO- rather mark user as deleted
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        return jsonify({'status': False, 'message': 'user not found'}), 500

    @use_context
    @handle_view_errors
    async def delete_user_async(self, uid: typing.Union[str, None] = None, email: typing.Union[str, None] = None,
                    cell:  typing.Union[str, None] = None) -> tuple:
        """
            given either, uid, email or cell delete user
        :param uid:
        :param email:
        :param cell:
        :return:
        """
        if (uid != "") and (uid is not None):
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        elif (email != "") and (email is not None):
            user_instance: UserModel = UserModel.query(UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel):
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        elif (cell != "") and (cell is not None):
            user_instance: UserModel = UserModel.query(UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel):
                # TODO- rather mark user as deleted
                user_instance.key.delete()
                return jsonify({'status': True, 'message': 'successfully deleted user'}), 200
        return jsonify({'status': False, 'message': 'user not found'}), 500

    @cache_users.cached(timeout=return_ttl(name='short'))
    @use_context
    @handle_view_errors
    def get_active_users(self) -> tuple:
        """
            return a list of all users
        :return:
        """
        users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.is_active == True).fetch()]
        return jsonify({'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

    @cache_users.cached(timeout=return_ttl(name='short'))
    @use_context
    @handle_view_errors
    async def get_active_users_async(self) -> tuple:
        """
            return a list of all users
        :return:
        """
        users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.is_active == True).fetch_async().get_result()]
        return jsonify({'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

    @cache_users.cached(timeout=return_ttl(name='short'))
    @use_context
    @handle_view_errors
    def get_in_active_users(self) -> tuple:
        """
            return a list of non active users
        :return:
        """
        users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.is_active == False).fetch()]
        return jsonify({'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200

    @cache_users.cached(timeout=return_ttl(name='short'))
    @use_context
    @handle_view_errors
    async def get_in_active_users_async(self) -> tuple:
        """
            return a list of non active users
        :return:
        """
        users_list: dict_list_type = [user.to_dict() for user in UserModel.query(UserModel.is_active == False).fetch_async().get_result()]
        return jsonify({'status': True, 'payload': users_list, 'message': 'successfully retrieved active users'}), 200


    @cache_users.cached(timeout=return_ttl(name='short'))
    @use_context
    @handle_view_errors
    def get_all_users(self) -> tuple:
        """
            get a list of all users
        :return:
        """
        users_list: dict_list_type = [user.to_dict() for user in UserModel.query().fetch()]
        message: str = 'successfully retrieved active users'
        return jsonify({'status': True, 'payload': users_list, 'message': message}), 200

    @cache_users.cached(timeout=return_ttl(name='short'))
    @use_context
    @handle_view_errors
    async def get_all_users_async(self) -> tuple:
        """
            get a list of all users
        :return:
        """
        users_list: dict_list_type = [user.to_dict() for user in UserModel.query().fetch_async().get_result()]
        message: str = 'successfully retrieved active users'
        return jsonify({'status': True, 'payload': users_list, 'message': message}), 200

    @cache_users.cached(timeout=return_ttl(name='medium'))
    @use_context
    @handle_view_errors
    def get_user(self, uid:  typing.Union[str, None] = None, cell:  typing.Union[str, None] = None,
                 email:  typing.Union[str, None] = None) -> tuple:
        """
            return a user either by uid, cell or email
        :param uid:
        :param cell:
        :param email:
        :return:
        """
        if (uid is not None) and (uid != ""):
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by uid'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        if (cell is not None) and (cell != ""):
            user_instance: UserModel = UserModel.query(UserModel.cell == cell).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by cell'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        if (email is not None) and (email != ""):
            user_instance: UserModel = UserModel.query(UserModel.email == email).get()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by email'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        return jsonify({'status': False, 'message': 'to retrieve a user either submit an email, cell or user id'}), 500

    @cache_users.cached(timeout=return_ttl(name='medium'))
    @use_context
    @handle_view_errors
    async def get_user_async(self, uid:  typing.Union[str, None] = None, cell:  typing.Union[str, None] = None,
                             email:  typing.Union[str, None] = None) -> tuple:
        """
            return a user either by uid, cell or email
            :param uid:
            :param cell:
            :param email:
            :return:
        """
        if (uid is not None) and (uid != ""):
            user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by uid'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        if (cell is not None) and (cell != ""):
            user_instance: UserModel = UserModel.query(UserModel.cell == cell).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by cell'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        if (email is not None) and (email != ""):
            user_instance: UserModel = UserModel.query(UserModel.email == email).get_async().get_result()
            if isinstance(user_instance, UserModel):
                message: str = 'successfully retrieved user by email'
                return jsonify({'status': True, 'payload': user_instance.to_dict(), 'message': message}), 200

        return jsonify({'status': False, 'message': 'to retrieve a user either submit an email, cell or user id'}), 500

    @use_context
    @handle_view_errors
    def check_password(self, uid: typing.Union[str, None], password:  typing.Union[str, None]) -> tuple:
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'please submit user id'}), 500
        if (password is None) or (password == ""):
            return jsonify({'status': False, 'message': 'please submit password'}), 500

        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            if check_password_hash(password=password, pwhash=user_instance.password) is True:
                return jsonify({'status': True, 'message': 'passwords match'}), 200
            else:
                return jsonify({'status': False, 'message': 'passwords do not match'}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found'}), 200

    @use_context
    @handle_view_errors
    async def check_password_async(self, uid: typing.Union[str, None], password:  typing.Union[str, None]) -> tuple:
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'please submit user id'}), 500
        if (password is None) or (password == ""):
            return jsonify({'status': False, 'message': 'please submit password'}), 500

        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
        if isinstance(user_instance, UserModel):
            if check_password_hash(password=password, pwhash=user_instance.password) is True:
                return jsonify({'status': True, 'message': 'passwords match'}), 200
            else:
                return jsonify({'status': False, 'message': 'passwords do not match'}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found'}), 200

    @use_context
    @handle_view_errors
    def deactivate_user(self, uid: typing.Union[str, None]) -> tuple:
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'please submit user id'}), 500
        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get()
        if isinstance(user_instance, UserModel):
            if user_instance.set_is_active(is_active=False) is True:
                user_instance.put()
                return jsonify({'status': True, 'message': 'user deactivated'}), 200
            else:
                return jsonify({'status': False, 'message': 'could not de-activate user'}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found'}), 200

    @use_context
    @handle_view_errors
    async def deactivate_user_async(self, uid: typing.Union[str, None]) -> tuple:
        if (uid is None) or (uid == ""):
            return jsonify({'status': False, 'message': 'please submit user id'}), 500
        user_instance: UserModel = UserModel.query(UserModel.uid == uid).get_async().get_result()
        if isinstance(user_instance, UserModel):
            if user_instance.set_is_active(is_active=False) is True:
                key = user_instance.put_async().get_result()
                return jsonify({'status': True, 'message': 'user deactivated'}), 200
            else:
                return jsonify({'status': False, 'message': 'could not de-activate user'}), 200
        else:
            return jsonify({'status': False, 'message': 'user not found'}), 200

    @use_context
    @handle_view_errors
    def login(self, email:   typing.Union[str, None], password: typing.Union[str, None]) -> tuple:
        """
            this login utility may support client app , not necessary for admin and service to service calls
            Options:
            firebase login, JWT Token
        """
        pass

