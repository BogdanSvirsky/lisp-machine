from lexer.tokens import *
from typing import Sequence
from .ast import *


class ParseException(Exception):
    pass


class Parser:
    def __init__(self):
        self.tokens: list[Token] = []
        self.pos: int = 0
    
    def parse(self, tokens: Sequence[Token]) -> ASTProgram:
        self.tokens = list(tokens)
        self.pos = 0
        expressions = []
        
        while self.pos < len(self.tokens):
            token = self._peek()
            
            if not isinstance(token, LParen):
                raise ParseException(f"Expected '(', got {type(token).__name__}")
            
            expr = self._parse_expr()
            expressions.append(expr)
        
        return ASTProgram(expressions)
    
    def _parse_expr(self) -> ASTNode:
        token = self._peek()
        
        if isinstance(token, LParen):
            return self._parse_list()
        elif isinstance(token, Number):
            self._advance()
            return ASTLiteral(token.value)
        elif isinstance(token, String):
            self._advance()
            return ASTLiteral(token.value)
        elif isinstance(token, Boolean):
            self._advance()
            # print(f"DEBUG: Parsing Boolean with value {token.value}")
            return ASTLiteral(token.value)
        elif isinstance(token, Symbol):
            self._advance()
            return ASTSymbol(token.value)
        else:
            raise ParseException(f"Unexpected token: {token}")
    
    def _parse_list(self) -> ASTNode:
        self._advance()
        
        # Пустой список не поддерживаем 
        if isinstance(self._peek(), RParen):
            self._advance()
            raise ParseException("Empty list not supported yet")
        
        first = self._parse_expr()
        
        if not isinstance(first, ASTSymbol):
            raise ParseException("First element of list must be a symbol (function name)")
        
        if first.name == 'if':
            return self._parse_if()
        
        args = []
        while not isinstance(self._peek(), RParen):
            args.append(self._parse_expr())
        
        self._advance()
        
        return ASTCall(function=first, args=args)
    
    def _parse_if(self) -> ASTIf:
        """Парсит (if cond then else)"""
        condition = self._parse_expr()
        
        then_branch = self._parse_expr()
        
        else_branch = None
        if not isinstance(self._peek(), RParen):
            else_branch = self._parse_expr()
        
        if not isinstance(self._peek(), RParen):
            raise ParseException("Expected ')'")
        self._advance()
        
        return ASTIf(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch
        )
    
    def _peek(self) -> Token:
        if self.pos >= len(self.tokens):
            raise ParseException("Unexpected end of input")
        return self.tokens[self.pos]
    
    def _advance(self) -> Token:
        token = self._peek()
        self.pos += 1
        return token