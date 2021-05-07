from datetime import datetime
from data_service.views.affiliates import AffiliatesView
from data_service.utils.utils import create_id
from .. import test_app
from data_service.config import Config
from pytest import raises


affiliate_data_mock: dict = {
    "uid": create_id(),
    "affiliate_id": create_id(),
    "last_updated": datetime.now(),
    "total_recruits": 0,
    "is_active": True,
    "is_deleted": False
}
def test_register_affiliate():
    app = test_app()
    with app.app_context():
        affiliates_view_instance = AffiliatesView()
        response = affiliates_view_instance.register_affiliate(affiliate_data=affiliate_data_mock)

def test_increment_total_recruits():
    pass

def test_delete_affiliate():
    pass

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


