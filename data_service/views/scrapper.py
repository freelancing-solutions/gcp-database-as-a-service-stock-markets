import typing
from flask import current_app, jsonify
from google.cloud import ndb
from data_service.store.scrapper import ScrapperTempStore
from data_service.utils.utils import create_id


class ScrapperView:

    def __init__(self):
        self.client = ndb.Client(namespace="main", project=current_app.config.PROJECT)

    def add_data(self, scrapper_data: dict) -> tuple:
        if isinstance(scrapper_data, dict):
            with self.client.context():
                try:
                    scrapper_instance = ScrapperTempStore()
                    scrapper_instance.status = scrapper_data.get('status') or False
                    scrapper_instance.data_id = create_id()
                    scrapper_instance.data = scrapper_data.get('data')
                    scrapper_instance.put()
                except ValueError as e:
                    return jsonify({'status': False, 'message': str(e)}), 500
                except TypeError as e:
                    return jsonify({'status': False, 'message': str(e)}), 500

        else:
            return jsonify({'status': False, 'message': "invalid data format"}), 500

    def delete_data(self, data_id: str) -> tuple:
        if isinstance(data_id, str):
            with self.client.context():
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



