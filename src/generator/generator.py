from typing import TextIO
from parser.ast import *


class UndefinedSymbol(Exception):
    pass


def generate(roots: list[ASTNode], text_io: TextIO) -> None:
    for root in roots:
        pass


def _process_node(node: ASTNode) -> str:
    if isinstance(node, ASTLiteral):
        return str(node.value)
    if isinstance(node, ASTCall):
        if node.name == '+':
