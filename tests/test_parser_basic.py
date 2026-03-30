import pytest
from parser.ast import *
from test_parser_helpers import parse_source


class TestParser:

    def test_simple_call(self):
        """Тест простого вызова функции: (print 42)"""
        source = "(print 42)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("print"),
                args=[ASTLiteral(42)]
            )
        ])

        assert ast == expected

    def test_add_two_numbers(self):
        """Тест сложения двух чисел: (+ 1 2)"""
        source = "(+ 1 2)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("+"),
                args=[
                    ASTLiteral(1),
                    ASTLiteral(2)
                ]
            )
        ])

        assert ast == expected

    def test_add_three_numbers(self):
        """Тест сложения трех чисел: (+ 1 2 3)"""
        source = "(+ 1 2 3)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("+"),
                args=[
                    ASTLiteral(1),
                    ASTLiteral(2),
                    ASTLiteral(3)
                ]
            )
        ])

        assert ast == expected

    def test_nested_calls(self):
        """Тест вложенных вызовов: (print (+ 1 2))"""
        source = "(print (+ 1 2))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("print"),
                args=[
                    ASTCall(
                        function=ASTSymbol("+"),
                        args=[
                            ASTLiteral(1),
                            ASTLiteral(2)
                        ]
                    )
                ]
            )
        ])

        assert ast == expected

    def test_deeply_nested(self):
        """Тест глубокой вложенности: (* (+ 1 2) (- 3 4))"""
        source = "(* (+ 1 2) (- 3 4))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("*"),
                args=[
                    ASTCall(
                        function=ASTSymbol("+"),
                        args=[ASTLiteral(1), ASTLiteral(2)]
                    ),
                    ASTCall(
                        function=ASTSymbol("-"),
                        args=[ASTLiteral(3), ASTLiteral(4)]
                    )
                ]
            )
        ])

        assert ast == expected

    def test_multiple_expressions(self):
        """Тест нескольких выражений в программе"""
        source = "(print 1) (print 2) (+ 3 4)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("print"),
                args=[ASTLiteral(1)]
            ),
            ASTCall(
                function=ASTSymbol("print"),
                args=[ASTLiteral(2)]
            ),
            ASTCall(
                function=ASTSymbol("+"),
                args=[ASTLiteral(3), ASTLiteral(4)]
            )
        ])

        assert ast == expected

    def test_string_literal(self):
        """Тест строковых литералов"""
        source = '(print "hello world")'
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("print"),
                args=[ASTLiteral("hello world")]
            )
        ])

        assert ast == expected

    def test_boolean_literals(self):
        """Тест булевых литералов (nil и t)"""
        source = "(if t (print 1) (print 2))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTIf(
                condition=ASTLiteral(True),   # t
                then_branch=ASTCall(
                    function=ASTSymbol("print"),
                    args=[ASTLiteral(1)]
                ),
                else_branch=ASTCall(
                    function=ASTSymbol("print"),
                    args=[ASTLiteral(2)]
                )
            )
        ])

        assert ast == expected

    def test_float_numbers(self):
        """Тест чисел с плавающей точкой"""
        source = "(+ 3.14 2.718)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("+"),
                args=[
                    ASTLiteral(3.14),
                    ASTLiteral(2.718)
                ]
            )
        ])

        assert ast == expected

    def test_negative_numbers(self):
        """Тест отрицательных чисел"""
        source = "(+ -5 -3)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("+"),
                args=[
                    ASTLiteral(-5),
                    ASTLiteral(-3)
                ]
            )
        ])

        assert ast == expected

    def test_symbols_as_args(self):
        """Тест символов в качестве аргументов"""
        source = "(define x 42)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("define"),
                args=[
                    ASTSymbol("x"),
                    ASTLiteral(42)
                ]
            )
        ])

        assert ast == expected

    def test_function_with_many_args(self):
        """Тест функции с большим количеством аргументов"""
        source = "(+ 1 2 3 4 5 6 7 8 9 10)"
        ast = parse_source(source)

        expected_args = [ASTLiteral(i) for i in range(1, 11)]

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("+"),
                args=expected_args
            )
        ])

        assert ast == expected
