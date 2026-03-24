from dataclasses import dataclass
from typing import Any


class ASTNode:
    pass


@dataclass
class ASTLiteral(ASTNode):
    value: Any


@dataclass
class ASTSymbol(ASTNode):
    name: str


@dataclass
class ASTCall(ASTNode):
    function: ASTSymbol
    args: list[ASTNode]


@dataclass
class ASTProgram(ASTNode):
    expressions: list[ASTNode]