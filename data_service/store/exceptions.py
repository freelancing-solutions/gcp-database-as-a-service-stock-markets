from werkzeug.exceptions import HTTPException

class DataServiceError(HTTPException):
    """
        use this error to throw a custom error explaining something is wrong with the datastore
    """
    code: int = 512
    description: str = 'We have a problem connection to our Database'

    def __init__(self, description: str):
        self.description = description
        super(DataServiceError, self).__init__()

class InputError(HTTPException):
    code: int = 513
    description: str = "Unable to process input"

    def __init__(self, description: str):
        self.description = description
        super(InputError, self).__init__()
