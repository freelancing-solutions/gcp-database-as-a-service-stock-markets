from flask import Blueprint

stocks_bp = Blueprint('stocks_bp', __name__)


@stocks_bp.route('/api/v1/stocks', methods=['GET', 'POST'])
def stocks():
    pass