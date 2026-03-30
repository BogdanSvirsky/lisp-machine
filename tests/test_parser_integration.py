import pytest
from parser.ast import *
from test_parser_helpers import parse_source


class TestParserWithLexer:
    """Интеграционные тесты: лексер + парсер"""

    def test_complex_expression(self):
        """Тест сложного выражения"""
        source = """
        (if (== 17 17)
            (print "good")
            (print "bad"))
        """
        ast = parse_source(source)

        expected = ASTProgram([
            ASTIf(
                condition=ASTCall(
                    function=ASTSymbol("=="),
                    args=[ASTLiteral(17), ASTLiteral(17)]
                ),
                then_branch=ASTCall(
                    function=ASTSymbol("print"),
                    args=[ASTLiteral("good")]
                ),
                else_branch=ASTCall(
                    function=ASTSymbol("print"),
                    args=[ASTLiteral("bad")]
                )
            )
        ])

        assert ast == expected

    def test_arithmetic_expression(self):
        """Тест арифметического выражения"""
        source = "(* (+ 1 2) (- 5 3) (/ 10 2))"
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
                        args=[ASTLiteral(5), ASTLiteral(3)]
                    ),
                    ASTCall(
                        function=ASTSymbol("/"),
                        args=[ASTLiteral(10), ASTLiteral(2)]
                    )
                ]
            )
        ])

        assert ast == expected

    def test_multiline_program(self):
        """Тест многострочной программы"""
        source = """
        (define x 10)
        (define y 20)
        (print (+ x y))
        """
        ast = parse_source(source)

        expected = ASTProgram([
            ASTCall(
                function=ASTSymbol("define"),
                args=[ASTSymbol("x"), ASTLiteral(10)]
            ),
            ASTCall(
                function=ASTSymbol("define"),
                args=[ASTSymbol("y"), ASTLiteral(20)]
            ),
            ASTCall(
                function=ASTSymbol("print"),
                args=[
                    ASTCall(
                        function=ASTSymbol("+"),
                        args=[ASTSymbol("x"), ASTSymbol("y")]
                    )
                ]
            )
        ])

        assert ast == expected
