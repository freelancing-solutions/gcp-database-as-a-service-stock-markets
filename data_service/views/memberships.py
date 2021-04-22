import typing
from google.api_core.exceptions import RetryError, Aborted
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadQueryError, BadRequestError
from flask import current_app, jsonify
from datetime import datetime, date
from data_service.store.exceptions import DataServiceError
from data_service.store.memberships import MembershipPlans, AccessRights, Memberships
from data_service.store.memberships import PlanValidators as PlanValid
from data_service.store.users import UserValidators as UserValid
from data_service.store.memberships import MembershipValidators as MemberValid
from data_service.utils.utils import create_id, end_of_month, return_ttl
from data_service.main import cache_stock_buys_sells


class Validators(UserValid, PlanValid, MemberValid):

    def __init__(self):
        self.max_put_retries: int = 10

    def can_add_member(self, uid: str, plan_id: str, start_date: date) -> bool:
        user_valid: bool = self.is_user_valid(uid=uid)
        plan_exist: bool = self.plan_exist(plan_id=plan_id)
        date_valid: bool = self.start_date_valid(start_date=start_date)
        if isinstance(user_valid, bool) and isinstance(plan_exist, bool) and isinstance(date_valid, bool):
            return user_valid and plan_exist and date_valid
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(message)

    def can_add_plan(self, plan_name: str) -> bool:
        name_exist: bool = self.plan_name_exist(plan_name)
        if isinstance(name_exist, bool):
            return name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(message)

    def can_update_plan(self, plan_id: str, plan_name: str) -> bool:
        plan_exist: bool = self.plan_exist(plan_id=plan_id)
        plan_name_exist: bool = self.plan_name_exist(plan_name=plan_name)
        if isinstance(plan_exist, bool) and isinstance(plan_name_exist, bool):
            return plan_exist and plan_name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(message)

