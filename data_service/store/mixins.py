from google.cloud import ndb


class AmountMixin(ndb.Model):
    amount: int = ndb.IntegerProperty(default=0)
    currency: str = ndb.StringProperty()

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.amount != other.amount:
            return False
        if self.currency != other.currency:
            return False
        return True

    def __str__(self) -> str:
        return "{} {}".format(self.currency, self.amount)

    def __repr__(self) -> str:
        return self.__str__()


class UserMixin(ndb.Model):
    email: str = ndb.StringProperty()
    password: str = ndb.StringProperty()

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


class AddressMixin(ndb.Model):
    line_1: str = ndb.StringProperty()
    city: str = ndb.StringProperty()
    zip_code: str = ndb.StringProperty()
    province: str = ndb.StringProperty()

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
        return "<Address : {} {} {} {}".format(self.line_1, self.city, self.zip_code, self.province)

    def __repr__(self) -> str:
        return self.__str__()
