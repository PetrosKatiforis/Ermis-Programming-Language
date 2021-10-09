from .builtins import ermis_globals
from .token import TokenTypes
from .scope import LocalScope
from .utils import Visitor, when
from .exceptions import *
from .AST import *

class ErmisVisitor(Visitor):
    def __init__(self, parser):
        self.parser = parser
        self.current_scope = None

        super().__init__()

    def execute(self):
        """
        Executes the parser and creates a Program instance
        """

        data = self.parser.parse_compound()
        program = Program(data)

        return self.visit(program)


    @when(Program)
    def visit_program(self, node):
        """
        Visits the main program instance

        It will initialize the global scope
        and then visit the compound containing all of the source's code
        """

        global_scope = LocalScope(
            scope_name = "global",
            scope_level = 1,
            enclosing_scope = self.current_scope
        )

        self.current_scope = global_scope
        self.visit(node.data)


    @when(NOOP)
    def visit_no_operator(self, node):
        pass


    @when(Compound)
    def visit_compound(self, node):
        """
        Visits a compound statements

        It maps its children with the Visitor.visit function
        """

        for child in node.children:
            self.visit(child)


    @when(Number, Float, String)
    def visit_string(self, node):
        return node.value


    @when(Boolean)
    def visit_boolean(self, node):
        return node.value == "Αληθές"


    @when(Function)
    def visit_function(self, node):
        self.current_scope.insert(node.name, node)


    @when(Return)
    def visit_return(self, node):
        """
        Raises a FoundReturn 'Error'

        It's a quick way to notify the function call whenever a return statement is found,
        which will stop the executing of the next lines inside the function
        """

        raise FoundReturn(self.visit(node.right))


    @when(VariableDefinition)
    def visit_variable_definition(self, node):
        """
        Visits a variable definition

        It will insert the variable to the current scope
        The variable's value will be visitted as an expression
        """

        self.current_scope.insert(node.name, self.visit(node.right))


    @when(VariableAssignment)
    def visit_variable_assignment(self, node):
        variable = self.current_scope.find(node.name)
        new_value = self.visit(node.right)

        if variable is None:
            raise UndefinedVariableError(node.name)

        if type(variable) != type(new_value):
            raise WrongTypeError(node.name)

        self.current_scope.insert(node.name, new_value)


    @when(Variable)
    def visit_variable(self, node):
        """
        Visits an individual variable
        and returns its value from the current scope
        """

        return self.current_scope.find(node.name)


    @when(IfStatement)
    def visit_if_statement(self, node):
        condition = self.visit(node.condition)

        if (condition):
            self.visit(node.block)

        elif node.else_block is not None:
            self.visit(node.else_block)


    @when(WhileStatement)
    def visit_while_statement(self, node):

        while (self.visit(node.condition)):
            self.visit(node.block)


    @when(FunctionCall)
    def visit_function_call(self, node):
        """
        Visits a function call

        It will visit each parameter and then process the call
        Before executing, it will first check if it's a builtin method
        """

        parameters = list(map(self.visit, node.parameters))

        # Searching for a builtin method
        builtin = ermis_globals.get(node.name)

        if builtin is not None:
            return builtin(*parameters)

        # Creating the function's scope
        function = self.current_scope.find(node.name)

        function_scope = LocalScope(
            scope_name = node.name,
            scope_level = self.current_scope.scope_level + 1,
            enclosing_scope = self.current_scope
        )

        if len(function.parameters) != len(node.parameters):
            raise MissingFunctionParameter(function.name)

        for argument, param in zip(parameters, function.parameters):
            function_scope.insert(param.name, argument)

        self.current_scope = function_scope
        return_value = None

        try:
            self.visit(function.block)

        except FoundReturn as return_block:
            return_value = return_block.value

        # Resetting the current_scope
        self.current_scope = self.current_scope.enclosing_scope

        return return_value


    @when(BinaryOperation)
    def visit_binary_operation(self, node):
        """
        Visits an ermis binary operation

        Depending on the current_token's type,
        it will execute the correct operation between two expressions
        """

        left = self.visit(node.left)
        right = self.visit(node.right)

        match node.token.type:
            case TokenTypes.Plus:         return left + right
            case TokenTypes.Minus:        return left - right
            case TokenTypes.Multiply:     return left * right
            case TokenTypes.Divide:       return left / right
            case TokenTypes.GreaterThan:  return left > right
            case TokenTypes.GreaterEqual: return left >= right
            case TokenTypes.LessThan:     return left < right
            case TokenTypes.LessEqual:    return left <= right
            case TokenTypes.NotEquals:    return left != right
            case TokenTypes.And:          return left and right
            case TokenTypes.Or:           return left or right


    @when(UnaryOperation)
    def visit_unary(self, node):
        operator = node.token.type

        if operator == TokenTypes.Plus:
            return +self.visit(node.expression)

        else:
            return -self.visit(node.expression)


