from parser.ast import *


class CCodeGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.functions = []
        self.current_function = None
        self.current_params = []
    
    def generate(self, ast: ASTProgram) -> str:
        code = []

        code.append('#include "runtime/runtime.h"\n\n')

        for expr in ast.expressions:
            if isinstance(expr, ASTDefun):
                func_code = self._generate_defun(expr)
                self.functions.append(func_code)

        for func_code in self.functions:
            code.append(func_code)
            code.append('\n\n')
        
        code.append('int main() {\n')
        code.append('    lisp_init();\n\n')

        for expr in ast.expressions:
            if isinstance(expr, ASTDefun):
                code.append(f'    lisp_define("{expr.name}", {expr.name});\n')

        code.append('\n')

        for expr in ast.expressions:
            if not isinstance(expr, ASTDefun):
                c_expr = self._generate_expr(expr, tail=False)
                code.append(f'    {c_expr};\n')

        code.append('    return 0;\n')
        code.append('}\n')

        return ''.join(code)

    def _generate_defun(self, node: ASTDefun) -> str:
        self.current_function = node.name
        self.current_params = node.params
        
        code = []
        code.append(f'LispObject* {node.name}(LispObject* args) {{')

        for i, param in enumerate(node.params):
            code.append(f'    LispObject* {param} = get_arg({i}, args);')
        
        code.append(f'start_{node.name}:')
        
        body_code = self._generate_expr(node.body, tail=True)
        code.append(f'    return {body_code};')
        code.append('}')
        
        self.current_function = None
        self.current_params = []
        
        return '\n'.join(code)
    
    def _generate_expr(self, node: ASTNode, tail: bool = False) -> str:
        if isinstance(node, ASTLiteral):
            return self._generate_literal(node)
        elif isinstance(node, ASTSymbol):
            return self._generate_symbol(node)
        elif isinstance(node, ASTCall):
            return self._generate_call(node, tail)
        elif isinstance(node, ASTIf):
            return self._generate_if(node, tail)
        elif isinstance(node, ASTLet):
            return self._generate_let(node)
        elif isinstance(node, ASTProgram):
            return self._generate_progn(node)
        elif isinstance(node, ASTAnd):
            return self._generate_and(node, tail)
        elif isinstance(node, ASTOr):
            return self._generate_or(node, tail)
        else:
            raise NotImplementedError(f"Unknown node: {type(node)}")

    def _generate_literal(self, node: ASTLiteral) -> str:
        if isinstance(node.value, bool):
            return 'LISP_T' if node.value else 'LISP_NIL'
        elif isinstance(node.value, int):
            return f'make_integer({node.value})'
        elif isinstance(node.value, float):
            return f'make_float({node.value})'
        elif isinstance(node.value, str):
            escaped = node.value.replace('\\', '\\\\').replace('"', '\\"')
            return f'make_string("{escaped}")'
        else:
            raise NotImplementedError(f"Unknown literal: {type(node.value)}")

    def _generate_symbol(self, node: ASTSymbol) -> str:
        return node.name
    
    def _generate_call(self, node: ASTCall, tail: bool = False) -> str:
        func_name = node.function.name

        if not node.args:
            args_list = 'LISP_NIL'
        else:
            args_list = 'LISP_NIL'
            for arg in reversed(node.args):
                arg_code = self._generate_expr(arg, tail=False)
                args_list = f'make_cons({arg_code}, {args_list})'

        builtins_map = {
            '+': 'add',
            '-': 'sub',
            '*': 'mul',
            '/': 'div',
            '>': 'gt',
            '>=': 'ge',
            '<': 'lt',
            '<=': 'le',
            '==': 'eq',
            'print': 'print',
            'car': 'car',
            'cdr': 'cdr',
            'cons': 'cons',
            'null?': 'null'
        }

        if func_name in builtins_map:
            return f'lisp_{builtins_map[func_name]}({args_list})'
        
        if tail and func_name == self.current_function:
            return self._generate_tail_call(node)
        else:
            apply_args = f'make_cons(lisp_lookup("{func_name}"), make_cons({args_list}, LISP_NIL))'
            return f'lisp_apply({apply_args})'
    
    def _generate_tail_call(self, node: ASTCall) -> str:
        updates = []
        
        updates.append(f'')
        
        for i, arg in enumerate(node.args):
            arg_code = self._generate_expr(arg, tail=False)
            temp_var = f"_new_{self.current_params[i]}"
            updates.append(f'            LispObject* {temp_var} = {arg_code};')
        
        for i, param in enumerate(self.current_params):
            temp_var = f"_new_{param}"
            updates.append(f'            {param} = {temp_var};')
        
        updates.append(f'            goto start_{self.current_function}')
        
        return '\n'.join(updates)
    
    def _generate_if(self, node: ASTIf, tail: bool = False) -> str:
        cond = self._generate_expr(node.condition, tail=False)
        then_branch = self._generate_expr(node.then_branch, tail)
        cond_var = f"_cond_{self.temp_counter}"
        result_var = f"_result_{self.temp_counter}"
        self.temp_counter += 1

        if node.else_branch:
            else_branch = self._generate_expr(node.else_branch, tail)
            
            is_then_tail = self._is_tail_call(node.then_branch)
            is_else_tail = self._is_tail_call(node.else_branch)
            
            if is_then_tail and is_else_tail:
                return f"""({{
        LispObject* {cond_var} = {cond};
        if ({cond_var} != LISP_NIL) {{
            {then_branch};
        }} else {{
            {else_branch};
        }}
        return LISP_NIL;  // никогда не выполнится
    }})"""
            elif is_then_tail:
                return f"""({{
        LispObject* {cond_var} = {cond};
        LispObject* {result_var};
        if ({cond_var} != LISP_NIL) {{
            {then_branch};
        }} else {{
            {result_var} = {else_branch};
        }}
        {result_var};
    }})"""
            elif is_else_tail:
                return f"""({{
        LispObject* {cond_var} = {cond};
        LispObject* {result_var};
        if ({cond_var} != LISP_NIL) {{
            {result_var} = {then_branch};
        }} else {{
            {else_branch};
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
    
    def _generate_let(self, node: ASTLet, tail: bool = False) -> str:
        code = []
        code.append('({')

        for name, value in node.bindings:
            val_code = self._generate_expr(value, tail=False)
            code.append(f'    LispObject* {name} = {val_code};')
        
        body_code = self._generate_expr(node.body, tail)
        code.append(f'    {body_code};')
        code.append('})')
        
        return '\n'.join(code)
      
    
    def _generate_progn(self, node: ASTProgram) -> str:
        return '({' + ';'.join([self._generate_expr(node)
                                for node in node.expressions]) + ';})'
    
    def _is_tail_call(self, node: ASTNode) -> bool:
        if not isinstance(node, ASTCall):
            return False
        if node.function.name != self.current_function:
            return False
        return True

    def _generate_and(self, node: ASTAnd, tail: bool = False) -> str:
        if not node.args:
            return 'LISP_T'
        
        if len(node.args) == 1:
            return self._generate_expr(node.args[0], tail)
        
        result_var = f"_and_{self.temp_counter}"
        self.temp_counter += 1
        
        code = []
        code.append(f'LispObject* {result_var} = LISP_T;')
        
        for i, arg in enumerate(node.args[:-1]):
            arg_code = self._generate_expr(arg, tail=False)
            code.append(f'LispObject* _tmp_{i} = {arg_code};')
            code.append(f'if (_tmp_{i} == LISP_NIL) {{')
            code.append(f'    {result_var} = LISP_NIL;')
            code.append(f'    goto and_end_{self.temp_counter};')
            code.append(f'}}')
        
        last_code = self._generate_expr(node.args[-1], tail=False)
        code.append(f'{result_var} = {last_code};')
        code.append(f'and_end_{self.temp_counter}:')
        code.append(f'{result_var};')
        
        result = '\n'.join(code)
        
        return f'({{\n{result}\n}})'

    def _generate_or(self, node: ASTOr, tail: bool = False) -> str:
        if not node.args:
            return 'LISP_NIL'
        
        if len(node.args) == 1:
            return self._generate_expr(node.args[0], tail)
        
        result_var = f"_or_{self.temp_counter}"
        self.temp_counter += 1
        
        code = []
        code.append(f'LispObject* {result_var} = LISP_NIL;')
        
        for i, arg in enumerate(node.args[:-1]):
            arg_code = self._generate_expr(arg, tail=False)
            code.append(f'LispObject* _tmp_{i} = {arg_code};')
            code.append(f'if (_tmp_{i} != LISP_NIL) {{')
            code.append(f'    {result_var} = _tmp_{i};')
            code.append(f'    goto or_end_{self.temp_counter};')
            code.append(f'}}')
        
        last_code = self._generate_expr(node.args[-1], tail=False)
        code.append(f'{result_var} = {last_code};')
        code.append(f'or_end_{self.temp_counter}:')
        code.append(f'{result_var};')
        
        result = '\n'.join(code)
        
        return f'({{\n{result}\n}})'