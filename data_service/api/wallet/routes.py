from flask import Blueprint, request, jsonify
from data_service.api.api_authenticator import handle_auth
from data_service.views.wallet import WalletView

wallet_bp = Blueprint("wallet", __name__)


@wallet_bp.route('/api/v1/wallet', methods=["GET", "POST", "DELETE", "PUT"])
def wallet() -> tuple:
    wallet_instance: WalletView = WalletView()

    if request.method == "GET":
        json_data: dict = request.get_json()
        return wallet_instance.get_wallet(uid=json_data['uid'])
    elif request.method == "POST":
        json_data: dict = request.get_json()
        return wallet_instance.create_wallet(uid=json_data['uid'],
                                             currency=json_data['currency'],
                                             paypal_address=json_data['paypal_address'])
    elif request.method == "PUT":
        json_data: dict = request.get_json()
        return wallet_instance.update_wallet(wallet_data=json_data)

    elif request.method == "DELETE":
        json_data: dict = request.get_json()
        return wallet_instance.reset_wallet(wallet_data=json_data)
    else:
        return jsonify({'status': False, 'message': 'Unable to process this request please check your parameters'}), 500



