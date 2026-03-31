from lexer.tokens import *
from typing import Sequence
from .ast import *


class ParseException(Exception):
    pass


class Parser:
    def __init__(self):
        self.tokens: list[Token] = []
        self.pos: int = 0
        self.macros: dict[str, ASTMacro] = {}

    def parse(self, tokens: Sequence[Token]) -> ASTProgram:
        self.tokens = list(tokens)
        self.pos = 0
        self.macros = {}
        expressions = []

        while self.pos < len(self.tokens):
            token = self._peek()

            if not isinstance(token, LParen):
                raise ParseException(
                    f"Expected '(', got {type(token).__name__}")

            expr = self._parse_expr()

            if isinstance(expr, ASTMacro):
                self.macros[expr.name] = expr
            else:
                expressions.append(expr)

        return ASTProgram(expressions)

    def _parse_expr(self, in_quote: bool = False, quote_params: list[str] = [
    ], splicing_param: str = "") -> ASTNode:
        token = self._peek()

        if isinstance(token, Backquote):
            self._advance()
            return self._parse_expr(True)
        if isinstance(token, Unquote):
            if not in_quote:
                raise ParseException("Unquote without Backquote")
            self._advance()
            token = self._peek()
            if not isinstance(token, Symbol):
                raise ParseException("No symbol after Unquote")
            if token.value not in quote_params:
                raise ParseException(f"Symbol \"{token.value}\" not in quote")
            self._advance()
            return ASTUnquote(token.value)
        if isinstance(token, UnquoteSplicing):
            if not in_quote:
                raise ParseException("Unquote splicing without Backquote")
            self._advance()
            token = self._peek()
            if not isinstance(token, Symbol):
                raise ParseException("No symbol after unquote splicing")
            if token.value != splicing_param:
                raise ParseException(
                    f"Symbol \"{
                        token.value}\" isn't unquote splicing param")
            self._advance()
            return ASTUnquoteSplicing(token.value)
        if isinstance(token, LParen):
            return self._parse_list()
        elif isinstance(token, Number) or isinstance(token, String) \
                or isinstance(token, Boolean):
            self._advance()
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
            raise ParseException(
                "First element of list must be a symbol (function name)")

        match first.name:
            case 'if':
                return self._parse_if()
            case 'defun':
                return self._parse_defun()
            case 'let':
                return self._parse_let()
            case 'defmacro':
                return self._parse_defmacro()

        args = []
        while not isinstance(self._peek(), RParen):
            args.append(self._parse_expr())

        self._advance()

        if first.name in self.macros:
            return self._unpack_macro(self.macros[first.name], args)

        return ASTCall(function=first, args=args)

    def _parse_if(self) -> ASTIf:
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

    def _parse_defun(self) -> ASTDefun:
        name_token = self._peek()
        if not isinstance(name_token, Symbol):
            raise ParseException("Expected function name")
        self._advance()
        name = name_token.value

        if not isinstance(self._peek(), LParen):
            raise ParseException("Expected parameter list")
        self._advance()

        params = []
        while not isinstance(self._peek(), RParen):
            param_token = self._peek()
            if not isinstance(param_token, Symbol):
                raise ParseException("Expected parameter name")
            params.append(param_token.value)
            self._advance()

        self._advance()

        body = self._parse_expr()

        if not isinstance(self._peek(), RParen):
            raise ParseException("Expected ')'")
        self._advance()

        return ASTDefun(name=name, params=params, body=body)

    def _parse_let(self) -> ASTLet:
        if not isinstance(self._peek(), LParen):
            raise ParseException("Expected bindings list")
        self._advance()

        bindings = []
        while not isinstance(self._peek(), RParen):
            if not isinstance(self._peek(), LParen):
                raise ParseException("Expected binding pair")
            self._advance()

            var_token = self._peek()
            if not isinstance(var_token, Symbol):
                raise ParseException("Expected variable name")
            self._advance()

            val_expr = self._parse_expr()

            if not isinstance(self._peek(), RParen):
                raise ParseException("Expected ')'")
            self._advance()

            bindings.append((var_token.value, val_expr))

        self._advance()

        body = self._parse_expr()

        if not isinstance(self._peek(), RParen):
            raise ParseException("Expected ')'")
        self._advance()

        return ASTLet(bindings=bindings, body=body)

    def _parse_defmacro(self) -> ASTMacro:
        name_token = self._peek()
        if not isinstance(name_token, Symbol):
            raise ParseException("Expected macro name")
        self._advance()
        name = name_token.value

        if not isinstance(self._peek(), LParen):
            raise ParseException("Expected macro parameter list")
        self._advance()

        params = []
        splicing_param = ""
        while not isinstance(self._peek(), RParen):
            param_token = self._peek()
            if not isinstance(param_token, Symbol):
                raise ParseException("Expected macro parameter name")
            elif param_token.value == '&body':
                if splicing_param != "":
                    raise ParseException("Splicing param already defined")
                self._advance()
                param_token = self._peek()
                if not isinstance(param_token, Symbol):
                    raise ParseException("Expected splicing param name")
                splicing_param = param_token.value
                self._advance()
                continue
            params.append(param_token.value)
            self._advance()

        self._advance()

        body = self._parse_expr(
            quote_params=params,
            splicing_param=splicing_param)

        if not isinstance(self._peek(), RParen):
            raise ParseException("Expected ')'")
        self._advance()

        return ASTMacro(
            name, params, splicing_param if splicing_param != '' else None, body)

    def _unpack_macro(self, macro: ASTMacro, args: list[ASTNode]) -> ASTNode:
        if len(macro.params) < len(args) or \
                (len(macro.params) > len(args) and macro.splicing_param is None):
            raise ParseException(
                f'Invalid arguments count for macro {macro.name}: {str(args)}')

        params: dict[str, ASTNode] = {}
        for key, value in zip(macro.params, args[:len(macro.params)]):
            params[key] = value

        splicing_args = args[len(macro.params):]
        if len(splicing_args) == 0:
            splicing_args.append(ASTLiteral(False))

        def unpack(node: ASTNode) -> ASTNode:
            if isinstance(node, ASTUnquote):
                if node.name not in params:
                    raise ParseException(
                        f'Invalid name to unquote: {node.name}')
                return params[node.name]
            elif isinstance(node, ASTUnquoteSplicing):
                raise ParseException('Unpacking unquote splicing')
            elif isinstance(node, ASTCall):
                call_args = []
                for arg in node.args:
                    if isinstance(arg, ASTUnquoteSplicing):
                        if arg.name != macro.splicing_param:
                            raise ParseException(
                                f'Invalid name to unquote splicing: {arg.name}')
                        else:
                            call_args.extend(splicing_args)
                    else:
                        call_args.append(arg)

                return ASTCall(
                    function=node.function,
                    args=[unpack(arg) for arg in node.args]
                )
            elif isinstance(node, ASTIf):
                return ASTIf(
                    condition=unpack(node.condition),
                    then_branch=unpack(node.then_branch),
                    else_branch=unpack(
                        node.else_branch) if node.else_branch else None
                )
            elif isinstance(node, ASTLet):
                return ASTLet(
                    bindings=[(name, unpack(val))
                              for name, val in node.bindings],
                    body=unpack(node.body)
                )
            return node

        return unpack(macro.body)

    def _peek(self) -> Token:
        if self.pos >= len(self.tokens):
            raise ParseException("Unexpected end of input")
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        token = self._peek()
        self.pos += 1
        return token
