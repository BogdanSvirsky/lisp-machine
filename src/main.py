from generator import CCodeGenerator
from parser import Parser
from lexer import Lexer
import sys
import os
import subprocess
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

def format_c_code(c_code: str) -> str:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
        f.write(c_code)
        temp_path = f.name
    
    style = "{BasedOnStyle: LLVM, IndentWidth: 4, UseTab: false, ColumnLimit: 100}"
    
    try:
        subprocess.run(
            ['clang-format', '-i', f'-style={style}', temp_path],
            check=True,
            capture_output=True,
            text=True
        )
        
        with open(temp_path, 'r') as f:
            formatted = f.read()
        
        return formatted
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: clang-format not found, skipping formatting")
        return c_code
    finally:
        os.unlink(temp_path)


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

    c_code = format_c_code(c_code)

    with open('main.c', 'w') as f:
        f.write(c_code)

    print("Generated main.c")

    runtime_path = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)),
        'runtime',
        'runtime.c')

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