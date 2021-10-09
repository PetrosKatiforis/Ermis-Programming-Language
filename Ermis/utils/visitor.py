class Visitor:
    def __init__(self):
        self.handlers = {}

        for function in dir(self):
            if function.startswith("visit_"):
                getattr(self, function)()

    def visit(self, node):
        type_name = type(node).__name__

        return self.handlers[type_name](self, node)

def when(*parameters):
    """
    A utility decorator for the visitor class

    It saves the decorated function into the visitor's handlers,
    which will then fire when it encounter a node of type ast_type
    """

    def decorator(function):
        def wrapper(self, **kwargs):
            for ast_type in parameters:
                type_name = ast_type.__name__

                self.handlers[type_name] = function

        return wrapper

    return decorator
