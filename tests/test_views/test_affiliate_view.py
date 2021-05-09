import typing
from datetime import datetime
from random import randint

from data_service.views.affiliates import AffiliatesView
from data_service.store.affiliates import Affiliates
from data_service.utils.utils import create_id
from .. import test_app
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker

affiliate_data_mock: dict = {
    "uid": create_id(),
    "affiliate_id": create_id(),
    "last_updated": datetime.now(),
    "total_recruits": 0,
    "is_active": True,
    "is_deleted": False
}


class AffiliateQueryMock:
    affiliate_instance: Affiliates = Affiliates()
    results_range: int = randint(0, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[Affiliates]:
        return [self.affiliate_instance for _ in range(self.results_range)]

    def get(self) -> Affiliates:
        return self.affiliate_instance


# noinspection PyShadowingNames
def test_register_affiliate(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())
    mocker.patch('data_service.store.affiliates.AffiliatesValidators.user_already_registered', return_value=False)

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        response, status = affiliates_view_instance.register_affiliate(affiliate_data=affiliate_data_mock)
        response_dict: dict = response.get_json()
        assert status == 200, response_dict['message']
        assert response_dict['status'], "response status not set correctly"
        assert response_dict.get('payload') is not None, "affiliates payload is not being set correctly"
        assert response_dict.get('message') is not None, "affiliate message is not being set correctly"

        # print(affiliate_data_mock)
        # Results here means the registration attempt will fail because uid is empty
        affiliate_data_mock['uid'] = ""
        response, status = affiliates_view_instance.register_affiliate(affiliate_data=affiliate_data_mock)
        response_dict: dict = response.get_json()
        assert status != 200, response_dict['message']
        assert not response_dict['status'], "response status not set correctly"
        assert response_dict.get('message') is not None, "affiliate message is not being set correctly"

        mocker.patch('data_service.store.affiliates.AffiliatesValidators.user_already_registered', return_value=True)
        affiliate_data_mock['uid'] = create_id()
        response, status = affiliates_view_instance.register_affiliate(affiliate_data=affiliate_data_mock)
        response_dict: dict = response.get_json()
        assert status != 200, response_dict['message']
        assert not response_dict['status'], "response status not set correctly"
        assert response_dict.get('message') is not None, "affiliate message is not being set correctly"
    mocker.stopall()


# noinspection PyShadowingNames
def test_increment_decrement_total_recruits(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        response, status = affiliates_view_instance.increment_total_recruits(affiliate_data=affiliate_data_mock)
        affiliate_dict: dict = response.get_json()
        assert affiliate_dict['payload']['total_recruits'] == 1, 'failed to increment number of affiliates'
        assert affiliate_dict['status'], "failing to set the return boolean status"
        assert affiliate_dict.get('message') is not None, "failed to set message"
    mocker.stopall()


# noinspection PyShadowingNames
def test_delete_affiliate(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        response, status = affiliates_view_instance.delete_affiliate(affiliate_data=affiliate_data_mock)
        assert status == 200, "unable to delete affiliate"
        affiliate_dict: dict = response.get_json()
        assert affiliate_dict.get('payload') is not None, "could not access delete affiliate payload"
        assert affiliate_dict.get('message') is not None, "delete_affiliate response message must be set"
        message: str = "affiliate delete operation response status was not set correctly"
        assert isinstance(affiliate_dict['status'], bool) and affiliate_dict['status'], message
    mocker.stopall()


# noinspection PyShadowingNames
def test_mark_active(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        response, status = affiliates_view_instance.mark_active(affiliate_data=affiliate_data_mock, is_active=False)
        assert status == 200, "Unable to mark affiliate as in-active"
        response, status = affiliates_view_instance.mark_active(affiliate_data=affiliate_data_mock, is_active=True)
        assert status == 200, "Unable to mark affiliate as active"
        # noinspection PyTypeChecker
        response, status = affiliates_view_instance.mark_active(affiliate_data=affiliate_data_mock, is_active="True")
        assert status == 500, "passing invalid values is not triggering errors"
        affiliate_data_mock['affiliate_id'] = None
        response, status = affiliates_view_instance.mark_active(affiliate_data=affiliate_data_mock, is_active="True")
        assert status == 500, "passing invalid values is not triggering errors"
    mocker.stopall()


# noinspection PyShadowingNames
def test_get_affiliate(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        response, status = affiliates_view_instance.get_affiliate(affiliate_data=affiliate_data_mock)
        assert status == 200, 'unable to locate affiliate'
        # TODO expand the test cases
    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_get_all_affiliate(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())
    # TODo complete the test cases
    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_all_affiliates()
        assert status == 200, "get_all_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_all_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_all_affiliates message is not set properly"

    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_active_affiliates(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())
    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_active_affiliates()
        assert status == 200, "get_active_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_active_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_active_affiliates message is not set properly"

    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_inactive_affiliates(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_in_active_affiliates()
        assert status == 200, "get_inactive_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_inactive_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_inactive_affiliates message is not set properly"
    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_deleted_affiliates(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_deleted_affiliates()
        assert status == 200, "get_deleted_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_deleted_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_deleted_affiliates message is not set properly"
    mocker.stopall()


# noinspection PyShadowingNames,DuplicatedCode
def test_undeleted_affiliates(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())

    with test_app().app_context():
        affiliate_instance: AffiliatesView = AffiliatesView()
        response, status = affiliate_instance.get_not_deleted_affiliates()
        assert status == 200, "get_not_deleted_affiliates unable to fetch affiliates"
        response_data: dict = response.get_json()
        assert response_data.get('payload') is not None, "get_not_deleted_affiliates payload is not set properly"
        assert response_data.get('message') is not None, "get_not_deleted_affiliates message is not set properly"
    mocker.stopall()
