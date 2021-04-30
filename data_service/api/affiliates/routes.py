from flask import Blueprint, request

from data_service.api.api_authenticator import handle_auth
from data_service.views.affiliates import AffiliatesView, RecruitsView

affiliates_bp = Blueprint('affiliates', __name__)

@affiliates_bp.route('/api/v1/affiliate/<path:path>', methods=['POST'])
@handle_auth
def affiliate(path: str) -> tuple:
    affiliate_view_instance: AffiliatesView = AffiliatesView()
    affiliate_data: dict = request.get_json()

    if path == "get":
        return affiliate_view_instance.get_affiliate(affiliate_data=affiliate_data)
    elif path == "get-all":
        return affiliate_view_instance.get_all_affiliates()
    elif path == "get-active":
        return affiliate_view_instance.get_active_affiliates()
    elif path == "get-not-active":
        return affiliate_view_instance.get_in_active_affiliates()
    elif path == "get-deleted":
        return affiliate_view_instance.get_deleted_affiliates()
    elif path == "get-not-deleted":
        return affiliate_view_instance.get_not_deleted_affiliates()
    elif path == "register":
        return affiliate_view_instance.register_affiliate(affiliate_data=affiliate_data)
    elif path == "inc-recruits":
        return affiliate_view_instance.increment_total_recruits(affiliate_data=affiliate_data)
    elif path == 'dec-recruits':
        pass
    elif path == 'delete':
        return affiliate_view_instance.delete_affiliate(affiliate_data=affiliate_data)
    elif path == 'mark-active':
        return affiliate_view_instance.mark_active(affiliate_data=affiliate_data, is_active=True)
    elif path == 'mark-not-active':
        return affiliate_view_instance.mark_active(affiliate_data=affiliate_data, is_active=False)
    else:
        pass


@affiliates_bp.route('/api/v1/recruits/<path:path>', methods=['POST'])
@handle_auth
def recruits(path: str) -> tuple:
    recruits_view_instance: RecruitsView = RecruitsView()
    recruit_data: dict = request.get_json()
    if path == "get":
        return recruits_view_instance.get_recruit(recruit_data=recruit_data)
    elif path == "register":
        return recruits_view_instance.add_recruit(recruit_data=recruit_data)
    elif path == "delete":
        return recruits_view_instance.delete_recruit(recruit_data=recruit_data)
    elif path == "mark-active":
        return recruits_view_instance.mark_active(recruit_data=recruit_data, is_active=True)
    elif path == "mark-not-active":
        return recruits_view_instance.mark_active(recruit_data=recruit_data, is_active=False)
    elif path == "get-active":
        return recruits_view_instance.get_recruits_by_active_status(recruit_data=recruit_data, is_active=True)
    elif path == "get-not-active":
        return recruits_view_instance.get_recruits_by_active_status(recruit_data=recruit_data, is_active=False)
    elif path == "get-deleted":
        return recruits_view_instance.get_recruits_by_deleted_status(recruit_data=recruit_data, is_deleted=True)
    elif path == "get-not-deleted":
        return recruits_view_instance.get_recruits_by_deleted_status(recruit_data=recruit_data, is_deleted=False)
    elif path == "get-by-affiliate":
        return recruits_view_instance.get_recruits_by_affiliate(affiliate_data=recruit_data)
    elif path == "get-by-active-affiliate":
        return recruits_view_instance.get_recruits_by_active_and_affiliate(affiliate_data=recruit_data, is_active=True)
    elif path == "get-by-not-active-affiliate":
        return recruits_view_instance.get_recruits_by_active_and_affiliate(affiliate_data=recruit_data, is_active=False)
    else:
        pass

    # TODO Fully intergrate the Affiliate API to the Admin App