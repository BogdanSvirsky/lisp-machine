from dataclasses import dataclass
from lexer.tokens import *


@dataclass
class ASTNode:
    children: list['ASTNode']


@dataclass
class ASTLiteral(ASTNode):
    children = 
    token: Number | String | Boolean


@dataclass
class ASTCall(ASTNode):
    children = []
    name: str
