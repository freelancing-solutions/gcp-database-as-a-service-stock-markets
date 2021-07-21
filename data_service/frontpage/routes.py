from flask import Blueprint, render_template
from data_service.main import cache_stocks, default_timeout

home_bp = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home_bp.route('/', methods=["GET"])
# @cache_stocks.cached(timeout=default_timeout)
def home():
    return render_template('index.html')

# TODO create a decent front page with
# API Documentation and a github link to support further development
