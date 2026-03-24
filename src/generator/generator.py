from parser.ast import *


class CCodeGenerator:
    def __init__(self):
        self.temp_counter = 0
    
    def generate(self, ast: ASTProgram) -> str:
        code = []
        
        code.append('#include "runtime/runtime.h"\n\n')
        
        code.append('int main() {\n')
        
        for expr in ast.expressions:
            c_expr = self._generate_expr(expr)
            code.append(f'    {c_expr};\n')
        
        code.append('    return 0;\n')
        code.append('}\n')
        
        return ''.join(code)
    
    def _generate_expr(self, node: ASTNode) -> str:
        if isinstance(node, ASTLiteral):
            return self._generate_literal(node)
        elif isinstance(node, ASTCall):
            return self._generate_call(node)
        elif isinstance(node, ASTIf):
            return self._generate_if(node)
        else:
            raise NotImplementedError(f"Unknown node: {type(node)}")
    
    def _generate_literal(self, node: ASTLiteral) -> str:
        if isinstance(node.value, int):
            return f'make_integer({node.value})'
        elif isinstance(node.value, float):
            return f'make_float({node.value})'
        elif isinstance(node.value, float):
            return f'make_float({node.value})'
        elif isinstance(node.value, str):
            escaped = node.value.replace('\\', '\\\\').replace('"', '\\"')
            return f'make_string("{escaped}")'
        elif isinstance(node.value, bool):
            return 'LISP_T' if node.value else 'LISP_NIL'
        else:
            raise NotImplementedError(f"Unknown literal: {type(node.value)}")
    
    def _generate_call(self, node: ASTCall) -> str:
        func_name = node.function.name
        
        arg_codes = [self._generate_expr(arg) for arg in node.args]
        
        if func_name == 'print':
            if len(arg_codes) != 1:
                raise Exception(f"print expects 1 argument, got {len(arg_codes)}")
            return f'lisp_print({arg_codes[0]})'
        
        elif func_name == '+':
            if len(arg_codes) < 2:
                raise Exception(f"+ expects at least 2 arguments, got {len(arg_codes)}")
            result = arg_codes[0]
            for arg in arg_codes[1:]:
                result = f'lisp_add({result}, {arg})'
            return result
        
        elif func_name == '-':
            if len(arg_codes) < 2:
                raise Exception(f"- expects at least 2 arguments, got {len(arg_codes)}")
            result = arg_codes[0]
            for arg in arg_codes[1:]:
                result = f'lisp_sub({result}, {arg})'
            return result
        
        elif func_name == '*':
            if len(arg_codes) < 2:
                raise Exception(f"* expects at least 2 arguments, got {len(arg_codes)}")
            result = arg_codes[0]
            for arg in arg_codes[1:]:
                result = f'lisp_mul({result}, {arg})'
            return result
        
        elif func_name == '/':
            if len(arg_codes) < 2:
                raise Exception(f"/ expects at least 2 arguments, got {len(arg_codes)}")
            result = arg_codes[0]
            for arg in arg_codes[1:]:
                result = f'lisp_div({result}, {arg})'
            return result
        
        elif func_name == '>':
            if len(arg_codes) != 2:
                raise Exception(f"> expects 2 arguments, got {len(arg_codes)}")
            return f'lisp_gt({arg_codes[0]}, {arg_codes[1]})'
        
        elif func_name == '>=':
            if len(arg_codes) != 2:
                raise Exception(f">= expects 2 arguments, got {len(arg_codes)}")
            return f'lisp_ge({arg_codes[0]}, {arg_codes[1]})'
        
        elif func_name == '<':
            if len(arg_codes) != 2:
                raise Exception(f"< expects 2 arguments, got {len(arg_codes)}")
            return f'lisp_lt({arg_codes[0]}, {arg_codes[1]})'
        
        elif func_name == '<=':
            if len(arg_codes) != 2:
                raise Exception(f"<= expects 2 arguments, got {len(arg_codes)}")
            return f'lisp_le({arg_codes[0]}, {arg_codes[1]})'
        
        elif func_name == '==':
            if len(arg_codes) != 2:
                raise Exception(f"== expects 2 arguments, got {len(arg_codes)}")
            return f'lisp_eq({arg_codes[0]}, {arg_codes[1]})'
        
        else:
            raise Exception(f"Unknown built-in function: {func_name}")
        
    def _generate_if(self, node: ASTIf) -> str:
        cond = self._generate_expr(node.condition)
        then_branch = self._generate_expr(node.then_branch)
        
        cond_var = f"_cond_{self.temp_counter}"
        result_var = f"_result_{self.temp_counter}"
        self.temp_counter += 1
        
        if node.else_branch:
            else_branch = self._generate_expr(node.else_branch)
            return f"""({{
        LispObject* {cond_var} = {cond};
        LispObject* {result_var};
        if ({cond_var} != LISP_NIL) {{
            {result_var} = {then_branch};
        }} else {{
            {result_var} = {else_branch};
        }}
        {result_var};
    }})"""
        else:
            return f"""({{
        LispObject* {cond_var} = {cond};
        LispObject* {result_var};
        if ({cond_var} != LISP_NIL) {{
            {result_var} = {then_branch};
        }} else {{
            {result_var} = LISP_NIL;
        }}
        {result_var};
    }})"""