import re
from typing import TextIO
from .tokens import *


STRING_PATTERN = r'"[^"]*"'


class Lexer:
    _current_token: str

    def tokenize(self, text: TextIO) -> list[Token]:
        tokens: list[Token] = []

        self._current_token = ''
        content = text.read()
        i = 0
        length = len(content)

        while i < length:
            symb = content[i]
            
            if re.match(r'\s', symb):
                token = self._process_current_token()
                if token:
                    tokens.append(token)
                i += 1
                continue

            if symb == '(' or symb == ')':
                token = self._process_current_token()
                if token:
                    tokens.append(token)
                tokens.append(LParen() if symb == '(' else RParen())
                i += 1
                continue
            
            if symb == '"':
                token = self._process_current_token()
                if token:
                    tokens.append(token)
                
                end = content.find('"', i + 1)
                if end == -1:
                    raise Exception("Unclosed string")
                
                self._current_token = content[i:end + 1]
                token = self._process_current_token()
                if token:
                    tokens.append(token)
                i = end + 1
                continue
            
            self._current_token += symb
            i += 1

        token = self._process_current_token()
        if token:
            tokens.append(token)

        return tokens

    def _process_current_token(self) -> Token | None:
        if self._current_token == '':
            return None

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
                token = String(self._current_token[1:-1])
            elif self._current_token == 'nil' or self._current_token == 't':
                token = Boolean(self._current_token == 't')
            else:
                token = Symbol(self._current_token)
        
        self._current_token = ''
        return token