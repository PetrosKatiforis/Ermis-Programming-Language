class AST:
    pass

class NOOP(AST):
    pass


class Program(AST):
    def __init__(self, data):
        self.data = data


class Compound(AST):
    def __init__(self, value = []):
        self.children = value


class Number(AST):
    def __init__(self, token):
        self.token = token
        self.value = int(token.value)


class Float(AST):
    def __init__(self, token):
        self.token = token
        self.value = float(token.value)


class Boolean(AST):
    def __init__(self, value):
        self.value = value


class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class BinaryOperation(AST):
    def __init__(self, left, token, right):
        self.token = token
        self.right = right
        self.left = left


class UnaryOperation(AST):
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression


class VariableDefinition(AST):
    def __init__(self, name, right):
        self.name = name
        self.right = right


class VariableAssignment(AST):
    def __init__(self, name, right):
        self.name = name
        self.right = right


class Variable(AST):
    def __init__(self, token):
        self.name = token.value


class FunctionCall(AST):
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters


class Function(AST):
    def __init__(self, name, parameters, block):
        self.name = name
        self.parameters = parameters
        self.block = block


class Return(AST):
    def __init__(self, right = NOOP()):
        self.right = right


class IfStatement(AST):
    def __init__(self, condition, block, else_block):
        self.condition = condition
        self.block = block
        self.else_block = else_block


class WhileStatement(AST):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

