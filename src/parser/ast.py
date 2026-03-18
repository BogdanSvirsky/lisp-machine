from dataclasses import dataclass, field
from lexer.tokens import *


@dataclass
class ASTNode:
    children: list['ASTNode'] = field(default=[])


@dataclass
class ASTLiteral(ASTNode):
    value: str | bool | float | int 


@dataclass
class ASTCall(ASTNode):
    name: str = field()
