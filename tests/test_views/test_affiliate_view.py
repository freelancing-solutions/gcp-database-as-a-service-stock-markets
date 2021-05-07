from datetime import datetime
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
    affiliate_instance = Affiliates()

    def __init__(self):
        pass

    def fetch(self) -> list:
        return [self.affiliate_instance]

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


def test_mark_active():
    pass

def test_get_affiliate():
    pass

def test_get_all_affiliate():
    pass

def get_active_affiliates():
    pass

def get_inactive_affiliates():
    pass

def get_deleted_affiliates():
    pass


