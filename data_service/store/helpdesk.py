import typing
from google.cloud import ndb
from datetime import datetime
import re

class Setters:

    @staticmethod
    def set_int(prop, value: int) -> int:
        """
            set positive integer
        """
        if not (isinstance(value, int)):
            raise TypeError("{} can only be an integer".format(str(prop)))
        if value < 0:
            raise ValueError("{} can only be a positive integer".format(str(prop)))
        return value

    @staticmethod
    def set_email(prop, value: str) -> str:
        """
            TODO validate emailx
        """
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(regex, value):
            return value
        raise ValueError("Invalid email address")

    @staticmethod
    def set_cell(prop, value: str) -> str:
        """
            TODO validate cell
        """
        return value

    @staticmethod
    def set_bool(prop, value: bool) -> bool:
        if not (isinstance(value, bool)):
            raise TypeError("{} can only be a boolean".format(str(prop)))
        return value

    @staticmethod
    def set_str(prop, value: str) -> str:
        if not (isinstance(value, str)):
            raise TypeError("{} can only be a string".format(str(prop)))
        return value


setters_init: Setters = Setters()


class HelpDeskValid:
    pass


class HelpDesk(ndb.Model):
    total_tickets: int = ndb.IntegerProperty(default=0, validator=setters_init.set_int)
    total_tickets_opened: int = ndb.IntegerProperty(default=0, validator=setters_init.set_int)
    total_tickets_closed: int = ndb.IntegerProperty(default=0, validator=setters_init.set_int)

    def __str__(self) -> str:
        return "<HelpDesk total_tickets: {}, total_open : {}, total_closed: {}".format(str(self.total_tickets),
                                                                                       str(self.total_tickets_closed),
                                                                                       str(self.total_tickets_opened))

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.total_tickets != other.total_tickets:
            return False
        if self.total_tickets_opened != other.total_tickets_opened:
            return False
        if self.total_tickets_closed != other.total_tickets_closed:
            return False
        return True


class TicketValid:

    @staticmethod
    def is_topic_valid(topic: typing.Union[str, None]) -> bool:
        if not(isinstance(topic, str)) or (topic == ""):
            return False
        return True

    @staticmethod
    def is_subject_valid(subject: typing.Union[str, None]) -> bool:
        if not(isinstance(subject, str)) or (subject == ""):
            return False
        return True

    @staticmethod
    def is_message_valid(message: typing.Union[str, None]) -> bool:
        if not(isinstance(message, str)) or (message == ""):
            return False
        return True


class Ticket(ndb.Model):
    ticket_id: str = ndb.StringProperty(validator=setters_init.set_str)
    uid: str = ndb.StringProperty(validator=setters_init.set_str)
    topic: str = ndb.StringProperty(validator=setters_init.set_str)
    subject: str = ndb.StringProperty(validator=setters_init.set_str)
    message: str = ndb.StringProperty(validator=setters_init.set_str)
    email: str = ndb.StringProperty(validator=setters_init.set_email)
    cell: str = ndb.StringProperty(validator=setters_init.set_cell)
    assigned: bool = ndb.BooleanProperty(default=False)
    assigned_to_uid: str = ndb.StringProperty(validator=setters_init.set_str)
    response_sent: bool = ndb.BooleanProperty(default=False, validator=setters_init.set_bool)
    is_resolved: bool = ndb.BooleanProperty(default=False, validator=setters_init.set_bool)
    client_not_responding: bool = ndb.BooleanProperty(default=False, validator=setters_init.set_bool)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)
    time_updated: datetime = ndb.DateTimeProperty(auto_now=True)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.ticket_id != other.ticket_id:
            return False
        if self.uid != other.uid:
            return False
        if self.topic != other.topic:
            return False
        return True

    def __str__(self) -> str:
        return "<Ticket topic: {}, subject: {}, message: {}, email: {}, cell: {}, is_resolved: {}".format(
            self.topic, self.subject, self.message, self.email, self.cell, self.is_resolved)

    def __repr__(self) -> str:
        return self.__str__()


class TicketThreadValid:
    pass


class TicketThread(ndb.Model):
    """
        sort by ticket_id, then time_created , then mark by sent_by to create thread
    """
    ticket_id: str = ndb.StringProperty(validator=setters_init.set_str)
    thread_id: str = ndb.StringProperty(validator=setters_init.set_str)
    sent_by: str = ndb.StringProperty(validator=setters_init.set_str)  # Support Staff or Client
    subject: str = ndb.StringProperty(validator=setters_init.set_str)
    message: str = ndb.StringProperty(validator=setters_init.set_str)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)

    # noinspection DuplicatedCode
    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.ticket_id != other.ticket_id:
            return False
        if self.thread_id != other.thread_id:
            return False
        if self.sent_by != other.sent_by:
            return False
        if self.time_created != other.time_created:
            return False
        return True

    def __str__(self) -> str:
        return "<TicketThread Sent_by: {}, Subject: {}, Message {} Time_Created: {}".format(self.sent_by, self.subject,
                                                                                            self.message,
                                                                                            str(self.time_created))

    def __repr__(self) -> str:
        return self.__str__()
