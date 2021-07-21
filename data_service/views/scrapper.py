import typing
from flask import jsonify, current_app

from data_service.config.exceptions import DataServiceError
from data_service.store.scrapper import ScrapperTempStore
from data_service.utils.utils import create_id
from data_service.config.exception_handlers import handle_view_errors
from data_service.config.use_context import use_context


# TODO Create Test Cases for Scrapper and Documentations
class ScrapperView:
    def __init__(self):
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def add_data(self, scrapper_data: dict) -> tuple:
        if isinstance(scrapper_data, dict):
            scrapper_instance: ScrapperTempStore = ScrapperTempStore()
            scrapper_instance.status = scrapper_data.get('status')
            scrapper_instance.data_id = create_id()
            scrapper_instance.data = scrapper_data.get('data')
            key = scrapper_instance.put()
            if key is None:
                message: str = "Unable to save database"
                raise DataServiceError(status=500, description=message)
            return jsonify({'status': False, 'message': "successfully created scrapped data"}), 200
        else:
            return jsonify({'status': False, 'message': "invalid data format"}), 500

    @use_context
    @handle_view_errors
    def delete_data(self, data_id: str) -> tuple:
        if isinstance(data_id, str):
            scrapper_temp_list: typing.List[ScrapperTempStore] = ScrapperTempStore.query(ScrapperTempStore.data_id == data_id).fetch()
            if len(scrapper_temp_list) > 0:
                scrapper_temp_instance = scrapper_temp_list[0]
                scrapper_temp_instance.key.delete()
                return jsonify({'status': True, 'message': "successfully deleted scrapper data" }), 200
            else:
                return jsonify({"status": False, "message": "scrapper data already deleted"}), 500
        else:
            return jsonify({"status": False, "message": "Invalid data_id format"}), 500
