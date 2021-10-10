from .exceptions import (
    UndefinedVariableError, 
    AlreadyDefinedError
)

class LocalScope:
    """
    A class dedicated to storing variables
    It is used for both global and local scopes
    """

    def __init__(self, scope_name, enclosing_scope = None):
        self.data = enclosing_scope.data if enclosing_scope is not None else {}

        self.scope_name = scope_name
        self.enclosing_scope = enclosing_scope

    def insert(self, name, value):
        if name in self.data:
            raise AlreadyDefinedError(name)

        self.data[name] = value

    def find(self, name):
        """
        Fetches a variable from the store
        If the function fails to find it, it will error out
        """

        value = self.data.get(name)

        if value is None:
            raise UndefinedVariableError(name)

        return value

    def __str__(self):
        return f"Variables: {self.data}"


