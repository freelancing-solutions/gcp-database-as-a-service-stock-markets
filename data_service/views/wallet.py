import typing
from flask import jsonify, current_app

from data_service.store.mixins import AmountMixin
from data_service.store.wallet import WalletModel
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context


class Validator:

    @staticmethod
    def can_add_wallet(uid: str) -> bool:
        return True

    @staticmethod
    def can_update_wallet(uid: str) -> bool:
        return True


class WalletView(Validator):
    """
        view functions for the wallet
    """
    def __init__(self):
        pass

    @use_context
    @handle_view_errors
    def create_wallet(self, uid: str, currency: str, paypal_address: str) -> tuple:
        if self.can_add_wallet(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel()
            amount_instance: AmountMixin = AmountMixin()
            amount_instance.amount = 0
            amount_instance.currency = currency
            wallet_instance.uid = uid
            wallet_instance.available_funds = amount_instance
            wallet_instance.paypal_address = paypal_address
            key = wallet_instance.put

            return jsonify({'status': True, 'message': 'successfully created wallet', 'payload': wallet_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    def get_wallet(self, uid: str) -> tuple:
        wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
        return jsonify({'status': True, 'payload': wallet_instance.to_dict(), 'message': 'wallet found'}), 200

    @use_context
    @handle_view_errors
    def update_wallet(self, wallet_data: dict) -> tuple:
        uid: str = wallet_data.get("uid")
        available_funds: int = wallet_data.get("available_funs")
        paypal_address: str = wallet_data.get("paypal_address")
        if self.can_update_wallet(uid=uid) is True:
            wall_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            wall_instance.uid = uid
            wall_instance.available_funds = available_funds
            wall_instance.paypal_address = paypal_address
            key = wall_instance.put()
            

    @use_context
    @handle_view_errors
    def reset_wallet(self, wallet_data: dict) -> tuple:
        pass

    @use_context
    @handle_view_errors
    def return_all_wallets(self) -> tuple:
        pass

    @use_context
    @handle_view_errors
    def return_wallets_by_balance(self, lower_than: int, higher_than: int) -> tuple:
        pass

