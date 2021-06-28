from google.cloud import ndb
from data_service.config.stocks import currency_symbols
import re


class Setters:
    def __init__(self):
        pass

    @staticmethod
    def set_amount(prop, value) -> int:
        if not (isinstance(value, int)):
            raise TypeError("{} can only be integer".format(str(prop)))
        return value

    @staticmethod
    def set_currency(prop, value) -> str:
        if not (isinstance(value, str)):
            raise TypeError("{} can only be string".format(prop))
        if value not in currency_symbols():
            raise ValueError("{} not a valid currency symbol".format(str(prop)))
        return value

    @staticmethod
    def set_email(prop, value) -> str:
        """
            TODO validate email here
        """
        regex = '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
        if re.search(regex, value) is not None:
            return value
        raise ValueError("{} invalid email address".format(str(prop)))

    @staticmethod
    def set_password(prop, value) -> str:
        """
            TODO validate password here
        """
        return value


setters: Setters = Setters()


class AmountMixin(ndb.Model):
    amount: int = ndb.IntegerProperty(default=0, validator=setters.set_amount)
    currency: str = ndb.StringProperty(validator=setters.set_currency)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.amount != other.amount:
            return False
        if self.currency != other.currency:
            return False
        return True

    def __str__(self) -> str:
        return "Amount: {} {}".format(self.currency, self.amount)

    def __repr__(self) -> str:
        return self.__str__()


class UserMixin(ndb.Model):
    email: str = ndb.StringProperty(validator=setters.set_email)
    password: str = ndb.StringProperty(validator=setters.set_password)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.email != other.email:
            return False
        if self.password != other.password:
            return False
        return True

    def __str__(self) -> str:
        return "<User {}".format(self.email)

    def __repr__(self) -> str:
        return self.__str__()


# TODO add validators for address
class AddressMixin(ndb.Model):
    line_1: str = ndb.StringProperty()
    city: str = ndb.StringProperty()
    zip_code: str = ndb.StringProperty()
    province: str = ndb.StringProperty()
    country: str = ndb.StringProperty()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.line_1 != other.line_1:
            return False
        if self.city != other.city:
            return False
        if self.zip_code != other.zip_code:
            return False
        if self.province != other.province:
            return False
        return True

    def __str__(self) -> str:
        return "<Address : {} {} {} {}".format(self.line_1, self.city, self.zip_code,
                                               self.province)

    def __repr__(self) -> str:
        return self.__str__()
