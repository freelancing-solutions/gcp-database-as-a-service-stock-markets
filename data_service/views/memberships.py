import typing
from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError
from flask import current_app, jsonify
from datetime import datetime
from data_service.store.memberships import Memberships, MembershipPlans, AccessRights
from data_service.store.memberships import PlanValidators as PlanValid
from data_service.store.users import UserValidators as UserValid
from data_service.store.memberships import MembershipValidators as MemberValid
from data_service.utils.utils import create_id


class Validators(UserValid, PlanValid, MemberValid):
    def __init__(self):
        pass

    def can_add_member(self, uid: str, plan_id: str, start_date: datetime) -> bool:
        user_valid: bool = self.is_user_valid(uid=uid)
        plan_exist: bool = self.plan_exist(plan_id=plan_id)
        date_valid: bool = self.start_date_valid(start_date=start_date)
        return user_valid and plan_exist and date_valid


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
                    key = membership_instance.put()
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
        self._create_or_update_membership(uid=uid, plan_id=plan_id, plan_start_date=plan_start_date)

    def update_membership(self, uid: str, plan_id: str, plan_start_date: datetime) -> tuple:
        self._create_or_update_membership(uid=uid, plan_id=plan_id, plan_start_date=plan_start_date)

    def set_membership_status(self, uid: str, status: str) -> tuple:
        with self.client.context():
            membership_list: typing.List[Memberships] = Memberships.query(Memberships.uid == uid).fetch()
            if isinstance(membership_list, list) and len(membership_list) > 0:
                membership_instance: Memberships = membership_list[0]
                try:
                    membership_instance.status = status
                    key = membership_instance.put()
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
                            key = membership_instance.put(use_cache=True, retries=5)
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
            if isinstance(response_data,list) and len(response_data):
                return jsonify({'status': True, 'payload': response_data[0], 'message': 'successfully fetched members'}), 200
            else:
                return jsonify({'status': False, 'message': 'user does not have any membership plan'}), 500


    def payment_amount(self, uid: str) -> tuple:
        """
            for a specific user return payment amount
        """
        pass

    def set_payment_status(self, uid: str, status: bool) -> tuple:
        """
            for a specific user set payment status
        """
        pass




class MembershipPlansView:
    def __init__(self):
        pass

    def add_plan(self, membership_name: str, description: str, schedule_day: int, schedule_term: str) -> tuple:
        pass

    def update_plan(self, plan_id, membership_name: str, description: str, schedule_day: int, schedule_term: str) -> tuple:
        pass

    def set_plan_status(self, plan_id: str, status: bool) -> tuple:
        pass

    def return_monthly_plans(self) -> tuple:
        pass
    
    def return_quarterly_plan(self) -> tuple:
        pass

    def return_annual_plans(self) -> tuple:
        pass


class AccessRightsView:
    def __init__(self):
        pass


