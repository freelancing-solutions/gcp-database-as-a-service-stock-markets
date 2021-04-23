import functools
import typing
from google.api_core.exceptions import RetryError, Aborted
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadQueryError, BadRequestError
from flask import jsonify, current_app
from datetime import datetime, date
from data_service.store.exceptions import DataServiceError
from data_service.store.memberships import MembershipPlans, AccessRights, Memberships, Coupons
from data_service.store.memberships import PlanValidators as PlanValid
from data_service.store.mixins import AmountMixin
from data_service.store.users import UserValidators as UserValid
from data_service.store.memberships import MembershipValidators as MemberValid
from data_service.store.memberships import CouponsValidator as CouponValid
from data_service.utils.utils import create_id, end_of_month, return_ttl, timestamp
from data_service.main import cache_memberships
from data_service.views.use_context import use_context


class Validators(UserValid, PlanValid, MemberValid, CouponValid):

    def __init__(self):
        super(Validators, self).__init__()
        self._max_retries = current_app.config.get('DATASTORE_RETRIES')
        self._max_timeout = current_app.config.get('DATASTORE_TIMEOUT')

    @ndb.tasklet
    def can_add_member(self, uid: str, plan_id: str, start_date: date) -> any:
        user_valid: typing.Union[None, bool] = yield self.is_user_valid(uid=uid)
        plan_exist: typing.Union[None, bool] = yield self.plan_exist(plan_id=plan_id)
        date_valid: typing.Union[None, bool] = yield self.start_date_valid(start_date=start_date)

        if isinstance(user_valid, bool) and isinstance(plan_exist, bool) and isinstance(date_valid, bool):
            return user_valid and plan_exist and date_valid
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(message)

    @ndb.tasklet
    def can_add_plan(self, plan_name: str) -> any:
        name_exist: typing.Union[None, bool] = yield self.plan_name_exist(plan_name)
        if isinstance(name_exist, bool):
            return name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(message)

    @ndb.tasklet
    def can_update_plan(self, plan_id: str, plan_name: str) -> any:
        plan_exist: typing.Union[None, bool] = yield self.plan_exist(plan_id=plan_id)
        plan_name_exist: typing.Union[None, bool] = yield self.plan_name_exist(plan_name=plan_name)
        if isinstance(plan_exist, bool) and isinstance(plan_name_exist, bool):
            return plan_exist and plan_name_exist
        message: str = "Unable to verify input data, due to database error, please try again later"
        raise DataServiceError(message)

    @ndb.tasklet
    def can_add_coupon(self, code: str, expiration_time: int, discount: int) -> any:
        coupon_exist: typing.Union[None, bool] = yield self.coupon_exist(code=code)
        expiration_valid: typing.Union[None, bool] = yield self.expiration_valid(expiration_time=expiration_time)
        discount_valid: typing.Union[None, bool] = yield self.discount_valid(discount=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return (not coupon_exist) and expiration_valid and discount_valid
        message: str = "Unable to verify input data"
        raise DataServiceError(message)

    @ndb.tasklet
    def can_update_coupon(self, code: str, expiration_time: int, discount: int) -> any:
        coupon_exist: typing.Union[None, bool] = yield self.coupon_exist(code=code)
        expiration_valid: typing.Union[None, bool] = yield self.expiration_valid(expiration_time=expiration_time)
        discount_valid: typing.Union[None, bool] = yield self.discount_valid(discount=discount)

        if isinstance(coupon_exist, bool) and isinstance(expiration_valid, bool) and isinstance(discount_valid, bool):
            return coupon_exist and expiration_valid and discount_valid

        message: str = "Unable to verify input data"
        raise DataServiceError(message)


class MembershipsView(Validators):

    def __init__(self):
        super(MembershipsView, self).__init__()

    @use_context
    def _create_or_update_membership(self, uid: str, plan_id: str, plan_start_date: date) -> tuple:
        if self.can_add_member(uid=uid, plan_id=plan_id, start_date=plan_start_date).result() is True:
            try:
                # can use get to simplify this and make transactions faster
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
                key = membership_instance.put(use_cache=True, retries=self._max_retries, timeout=self._max_timeout)

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

    @use_context
    def set_membership_status(self, uid: str, status: str) -> tuple:
        try:
            membership_instance: Memberships = Memberships.query(Memberships.uid == uid).get()
            membership_instance.status = status
            key = membership_instance.put(use_cache=True, retries=self._max_retries, timeout=self._max_timeout)
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

    @use_context
    def change_membership(self, uid: str, origin_plan_id: str, dest_plan_id: str) -> tuple:
        try:
            membership_instance: Memberships = Memberships.query(Memberships.uid == uid).get()
            if membership_instance.plan_id == origin_plan_id:
                if self.plan_exist(plan_id=dest_plan_id):
                    membership_instance.plan_id = dest_plan_id
                    key = membership_instance.put(use_cache=True, retries=self._max_retries,
                                                  timeout=self._max_timeout)
                else:
                    # This maybe be because the original plan is deleted but its a rare case
                    membership_instance.plan_id = dest_plan_id
                    key = membership_instance.put(use_cache=True, retries=self._max_retries,
                                                  timeout=self._max_timeout)

                if key is None:
                    message: str = "Unable to Change Membership, please try again later"
                    raise DataServiceError(message)
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
    @use_context
    def send_welcome_email(self, uid: str, plan_id: str) -> tuple:
        """
            just send a request to the email service to send emails
        """
        return "Ok", 200

    @cache_memberships.cached(timeout=return_ttl(name='long'), unless=end_of_month)
    @use_context
    def return_plan_members_by_payment_status(self, plan_id: str, status: str) -> tuple:
        """
            for members of this plan_id return members by payment_status
            payment status should either be paid or unpaid
        """
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

    @cache_memberships.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    def return_plan_members(self, plan_id) -> tuple:
        """
            return all members of a plan
        """
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

    @cache_memberships.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    def is_member_off(self, uid: str) -> tuple:
        """
            returns user membership details
        """
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

    @cache_memberships.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    def payment_amount(self, uid: str) -> tuple:
        """
            for a specific user return payment amount
        """
        try:
            membership_instance: Memberships = Memberships.query(Memberships.uid == uid).get()
            if isinstance(membership_instance, Memberships):
                plan_id: str = membership_instance.plan_id
                membership_plan_instance: MembershipPlans = MembershipPlansView().get_plan(plan_id=plan_id)
                if membership_plan_instance is None:
                    message: str = 'could not find plan associate with the plan_id'
                    return jsonify({'status': False, 'message': message}), 500
                amount_data: dict = {
                    'term_payment_amount': str(membership_plan_instance.term_payment_amount),
                    'registration_amount': str(membership_plan_instance.registration_amount)}
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

    @use_context
    def set_payment_status(self, uid: str, status: str) -> tuple:  # status is paid or unpaid
        """
            for a specific user set payment status
        """
        try:
            membership_instance: Memberships = Memberships.query(Memberships.uid == uid).get()
            if isinstance(membership_instance, Memberships):
                membership_instance.status = status
                key = membership_instance.put(use_cache=True, retries=self._max_retries, timeout=self._max_timeout)
                if key is None:
                    message: str = 'for some reason we are unable to set payment status'
                    return jsonify({'status': False, 'message': message}), 500
            else:
                message: str = "Membership not found"
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

    @use_context
    def add_plan(self, plan_name: str, description: str, schedule_day: int, schedule_term: str,
                 term_payment: int, registration_amount: int, currency: str, is_active: bool) -> tuple:
        """
            checks to see if the plan actually exists and the new plan name wont cause a conflict with an existing name

        """
        try:
            if self.can_add_plan(plan_name=plan_name).result() is True:
                total_members: int = 0
                # Creating Amount Mixins to represent real currency
                curr_term_payment: AmountMixin = AmountMixin(amount=term_payment, currency=currency)
                curr_registration_amount: AmountMixin = AmountMixin(amount=registration_amount, currency=currency)

                plan_instance: MembershipPlans = MembershipPlans(plan_id=create_id(), plan_name=plan_name,
                                                                 description=description,
                                                                 total_members=total_members,
                                                                 schedule_day=schedule_day,
                                                                 schedule_term=schedule_term,
                                                                 term_payment=curr_term_payment,
                                                                 registration_amount=curr_registration_amount,
                                                                 is_active=is_active,
                                                                 date_created=datetime.now().date())
                key = plan_instance.put(use_cache=True, retries=self._max_retries, timeout=self._max_timeout)
                if key is None:
                    message: str = 'for some reason we are unable to create a new plan'
                    return jsonify({'status': False, 'message': message}), 500
            else:
                message: str = 'Unable to create plan'
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

    @use_context
    def update_plan(self, plan_id: str, plan_name: str, description: str, schedule_day: int, schedule_term: str,
                    term_payment: int, registration_amount: int, currency: str, is_active: bool) -> tuple:
        try:
            if self.can_update_plan(plan_id=plan_id, plan_name=plan_name).result() is True:
                membership_plans_instance: MembershipPlans = MembershipPlans.query(
                    MembershipPlans.plan_id == plan_id).get()
                if isinstance(membership_plans_instance, MembershipPlans):
                    curr_term_payment: AmountMixin = AmountMixin(amount=term_payment, currency=currency)
                    curr_registration_amount: AmountMixin = AmountMixin(amount=registration_amount,
                                                                        currency=currency)
                    membership_plans_instance.plan_name = plan_name
                    membership_plans_instance.description = description
                    membership_plans_instance.schedule_day = schedule_day
                    membership_plans_instance.schedule_term = schedule_term
                    membership_plans_instance.term_payment_amount = curr_term_payment
                    membership_plans_instance.registration_amount = curr_registration_amount
                    membership_plans_instance.is_active = is_active
                    key = membership_plans_instance.put(use_cache=True, retries=self._max_retries,
                                                        timeout=self._max_timeout)
                    if key is None:
                        message: str = 'for some reason we are unable to create a new plan'
                        return jsonify({'status': False, 'message': message}), 500

                    return jsonify({'status': True, 'message': 'successfully created new membership plan',
                                    'payload': membership_plans_instance.to_dict()}), 200

                else:
                    message: str = 'Membership plan not found'
                    return jsonify({'status': False, 'message': message}), 500

            else:
                message: str = 'Conditions to update plan not satisfied'
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

    @use_context
    def set_is_active(self, plan_id: str, is_active: bool) -> tuple:
        try:
            membership_plans_instance: MembershipPlans = MembershipPlans.query(MembershipPlans.plan_id == plan_id).get()
            if isinstance(membership_plans_instance, MembershipPlans):
                membership_plans_instance.is_active = is_active
                key = membership_plans_instance.put(use_cache=True, retries=self._max_retries,
                                                    timeout=self._max_timeout)
                if key is None:
                    message: str = 'for some reason we are unable to create a new plan'
                    return jsonify({'status': False, 'message': message}), 500

                return jsonify({'status': True, 'message': 'successfully update membership plan status',
                                'payload': membership_plans_instance.to_dict()}), 200

            else:
                message: str = 'Membership plan not found'
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

    @cache_memberships.cached(timeout=return_ttl(name='medium'), unless=end_of_month)
    @use_context
    def return_plans_by_schedule_term(self, schedule_term: str) -> tuple:
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

    @use_context
    def get_plan(self, plan_id: str) -> typing.Union[None, MembershipPlans]:
        """
            this utility will be used by other views to obtain information about membershipPlans
        """
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

    @cache_memberships.cached(timeout=return_ttl(name='long'))
    def return_plan(self, plan_id: str) -> tuple:
        plan_instance = self.get_plan(plan_id=plan_id)
        if plan_instance is not None:
            message: str = "successfully fetched plan"
            return jsonify({'status': True, 'payload': plan_instance.to_dict(), 'message': message}), 200
        return jsonify({'status': False, 'message': 'Unable to get plan'}), 500


class AccessRightsView:
    def __init__(self):
        pass

    @use_context
    def get_access_rights(self, plan_id: str) -> typing.Union[None, AccessRights]:
        if isinstance(plan_id, str):
            try:
                access_rights_instance: AccessRights = AccessRights.query(AccessRights.plan_id == plan_id).get()
                if isinstance(access_rights_instance, AccessRights):
                    return access_rights_instance
                return None
            except ConnectionRefusedError:
                return None
            except RetryError:
                return None
            except Aborted:
                return None
        return None


class CouponsView(Validators):
    def __init__(self):
        super(CouponsView, self).__init__()

    @staticmethod
    def get_coupon_data(func):
        functools.wraps(func)

        def wrapper(*args, **kwargs):
            coupon_data: dict = kwargs.get('coupon_data')
            if "code" in coupon_data and coupon_data['code'] != "":
                code: str = coupon_data.get('code')
            else:
                return jsonify({'status': False, 'message': 'coupon code is required'}), 500

            if "discount" in coupon_data and coupon_data['discount'] != "":
                discount: int = int(coupon_data.get('discount'))
            else:
                return jsonify({'status': False, 'message': 'discount is required'}), 500

            if "expiration_time" in coupon_data and coupon_data['expiration_time'] != "":
                expiration_time: int = int(coupon_data['expiration_time'])
            else:
                return jsonify({'status': False, 'message': 'expiration_time is required'}), 500

            return func(code=code, discount=discount, expiration_time=expiration_time, *args)

        return wrapper

    @get_coupon_data
    @use_context
    def add_coupon(self, code: str, discount: int, expiration_time: int) -> tuple:
        try:
            if self.can_add_coupon(code=code, expiration_time=expiration_time).result():
                coupons_instance: Coupons = Coupons(code=code, discount=discount, expiration_time=expiration_time)
                key = coupons_instance.put(use_cache=True, retries=self._max_retries, timeout=self._max_timeout)
                if key is None:
                    message: str = "an error occured while creating coupon"
                    return jsonify({'status': False, 'message': message}), 500
            else:
                message: str = 'Unable to add coupon, please check expiration time or coupon code'
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

        return jsonify({'status': True, 'message': 'successfully created coupon code',
                        'payload': coupons_instance.to_dict()}), 200

    @get_coupon_data
    @use_context
    def update_coupon(self, code: str, discount: int, expiration_time: int) -> tuple:
        if self.can_update_coupon(code=code, expiration_time=expiration_time).result():
            try:
                coupon_instance: Coupons = Coupons.query(Coupons.code == code).get()
                coupon_instance.discount = discount
                coupon_instance.expiration_time = expiration_time
                key = coupon_instance.put(use_cache=True, retries=self._max_retries, timeout=self._max_timeout)
                if key is None:
                    message: str = "Error updating coupon"
                    return jsonify({'status': False, 'message': message}), 500

                return jsonify({'status': True, 'message': 'successfully updated coupon'}), 200

            except ConnectionRefusedError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except RetryError as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
            except Aborted as e:
                message: str = str(e)
                return jsonify({'status': False, 'message': message}), 500
        else:
            message: str = "Unable to update coupon code"
            return jsonify({'status': False, 'message': message}), 500

    @use_context
    def cancel_coupon(self, coupon_data: dict) -> tuple:
        if "code" in coupon_data and coupon_data['code'] != "":
            code : str = coupon_data['code']
        else:
            message: str = "Coupon Code is required"
            return jsonify({'status': False, 'message': message}), 500

        try:
            coupon_instace: Coupons = Coupons.query(Coupons.code == code).get()
            if isinstance(coupon_instace, Coupons):
                coupon_instace.is_valid = False
                key = coupon_instace.put(use_cache=True, retries=self._max_retries, timeout=self._max_timeout)
                if key is None:
                    message: str = "Unable to cancel coupon"
                    return jsonify({'status': False, 'message': message}), 500
                return jsonify({'status': True, 'message': 'successfully cancelled coupon code'}), 200

        except ConnectionRefusedError as e:
            message: str = str(e)
            return jsonify({'status': False, 'message': message}), 500
        except RetryError as e:
            message: str = str(e)
            return jsonify({'status': False, 'message': message}), 500
        except Aborted as e:
            message: str = str(e)
            return jsonify({'status': False, 'message': message}), 500

        return jsonify({'status': False, 'message': 'unable to cancel coupon code'}), 500

    @use_context
    def get_all_coupons(self) -> tuple:
        coupons_list: typing.List[Coupons] = Coupons.query().fetch()
        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @use_context
    def get_valid_coupons(self) -> tuple:
        coupons_list: typing.List[Coupons] = Coupons.query(Coupons.is_valid == True).fetch()
        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200

    @use_context
    def get_expired_coupons(self) -> tuple:
        coupons_list: typing.List[Coupons] = Coupons.query(Coupons.expiration_time < timestamp()).fetch()
        payload: typing.List[dict] = [coupon.to_dict() for coupon in coupons_list]
        message: str = "coupons successfully created"
        return jsonify({'status': True, 'payload': payload, 'message': message}), 200
