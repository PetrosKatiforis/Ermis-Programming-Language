from .exceptions import WrongTokenError
from .token import TokenTypes
from .AST import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.current_token = self.lexer.get_next_token()
        self.previous_token = self.current_token

    def eat(self, token_type):
        """
        Advances the parser

        The eat function accepts a TokenType, which is later 'eaten' by the parser which moves to next token
        If the TokenType is different than what was expected, it will throw an exception
        """

        if self.current_token.type == token_type:
            # Advancing the previous token as well
            self.previous_token = self.current_token

            self.current_token = self.lexer.get_next_token()

        else:
            raise WrongTokenError(self.current_token, token_type)

    def parse_compound(self):
        """
        Creates the base compound

        A compound is the entry point of an ermis file.
        It contains a list of all the program's statements
        """

        results = [self.parse_statement()]

        while self.current_token.type != TokenTypes.EOF:
            if self.previous_token.type != TokenTypes.RightCurly:
                self.eat(TokenTypes.Semicolon)

            results.append(self.parse_statement())

        return Compound(results)

    def parse_statement(self):
        """
        Parses whatever can be found in the first token of a new line
        It will default to returning a NOOP instance
        """

        match self.current_token.type:
            case TokenTypes.Let:        return self.parse_definition()
            case TokenTypes.Identifier: return self.parse_variable()
            case TokenTypes.Function:   return self.parse_function()
            case TokenTypes.Return:     return self.parse_return()
            case TokenTypes.If:         return self.parse_if_statement()
            case TokenTypes.While:      return self.parse_while_statement()

        return NOOP()

    def parse_while_statement(self):
        """
        Returns a parsed while statement, containing a condition and a code block
        """

        self.eat(TokenTypes.While)

        self.eat(TokenTypes.LeftParen)

        condition = self.expression()

        self.eat(TokenTypes.RightParen)

        block = self.parse_block()

        return WhileStatement(condition, block)

    def parse_block(self):
        """
        Returns a compound instance
        by parsing a block of code inside curly brackets

        It's a utility function for other AST types, such as if statements and functions
        """

        self.eat(TokenTypes.LeftCurly)

        block = [self.parse_statement()]

        while self.current_token.type != TokenTypes.RightCurly:

            if self.previous_token.type != TokenTypes.RightCurly:
                self.eat(TokenTypes.Semicolon)

            block.append(self.parse_statement())

        self.eat(TokenTypes.RightCurly)

        return Compound(block)

    def parse_if_statement(self):
        """
        Parses an if statement, including it's false case
        It's recursive when the else case contains a condition
        Example:

        εάν (...) {}
        αλλιώς εάν (...) {}
        αλλιώς {}
        """

        self.eat(TokenTypes.If)
        self.eat(TokenTypes.LeftParen)

        condition = self.expression()

        self.eat(TokenTypes.RightParen)

        if_block = self.parse_block()

        else_block = None

        if self.current_token.type == TokenTypes.Else:
            self.eat(TokenTypes.Else)

            if self.current_token.type == TokenTypes.If:
                else_block = self.parse_if_statement()

            else:
                else_block = self.parse_block()

        return IfStatement(condition, if_block, else_block)

    def parse_function(self):
        """
        Parses an Ermis function declaration
        Simple example (including a return statement):

        συνάρτηση πες_γεια () {
            εμφάνισε ("Γειά!");

            επέστρεψε "Λειτουργεί";
        }
        """

        self.eat(TokenTypes.Function)

        name = self.current_token.value
        self.eat(TokenTypes.Identifier)

        parameters = self.collect_parameters()

        block = self.parse_block()

        return Function(name, parameters, block)

    def parse_return(self):
        """
        Parses a return statement
        Its value is seen as an expression
        """

        self.eat(TokenTypes.Return)
        value = self.expression()

        return Return(value)

    def collect_parameters(self):
        """
        Collects the parameters of a function.
        It expects a list of experssions, seperated by a comma

        Example: (a + 10, b)
        """

        self.eat(TokenTypes.LeftParen)

        parameters = []

        if self.current_token.type != TokenTypes.RightParen:
            parameters.append(self.expression())

            while self.current_token.type == TokenTypes.Comma:
                self.eat(TokenTypes.Comma)
                parameters.append(self.expression())

        self.eat(TokenTypes.RightParen)

        return parameters

    def parse_function_call(self):
        """
        Parses a function call
        Arguments are treated as indivdual expressions and they are seperated by a comma
        """

        name = self.previous_token.value
        parameters = self.collect_parameters()

        return FunctionCall(name, parameters)

    def parse_definition(self):
        """
        Parses a variable definition
        Example:

        έστω αριθμός = 5;
        """

        self.eat(TokenTypes.Let)
        name = self.current_token.value

        self.eat(TokenTypes.Identifier)
        self.eat(TokenTypes.Equals)

        right = self.expression()

        return VariableDefinition(name, right)

    def parse_variable(self):
        """
        Parses a single variable

        Depending on the next token, it may also return a function call
        or a variable change statement
        """

        token = self.current_token
        self.eat(TokenTypes.Identifier)

        if self.current_token.type == TokenTypes.Equals:
            return self.parse_variable_change()

        # If there's a left parenthesis, it has to be a function call
        if self.current_token.type == TokenTypes.LeftParen:
            return self.parse_function_call()

        return Variable(token)

    def parse_variable_change(self):
        """
        Parses a variable change statement
        Example:

        αριθμός = αριθμός + 1;
        """

        name = self.previous_token.value
        self.eat(TokenTypes.Equals)

        value = self.expression()

        return VariableAssignment(name, value)

    def factor(self):
        """
        Parses an expression factor

        A factor can be a variable, a value, a unary operator
        or a parenthesised expression
        """

        if self.current_token.type == TokenTypes.Identifier:
            return self.parse_variable()

        self.eat(self.current_token.type)
        token = self.previous_token

        match token.type:
            case TokenTypes.Plus | TokenTypes.Minus:
                return UnaryOperation(token, self.factor())

            case TokenTypes.LeftParen:
                node = self.expression()

                self.eat(TokenTypes.RightParen)
                return node

            case TokenTypes.Integer: return Number(token)
            case TokenTypes.Float:   return Float(token)
            case TokenTypes.Bool:    return Boolean(token)
            case TokenTypes.String:  return String(token)

    def term(self):
        """
        Parses a term

        A term is a combination of factors,
        connected by a higher order operation such as division or multiplication
        """

        node = self.factor()

        while self.current_token.type in \
                (TokenTypes.Multiply, TokenTypes.Divide):

            token = self.current_token
            self.eat(token.type)

            node = BinaryOperation(
                left=node,
                token=token,
                right=self.factor()
            )

        return node

    def expression(self):
        """
        Parses an ermis expression
        An expression is a combination of terms, connected by addition or substraction
        """

        node = self.term()

        while 15 <= self.current_token.type.value < 25:
            token = self.current_token
            self.eat(token.type)

            node = BinaryOperation(
                left=node,
                token=token,
                right=self.term()
            )

        return node


