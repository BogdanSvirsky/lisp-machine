import pytest
from parser.ast import *
from parser import ParseException
from test_parser_helpers import parse_source


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
