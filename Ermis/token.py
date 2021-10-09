from enum import Enum

class TokenTypes(Enum):
    Let          = 0
    Identifier   = 1
    Integer      = 2
    String       = 3
    Bool         = 4
    Equals       = 5
    LeftParen    = 6
    RightParen   = 7
    Comma        = 8
    Function     = 9
    Return       = 10

    GreaterThan  = 15
    GreaterEqual = 16
    LessThan     = 17
    LessEqual    = 18
    EqualsEquals = 19
    NotEquals    = 20
    And          = 21
    Or           = 22
    Plus         = 23
    Minus        = 24

    Multiply     = 25
    Divide       = 26
    If           = 37
    Else         = 28
    Semicolon    = 29
    LeftCurly    = 30
    RightCurly   = 31
    While        = 32
    EOF          = 33

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        """
        String representation of a string
        It servers as a debugging utility
        """

        return f"Token({self.type}, {self.value})"


