import typing
from werkzeug.exceptions import HTTPException


class DataServiceError(HTTPException):
    """
        use this error to throw a custom error explaining something is wrong with the datastore
    """
    code: int = 512
    description: str = 'We have a problem connection to the Database'

    def __init__(self, status: typing.Union[int, None], description: typing.Union[str, None] = None):
        if description is not None:
            self.description = description
        if status is not None:
            self.code = status

        super(DataServiceError, self).__init__()

    def __str__(self) -> str:
        return "<DataServiceError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class InputError(Exception):
    code: int = 513
    description: str = "Unable to process input"

    def __init__(self, status: typing.Union[int, None] = None, description: typing.Union[None, str] = None):
        if description is not None:
            self.description = description
        if status is not None:
            self.code = status
        super(InputError, self).__init__()

    def __str__(self) -> str:
        return "<InputError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class UnAuthenticatedError(HTTPException):
    code: int = 401
    description: str = "You are not authorized to use this resource"

    def __init__(self, status: typing.Union[int, None] = None, description: typing.Union[None, str] = None):
        if description is not None:
            self.description = description
        if status is not None:
            self.code = status

        super(UnAuthenticatedError, self).__init__()

    def __str__(self) -> str:
        return "<UnAuthenticated {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class RequestError(HTTPException):
    code: int = 404
    description: str = "Request unsuccessful"

    def __init__(self, status: typing.Union[int, None] = None,
                 description: typing.Union[str, None] = None,
                 url: typing.Union[str, None] = None):
        if description is not None:
            self.description = description
        if url is not None:
            self.description = "{} on url: {}".format(description, url)
        if status is not None:
            self.code = status

        super(RequestError, self).__init__()

    def __str__(self) -> str:
        return "<RequestError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


# Errors

class RemoteDataError(IOError):
    """
        Remote data exception
    """
    code: int = 406
    description: str = 'Error connecting to remote server'

    def __init__(self, status: typing.Union[int, None] = 406,
                 description: typing.Union[str, None] = None, url: str = None):
        if description is not None:
            self.description = "{} {}".format(description, url)
            self.code = status
        super(RemoteDataError, self).__init__()

    def __str__(self) -> str:
        return "<RemoteDataError {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()


class EnvironNotSet(Exception):
    """
        raised when environment variables are not set
    """
    code: int = 506
    description: str = "environment variables not set please inform admin"

    def __init__(self, status: typing.Union[int, None] = 406,
                 description: typing.Union[str, None] = None, url: str = None):
        if description is not None:
            self.description = "{} {}".format(description, url)
            self.code = status
        super(EnvironNotSet, self).__init__()

    def __str__(self) -> str:
        return "<EnvironNotSet {} Code: {}".format(self.description, str(self.code))

    def __repr__(self) -> str:
        return self.__str__()

