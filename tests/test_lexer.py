import io
from lexer import Lexer
from lexer.tokens import *
import pytest


@pytest.mark.parametrize(("text_in", "correct_tokens"),
                         [("(print 1)", [LParen(), Symbol('print'), Number(1), RParen()]),
                          ('("HELLO" 123213 3.1415168 nil)',
                           [LParen(), String('"HELLO"'), Number(123213), Number(3.1415168), Boolean(False), RParen()]),
                          ('(if \n\t(== 17 \n\t\t(/ \n\t\t\t(+ 1 \n\t\t\t\t(* 2 8))) 17)\n\t\t\t\t\t(print "good")\n\t\t\t\t\t(error "invalid!"))\n\n\n',
                          [LParen(), Symbol('if'),
                               LParen(), Symbol('=='), Number(17),
                                   LParen(), Symbol('/'),
                                       LParen(), Symbol('+'), Number(1),
                                           LParen(), Symbol('*'), Number(2), Number(8), RParen(),
                                       RParen(),
                                   RParen(),
                                   Number(17),
                               RParen(),
                               LParen(), Symbol('print'), String('"good"'), RParen(),
                               LParen(), Symbol('error'), String('"invalid!"'), RParen(),
                           RParen()])])
def test_basics(text_in: str, correct_tokens: list[Token]):
    lexer = Lexer()
    result = lexer.tokenize(io.StringIO(text_in))
    assert result == correct_tokens