class MembershipsView(Validators):

    def __init__(self):
        super(MembershipsView, self).__init__()
        self.client = ndb.Client(namespace="main", project=current_app.config.get('PROJECT'))

    def _create_or_update_membership(self, uid: str, plan_id: str, plan_start_date: date) -> tuple:
        with self.client.context():
            if self.can_add_member(uid=uid, plan_id=plan_id, start_date=plan_start_date) is True:
                try:
                    member_ships_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
                    if isinstance(member_ships_list, list) and len(member_ships_list) > 0:
                        membership_instance: Memberships = member_ships_list[0]
                    else:
                        membership_instance: Memberships = Memberships()
                        membership_instance.plan_id = create_id()
                        membership_instance.status = 'Unpaid'
                        membership_instance.date_created = datetime.now()

                    membership_instance.uid = uid
                    membership_instance.plan_start_date = plan_start_date
                    key = membership_instance.put(use_cache=True, retries=self.max_put_retries)
                    if key is None:
                        message: str = "Unable to save membership instance to database, please try again"
                        raise DataServiceError(message)

                except ValueError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except TypeError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except BadRequestError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except BadQueryError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except ConnectionRefusedError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except RetryError as e:
                    message: str = str(e.message or e)
                    return jsonify({'status': False, 'message': message}), 500
                except Aborted as e:
                    message: str = str(e.message or e)
                    return jsonify({'status': False, 'message': message}), 500

                return jsonify({'status': True, 'message': 'successfully updated membership',
                                'payload': membership_instance.to_dict()}), 200
            message: str = """Unable to create or update memberships this may be 
            due to errors in database connections or duplicate data"""
            return jsonify({'status': False, 'message': message}), 500

    def add_membership(self, uid: str, plan_id: str, plan_start_date: date) -> tuple:
        return self._create_or_update_membership(uid=uid, plan_id=plan_id, plan_start_date=plan_start_date)

    def update_membership(self, uid: str, plan_id: str, plan_start_date: date) -> tuple:
        return self._create_or_update_membership(uid=uid, plan_id=plan_id, plan_start_date=plan_start_date)

    def set_membership_status(self, uid: str, status: str) -> tuple:
        with self.client.context():
            membership_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
            if isinstance(membership_list, list) and len(membership_list) > 0:
                membership_instance: Memberships = membership_list[0]
                try:
                    membership_instance.status = status
                    key = membership_instance.put(use_cache=True, retries=self.max_put_retries)
                    if key is None:
                        message: str = "Unable to save membership instance to database, please try again"
                        raise DataServiceError(message)

                except ValueError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except BadRequestError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except BadQueryError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except ConnectionRefusedError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except RetryError as e:
                    message: str = str(e.message or e)
                    return jsonify({'status': False, 'message': message}), 500
                except Aborted as e:
                    message: str = str(e.message or e)
                    return jsonify({'status': False, 'message': message}), 500

                message: str = "Successfully update membership status"
                return jsonify({'status': True, 'payload': membership_instance.to_dict(), 'message': message})

    def change_membership(self, uid: str, origin_plan_id: str, dest_plan_id: str) -> tuple:
        with self.client.context():
            try:
                membership_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
                if isinstance(membership_list, list) and len(membership_list) > 0:
                    membership_instance: Memberships = membership_list[0]
                    if membership_instance.plan_id == origin_plan_id:
                        if self.plan_exist(plan_id=dest_plan_id):
                            membership_instance.plan_id = dest_plan_id
                            key = membership_instance.put(use_cache=True, retries=self.max_put_retries)
                        else:
                            # This maybe be because the original plan is deleted but its a rare case
                            membership_instance.plan_id = dest_plan_id
                            key = membership_instance.put(use_cache=True, retries=self.max_put_retries)

                        if key is None:
                            message: str = "Unable to Change Membership, please try again later"
                            raise DataServiceError(message)
                    else:
                        message: str = "Unable to change membership, cannot find original membership record"
                        return jsonify({'status': False, 'message': message}), 500

                else:
                    message: str = "Unable to change membership, cannot find original membership record"
                    return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except TypeError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadRequestError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadQueryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e.message or e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e.message or e)
                return jsonify({'status': False, 'message': message}), 500

            return jsonify({'status': True, 'message': 'successfully updated membership',
                            'payload': membership_instance.to_dict()}), 200

    # noinspection PyUnusedLocal
    def send_welcome_email(self, uid: str, plan_id: str) -> tuple:
        """
            just send a request to the email service to send emails
        """
        with self.client.context():
            return "Ok", 200

    @cache_stock_buys_sells.cached(timeout=return_ttl(name='long'), unless=end_of_month)
    def return_plan_members_by_payment_status(self, plan_id: str, status: str) -> tuple:
        """
            for members of this plan_id return members by payment_status
            payment status should either be paid or unpaid
        """
        with self.client.context():
            try:
                membership_list: typing.List[Memberships] = Memberships.query(
                    Memberships.plan_id == plan_id, Memberships.status == status).fetch()

                if isinstance(membership_list, list) and len(membership_list) > 0:
                    response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
                    message: str = 'successfully fetched members'
                    return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
                else:
                    message: str = "Unable to find plan members whose payment status is {}".format(status)
                    return jsonify({'status': False, 'message': message}), 500

            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e.message or e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e.message or e)
                return jsonify({'status': False, 'message': message}), 500

    @cache_stock_buys_sells.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    def return_plan_members(self, plan_id) -> tuple:
        """
            return all members of a plan
        """
        with self.client.context():
            try:
                membership_list: typing.List[Memberships] = Memberships.query(Memberships.plan_id == plan_id).fetch()
                if isinstance(membership_list, list) and len(membership_list) > 0:
                    response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
                    message: str = 'successfully fetched members'
                    return jsonify({'status': True, 'payload': response_data, 'message': message}), 200
                else:
                    plan_details: MembershipPlans = MembershipPlansView.get_plan(plan_id=plan_id)
                    if plan_details is not None:
                        message: str = "Unable to find members of plan {}".format(plan_details.plan_name)
                        return jsonify({'status': True, 'message': message}), 500

            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e.message or e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e.message or e)
                return jsonify({'status': False, 'message': message}), 500

    @cache_stock_buys_sells.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    def is_member_off(self, uid: str) -> tuple:
        """
            returns user membership details
        """
        with self.client.context():
            try:

                membership_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
                response_data: typing.List[dict] = [member.to_dict() for member in membership_list]

                if isinstance(response_data, list) and len(response_data):
                    return jsonify(
                        {'status': True, 'payload': response_data[0], 'message': 'successfully fetched members'}), 200
                else:
                    return jsonify({'status': False, 'message': 'user does not have any membership plan'}), 500
            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

    @cache_stock_buys_sells.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    def payment_amount(self, uid: str) -> tuple:
        """
            for a specific user return payment amount
        """
        with self.client.context():
            try:
                membership_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
                if isinstance(membership_list, list) and len(membership_list) > 0:
                    membership_instance: Memberships = membership_list[0]
                    plan_id = membership_instance.plan_id
                    membership_plan_instance: MembershipPlans = MembershipPlansView().get_plan(plan_id=plan_id)
                    if membership_plan_instance is None:
                        message: str = 'could not find plan associate with the plan_id'
                        return jsonify({'status': False, 'message': message}), 500
                    amount_data: dict = {
                        'term_payment_amount': membership_plan_instance.term_payment_amount,
                        'registration_amount': membership_plan_instance.registration_amount}
                    message: str = 'successfully returned payment details'
                    return jsonify({'status': True, 'payload': amount_data, 'message': message}), 200

                message: str = 'unable to locate membership details'
                return jsonify({'status': False, 'message': message}), 500
            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

    def set_payment_status(self, uid: str, status: str) -> tuple:  # status is paid or unpaid
        """
            for a specific user set payment status
        """
        with self.client.context():
            try:
                membership_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
                if isinstance(membership_list, list) and len(membership_list) > 0:
                    membership_instance: Memberships = membership_list[0]
                    membership_instance.status = status
                    key = membership_instance.put(use_cache=True, retries=self.max_put_retries)
                    if key is None:
                        message: str = 'for some reason we are unable to set payment status'
                        return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except TypeError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadRequestError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadQueryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

            return jsonify({'status': True, 'message': 'payment status has been successfully set',
                            'payload': membership_instance.to_dict()}), 200


