from lexer.tokens import *
from typing import Optional, Sequence, Iterator
from .ast import *


class ParseException(Exception):
    pass


class InvalidArgumentsCount(Exception):
    pass


BINARY_OPERATORS: list[str] = [
    '+', '-', '/', '*', '<', '>', '==', '<=', '>=']


def parse(tokens: Sequence[Token]) -> list[ASTNode]:
    roots = []
    iterator = iter(tokens)

    while True:
        try:
            token = next(iterator)
        except StopIteration:
            break

        if not isinstance(token, LParen):
            raise ParseException()
        tokens_list = _convert_to_list(iterator)
        roots.append(_parse_list(tokens_list))

    return roots


def _convert_to_list(iterator: Iterator[Token]) -> list[Token | list]:
    result = []
    while True:
        try:
            token = next(iterator)
        except StopIteration:
            raise ParseException()


: q
: q
        if isinstance(token, RParen):
            break
        if isinstance(token, LParen):
            result.append(_convert_to_list(iterator))
        else:
            result.append(token)

    return result


def _parse_list(tokens: list[Token | list]) -> ASTNode:
    if len(tokens) == 0:
        raise ParseException()

    if isinstance(tokens[0], Symbol):
        if tokens[0].value in BINARY_OPERATORS:
            if len(tokens) == 3:
                return ASTBinaryOp(tokens[0].value, _parse_list(tokens[1]) if isinstance(tokens[1], list) else _parse_literal(tokens[1], _parse_list(tokens[1]) if isinstance(tokens[1], list) else _parse_literal(tokens[1]))
            else:
                raise InvalidArgumentsCount()



def _parse_literal(token: Token) -> ASTNumber | ASTBoolean | ASTString:
    if isinstance(token, Number):
        return ASTNumber(token.value)
    elif isinstance(token, String):
        return ASTString(token.value)
    elif isinstance(token, Boolean):
        return ASTBoolean(token.value)
    else:
        raise ParseException()
