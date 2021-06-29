import typing
from werkzeug.exceptions import HTTPException


class DataServiceError(HTTPException):
    """
        use this error to throw a custom error explaining something is wrong with the datastore
    """
    code: int = 512
    description: str = 'We have a problem connection to the Database'

    def __init__(self, description: typing.Union[str, None] = None):
        if description is not None:
            self.description = description
        super(DataServiceError, self).__init__()

    def __str__(self) -> str:
        return "<DataServiceError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class InputError(HTTPException):
    code: int = 513
    description: str = "Unable to process input"

    def __init__(self, description: typing.Union[None, str] = None):
        if description is not None:
            self.description = description
        super(InputError, self).__init__()

    def __str__(self) -> str:
        return "<InputError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class UnAuthenticatedError(HTTPException):
    code: int = 401
    description: str = "You are not authorized to use this resource"

    def __init__(self, description: typing.Union[None, str] = None):
        if description is not None:
            self.description = description
        super(UnAuthenticatedError, self).__init__()

    def __str__(self) -> str:
        return "<UnAuthenticated {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()
