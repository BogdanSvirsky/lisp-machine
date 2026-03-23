from lexer.tokens import *
from typing import Generic, TypeVar, Union


class ASTNode:
    def __init__(self):
        self.children: list['ASTNode'] = []

    def __eq__(self, other) -> bool:
        return type(other) == type(self) and all(
            left == right for left, right in zip(self.children, other.children))


T = TypeVar('T', bool, str, Union[int, float])


class ASTLiteral(ASTNode, Generic[T]):
    def __init__(self, value: T):
        super().__init__()
        self.value: T = value

    def __eq__(self, other) -> bool:
        if super().__eq__(other):
            return self.value == other.value
        else:
            return False


class ASTNumber(ASTLiteral[Union[int, float]]):
    pass


class ASTString(ASTLiteral[str]):
    pass


class ASTBoolean(ASTLiteral[bool]):
    pass


V = TypeVar('V', ASTNumber, ASTString, ASTBoolean)


class ASTBinaryOp(ASTNode, Generic[V]):
    def __init__(self, operator: str, left: V, right: V):
        self.children = [left, right]
        self.operator = operator


class ASTCall(ASTNode):
    name: str

    def __init__(self, name: str, children: list[ASTNode] = []) -> None:
        self.children = children
        self.name = name

    def __eq__(self, other) -> bool:
        if super().__eq__(other):
            return self.name == other.name
        else:
            return False
