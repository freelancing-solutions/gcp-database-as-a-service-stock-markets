from flask import Blueprint, request
from data_service.api.api_authenticator import handle_auth
from data_service.views.scrapper import ScrapperView
scrapper_bp = Blueprint("scrapper", __name__)


@scrapper_bp.route('/api/v1/scrapper/<path:path>', methods=['POST'])
@handle_auth
def scrapper(path: str) -> tuple:
    scrapper_temp_storage: ScrapperView = ScrapperView()
    if path == "add":
        scrapper_data: dict = request.get_json()
        return scrapper_temp_storage.add_data(scrapper_data=scrapper_data)
    elif path == "delete":
        scrapper_data: dict = request.get_json()
        if "data_id" in scrapper_data and scrapper_data["data_id"] != "":
            data_id: str = scrapper_data.get("data_id")
            return scrapper_temp_storage.delete_data(data_id=data_id)
    else:
        pass





