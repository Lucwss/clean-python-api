class ServerError(Exception):
    def __init__(self, message='Internal Server Error'):
        super().__init__(message)

    def __eq__(self, other):
        return self.__class__ == other.__class__