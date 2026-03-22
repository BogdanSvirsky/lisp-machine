from lexer.tokens import *


class ASTNode:
    children: list['ASTNode'] = []

    def __eq__(self, other) -> bool:
        return type(other) == type(self) and all(
            left == right for left, right in zip(self.children, other.children))


class ASTLiteral(ASTNode):
    value: str | bool | float | int

    def __init__(self, value: str | bool | float | int,
                 children: list[ASTNode] = []) -> None:
        self.children = children
        self.value = value

    def __eq__(self, other) -> bool:
        if super().__eq__(other):
            return self.value == other.value
        else:
            return False


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
