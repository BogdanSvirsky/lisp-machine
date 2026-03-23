from lexer.tokens import *
from typing import Optional, Sequence, Iterator
from .ast import *


class ParseException(Exception):
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
        if not tokens_list:
            break
        # process list

    return roots


def _convert_to_list(iterator: Iterator[Token]) -> list[Token | list]:
    result = []
    while True:
        try:
            token = next(iterator)
        except StopIteration:
            raise ParseException()

        if isinstance(token, RParen):
            break
        if isinstance(token, LParen):
            result.append(_convert_to_list(iterator))
        else:
            result.append(token)

    return result


def _parse_list(tokens: list[Token | list]) -> ASTNode:
    node: Optional[ASTNode] = None
    for elem in tokens:
        if isinstance(token, RParen):
            break

        new_node: ASTNode
        if isinstance(token, LParen):
            if node is None:
                raise ParseException()
            new_node = _parse_list(iterator)
        elif isinstance(token, Symbol):
            if token.value in BINARY_OPERATORS:
                left =
            new_node = ASTCall(token.value)
        else:
            new_node = _parse_literal(token)

        if node is None:
            node = new_node
        else:
            node.children.append(new_node)

    if node is None:
        raise ParseException()
    return node


def _parse_literal(token: Token) -> ASTNumber | ASTBoolean | ASTString:
    if isinstance(token, Number):
        return ASTNumber(token.value)
    elif isinstance(token, String):
        return ASTString(token.value)
    elif isinstance(token, Boolean):
        return ASTBoolean(token.value)
    else:
        raise ParseException()
