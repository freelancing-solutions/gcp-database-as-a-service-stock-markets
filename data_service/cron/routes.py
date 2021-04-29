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

    """




