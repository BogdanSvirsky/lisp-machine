import pytest
from lexer.tokens import *
from parser import Parser
from parser.ast import ASTNode


@pytest.mark.parametrize(
        ('tokens', 'roots'), 
        (
            (
                [LParen(), Symbol('+'), Number(1), Number(2), RParen()],
                []
            )
        )
def test_basics(tokens: list[Token], roots: list[ASTNode]):
    parser = Parser() 
    assert parser.parse(tokens) == roots
