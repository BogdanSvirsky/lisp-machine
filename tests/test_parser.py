from lexer.tokens import *
from parser import Parser
from parser.ast import *


def test_basics():
    parser = Parser()
    root = ASTCall('+')
    root.children.extend([ASTLiteral(2), ASTLiteral(2)])
    assert parser.parse([LParen(), Symbol('+'), Number(1), Number(2), RParen()]) == [root]
