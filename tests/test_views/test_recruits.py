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
    mocker.stopall()


# noinspection PyShadowingNames
def test_get_recruit(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=RecruitsQueryMock())

    with test_app().app_context():
        recruits_view_instance: RecruitsView = RecruitsView()
        response, status = recruits_view_instance.get_recruit(recruit_data=recruit_data_mock)
        assert status == 200, "Unable to fetch recruit"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_recruit payload data not being set correctly"
        assert response_data.get('message') is not None, "get_recruit message data not being set correctly"
    mocker.stopall()


# noinspection PyShadowingNames
def test_recruits_by_active_status(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=RecruitsQueryMock())

    with test_app().app_context():
        recruits_view_instance: RecruitsView = RecruitsView()
        response, status = recruits_view_instance.get_recruit(recruit_data=recruit_data_mock)
        assert status == 200, "Unable to fetch recruit"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_recruit payload is not set"
        assert response_data.get('message') is not None, "get_recruit message is not set"
    mocker.stopall()


# noinspection PyShadowingNames
def test_recruits_by_deleted_status(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=RecruitsQueryMock())

    with test_app().app_context():
        recruits_view_instance: RecruitsView = RecruitsView()
        response, status = recruits_view_instance.get_recruits_by_deleted_status(is_deleted=False)
        assert status == 200, "Unable to get recruits by deleted status"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "payload for get_recruit_by_deleted_status not set"
        assert response_data.get('message') is not None, "message gor get_recruit_by_deleted status not set"
    mocker.stopall()


# noinspection PyShadowingNames
def test_recruits_by_affiliate(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=RecruitsQueryMock())
    from .test_affiliate_view import affiliate_data_mock
    affiliate_data_mock['affiliate_id'] = create_id()
    with test_app().app_context():
        recruits_view_instance: RecruitsView = RecruitsView()
        response, status = recruits_view_instance.get_recruits_by_affiliate(affiliate_data=affiliate_data_mock)
        assert status == 200, "Unable to get recruits by affiliate"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, response_data['message']
        assert response_data.get('message') is not None, "message for get_recruits_by_affiliate not set"

    mocker.stopall()


# noinspection PyShadowingNames
def test_recruits_by_active_and_affiliate(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=RecruitsQueryMock())
    from .test_affiliate_view import affiliate_data_mock
    affiliate_data_mock['affiliate_id'] = create_id()
    with test_app().app_context():
        recruits_view_instance: RecruitsView = RecruitsView()
        response, status = recruits_view_instance.get_recruits_by_active_affiliate(affiliate_data=affiliate_data_mock,
                                                                                   is_active=True)
        assert status == 200, "Unable to get affiliates by active status"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, response_data['message']
    mocker.stopall()
