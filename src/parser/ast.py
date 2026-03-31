from dataclasses import dataclass
from typing import Any, Optional, dataclass_transform


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
class ASTMacro(ASTNode):
    name: str
    params: list[str]
    splicing_param: str | None
    body: ASTNode


@dataclass
class ASTLet(ASTNode):
    bindings: list[tuple[str, ASTNode]]
    body: ASTNode


@dataclass
class ASTUnquote(ASTNode):
    name: str


@dataclass
class ASTUnquoteSplicing(ASTNode):
    name: str


@dataclass
class ASTProgram(ASTNode):
    expressions: list[ASTNode]
