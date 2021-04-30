import typing
from flask import jsonify, current_app


class WalletView:
    """
        view functions for the wallet
    """
    def __init__(self):
        pass

    def get_wallet(self) -> tuple:
        pass

    def create_wallet(self, wallet_data: dict) -> tuple:
        pass

    def update_wallet(self, wallet_data: dict) -> tuple:
        pass

    def reset_wallet(self, wallet_data: dict) -> tuple:
        pass

    def return_all_wallets(self) -> tuple:
        pass

    def return_wallets_by_balance(self, lower_than: int, higher_than: int) -> tuple:
        pass

    