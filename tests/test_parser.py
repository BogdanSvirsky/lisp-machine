from lexer.tokens import *
from parser import Parser, ParseException
from parser.ast import *
import pytest


testdata = [
    ([LParen(), Symbol('+'), Number(1), Number(2), RParen()],
     [ASTCall('+', children=[
         ASTLiteral(1), ASTLiteral(2)])], None),
    ([LParen(), Symbol('print'), String('Hello, world!')], None, ParseException),
    ([LParen(), Symbol('-'),
      LParen(), Symbol('+'), Number(1), Number(2), RParen(),
      LParen(), Number(1.5), RParen()],
     None, ParseException)
]


@pytest.mark.parametrize(('tokens', 'roots', 'expected_exception'), testdata)
def test_basics(tokens: list[Token], roots: list[ASTNode], expected_exception):
    parser = Parser()
    if expected_exception:
        with pytest.raises(expected_exception):
            parser.parse(tokens)
    else:
        assert all([left_root == right_root for left_root,
                    right_root in zip(parser.parse(tokens), roots)])
