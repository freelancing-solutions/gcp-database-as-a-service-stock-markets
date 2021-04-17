import typing
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError
from flask import current_app, jsonify
from datetime import datetime
from data_service.store.memberships import MembershipPlans, AccessRights, Memberships
from data_service.store.memberships import PlanValidators as PlanValid
from data_service.store.users import UserValidators as UserValid
from data_service.store.memberships import MembershipValidators as MemberValid
from data_service.utils.utils import create_id


class Validators(UserValid, PlanValid, MemberValid):
    def __init__(self):
        self.max_put_retries = 10

    def can_add_member(self, uid: str, plan_id: str, start_date: datetime) -> bool:
        user_valid: bool = self.is_user_valid(uid=uid)
        plan_exist: bool = self.plan_exist(plan_id=plan_id)
        date_valid: bool = self.start_date_valid(start_date=start_date)
        return user_valid and plan_exist and date_valid

    def can_add_plan(self, plan_name: str) -> bool:
        return not self.plan_name_exist(plan_name=plan_name)

    def can_update_plan(self, plan_id: str, plan_name: str) -> bool:
        return self.plan_exist(plan_id=plan_id) and not self.plan_name_exist(plan_name=plan_name)

class MembershipsView(Validators):
    def __init__(self):
        super(MembershipsView, self).__init__()
        self.client = ndb.Client(namespace="main", project=current_app.config.get('PROJECT'))

    def _create_or_update_membership(self, uid: str, plan_id: str, plan_start_date: datetime) -> tuple:
        with self.client.context():
            if self.can_add_member(uid=uid, plan_id=plan_id, start_date=plan_start_date) is True:
                try:
                    member_ships_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
                    if isinstance(member_ships_list, list) and len(member_ships_list) > 0:
                        membership_instance: Memberships = member_ships_list[0]
                    else:
                        membership_instance: Memberships = Memberships()

                    membership_instance.uid = uid
                    membership_instance.plan_id = create_id()
                    membership_instance.status = 'Unpaid'
                    membership_instance.date_created = datetime.now()
                    membership_instance.plan_start_date = plan_start_date
                    key = membership_instance.put(use_cache=True, retries=self.max_put_retries)
                    if key is None:
                        return jsonify({'status': False, 'message': 'for some reason we where unable to create '}), 500
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

                return jsonify({'status': True, 'message': 'successfully updated membership',
                                'payload': membership_instance.to_dict()}), 200

    def add_membership(self, uid: str, plan_id: str, plan_start_date: datetime) -> tuple:
        return self._create_or_update_membership(uid=uid, plan_id=plan_id, plan_start_date=plan_start_date)

    def update_membership(self, uid: str, plan_id: str, plan_start_date: datetime) -> tuple:
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
                        message: str = 'For some reason we where unable to update the membership status'
                        return jsonify({'status': False, 'message': message}), 500
                except ValueError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except BadRequestError as e:
                    message: str = str(e)
                    return jsonify({'status': False, 'message': message}), 500
                except BadQueryError as e:
                    message: str = str(e)
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
                            if key is None:
                                message: str = "for some reason we are unable to change the membership"
                                return jsonify({'status': False, 'message': message}), 200
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

            return jsonify({'status': True, 'message': 'successfully updated membership',
                            'payload': membership_instance.to_dict()}), 200

    def send_welcome_email(self, uid: str, plan_id: str) -> tuple:
        """
            just send a request to the email service to send emails
        """
        with self.client.context():
            pass

    def return_plan_members_by_payment_status(self, plan_id: str, status: bool) -> tuple:
        """
            for members of this plan_id return members by payment_status
        """
        with self.client.context():
            membership_list: typing.List[Memberships] = Memberships.query(
                Memberships.plan_id == plan_id, Memberships.status == status).fetch()
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            return jsonify({'status': True, 'payload': response_data, 'message': 'successfully fetched members'}), 200

    def return_plan_members(self, plan_id) -> tuple:
        """
            return all members of a plan
        """
        with self.client.context():
            membership_list: typing.List[Memberships] = Memberships.query(Memberships.plan_id == plan_id).fetch()
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            return jsonify({'status': True, 'payload': response_data, 'message': 'successfully fetched members'}), 200

    def is_member_off(self, uid: str) -> tuple:
        """
            returns user membership details
        """
        with self.client.context():
            membership_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
            response_data: typing.List[dict] = [member.to_dict() for member in membership_list]
            if isinstance(response_data, list) and len(response_data):
                return jsonify(
                    {'status': True, 'payload': response_data[0], 'message': 'successfully fetched members'}), 200
            else:
                return jsonify({'status': False, 'message': 'user does not have any membership plan'}), 500

    def payment_amount(self, uid: str) -> tuple:
        """
            for a specific user return payment amount
        """
        with self.client.context():
            membership_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
            if isinstance(membership_list, list) and len(membership_list) > 0:
                membership_instance: Memberships = membership_list[0]
                plan_id = membership_instance.plan_id
                membership_plan_instance: MembershipPlans = MembershipPlansView().get_plan(plan_id=plan_id)
                if membership_plan_instance is None:
                    return jsonify({'status': False, 'message': 'could not find plan associate with the plan_id'}), 500
                amount_data: dict = {
                    'term_payment_amount': membership_plan_instance.term_payment_amount,
                    'registration_amount': membership_plan_instance.registration_amount}
                message: str = 'successfully returned payment details'
                return jsonify({'status': True, 'payload': amount_data, 'message': message}), 200

            message: str = 'unable to locate membership details'
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
                                                                     description=description, total_members=total_members,
                                                                     schedule_day=schedule_day, schedule_term=schedule_term,
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

            return jsonify({'status': True, 'message': 'successfully created new membership plan',
                            'payload': membership_plans_instance.to_dict()}), 200

    def set_plan_status(self, plan_id: str, status: bool) -> tuple:
        pass

    def return_monthly_plans(self) -> tuple:
        pass

    def return_quarterly_plan(self) -> tuple:
        pass

    def return_annual_plans(self) -> tuple:
        pass

    def get_plan(self, plan_id: str) -> typing.Union[None, MembershipPlans]:
        """
            this utility will be used by other views to obtain information about membershipPlans
        """
        with self.client.context():
            if isinstance(plan_id, str):
                membership_plans_list: typing.List[MembershipPlans] = MembershipPlans.query(
                    MembershipPlans.plan_id == plan_id).fetch()
                if isinstance(membership_plans_list, list) and len(membership_plans_list) > 0:
                    membership_instance: MembershipPlans = membership_plans_list[0]
                    return membership_instance
                else:
                    return None
            return None


class AccessRightsView:
    def __init__(self):
        self.client = ndb.Client(namespace="main", project=current_app.config.get('PROJECT'))

    def get_access_rights(self, plan_id: str) -> typing.Union[None, AccessRights]:
        with self.client.context():
            if isinstance(plan_id, str):
                access_rights_list: typing.List[AccessRights] = AccessRights.query(AccessRights.plan_id == plan_id)
                if isinstance(access_rights_list, list) and len(access_rights_list) > 0:
                    access_rights_instance: AccessRights = access_rights_list[0]
                    return access_rights_instance
                return None
            return None
