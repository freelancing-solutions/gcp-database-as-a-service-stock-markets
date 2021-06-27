from flask import Blueprint, request, jsonify
from datetime import datetime, date
from data_service.api.api_authenticator import handle_auth
from data_service.config.exceptions import InputError
from data_service.utils.utils import date_string_to_date
from data_service.views.memberships import MembershipsView, MembershipPlansView

memberships_bp = Blueprint('memberships', __name__)


@memberships_bp.route("/api/v1/members/<path:plan_id>", methods=['POST'])
@handle_auth
def get_members(plan_id: str) -> tuple:
    members_instance: MembershipsView = MembershipsView()
    return members_instance.return_plan_members(plan_id=plan_id)


@memberships_bp.route("/api/v1/member", methods=['POST', 'PUT'])
@handle_auth
def create_member() -> tuple:
    """
        create or update member
    """
    try:
        member_details: dict = request.get_json()
        if ("uid" in member_details) and (member_details["uid"] != ""):
            uid: str = member_details.get("uid")
        else:
            message: str = "uid is required"
            return jsonify({"status": False, "message": message}), 500
        if ("plan_id" in member_details) and (member_details["plan_id"] != ""):
            plan_id: str = member_details.get("plan_id")
        else:
            message: str = "plan_id is required"
            return jsonify({"status": False, "message": message}), 500

        if ("plan_start_date" in member_details) and (member_details["plan_start_date"] != ""):
            plan_start_date: date = date_string_to_date(member_details.get("plan_start_date"))
        else:
            plan_start_date: date = datetime.now().date()
    except ValueError as e:
        raise InputError(str(e))

    members_view_instance: MembershipsView = MembershipsView()
    return members_view_instance.add_membership(uid=uid, plan_id=plan_id, plan_start_date=plan_start_date)


@memberships_bp.route("/api/v1/member/status/<path:uid>", methods=['GET', 'PUT'])
@handle_auth
def get_update_status(uid: str) -> tuple:
    """
        plan_id for the status to get or update
    """
    if request.method == "PUT":
        json_data: dict = request.get_json()
        if ("status" in json_data) and (json_data["status"] != ""):
            status: str = json_data.get("status")
        else:
            message: str = "status is required and should be paid or unpaid"
            return jsonify({'status': True, 'message': message}), 500
        membership_view_instance: MembershipsView = MembershipsView()
        return membership_view_instance.set_membership_status(uid=uid, status=status)
    elif request.method == "GET":
        """
            return membership record    
        """
        membership_view_instance: MembershipsView = MembershipsView()
        return membership_view_instance.is_member_off(uid=uid)


@memberships_bp.route("/api/v1/members/<path:plan_id>/status/<path:status>", methods=["GET"])
@handle_auth
def get_plan_members_by_payment_status(plan_id: str, status: str) -> tuple:
    if (plan_id != "") and (status != ""):
        membership_view_instance: MembershipsView = MembershipsView()
        return membership_view_instance.return_plan_members_by_payment_status(plan_id=plan_id, status=status)


@memberships_bp.route("/api/v1/membership/plan/<path:plan_id>")
@handle_auth
def change_membership_plan(plan_id: str) -> tuple:
    if plan_id != "":
        json_data: dict = request.get_json()
        if ("uid" in json_data) and (json_data['uid'] != ""):
            uid: str = json_data.get("uid")
        else:
            return jsonify({'status': False, 'message': 'User Id is required'}), 500

        if ('dest_plan_id' in json_data) and (json_data['dest_plan_id'] != ""):
            dest_plan_id: str = json_data.get("dest_plan_id")
        else:
            return jsonify({"status": False, "message": "destination plan id is required"}), 500

        member_ship_instance_view: MembershipsView = MembershipsView()
        return member_ship_instance_view.change_membership(uid=uid, origin_plan_id=plan_id, dest_plan_id=dest_plan_id)


@memberships_bp.route('/api/v1/membership-plan', methods=["POST"])
def create_membership_plan() -> tuple:
    membership_plan_data: dict = request.get_json()
    member_ship_instance_view: MembershipPlansView = MembershipPlansView()
    return member_ship_instance_view.add_plan(membership_plan_data=membership_plan_data)


@memberships_bp.route('/api/v1/membership-plans', methods=["GET"])
def get_membership_plans() -> tuple:
    member_ship_instance_view: MembershipPlansView = MembershipPlansView()
    return member_ship_instance_view.return_all_plans()

#  API also refer to admin app
