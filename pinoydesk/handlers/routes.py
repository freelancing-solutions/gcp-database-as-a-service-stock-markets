from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, MethodNotAllowed, Unauthorized, HTTPException
default_handlers_bp = Blueprint('handlers', __name__)


@default_handlers_bp.route('/_ah/warmup')
def warmup():
    """
        APP-Engine Warm UP Handler
        # TODO - read settings database
        # TODO - check if task schedulers are set if not set them up
    """
    pass


@default_handlers_bp.app_errorhandler(BadRequest)
def handle_bad_request(e: BadRequest) -> tuple:
    return jsonify({'status': False, 'message': 'Bad Request'}), e.code


@default_handlers_bp.app_errorhandler(Forbidden)
def handle_forbidden_error(e: Forbidden) -> tuple:
    return jsonify({'status': False, 'message': 'Forbidden Request'}), e.code


@default_handlers_bp.app_errorhandler(NotFound)
def handle_not_found_error(e: NotFound) -> tuple:
    return jsonify({'status': False, 'message': 'Resource Not Found'}), e.code


@default_handlers_bp.app_errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e: MethodNotAllowed) -> tuple:
    return jsonify({'status': False, 'message': 'Request Method not Allowed'}), e.code


@default_handlers_bp.app_errorhandler(Unauthorized)
def handle_un_authorized_requests(e: Unauthorized) -> tuple:
    return jsonify({'status': False, 'message': 'Request Not Authorized'}), e.code


@default_handlers_bp.app_errorhandler(HTTPException)
def handle_http_exception(e: HTTPException) -> tuple:
    return jsonify({'status': False, 'message': 'HTTP Error'}), e.code