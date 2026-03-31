from dataclasses import dataclass
from typing import Any


class Token:
    value: Any = None

    def __eq__(self, value) -> bool:
        return type(value) == type(self) and self.value == value.value


class LParen(Token):
    pass


class RParen(Token):
    pass


@dataclass
class Number(Token):
    value: int | float


@dataclass
class String(Token):
    value: str


@dataclass
class Boolean(Token):
    value: bool


@dataclass
class Symbol(Token):
    value: str


class Backquote(Token):
    pass


class Unquote(Token):
    pass


class UnquoteSplicing(Token):
    pass
