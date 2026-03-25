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
        # print(f"DEBUG: Generating literal: {node.value}, type: {type(node.value)}")
        if isinstance(node.value, bool):
            return 'LISP_T' if node.value else 'LISP_NIL'
        if isinstance(node.value, int):
            return f'make_integer({node.value})'
        elif isinstance(node.value, float):
            return f'make_float({node.value})'
        elif isinstance(node.value, str):
            escaped = node.value.replace('\\', '\\\\').replace('"', '\\"')
            return f'make_string("{escaped}")'
        else:
            raise NotImplementedError(f"Unknown literal: {type(node.value)}")
    
    def _generate_call(self, node: ASTCall) -> str:
        func_name = node.function.name
        
        if not node.args:
            args_list = 'LISP_NIL'
        else:
            args_list = 'LISP_NIL'
            for arg in reversed(node.args):
                arg_code = self._generate_expr(arg)
                args_list = f'make_cons({arg_code}, {args_list})'
        
        if func_name == 'print':
            return f'lisp_print({args_list})'
        elif func_name == '+':
            return f'lisp_add({args_list})'
        elif func_name == '-':
            return f'lisp_sub({args_list})'
        elif func_name == '*':
            return f'lisp_mul({args_list})'
        elif func_name == '/':
            return f'lisp_div({args_list})'
        elif func_name == '>':
            return f'lisp_gt({args_list})'
        elif func_name == '>=':
            return f'lisp_ge({args_list})'
        elif func_name == '<':
            return f'lisp_lt({args_list})'
        elif func_name == '<=':
            return f'lisp_le({args_list})'
        elif func_name == '==':
            return f'lisp_eq({args_list})'
        elif func_name == 'car':
            return f'lisp_car({args_list})'
        elif func_name == 'cdr':
            return f'lisp_cdr({args_list})'
        elif func_name == 'cons':
            return f'lisp_cons({args_list})'
        elif func_name == 'null?':
            return f'lisp_null({args_list})'
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