class MembershipPlansView(Validators):
    def __init__(self):
        super(MembershipPlansView, self).__init__()
        self.client = ndb.Client(namespace="main", project=current_app.config.get('PROJECT'))

    def add_plan(self, plan_name: str, description: str, schedule_day: int, schedule_term: str,
                 term_payment: int, registration_amount: int, is_active: bool) -> tuple:
        """
            checks to see if the plan actually exists and the new plan name wont cause a conflict with an existing name

        """
        with self.client.context():
            try:
                if self.can_add_plan(plan_name=plan_name) is True:
                    total_members: int = 0
                    plan_instance: MembershipPlans = MembershipPlans(plan_id=create_id(), plan_name=plan_name,
                                                                     description=description,
                                                                     total_members=total_members,
                                                                     schedule_day=schedule_day,
                                                                     schedule_term=schedule_term,
                                                                     term_payment=term_payment,
                                                                     registration_amount=registration_amount,
                                                                     is_active=is_active,
                                                                     date_created=datetime.now().date())
                    key = plan_instance.put(use_cache=True, retries=self.max_put_retries)
                    if key is None:
                        message: str = 'for some reason we are unable to create a new plan'
                        return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except TypeError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadRequestError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadQueryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

            return jsonify({'status': True, 'message': 'successfully created new membership plan',
                            'payload': plan_instance.to_dict()}), 200

    def update_plan(self, plan_id: str, plan_name: str, description: str, schedule_day: int, schedule_term: str,
                    term_payment: int, registration_amount: int, is_active: bool) -> tuple:

        with self.client.context():
            try:
                if self.can_update_plan(plan_id=plan_id, plan_name=plan_name) is True:
                    membership_plans_list: typing.List[MembershipPlans] = MembershipPlans.query(
                        MembershipPlans.plan_id == plan_id).fetch()
                    if isinstance(membership_plans_list, list) and len(membership_plans_list) > 0:
                        membership_plans_instance: MembershipPlans = membership_plans_list[0]
                        membership_plans_instance.plan_name = plan_name
                        membership_plans_instance.description = description
                        membership_plans_instance.schedule_day = schedule_day
                        membership_plans_instance.schedule_term = schedule_term
                        membership_plans_instance.term_payment_amount = term_payment
                        membership_plans_instance.registration_amount = registration_amount
                        membership_plans_instance.is_active = is_active
                        key = membership_plans_instance.put(use_cache=True, retries=self.max_put_retries)
                        if key is None:
                            message: str = 'for some reason we are unable to create a new plan'
                            return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except TypeError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadRequestError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadQueryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

            return jsonify({'status': True, 'message': 'successfully created new membership plan',
                            'payload': membership_plans_instance.to_dict()}), 200

    def set_is_active(self, plan_id: str, is_active: bool) -> tuple:
        with self.client.context():
            try:
                membership_plan_list: typing.List[MembershipPlans] = MembershipPlans.query(
                    MembershipPlans.plan_id == plan_id).fetch()
                if isinstance(membership_plan_list, list) and len(membership_plan_list) > 0:
                    membership_plans_instance: MembershipPlans = membership_plan_list[0]
                    membership_plans_instance.is_active = is_active
                    key = membership_plans_instance.put(use_cache=True, retries=self.max_put_retries)
                    if key is None:
                        message: str = 'for some reason we are unable to create a new plan'
                        return jsonify({'status': False, 'message': message}), 500

            except ValueError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except TypeError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadRequestError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadQueryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

            return jsonify({'status': True, 'message': 'successfully update membership plan status',
                            'payload': membership_plans_instance.to_dict()}), 200

    @cache_stock_buys_sells.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    def return_plans_by_schedule_term(self, schedule_term: str) -> tuple:
        with self.client.context():
            try:
                membership_plan_list: typing.List[MembershipPlans] = MembershipPlans.query(
                    MembershipPlans.schedule_term == schedule_term).fetch()
                payload: typing.List[dict] = [membership.to_dict() for membership in membership_plan_list]
                return jsonify({'status': False, 'payload': payload,
                                'message': 'successfully retrieved monthly plans'}), 200
            except BadRequestError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except BadQueryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500

    @cache_stock_buys_sells.cached(timeout=return_ttl(name='short'))
    def get_plan(self, plan_id: str) -> typing.Union[None, MembershipPlans]:
        """
            this utility will be used by other views to obtain information about membershipPlans
        """
        with self.client.context():
            if isinstance(plan_id, str):
                try:
                    membership_plans_list: typing.List[MembershipPlans] = MembershipPlans.query(
                        MembershipPlans.plan_id == plan_id).fetch()
                    if isinstance(membership_plans_list, list) and len(membership_plans_list) > 0:
                        membership_instance: MembershipPlans = membership_plans_list[0]
                        return membership_instance
                    else:
                        return None
                except ConnectionRefusedError:
                    return None
                except RetryError:
                    return None
                except Aborted:
                    return None

            return None

    @cache_stock_buys_sells.cached(timeout=return_ttl(name='long'))
    def return_plan(self, plan_id: str) -> tuple:
        plan_instance = self.get_plan(plan_id=plan_id)
        if plan_instance is not None:
            message: str = "successfully fetched plan"
            return jsonify({'status': True, 'payload': plan_instance.to_dict(), 'message': message}), 200
        return jsonify({'status': False, 'message': 'Unable to get plan'}), 500

class AccessRightsView:
    def __init__(self):
        self.client = ndb.Client(namespace="main", project=current_app.config.get('PROJECT'))

    @cache_stock_buys_sells.cached(timeout=return_ttl(name='short'))
    def get_access_rights(self, plan_id: str) -> typing.Union[None, AccessRights]:
        with self.client.context():
            if isinstance(plan_id, str):
                try:
                    access_rights_list: typing.List[AccessRights] = AccessRights.query(AccessRights.plan_id == plan_id)
                    if isinstance(access_rights_list, list) and len(access_rights_list) > 0:
                        access_rights_instance: AccessRights = access_rights_list[0]
                        return access_rights_instance
                    return None
                except ConnectionRefusedError:
                    return None
                except RetryError:
                    return None
                except Aborted:
                    return None
            return None
