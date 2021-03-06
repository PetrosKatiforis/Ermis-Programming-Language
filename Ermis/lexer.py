from .exceptions import UnexpectedTokenError
from .config import tokens, keywords
from .token import TokenTypes, Token

class Lexer:
    def __init__(self, source):
        """
        Initalizing the Lexer object
        Saving the position and the current character
        """

        self.source = source
        self.pos = 0

        self.current_char = self.source[self.pos]

    def advance(self):
        """
        Advancing to the next character in the source string
        If it has reached the end, set current_char to None
        """

        self.pos += 1

        if self.has_reached_end():
            self.current_char = None

        else:
            self.current_char = self.source[self.pos]

    def peek(self, offset = 1):
        """
        Peeks on the next characters of the lexer source
        It's useful for tokens that are made of multiple characters
        """

        return self.source[min(self.pos + offset, len(self.source) - 1)]

    def skip_whitespace(self):
        while self.current_char \
                and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """
        Skips an ermis comment
        Comment are represented with a double 'greater than' character:

        >> This is a comment
        """

        if self.current_char == self.peek() == ">":
            while self.current_char != "\n":
                self.advance()

            self.skip_whitespace()
            self.skip_comment()

    def advance_token(self, token_type):
        """
        A utility function to quickly create tokens that require a single character for their values
        Before returning, it will also advance to the next character
        """

        value = self.current_char
        self.advance()

        return Token(token_type, value)

    def has_reached_end(self):
        """
        Determines whether the lexer
        has reached the end of the source file
        """

        return self.pos > len(self.source) - 1

    def collect_sequence(self, condition, token_type):
        """
        A utility function to capture sequences of characters
        It accepts a condition and the requested type of the resulting token
        """

        result = ""

        while self.current_char is not None and condition(self.current_char):
            result += self.current_char
            self.advance()

        return Token(token_type, result)

    def check_keyword(self, value):
        """
        Checks if an Identifier is a keyword and returns its type
        Otherwise, it will default to TokenTypes.Identifier
        """

        return keywords.get(value, TokenTypes.Identifier)

    def collect_string(self):
        self.advance()

        token = self.collect_sequence(
            lambda s: s != '"',
            TokenTypes.String
        )

        self.advance()

        return token

    def collect_identifier(self):
        """
        Collects an identifier token
        It will later check if it's a keyword
        """
        
        token = self.collect_sequence(
            lambda s: s.isalnum() or s == "_",
            TokenTypes.Identifier
        )

        token.type = self.check_keyword(token.value)

        return token

    def collect_number_value(self):
        """
        Collects the value of the current number token
        It's a utility function for self.collect_number
        """

        value = ""

        while self.current_char and self.current_char.isdigit():
            value += self.current_char
            self.advance()

        return value

    def collect_number(self):
        """
        Collects a number token
        It can either be an integer or a float
        """

        value = self.collect_number_value()

        if self.current_char == ".":
            value += self.current_char
            self.advance()

            value += self.collect_number_value()
            return Token(TokenTypes.Float, value)

        return Token(TokenTypes.Integer, value)

    def advance_double(self, token_type):
        """
        Returns a 2 characters long token
        and advances the lexer twice
        """
        
        token = Token(token_type, self.current_char + self.peek())

        self.advance()
        self.advance()

        return token

    def get_next_token(self):
        """
        Returns the next token of the lexer's state
        It skips whitespace and comments

        If it has reached the end, it will return an EOF token
        """

        self.skip_whitespace()
        self.skip_comment()

        if self.current_char is not None:
            if self.current_char.isdigit():
                return self.collect_number()

            if self.current_char == '"':
                return self.collect_string()

            if self.current_char.isalnum():
                return self.collect_identifier()

            match self.current_char + self.peek():
                case "==": return self.advance_double(TokenTypes.EqualsEquals)
                case "!=": return self.advance_double(TokenTypes.NotEquals)
                case ">=": return self.advance_double(TokenTypes.GreaterEqual)
                case "<=": return self.advance_double(TokenTypes.LessEqual)

            for character, token_type in tokens.items():
                if self.current_char == character:
                    return self.advance_token(token_type)

            raise UnexpectedTokenError(self.current_char)

        return Token(TokenTypes.EOF, "<EOF>")

