from dataclasses import dataclass
from typing import Any, Optional


class ASTNode:
    pass


@dataclass
class ASTLiteral(ASTNode):
    value: Any


@dataclass
class ASTSymbol(ASTNode):
    name: str
    
@dataclass
class ASTIf(ASTNode):
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode]


@dataclass
class ASTCall(ASTNode):
    function: ASTSymbol
    args: list[ASTNode]
    
@dataclass
class ASTDefun(ASTNode):
    name: str
    params: list[str]
    body: ASTNode

@dataclass
class ASTProgram(ASTNode):
    expressions: list[ASTNode]