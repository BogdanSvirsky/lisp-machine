import pytest
from lexer.tokens import *
from parser.ast import *
from parser import ParseException, Parser
from test_parser_helpers import parse_source


class TestParserMacros:
    """Тесты для defmacro"""

    def test_macro_simple(self):
        """Тест простого макроопределения: (defmacro twice (x) (* 2 x))

        Macros are stored internally but not included in AST expressions.
        """
        source = "(defmacro twice (x) (* 2 x))"
        ast = parse_source(source)

        assert len(ast.expressions) == 0

    def test_macro_no_params(self):
        """Тест макроса без параметров: (defmacro hello () 42)"""
        source = "(defmacro hello () 42)"
        ast = parse_source(source)

        assert len(ast.expressions) == 0

    def test_macro_two_params(self):
        """Тест макроса с двумя параметрами"""
        source = "(defmacro swap (a b) (list b a))"
        ast = parse_source(source)

        assert len(ast.expressions) == 0

    def test_macro_with_unquote(self):
        """Тест макроса с unquote в теле"""
        source = "(defmacro add-one (x) `(+ ,x 1))"
        ast = parse_source(source)

        assert len(ast.expressions) == 0

    def test_macro_defined_then_used(self):
        """Тест: определение макроса и его использование

        Macro is defined but not in expressions; only the expanded call appears.
        """
        source = "(defmacro twice (x) `(* ,x 2)) (twice 5)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("*"),
                args=[ASTLiteral(5), ASTLiteral(2)]
            )
        ])

        assert ast == expected

    def test_macro_multiple_params_expansion(self):
        """Тест раскрытия макроса с несколькими параметрами"""
        source = "(defmacro swap (a b) `(+ ,a ,b)) (swap 10 20)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("+"),
                args=[ASTLiteral(10), ASTLiteral(20)]
            )
        ])

        assert ast == expected

    def test_macro_with_if(self):
        """Тест макроса с if - unquote only at top level"""
        source = "(defmacro unless (cond) `(if ,cond nil))"
        ast = parse_source(source)

        assert len(ast.expressions) == 0

    def test_macro_expansion_preserves_nested_calls(self):
        """Тест: макрос сохраняет вложенные вызовы в аргументах"""
        source = "(defmacro print-val (x) `(print ,x)) (print-val (+ 1 2))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("print"),
                args=[
                    ASTCall(
                        function=ASTSymbol("+"),
                        args=[ASTLiteral(1), ASTLiteral(2)]
                    )
                ]
            )
        ])

        assert ast == expected

    def test_macro_then_defun(self):
        """Тест: макрос затем функция"""
        source = "(defmacro add5 (x) `(+ ,x 5)) (defun square (y) (* y y))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTDefun(
                name="square",
                params=["y"],
                body=ASTCall(
                    function=ASTSymbol("*"),
                    args=[ASTSymbol("y"), ASTSymbol("y")]
                )
            )
        ])

        assert ast == expected


class TestParserMacrosErrors:
    """Тесты ошибок макросов"""

    def test_macro_invalid_no_name(self):
        """Тест: (defmacro (x) (* x x)) — нет имени макроса"""
        source = "(defmacro (x) (* x x))"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Expected macro name" in str(exc.value)

    def test_macro_invalid_no_params_list(self):
        """Тест: (defmacro twice x (* x x)) — нет списка параметров"""
        source = "(defmacro twice x (* x x))"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Expected macro parameter list" in str(exc.value)

    def test_macro_invalid_wrong_arg_count(self):
        """Тест: вызов макроса с неправильным числом аргументов"""
        source = "(defmacro twice (x) `(* ,x 2)) (twice 1 2)"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Invalid arguments count for macro twice" in str(exc.value)

    def test_unquote_without_backquote(self):
        """Тест: unquote без backquote"""
        source = "(defmacro twice (x) (,x 2))"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Unquote without Backquote" in str(exc.value)

    def test_macro_invalid_unquote_name(self):
        """Тест: невалидное имя в unquote - ошибка при вызове макроса"""
        source = "(defmacro twice (x) `(* ,y 2)) (twice 5)"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Invalid name to unquote" in str(exc.value)

    def test_unquote_splicing_catching(self):

        tokens = [
            LParen(), Symbol('defmacro'), Symbol('when'),
            LParen(), Symbol('cond'), Symbol('&body'), Symbol('body'), RParen(),
            Backquote(), LParen(), Symbol('if'), Unquote(), Symbol('cond'),
            LParen(), Symbol('progn'), UnquoteSplicing(), Symbol('body'), RParen(),
            RParen(),
            RParen()
        ]

        parser = Parser()
        roots = parser.parse(tokens)

        expected = ASTMacro('when', ['cond'], 'body', ASTIf(condition=ASTUnquote('cond'),
                                                            then_branch=ASTCall(ASTSymbol('progn'), []
