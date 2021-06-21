import os
from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, MethodNotAllowed, Unauthorized, HTTPException
from data_service.config.exceptions import DataServiceError, InputError

cron_bp = Blueprint('cron', __name__)


@cron_bp.route('/cron/get-tickers-eod', methods=['GET'])
def get_exchange_tickers():
    """
        https://eodhistoricaldata.com/api/exchange-symbol-list/PSE?api_token=6082f94d7285f7.55471245
        use the above url to get exchange tickers data
        #TODO see open issue about cron jobs on github
    """
    pass


@cron_bp.route('/cron/get-sell-volume', methods=["GET"])
def get_sell_volume():
    pass


@cron_bp.route('/cron/get-buy-volume', methods=["GET"])
def get_buy_volume():
    pass


@cron_bp.route('/cron/get-net-volume', methods=["GET"])
def get_net_volume():
    pass


# Memberships cron jobs
@cron_bp.route('/cron/pay-memberships', methods=["GET"])
def pay_memberships():
    """
        used to go through each membership plans and executes payments
    """
    pass


@cron_bp.route('/cron/downgrade-memberships', methods=["GET"])
def downgrade_unpaid():
    """
        goes through memberships plans and downgrade unpaid plans
    """
    pass


# Affiliates cron jobs
@cron_bp.route('/cron/send-affiliate-payment', methods=['GET'])
def send_affiliate_payment():
    """
        send affiliate payment to wallet
    """
    pass
