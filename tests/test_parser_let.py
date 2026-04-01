import pytest
from parser.ast import *
from parser import ParseException
from test_parser_helpers import parse_source


class TestParserLet:
    """Тесты для let"""

    def test_let_simple(self):
        """Тест: (let ((x 10)) (+ x 5))"""
        source = "(let ((x 10)) (+ x 5))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTLet(
                bindings=[("x", ASTLiteral(10))],
                body=ASTCall(
                    function=ASTSymbol("+"),
                    args=[ASTSymbol("x"), ASTLiteral(5)]
                )
            )
        ])

        assert ast == expected

    def test_let_two_bindings(self):
        """Тест: (let ((x 10) (y 20)) (+ x y))"""
        source = "(let ((x 10) (y 20)) (+ x y))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTLet(
                bindings=[
                    ("x", ASTLiteral(10)),
                    ("y", ASTLiteral(20))
                ],
                body=ASTCall(
                    function=ASTSymbol("+"),
                    args=[ASTSymbol("x"), ASTSymbol("y")]
                )
            )
        ])

        assert ast == expected

    def test_let_with_expressions(self):
        """Тест: (let ((x (+ 1 2)) (y (* 3 4))) (+ x y))"""
        source = "(let ((x (+ 1 2)) (y (* 3 4))) (+ x y))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTLet(
                bindings=[
                    ("x", ASTCall(
                        function=ASTSymbol("+"),
                        args=[ASTLiteral(1), ASTLiteral(2)]
                    )),
                    ("y", ASTCall(
                        function=ASTSymbol("*"),
                        args=[ASTLiteral(3), ASTLiteral(4)]
                    ))
                ],
                body=ASTCall(
                    function=ASTSymbol("+"),
                    args=[ASTSymbol("x"), ASTSymbol("y")]
                )
            )
        ])

        assert ast == expected

    def test_let_nested(self):
        """Тест: (let ((x 10)) (let ((y 20)) (+ x y)))"""
        source = "(let ((x 10)) (let ((y 20)) (+ x y)))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTLet(
                bindings=[("x", ASTLiteral(10))],
                body=ASTLet(
                    bindings=[("y", ASTLiteral(20))],
                    body=ASTCall(
                        function=ASTSymbol("+"),
                        args=[ASTSymbol("x"), ASTSymbol("y")]
                    )
                )
            )
        ])

        assert ast == expected

    def test_let_with_print(self):
        """Тест: (let ((x 10)) (print x))"""
        source = "(let ((x 10)) (print x))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTLet(
                bindings=[("x", ASTLiteral(10))],
                body=ASTCall(
                    function=ASTSymbol("print"),
                    args=[ASTSymbol("x")]
                )
            )
        ])

        assert ast == expected

    def test_let_with_if(self):
        """Тест: (let ((x 10)) (if (> x 5) (print "big") (print "small")))"""
        source = '(let ((x 10)) (if (> x 5) (print "big") (print "small")))'
        ast = parse_source(source)

        expected = ASTProgram([
            ASTLet(
                bindings=[("x", ASTLiteral(10))],
                body=ASTIf(
                    condition=ASTCall(
                        function=ASTSymbol(">"),
                        args=[ASTSymbol("x"), ASTLiteral(5)]
                    ),
                    then_branch=ASTCall(
                        function=ASTSymbol("print"),
                        args=[ASTLiteral("big")]
                    ),
                    else_branch=ASTCall(
                        function=ASTSymbol("print"),
                        args=[ASTLiteral("small")]
                    )
                )
            )
        ])

        assert ast == expected

    def test_let_without_bindings(self):
        """Тест: (let () 42) — пустой список биндингов"""
        source = "(let () 42)"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTLet(
                bindings=[],
                body=ASTLiteral(42)
            )
        ])

        assert ast == expected

    def test_let_invalid_no_bindings_list(self):
        """Тест: (let x 10) — нет списка биндингов"""
        source = "(let x 10)"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Expected bindings list" in str(exc.value)

    def test_let_invalid_binding_not_pair(self):
        """Тест: (let (x 10) (+ x 5)) — биндинг не в скобках"""
        source = "(let (x 10) (+ x 5))"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Expected binding pair" in str(exc.value)

    def test_let_invalid_no_var_name(self):
        """Тест: (let ((10 5)) (+ 10 5)) — вместо имени переменной число"""
        source = "(let ((10 5)) (+ 10 5))"

        with pytest.raises(ParseException) as exc:
            parse_source(source)

        assert "Expected variable name" in str(exc.value)

    def test_let_shadowing(self):
        """Тест: затенение переменных"""
        source = "(let ((x 10)) (let ((x 20)) x))"
        ast = parse_source(source)

        expected = ASTProgram([
            ASTLet(
                bindings=[("x", ASTLiteral(10))],
                body=ASTLet(
                    bindings=[("x", ASTLiteral(20))],
                    body=ASTSymbol("x")
                )
            )
        ])

        assert ast == expected
