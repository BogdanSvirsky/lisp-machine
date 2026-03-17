from lexer.tokens import *
from typing import Optional, Sequence, Iterator
from .ast import *


class ParseException(Exception):
    pass


class Parser:
    def parse(self, tokens: Sequence[Token]) -> list[ASTNode]:
        roots = []
        iterator = iter(tokens)
        while True:
            try:
                token = next(iterator)
            except StopIteration:
                break

            if isinstance(token, LParen):
                roots.append(self._parse_list(iterator))
            elif isinstance(token, RParen):
                raise ParseException()

        return roots

    def _parse_list(self, iterator: Iterator[Token]) -> ASTNode:
        node: Optional[ASTNode] = None
        while True:
            try:
                token = next(iterator)
            except StopIteration:
                raise ParseException()

            if isinstance(token, RParen):
                break

            new_node: ASTNode
            if isinstance(token, LParen):
                if node is None:
                    raise ParseException()
                new_node = self._parse_list(iterator)
            elif isinstance(token, Number) or isinstance(
                    token, String) or isinstance(token, Boolean):
                new_node = ASTLiteral(token)
            elif isinstance(token, Symbol):
                new_node = ASTCall(token.value)
            else:
                raise ParseException()

            if node is None:
                node = new_node
            else:
                node.children.append(new_node)

        if node is None:
            raise ParseException()
        return node
