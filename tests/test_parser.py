import io
from parser import ast
import pytest
from lexer import Lexer
from parser import Parser, ParseException
from parser.ast import *


@pytest.fixture
def parser():
    return Parser()


@pytest.fixture
def lexer():
    return Lexer()


def parse_source(source: str) -> ASTProgram:
    lexer = Lexer()
    tokens = lexer.tokenize(io.StringIO(source))
    parser = Parser()
    return parser.parse(tokens)


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


class TestParserErrors:
    """Тесты на ошибки парсера"""

    def test_empty_program(self):
        """Тест пустой программы"""
        source = ""
        ast = parse_source(source)
        expected = ASTProgram([])
        assert ast == expected

    def test_missing_closing_paren(self):
        """Тест на отсутствие закрывающей скобки"""
        source = "(print 1"
        
        with pytest.raises(ParseException) as exc_info:
            parse_source(source)
        
        assert "Unexpected end of input" in str(exc_info.value)

    def test_extra_closing_paren(self):
        """Тест на лишнюю закрывающую скобку"""
        source = "(print 1))"
        
        with pytest.raises(ParseException):
            parse_source(source)

    def test_empty_list(self):
        """Тест на пустой список (пока не поддерживается)"""
        source = "()"
        
        with pytest.raises(ParseException) as exc_info:
            parse_source(source)
        
        assert "Empty list not supported" in str(exc_info.value)

    def test_invalid_syntax(self):
        """Тест на невалидный синтаксис"""
        source = "print 1"
        
        with pytest.raises(ParseException):
            parse_source(source)

    def test_malformed_expression(self):
        """Тест на неправильно сформированное выражение"""
        source = "(print 1 2"
        
        with pytest.raises(ParseException):
            parse_source(source)


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