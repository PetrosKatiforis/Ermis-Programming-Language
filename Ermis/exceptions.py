from .utils import red

class ErmisError(Exception):
    def __init__(self, message):

        print(f"""{red("Σφάλμα! Κάτι πήγε στραβά...")} \n{message}""")
        exit()


class WrongTokenError(ErmisError):
    """
    Custom exceptions for token predictions
    It's used inside the parser's eat function
    """

    def __init__(self, current_token, expected_type):
        super().__init__(
            f"Περίμενα σύμβολο τύπου {expected_type}, αλλά πήρα {current_token.type}"
        )


class UnexpectedTokenError(ErmisError):
    """
    A special exception to get triggered
    when the lexer encounters an unrecognized token
    """

    def __init__(self, character):
        super().__init__(f"Άκειρο σύμβολο <<{character}>>")


class WrongTypeError(ErmisError):
    """
    Fires when modifying a variable's type
    without using type conversion first
    """

    def __init__(self, name):
        super().__init__(
            f"Δεν μπορώ να αλλάξω τον τύπο της μεταβλητής <<{name}>>!"
        )


class UndefinedVariableError(ErmisError):
    """
    A custom error which fires when the visior
    meets an unrecongized variable (Can't find it inside the score)
    """

    def __init__(self, name):
        super().__init__(f"Άγνωστη μεταβλητή με όνομα <<{name}>>")


class MissingFunctionParameter(ErmisError):
    def __init__(self, name):
        super().__init__(
            f"Το κάλεσμα της συνάρτησης {name} δεν έχει τις απαρέτητες παραμέτρους..."
        )


class FoundReturn(Exception):
    """
    An 'error' that fires whenever a function visitor finds a return block
    It works mostly as a simple workaround for an event emitter
    """
    
    def __init__(self, value):
        self.value = value

        super().__init__()
