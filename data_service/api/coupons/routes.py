from flask import Blueprint, request

from data_service.api.api_authenticator import handle_auth
from data_service.views.memberships import CouponsView
coupons_bp = Blueprint('coupons', __name__)

@coupons_bp.route('/api/v1/coupons/<path:path>', methods=['POST'])
@handle_auth
def coupons(path: str) -> tuple:
    coupons_view_instance: CouponsView = CouponsView()
    if path == "get":
        coupon_data: dict = request.get_json()
        return coupons_view_instance.get_coupon(coupon_data=coupon_data)
    elif path == "create":
        coupon_data: dict = request.get_json()
        return coupons_view_instance.add_coupon(coupon_data=coupon_data)
    elif path == "update":
        coupon_data: dict = request.get_json()
        return coupons_view_instance.update_coupon(coupon_data=coupon_data)
    elif path == "cancel":
        coupon_data: dict = request.get_json()
        return coupons_view_instance.cancel_coupon(coupon_data=coupon_data)
    elif path == "get-all":
        return coupons_view_instance.get_all_coupons()
    elif path == "get-valid":
        return coupons_view_instance.get_valid_coupons()
    elif path == "get-expired":
        return coupons_view_instance.get_expired_coupons()
    else:
        pass

    # TODO intergrate Coupons to admin app and allow for the app to
    # generate and manage them
