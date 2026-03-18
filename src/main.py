from lexer.tokens import *
from parser import Parser
from parser.ast import *


parser = Parser()
print(parser.parse([LParen(), Symbol('+'), Number(1), Number(2), RParen()]))
