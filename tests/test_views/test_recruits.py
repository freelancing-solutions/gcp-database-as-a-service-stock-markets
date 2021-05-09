import typing
from datetime import datetime
from random import randint

from data_service.views.affiliates import RecruitsView
from data_service.store.affiliates import Recruits
from data_service.utils.utils import create_id
from .. import test_app
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class RecruitsQueryMock:
    recruits_instance: Recruits = Recruits()
    results_range: int = randint(0, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[Recruits]:
        return [self.recruits_instance for _ in range(self.results_range)]

    def get(self) -> Recruits:
        return self.recruits_instance


recruit_data_mock: dict = {
    'affiliate_id': create_id(),
    'referrer_uid': create_id(),
    'datetime_recruited': datetime.now(),
    'datetime_updated': datetime.now(),
    'is_member': True,
    'plan_id': create_id(),
    'is_active': True,
    'is_deleted': False
}


# noinspection PyShadowingNames
def test_add_recruit(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=RecruitsQueryMock())

    with test_app().app_context():
        recruits_view_instance: RecruitsView = RecruitsView()
        response, status = recruits_view_instance.add_recruit(recruit_data=recruit_data_mock)
        assert status == 200, "unable to create new recruit"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, response_data['message']
        assert response_data.get('message') is not None, response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_delete_recruit(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=RecruitsQueryMock())

    with test_app().app_context():
        recruits_view_instance: RecruitsView = RecruitsView()
        response, status = recruits_view_instance.delete_recruit(recruit_data=recruit_data_mock)
        assert status == 200, "unable to delete_recruit"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "delete_recruit payload not being set properly"
        assert response_data.get('message') is not None, "delete_recruit message not being set properly"

    mocker.stopall()


# noinspection PyShadowingNames
def test_mark_active(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=RecruitsQueryMock())

    with test_app().app_context():
        recruits_view_instance: RecruitsView = RecruitsView()
        response, status = recruits_view_instance.mark_active(recruit_data=recruit_data_mock, is_active=False)
        assert status == 200, "Unable to set is_active to False"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "mark_active payload not being set properly"
        assert response_data.get('message') is not None, "mark_active message not being set properly"
        response, status = recruits_view_instance.mark_active(recruit_data=recruit_data_mock, is_active=True)
        assert status == 200, "Unable to set is_active to True"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "mark_active payload not being set properly"
        assert response_data.get('message') is not None, "mark_active message not being set properly"


