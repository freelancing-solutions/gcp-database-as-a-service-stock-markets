import typing
from flask import current_app, jsonify
from data_service.main import cache_affiliates
from data_service.store.affiliates import AffiliatesValidators as ValidAffiliate
from data_service.store.affiliates import RecruitsValidators as ValidRecruit
from data_service.store.affiliates import EarningsValidators as ValidEarnings
from data_service.store.affiliates import Affiliates, Recruits
from data_service.config.exceptions import DataServiceError
from data_service.utils.utils import create_id, return_ttl, end_of_month
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context


# TODO Create Test Cases for Affiliates View and Documentations
# Dont Edit Just Watch can you see this

class Validator(ValidAffiliate, ValidRecruit, ValidEarnings):

    def can_register_affiliate(self, uid: str) -> bool:
        already_registered: bool = self.user_already_registered(uid=uid)
        if not isinstance(already_registered, bool):
            raise ValueError("invalid user id")
        print("User Already Registered: {}".format(already_registered))
        return not already_registered


class AffiliatesView(Validator):
    """
        Register new affiliates using this class
    """

    def __init__(self):
        super(AffiliatesView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def register_affiliate(self, affiliate_data: dict) -> tuple:
        """
            Register new affiliate
        """
        uid: typing.Union[None, str] = affiliate_data.get('uid')
        if uid is None or uid == "":
            return jsonify({'status': False, 'message': 'user id cannot be Null'}), 500
        if self.can_register_affiliate(uid=uid) is True:
            affiliate_instance: Affiliates = Affiliates(affiliate_id=create_id(), uid=uid)
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "There was an error creating Affiliate"
                raise DataServiceError(message)
            return jsonify({'status': True,
                            'message': 'successfully registered an affiliate',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'User already registered as an Affiliate'}), 500

    @use_context
    @handle_view_errors
    def increment_total_recruits(self, affiliate_data: dict) -> tuple:
        """
            update an existing affiliate
        """
        affiliate_id: typing.Union[str, None] = affiliate_data.get('affiliate_id')
        if affiliate_id is None or affiliate_id == "":
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500
        affiliate_instance: Affiliates = Affiliates.query(Affiliates.affiliate_id == affiliate_id).get()
        if isinstance(affiliate_instance, Affiliates):
            affiliate_instance.total_recruits += 1
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "Something went wrong while updating affiliate"
                raise DataServiceError(message)
            return jsonify({'status': True,
                            'message': 'successfully incremented total recruits',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'Failed to locate affiliate'}), 500

    @use_context
    @handle_view_errors
    def delete_affiliate(self, affiliate_data: dict) -> tuple:
        """
            delete affiliate
        """
        affiliate_id: typing.Union[None, str] = affiliate_data.get('affiliate_id')
        if affiliate_id is None or affiliate_id == "":
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500
        affiliate_instance: Affiliates = Affiliates.query(Affiliates.affiliate_id == affiliate_id).get()
        if isinstance(affiliate_instance, Affiliates):
            affiliate_instance.is_active = False
            affiliate_instance.is_deleted = True
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = 'something went wrong while deleting affiliate'
                return jsonify({'status': False, 'message': message}), 500
            return jsonify({'status': True,
                            'message': 'successfully deleted the affiliate',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'error locating that affiliate'}), 500

    @use_context
    @handle_view_errors
    def mark_active(self, affiliate_data: dict, is_active: bool) -> tuple:
        """
            mark a specific affiliate as active or not active
        """
        affiliate_id: typing.Union[None, str] = affiliate_data.get('affiliate_id')
        if affiliate_id is None or affiliate_id == "":
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500
        if not isinstance(is_active, bool):
            raise ValueError("is_active is required and can only be a boolean")
        affiliate_instance: Affiliates = Affiliates.query(Affiliates.affiliate_id == affiliate_id).get()
        if isinstance(affiliate_instance, Affiliates):
            affiliate_instance.is_active = is_active
            key = affiliate_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Unknown Error occurred while trying to mark affiliate as in-active"
                return jsonify({'status': False, 'message': message}), 500
            return jsonify({'status': True, 'message': 'successfully marked affiliate as inactive',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            message: str = "Unable to locate affiliate record"
            return jsonify({'status': False, 'message': message}), 500

    @cache_affiliates.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_affiliate(self, affiliate_data: dict) -> tuple:
        """
            with affiliate_id or uid return affiliate
        """
        affiliate_id: typing.Union[None, str] = affiliate_data.get('affiliate_id')
        uid: typing.Union[None, str] = affiliate_data.get('uid')

        if (uid is None) and (affiliate_id is None):
            return jsonify({'status': False, 'message': 'uid or affiliate_id is required to fetch affiliate'}), 500
        if uid is not None:
            affiliate_instance: Affiliates = Affiliates.query(Affiliates.uid == uid).get()
        else:
            affiliate_instance: Affiliates = Affiliates.query(Affiliates.affiliate_id == affiliate_id).get()

        if isinstance(affiliate_instance, Affiliates):
            return jsonify({'status': True,
                            'message': 'successfully obtained affiliate data',
                            'payload': affiliate_instance.to_dict()}), 200
        else:
            return jsonify({'status': False, 'message': 'unable to locate affiliate'}), 500

    @cache_affiliates.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_all_affiliates(self) -> tuple:
        """
            return all affiliates
        """
        affiliates_list: typing.List[Affiliates] = Affiliates.query().fetch()
        payload = [affiliate.to_dict() for affiliate in affiliates_list]
        return jsonify({'status': True, 'message': 'Successfully returned all affiliates',
                        'payload': payload}), 200

    @cache_affiliates.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_active_affiliates(self) -> tuple:
        """
            return affiliates who are not deleted and are active
        """
        affiliates_list: typing.List[Affiliates] = Affiliates.query(
            Affiliates.is_active == True, Affiliates.is_deleted == False).fetch()
        payload = [affiliate.to_dict() for affiliate in affiliates_list]
        return jsonify({'status': True, 'message': 'successfully returned all affiliates',
                        'payload': payload}), 200

    @cache_affiliates.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_in_active_affiliates(self) -> tuple:
        """
            return affiliates who are not active
        """
        affiliates_list: typing.List[Affiliates] = Affiliates.query(
            Affiliates.is_active == False, Affiliates.is_deleted == False).fetch()
        payload = [affiliate.to_dict() for affiliate in affiliates_list]
        return jsonify({'status': True, 'message': 'successfully returned all affiliates',
                        'payload': payload}), 200

    @cache_affiliates.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_deleted_affiliates(self) -> tuple:
        """
            return affiliates who are not active
        """
        affiliates_list: typing.List[Affiliates] = Affiliates.query(Affiliates.is_deleted == True).fetch()
        payload = [affiliate.to_dict() for affiliate in affiliates_list]
        return jsonify({'status': True, 'message': 'Successfully returned deleted affiliates',
                        'payload': payload}), 200

    @cache_affiliates.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_not_deleted_affiliates(self) -> tuple:
        """
            return affiliates who are not active
        """
        affiliates_list: typing.List[Affiliates] = Affiliates.query(Affiliates.is_deleted == False).fetch()
        payload = [affiliate.to_dict() for affiliate in affiliates_list]
        return jsonify({'status': True, 'message': 'Successfully returned affiliates which are not deleted',
                        'payload': payload}), 200


class RecruitsView(Validator):
    """
        Used by affiliates to register newly recruited members
    """

    def __init__(self):
        super(RecruitsView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @use_context
    @handle_view_errors
    def add_recruit(self, recruit_data: dict) -> tuple:
        """
            recruit_data: dict
        """
        referrer_uid: typing.Union[None, str] = recruit_data.get('referrer_uid')
        if referrer_uid is None or referrer_uid == "":
            return jsonify({'status': False, 'message': 'referrer uid is required'}), 200

        # TODO - check if i can add recruit
        recruit_instance: Recruits = Recruits(affiliate_id=create_id(), referrer_uid=referrer_uid)
        key = recruit_instance.put(retries=self._max_retries, timeout=self._max_timeout)
        if key is None:
            message: str = "An Error occurred while adding new recruit"
            return jsonify({'status': False, 'message': message}), 500
        return jsonify({'status': True, 'message': 'Successfully created new recruit',
                        'payload': recruit_instance.to_dict()}), 200

    @use_context
    @handle_view_errors
    def delete_recruit(self, recruit_data: dict) -> tuple:

        affiliate_id: str = recruit_data.get('affiliate_id')
        if affiliate_id is None or affiliate_id == "":
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500

        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.affiliate_id == affiliate_id).fetch()
        if isinstance(recruits_list, list) and len(recruits_list) > 0:
            recruits_instance = recruits_list[0]
            recruits_instance.is_deleted = True
            recruits_instance.is_active = False
            key = recruits_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Error occurred while deleting recruit"
                return jsonify({'status': False, 'message': message}), 500
            return jsonify({'status': True, 'message': 'Successfully deleted recruit'}), 200
        else:
            message: str = "Recruit does not exist"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    @handle_view_errors
    def mark_active(self, recruit_data: dict, is_active: bool) -> tuple:
        affiliate_id: str = recruit_data.get('affiliate_id')
        if affiliate_id is None or affiliate_id == "":
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500

        if not isinstance(is_active, bool):
            return jsonify({'status': False, 'message': 'is_active is required and can only be a boolean'}), 500

        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.affiliate_id == affiliate_id).fetch()
        if isinstance(recruits_list, list) and len(recruits_list) > 0:
            recruits_instance: Recruits = recruits_list[0]
            recruits_instance.is_active = is_active
            key = recruits_instance.put(retries=self._max_retries, timeout=self._max_timeout)
            if key is None:
                message: str = "An Error occurred while changing recruit active status"
                return jsonify({'status': False, 'message': message}), 500
            return jsonify({'status': True, 'message': 'Successfully deleted recruit'}), 200
        else:
            message: str = "Recruit does not exist"
            return jsonify({'status': False, 'message': message}), 500

    @cache_affiliates.cached(timeout=return_ttl(name='short'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_recruit(self, recruit_data: dict) -> tuple:
        affiliate_id: str = recruit_data.get('affiliate_id')
        if affiliate_id is None or affiliate_id == "":
            return jsonify({'status': False, 'message': 'affiliate_id is required'}), 500
        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.affiliate_id == affiliate_id).fetch()
        if isinstance(recruits_list, list) and len(recruits_list) > 0:
            recruit_instance: Recruits = recruits_list[0]
            message: str = "Successfully retrieved recruit"
            return jsonify({'status': True, 'payload': recruit_instance.to_dict(), 'message': message}), 200
        else:
            message: str = "Recruit does not exist"
            return jsonify({'status': False, 'message': message}), 500

    @cache_affiliates.cached(timeout=return_ttl(name='short'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_recruits_by_active_status(self, is_active: bool) -> tuple:
        if not isinstance(is_active, bool):
            return jsonify({'status': False, 'message': 'is_active status is required'}), 500
        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.is_active == is_active).fetch()
        payload = [recruit.to_dict() for recruit in recruits_list]

        message: str = "{} recruits successfully fetched recruits by active status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200

    @cache_affiliates.cached(timeout=return_ttl(name='short'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_recruits_by_deleted_status(self, is_deleted: bool) -> tuple:
        if not isinstance(is_deleted, bool):
            return jsonify({'status': False, 'message': 'is_deleted status is required'}), 500
        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.is_deleted == is_deleted).fetch()
        payload = [recruit.to_dict() for recruit in recruits_list]

        message: str = "{} recruits successfully fetched recruits by deleted status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200

    @cache_affiliates.cached(timeout=return_ttl(name='short'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_recruits_by_affiliate(self, affiliate_data: dict) -> tuple:
        referrer_uid: str = affiliate_data.get('referrer_uid')
        if referrer_uid is None or referrer_uid == "":
            return jsonify({'status': False, 'message': 'referrer_uid is required'}), 500
        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.referrer_uid == referrer_uid).fetch()
        payload = [recruit.to_dict() for recruit in recruits_list]

        message: str = "{} recruits successfully fetched recruits by active status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200

    @cache_affiliates.cached(timeout=return_ttl(name='short'), unless=end_of_month)
    @use_context
    @handle_view_errors
    def get_recruits_by_active_and_affiliate(self, affiliate_data: dict, is_active: bool) -> tuple:
        referrer_uid: str = affiliate_data.get('referrer_uid')
        if referrer_uid is None or referrer_uid == "":
            return jsonify({'status': False, 'message': 'referrer_uid is required'}), 500

        if isinstance(is_active, bool):
            return jsonify({'status': False, 'message': 'is_active status can only be a boolean'}), 500
        recruits_list: typing.List[Recruits] = Recruits.query(Recruits.referrer_uid == referrer_uid,
                                                              Recruits.is_active == is_active).fetch()
        payload = [recruit.to_dict() for recruit in recruits_list]

        message: str = "{} recruits successfully fetched affiliate recruits by status".format(str(len(recruits_list)))
        return jsonify({'status': True, 'message': message, 'payload': payload}), 200


class EarningsView(Validator):
    """
        Used by system to register new earnings for affiliates
        # TODO finalize the Earnings Repository
    """

    def __init__(self):
        super(EarningsView, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    def register_earnings(self, earnings_data: dict) -> tuple:
        """
            register new earnings record
        """
        pass

    def mark_paid(self, earnings_data: dict, is_paid: bool) -> tuple:
        """
            mark earnings record as paid or not paid
        """
        pass

    def mark_on_hold(self, earnings_data: dict, on_hold: bool) -> bool:
        """
            mark earnings as on hold or not on hold
            earnings which are on-hold may not be paid until problem is resolved
        """
        pass

    def transfer_earnings_to_wallet(self, earnings_data: dict) -> tuple:
        """
            transfer earnings to wallet
            wallet earnings can be sent to paypal or through EFT
        """
        pass
