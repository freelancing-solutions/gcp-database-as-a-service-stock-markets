from flask import Blueprint, request, jsonify
from pinydesk.store.users import UserView

users_bp = Blueprint('users', __name__)


@users_bp.route('/api/v1/create-user', methods=['POST'])
def create_user() -> tuple:
    """
        given user details create new user
    :return: json response as tuple
    """
    # created new user
    user_data: dict = request.get_json()
    users_view_instance: UserView = UserView()
    names: str = user_data.get('names')
    surname: str = user_data.get('surname')
    cell: str = user_data.get('cell')
    email: str = user_data.get('email')
    password: str = user_data.get('password')
    uid: str = user_data.get('uid')
    return users_view_instance.add_user(names=names, surname=surname, cell=cell, email=email, password=password, uid=uid)


@users_bp.route('/api/v1/user/<path:path>', methods=['GET', 'POST'])
def user(path: str) -> tuple:
    """
        update or get a specific user by uid
    :param path:
    :return: json response as tuple
    """
    if request.method == "GET":
        # get a specific user
        users_view_instance: UserView = UserView()
        return users_view_instance.get_user(uid=path)
    else:
        # Updating user details
        users_view_instance: UserView = UserView()
        user_data: dict = request.get_json()
        uid: str = path
        names: str = user_data.get('names')
        surname: str = user_data.get('surname')
        cell: str = user_data.get('cell')
        email: str = user_data.get('email')
        return users_view_instance.update_user(uid=uid, names=names, surname=surname, cell=cell, email=email)


@users_bp.route('/api/v1/users/<path:path>', methods=['GET'])
def users(path: str) -> tuple:
    """
        get all , active or in-active users
    :param path:
    :return: json response as tuple
    """
    if path == "all":
        users_view_instance: UserView = UserView()
        return users_view_instance.get_all_users()
    if path == "active":
        users_view_instance: UserView = UserView()
        return users_view_instance.get_active_users()
    if path == "in-active":
        users_view_instance: UserView = UserView()
        return users_view_instance.get_in_active_users()

    return jsonify({'status': False, 'message': 'general error fetching users'}), 500


@users_bp.route('/api/v1/get-user-email/<path:path>', methods=['GET'])
def get_user_email(path: str) -> tuple:
    """

    :param path:
    :return: json response as tuple
    """
    users_view_instance: UserView = UserView()
    return users_view_instance.get_user(email=path)


@users_bp.route('/api/v1/get-user-cell/<path:path>', methods=['GET'])
def get_user_cell(path: str) -> tuple:
    """
        given cell number return user details
    :param path:
    :return: json response as tuple
    """
    users_view_instance: UserView = UserView()
    return users_view_instance.get_user(cell=path)


@users_bp.route('/api/v1/get-user-uid/<path:path>', methods=['GET'])
def get_user_uid(path: str) -> tuple:
    """
        given a user uid return user details
    :param path:
    :return: json response as tuple
    """
    users_view_instance: UserView = UserView()
    return users_view_instance.get_user(uid=path)


@users_bp.route('/api/v1/delete-user-cell/<path:path>', methods=['DELETE'])
def delete_user_cell(path: str) -> tuple:
    """
        given a user cell number delete user
    :param path:
    :return: json response as tuple
    """
    users_view_instance: UserView = UserView()
    return users_view_instance.delete_user(cell=path)


@users_bp.route('/api/v1/delete-user-email/<path:path>', methods=['DELETE'])
def delete_user_email(path: str) -> tuple:
    """
        given a user email address delete user
    :param path:
    :return: json response as tuple
    """
    users_view_instance: UserView = UserView()
    return users_view_instance.delete_user(email=path)


@users_bp.route('/api/v1/delete-user-uid/<path:path>', methods=['DELETE'])
def delete_user_uid(path: str) -> tuple:
    """
        given a user uid delete user details
    :param path:
    :return: json response as tuple
    """
    users_view_instance: UserView = UserView()
    return users_view_instance.delete_user(uid=path)


@users_bp.route('/api/v1/check-password', methods=["POST"])
def check_password() -> tuple:
    """
        given a password in json check if it matches the hash in file
    :return:
    """
    user_data = request.get_json()
    uid = user_data.get('uid')
    password = user_data('password')
    user_view_instance: UserView = UserView()
    return user_view_instance.check_password(uid=uid, password=password)
