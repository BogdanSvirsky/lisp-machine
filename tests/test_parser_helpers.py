import io
import pytest
from lexer import Lexer
from parser import Parser, ParseException
from parser.ast import *


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def lexer():
    return Lexer()


def parse_source(source: str) -> ASTProgram:
    lexer = Lexer()
    tokens = lexer.tokenize(io.StringIO(source))
    parser = Parser()
    return parser.parse(tokens)
