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


class WalletView(Validator):
    """
        view functions for the wallet
    """
    def __init__(self):
        pass

    @use_context
    @handle_view_errors
    def create_wallet(self, uid: str, currency: str, paypal_address: str) -> tuple:
        if self.can_add_wallet(uid=uid):
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
    def update_wallet(self, wallet_data: dict) -> tuple:
        pass

    @use_context
    def reset_wallet(self, wallet_data: dict) -> tuple:
        pass

    @use_context
    def return_all_wallets(self) -> tuple:
        pass

    @use_context
    def return_wallets_by_balance(self, lower_than: int, higher_than: int) -> tuple:
        pass

