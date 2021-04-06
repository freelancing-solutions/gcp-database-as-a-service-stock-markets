from flask import Blueprint

settings_bp = Blueprint('settings_bp', __name__)


@settings_bp.route('/api/v1/settings', methods=['GET', 'POST'])
def settings():
    pass