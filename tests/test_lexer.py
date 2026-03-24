import io
import pytest
from lexer import Lexer
from lexer.tokens import *


class TestLexer:
    """Тесты для лексера"""
    
    def test_simple_print(self):
        """Тест: (print 1)"""
        source = "(print 1)"
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(),
            Symbol("print"),
            Number(1),
            RParen()
        ]
        
        assert tokens == expected
    
    def test_string_with_spaces(self):
        """Тест: ("HE L LO" 123213 -3.1415168 nil)"""
        source = '("HE L LO" 123213 -3.1415168 nil)'
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(),
            String("HE L LO"),
            Number(123213),
            Number(-3.1415168),
            Boolean(False),
            RParen()
        ]
        
        assert tokens == expected
    
    def test_complex_nested_expression(self):
        """Тест: сложное вложенное выражение с if, ==, /, +, *"""
        source = """(if 
    (== 17 
        (/ 
            (+ 1 
                (* 2 8))) 17)
                    (print "good")
                    (error "invalid!"))"""
        
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(),
            Symbol("if"),
            LParen(),
            Symbol("=="),
            Number(17),
            LParen(),
            Symbol("/"),
            LParen(),
            Symbol("+"),
            Number(1),
            LParen(),
            Symbol("*"),
            Number(2),
            Number(8),
            RParen(),
            RParen(),
            RParen(),
            Number(17),
            RParen(),
            LParen(),
            Symbol("print"),
            String("good"),
            RParen(),
            LParen(),
            Symbol("error"),
            String("invalid!"),
            RParen(),
            RParen()
        ]
        
        assert tokens == expected
    
    def test_empty_program(self):
        """Тест: пустая программа"""
        source = ""
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        assert tokens == []
    
    def test_only_parentheses(self):
        """Тест: только скобки ()"""
        source = "()"
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(),
            RParen()
        ]
        
        assert tokens == expected
    
    def test_multiple_expressions(self):
        """Тест: несколько выражений в одной строке"""
        source = "(print 1) (print 2) (+ 3 4)"
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(),
            Symbol("print"),
            Number(1),
            RParen(),
            LParen(),
            Symbol("print"),
            Number(2),
            RParen(),
            LParen(),
            Symbol("+"),
            Number(3),
            Number(4),
            RParen()
        ]
        
        assert tokens == expected
    
    def test_negative_numbers(self):
        """Тест: отрицательные числа"""
        source = "(+ -5 -3)"
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(),
            Symbol("+"),
            Number(-5),
            Number(-3),
            RParen()
        ]
        
        assert tokens == expected
    
    def test_float_numbers(self):
        """Тест: числа с плавающей точкой"""
        source = "(+ 3.14 2.718)"
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(),
            Symbol("+"),
            Number(3.14),
            Number(2.718),
            RParen()
        ]
        
        assert tokens == expected
    
    def test_boolean_values(self):
        """Тест: булевы значения t и nil"""
        source = "(if t (print 1) (print nil))"
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(),
            Symbol("if"),
            Boolean(True),   # t
            LParen(),
            Symbol("print"),
            Number(1),
            RParen(),
            LParen(),
            Symbol("print"),
            Boolean(False),  # nil
            RParen(),
            RParen()
        ]
        
        assert tokens == expected
        
    def test_multiline_input(self):
        """Тест: многострочный ввод"""
        source = """
        (print 1)
        (print 2)
        (print 3)
        """
        lexer = Lexer()
        tokens = lexer.tokenize(io.StringIO(source))
        
        expected = [
            LParen(), Symbol("print"), Number(1), RParen(),
            LParen(), Symbol("print"), Number(2), RParen(),
            LParen(), Symbol("print"), Number(3), RParen()
        ]
        
        assert tokens == expected