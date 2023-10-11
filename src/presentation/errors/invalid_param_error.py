class InvalidParamError(Exception):
    def __init__(self, param_name: str):
        self.param_name = param_name
        super().__init__(f'Invalid Parameter: {param_name}')

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.param_name == other.param_name
