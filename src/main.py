import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(__file__))

from lexer import Lexer
from parser import Parser
from generator import CCodeGenerator


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <input.lisp>")
        sys.exit(1)
    
    input_file = sys.argv[1]
        
    lexer = Lexer()
    tokens = lexer.tokenize(open(input_file, 'r'))
    
    parser = Parser()
    ast = parser.parse(tokens)
    
    generator = CCodeGenerator()
    c_code = generator.generate(ast)
    
    with open('main.c', 'w') as f:
        f.write(c_code)
    
    print("Generated main.c")
    
    runtime_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'runtime', 'runtime.c')
    
    result = subprocess.run(
        ['gcc', 'main.c', runtime_path, '-o', 'main'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Compilation failed:")
        print(result.stderr)
        sys.exit(1)
    
    print("Compiled to program")


if __name__ == '__main__':
    main()