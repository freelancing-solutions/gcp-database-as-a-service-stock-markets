import typing
from flask import jsonify
from data_service.store.mixins import AmountMixin
from data_service.store.wallet import WalletModel, WalletValidator
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context


class Validator(WalletValidator):

    def __init__(self):
        super(Validator, self).__init__()

    def can_add_wallet(self, uid: typing.Union[None, str] = None) -> bool:
        if uid is None:
            return False

        wallet_exist: bool = self.wallet_exist(uid=uid)
        return wallet_exist

    def can_update_wallet(self, uid: typing.Union[None, str] = None) -> bool:
        if uid is None:
            return False

        wallet_exist: bool = self.wallet_exist(uid=uid)
        return wallet_exist

    def can_reset_wallet(self, uid: typing.Union[None, str]) -> bool:
        if uid is None:
            return False

        wallet_exist: bool = self.wallet_exist(uid=uid)
        return wallet_exist


class WalletView(Validator):
    """
        view functions for the wallet
        # TODO -  Refactor Wallet View and improve functionality
    """

    def __init__(self):
        super(WalletView, self).__init__()

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

            return jsonify({'status': True, 'payload': wall_instance.to_dict(),
                            'message': 'successfully updated wallet'}), 200

    @use_context
    @handle_view_errors
    def reset_wallet(self, wallet_data: dict) -> tuple:
        uid: str = wallet_data.get('uid')
        if self.can_reset_wallet(uid=uid) is True:
            wallet_instance: WalletModel = WalletModel.query(WalletModel.uid == uid).get()
            wallet_instance.available_funds = 0
            key = wallet_instance.put()
            return jsonify({'status': True, 'payload': wallet_instance.to_dict(),
                            'message': 'wallet is rest'}), 200

    @use_context
    @handle_view_errors
    def return_all_wallets(self) -> tuple:
        wallet_list: typing.List[WalletModel] = WalletModel.query().fetch()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True, 'payload': payload,
                        'message': 'wallets returned'}), 200

    @use_context
    @handle_view_errors
    def return_wallets_by_balance(self, lower_bound: int, higher_bound: int) -> tuple:
        wallet_list: typing.List[WalletModel] = WalletModel.query(WalletModel.available_funds > lower_bound,
                                                                  WalletModel.available_funds < higher_bound).fetch()
        payload: typing.List[dict] = [wallet.to_dict() for wallet in wallet_list]
        return jsonify({'status': True, 'payload': payload, 'message': 'wallets returned'}), 200