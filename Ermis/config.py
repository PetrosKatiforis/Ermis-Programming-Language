from .token import TokenTypes
from .builtins import *

tokens = {
    "=": TokenTypes.Equals,
    "(": TokenTypes.LeftParen,
    ")": TokenTypes.RightParen,
    "+": TokenTypes.Plus,
    "-": TokenTypes.Minus,
    "*": TokenTypes.Multiply,
    "/": TokenTypes.Divide,
    ";": TokenTypes.Semicolon,
    ",": TokenTypes.Comma,
    ">": TokenTypes.GreaterThan,
    "<": TokenTypes.LessThan,
    "{": TokenTypes.LeftCurly,
    "}": TokenTypes.RightCurly
}

keywords = {
    "έστω": TokenTypes.Let,
    "συνάρτηση": TokenTypes.Function,
    "επέστρεψε": TokenTypes.Return,
    "Αληθές": TokenTypes.Bool,
    "Ψευδές": TokenTypes.Bool,
    "εάν": TokenTypes.If,
    "αλλιώς": TokenTypes.Else,
    "όσο": TokenTypes.While,
    "και": TokenTypes.And,
    "ή": TokenTypes.Or
}

builtin_functions  = {
    "εμφάνισε": ermis_print,
    "διάβασε": ermis_input,
    "περίμενα": ermis_wait,
    "ρίζα": ermis_sqrt
}
