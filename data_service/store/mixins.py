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
