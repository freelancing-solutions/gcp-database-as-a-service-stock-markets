import typing
from flask import jsonify, current_app
from data_service.store.scrapper import ScrapperTempStore
from data_service.utils.utils import create_id
from data_service.views.use_context import use_context


class ScrapperView:

    def __init__(self):
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    def add_data(self, scrapper_data: dict) -> tuple:
        if isinstance(scrapper_data, dict):
            try:
                scrapper_instance = ScrapperTempStore()
                scrapper_instance.status = scrapper_data.get('status') or False
                scrapper_instance.data_id = create_id()
                scrapper_instance.data = scrapper_data.get('data')
                scrapper_instance.put(use_cache=True, retries=self._max_retries, timeout=self._max_timeout)
            except ValueError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
            except TypeError as e:
                return jsonify({'status': False, 'message': str(e)}), 500
        else:
            return jsonify({'status': False, 'message': "invalid data format"}), 500

    @use_context
    def delete_data(self, data_id: str) -> tuple:
        if isinstance(data_id, str):
            try:
                scrapper_temp_list: typing.List[ScrapperTempStore] = ScrapperTempStore.query(ScrapperTempStore.data_id == data_id).fetch()
                if len(scrapper_temp_list) > 0:
                    scrapper_temp_instance = scrapper_temp_list[0]
                    scrapper_temp_instance.key.delete()
                    return jsonify({'status': True, 'message': "successfully deleted scrapper data" }), 200
                else:
                    return jsonify({"status": False, "message": "scrapper data already deleted"}), 500
            except ValueError as e:
                return jsonify({"status": False, "message": str(e)}), 500
            except TypeError as e:
                return jsonify({"status": False, "message": str(e)}), 500
        else:
            return jsonify({"status": False, "message": "Invalid data_id format"}), 500
