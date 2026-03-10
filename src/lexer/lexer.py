from decimal import InvalidOperation
import re
from typing import TextIO
from .tokens import *


STRING_PATTERN = r'"[^"]*"'


class Lexer:
    _current_token: str

    def tokenize(self, text: TextIO) -> list[Token]:
        tokens: list[Token] = []

        self._current_token = ''
        for line in text.readlines():
            for symb in line:
                if re.match(r'\s', symb): 
                    token = self._process_current_token()
                    if token:
                        tokens.append(token)
                    continue

                if symb == '(' or symb == ')':
                    token = self._process_current_token()
                    if token:
                        tokens.append(token)
                    tokens.append(LParen() if symb == '(' else RParen())
                else:
                    self._current_token += symb

        return tokens

    def _process_current_token(self) -> Token | None:
        if self._current_token == '':
            return

        token = None
        try:
            token = Number(int(self._current_token))
        except ValueError:
            try:
                token = Number(float(self._current_token))
            except ValueError:
                pass

        if not token:
            if re.match(STRING_PATTERN, self._current_token):
                token = String(self._current_token)
            elif self._current_token == 'nil' or self._current_token == 't':
                token = Boolean(self._current_token == 't')
            else:
                token = Symbol(self._current_token)
        
        self._current_token = ''
        return token
