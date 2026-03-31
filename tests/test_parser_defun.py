import pytest
from parser.ast import *
from parser import ParseException
from test_parser_helpers import parse_source


class TestParserDefun:
    """Тесты для defun"""

    def test_defun_simple(self):
        """Тест: (defun square (x) (* x x))"""
        source = "(defun square (x) (* x x))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTDefun(
                name="square",
                params=["x"],
                body=ASTCall(
                    function=ASTSymbol("*"),
                    args=[
                        ASTSymbol("x"),
                        ASTSymbol("x")
                    ]
                )
            )
        ])

        assert ast == expected

    def test_defun_two_params(self):
        """Тест: (defun add (a b) (+ a b))"""
        source = "(defun add (a b) (+ a b))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTDefun(
                name="add",
                params=["a", "b"],
                body=ASTCall(
                    function=ASTSymbol("+"),
                    args=[
                        ASTSymbol("a"),
                        ASTSymbol("b")
                    ]
                )
            )
        ])

        assert ast == expected

    def test_defun_three_params(self):
        """Тест: (defun add3 (a b c) (+ a b c))"""
        source = "(defun add3 (a b c) (+ a b c))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTDefun(
                name="add3",
                params=["a", "b", "c"],
                body=ASTCall(
                    function=ASTSymbol("+"),
                    args=[
                        ASTSymbol("a"),
                        ASTSymbol("b"),
                        ASTSymbol("c")
                    ]
                )
            )
        ])

        assert ast == expected

    def test_defun_with_if(self):
        """Тест: (defun factorial (n) (if (== n 1) 1 (* n (factorial (- n 1)))))"""
        source = "(defun factorial (n) (if (== n 1) 1 (* n (factorial (- n 1)))))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTDefun(
                name="factorial",
                params=["n"],
                body=ASTIf(
                    condition=ASTCall(
                        function=ASTSymbol("=="),
                        args=[ASTSymbol("n"), ASTLiteral(1)]
                    ),
                    then_branch=ASTLiteral(1),
                    else_branch=ASTCall(
                        function=ASTSymbol("*"),
                        args=[
                            ASTSymbol("n"),
                            ASTCall(
                                function=ASTSymbol("factorial"),
                                args=[
                                    ASTCall(
                                        function=ASTSymbol("-"),
                                        args=[ASTSymbol("n"), ASTLiteral(1)]
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        ])

        assert ast == expected

    def test_defun_with_nested_call(self):
        """Тест: (defun square (x) (* x x)) (print (square 5))"""
        source = "(defun square (x) (* x x)) (print (square 5))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTDefun(
                name="square",
                params=["x"],
                body=ASTCall(
                    function=ASTSymbol("*"),
                    args=[ASTSymbol("x"), ASTSymbol("x")]
                )
            ),
            ASTCall(
                function=ASTSymbol("print"),
                args=[
                    ASTCall(
                        function=ASTSymbol("square"),
                        args=[ASTLiteral(5)]
                    )
                ]
            )
        ])

        assert ast == expected

    def test_defun_no_params(self):
        """Тест: (defun hello () (print "hello"))"""
        source = '(defun hello () (print "hello"))'
        ast = parse_source(source)

        expected = ASTProgram([
            ASTDefun(
                name="hello",
                params=[],
                body=ASTCall(
                    function=ASTSymbol("print"),
                    args=[ASTLiteral("hello")]
                )
            )
        ])

        assert ast == expected

    def test_defun_invalid_no_name(self):
        """Тест: (defun (x) (* x x)) — нет имени функции"""
        source = "(defun (x) (* x x))"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Expected function name" in str(exc.value)

    def test_defun_invalid_no_params_list(self):
        """Тест: (defun square x (* x x)) — нет списка параметров в скобках"""
        source = "(defun square x (* x x))"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Expected parameter list" in str(exc.value)

    def test_defun_invalid_no_body(self):
        """Тест: (defun square (x)) — нет тела"""
        source = "(defun square (x))"

        with pytest.raises(ParseException):
            parse_source(source)

    def test_multiple_defuns(self):
        """Тест: несколько определений функций"""
        source = """
        (defun square (x) (* x x))
        (defun cube (x) (* x x x))
        (print (square 5))
        (print (cube 3))
        """
        ast = parse_source(source)

        expected = ASTProgram([
            ASTDefun(
                name="square",
                params=["x"],
                body=ASTCall(
                    function=ASTSymbol("*"),
                    args=[ASTSymbol("x"), ASTSymbol("x")]
                )
            ),
            ASTDefun(
                name="cube",
                params=["x"],
                body=ASTCall(
                    function=ASTSymbol("*"),
                    args=[
                        ASTSymbol("x"),
                        ASTSymbol("x"),
                        ASTSymbol("x")
                    ]
                )
            ),
            ASTCall(
                function=ASTSymbol("print"),
                args=[
                    ASTCall(
                        function=ASTSymbol("square"),
                        args=[ASTLiteral(5)]
                    )
                ]
            ),
            ASTCall(
                function=ASTSymbol("print"),
                args=[
                    ASTCall(
                        function=ASTSymbol("cube"),
                        args=[ASTLiteral(3)]
                    )
                ]
            )
        ])

        assert ast == expected
