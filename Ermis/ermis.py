from .lexer import Lexer
from .parser import Parser
from .visitor import ErmisVisitor
from .utils import clear_console

class Ermis:
    def __init__(self, source):
        self.lexer = Lexer(source)
        self.parser = Parser(self.lexer)
        self.visitor = ErmisVisitor(self.parser)

    @classmethod
    def from_filename(cls, filename):
        """
        Alternative class constructor
        Initializing an Ermis interpreter from a filename
        """

        with open(filename, "r") as f:
            source = "\n".join(f.readlines())

            return cls(source)

    def execute(self):
        clear_console()

        self.visitor.execute()


