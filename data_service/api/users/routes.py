from flask import Blueprint, request, jsonify
from data_service.api.api_authenticator import handle_auth
from data_service.views.users import UserView
users_bp = Blueprint("users", __name__)


@users_bp.route("/api/v1/create-user", methods=["POST"])
@handle_auth
def create_user() -> tuple:
    """
        given user details create new user
    :return: json response as tuple
    """
    # created new user
    user_data: dict = request.get_json()
    users_view_instance: UserView = UserView()
    names: str = user_data.get("names")
    surname: str = user_data.get("surname")
    cell: str = user_data.get("cell")
    email: str = user_data.get("email")
    password: str = user_data.get("password")
    uid: str = user_data.get("uid")
    return users_view_instance.add_user(names=names, surname=surname, cell=cell,
                                        email=email, password=password, uid=uid)


@users_bp.route("/api/v1/user/<path:path>", methods=["GET", "POST"])
@handle_auth
def user(path: str) -> tuple:
    """
        update or get a specific user by uid
    :param path:
    :return: json response as tuple
    """
    users_view_instance: UserView = UserView()
    if request.method == "GET":
        # get a specific user
        return users_view_instance.get_user(uid=path)
    else:
        # Updating user details
        if path == "update":
            user_data: dict = request.get_json()
            uid: str = path
            names: str = user_data.get("names")
            surname: str = user_data.get("surname")
            cell: str = user_data.get("cell")
            email: str = user_data.get("email")
            return users_view_instance.update_user(uid=uid, names=names, surname=surname,
                                                   cell=cell, email=email)
        elif path == "delete":
            user_data: dict = request.get_json()
            if "uid" in user_data and user_data["uid"] != "":
                uid: str = user_data.get("uid")
            else:
                uid: str = ""

            if "email" in user_data and user_data["email"] != "":
                email: str = user_data.get("email")
            else:
                email: str = ""

            if "cell" in user_data and user_data["cell"] != "":
                cell: str = user_data.get("cell")
            else:
                cell: str = ""

            return users_view_instance.delete_user(uid=uid, email=email, cell=cell)
        elif path == "get":
            user_data: dict = request.get_json()
            if "uid" in user_data and user_data["uid"] != "":
                uid: str = user_data.get("uid")
            else:
                uid: str = ""

            if "email" in user_data and user_data["email"] != "":
                email: str = user_data.get("email")
            else:
                email: str = ""

            if "cell" in user_data and user_data["cell"] != "":
                cell: str = user_data.get("cell")
            else:
                cell: str = ""

            return users_view_instance.get_user(uid=uid, email=email, cell=cell)


@users_bp.route("/api/v1/users/<path:path>", methods=["GET"])
@handle_auth
def get_all(path: str) -> tuple:
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

    return jsonify({"status": False, "message": "general error fetching users"}), 500


@users_bp.route("/api/v1/check-password", methods=["POST"])
@handle_auth
def check_password() -> tuple:
    """
        given a password in json check if it matches the hash in file
    :return:
    """
    user_data: dict = request.get_json()
    uid: str = user_data.get("uid")
    password: str = user_data.get("password")
    user_view_instance: UserView = UserView()
    return user_view_instance.check_password(uid=uid, password=password)


@users_bp.route("/api/v1/deactivate-user", methods=["POST"])
@handle_auth
def de_activate_user() -> tuple:
    """
        given uid in json de-activate user
    :return: json as tuple
    """
    user_data: dict = request.get_json()
    uid: str = user_data.get("uid")
    user_view_instance: UserView = UserView()
    return user_view_instance.deactivate_user(uid=uid)


@users_bp.route("/api/v1/auth/login", methods=["POST"])
@handle_auth
def login() -> tuple:
    user_view_instance: UserView = UserView()
    user_data: dict = request.get_json()
    if "email" in user_data and user_data["email"] != "":
        email = user_data.get("email")
    else:
        return jsonify({"status": False,  "message": "email is required"}), 500
    if "password" in user_data and user_data["password"] != "":
        password = user_data.get("password")
    else:
        return jsonify({"status": False, "message": "password is required"}), 500

    return user_view_instance.login(email=email, password=password)


@users_bp.route("/api/v1/auth/logout", methods=["POST"])
@handle_auth
def logout() -> tuple:
    user_view_instance: UserView = UserView()
    user_data: dict = request.get_json()
    pass


@users_bp.route("/api/v1/auth/register", methods=["POST"])
@handle_auth
def register() -> tuple:
    user_view_instance: UserView = UserView()
    user_data: dict = request.get_json()
    if "email" in user_data and user_data["email"] != "":
        email: str = user_data.get("email")
    else:
        return jsonify({"status": False, "message": "Email is required"}), 500

    if "cell" in user_data and user_data["cell"] != "":
        cell: str = user_data.get("cell")
    else:
        return jsonify({"status": False, "message": "Cell is Required"})

    if "password" in user_data and user_data["password"] != "":
        password: str = user_data.get("password")
    else:
        return jsonify({"status": False, "message": "Password is required"}), 500

    if "names" in user_data and user_data["names"] != "":
        names: str = user_data.get("names")
    else:
        return jsonify({"status": False, "message": "Names is required"}), 500

    if "surname" in user_data and user_data["surname"] != "":
        surname: str = user_data.get("surname")
    else:
        return jsonify({"status": False, "message": "Surname is required"}), 500

    return user_view_instance.add_user(names=names, surname=surname, cell=cell,
                                       email=email, password=password)

        
    




