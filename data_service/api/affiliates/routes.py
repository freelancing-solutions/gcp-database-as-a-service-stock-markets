from flask import Blueprint, request, jsonify
from datetime import datetime, date

from data_service.store.exceptions import InputError
from data_service.utils.utils import date_string_to_date
from data_service.views.affiliates import AffiliatesView, RecruitsView

affiliates_bp = Blueprint('affiliates', __name__)

@affiliates_bp.route('/api/v1/affiliate/<path:path>', methods=['POST'])
def affiliate(path: str) -> tuple:
    affiliate_view_instance: AffiliatesView = AffiliatesView()
    affiliate_data: dict = request.get_json()

    if path == "get":
        return affiliate_view_instance.get_affiliate(affiliate_data=affiliate_data)
    elif path == "get-all":
        return affiliate_view_instance.get_all_affiliates()
    elif path == "get-active":
        return affiliate_view_instance.get_active_affiliates()
    elif path == "get-in-active":
        return affiliate_view_instance.get_in_active_affiliates()
    elif path == "get-deleted":
        return affiliate_view_instance.get_deleted_affiliates()
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
    elif path == 'mark-inactive':
        return affiliate_view_instance.mark_active(affiliate_data=affiliate_data, is_active=False)

