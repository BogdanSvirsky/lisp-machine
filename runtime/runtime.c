#include "runtime.h"

LispObject LISP_NIL_OBJ = {
    .type = TYPE_CONS,
    .value.cons.car = NULL,
    .value.cons.cdr = NULL
};

LispObject LISP_T_OBJ = {
    .type = TYPE_BOOLEAN,
    .value.bool_val = 1
};

LispObject* make_integer(int n) {
    LispObject* obj = malloc(sizeof(LispObject));
    if (!obj) {
        fprintf(stderr, "Error: memory allocation failed\n");
        exit(1);
    }
    obj->type = TYPE_INT;
    obj->value.int_val = n;
    return obj;
}

LispObject* make_float(double f) {
    LispObject* obj = malloc(sizeof(LispObject));
    if (!obj) {
        fprintf(stderr, "Error: memory allocation failed\n");
        exit(1);
    }
    obj->type = TYPE_FLOAT;
    obj->value.float_val = f;
    return obj;
}

LispObject* make_string(const char* str) {
    LispObject* obj = malloc(sizeof(LispObject));
    if (!obj) {
        fprintf(stderr, "Error: memory allocation failed\n");
        exit(1);
    }
    obj->type = TYPE_STRING;
    obj->value.str_val = strdup(str);
    if (!obj->value.str_val) {
        fprintf(stderr, "Error: memory allocation failed\n");
        free(obj);
        exit(1);
    }
    return obj;
}

LispObject* make_boolean(int b) {
    return b ? LISP_T : LISP_NIL;
}

LispObject* make_cons(LispObject* car, LispObject* cdr) {
    LispObject* obj = malloc(sizeof(LispObject));
    if (!obj) {
        fprintf(stderr, "Error: memory allocation failed\n");
        exit(1);
    }
    obj->type = TYPE_CONS;
    obj->value.cons.car = car;
    obj->value.cons.cdr = cdr;
    return obj;
}

LispObject* make_function(LispObject* (*func)(LispObject*)) {
    LispObject* obj = malloc(sizeof(LispObject));
    if (!obj) {
        fprintf(stderr, "Error: memory allocation failed\n");
        exit(1);
    }
    obj->type = TYPE_FUNCTION;
    obj->value.func_val = func;
    return obj;
}

LispObject* car(LispObject* obj) {
    if (obj == LISP_NIL) {
        fprintf(stderr, "Error: car of nil\n");
        exit(1);
    }
    if (obj->type != TYPE_CONS) {
        fprintf(stderr, "Error: car called on non-cons\n");
        exit(1);
    }
    return obj->value.cons.car;
}

LispObject* cdr(LispObject* obj) {
    if (obj == LISP_NIL) {
        fprintf(stderr, "Error: cdr of nil\n");
        exit(1);
    }
    if (obj->type != TYPE_CONS) {
        fprintf(stderr, "Error: cdr called on non-cons\n");
        exit(1);
    }
    return obj->value.cons.cdr;
}

int length(LispObject* list) {
    int len = 0;
    LispObject* current = list;
    while (current != LISP_NIL && current->type == TYPE_CONS) {
        len++;
        current = cdr(current);
    }
    return len;
}

LispObject* get_arg(int n, LispObject* args) {
    LispObject* current = args;
    for (int i = 0; i < n; i++) {
        if (current == LISP_NIL || current->type != TYPE_CONS) {
            fprintf(stderr, "Error: not enough arguments (need %d)\n", n + 1);
            exit(1);
        }
        current = cdr(current);
    }
    if (current == LISP_NIL || current->type != TYPE_CONS) {
        fprintf(stderr, "Error: argument %d not found\n", n);
        exit(1);
    }
    return car(current);
}

double to_double(LispObject* obj) {
    if (obj->type == TYPE_INT) {
        return (double)obj->value.int_val;
    } else if (obj->type == TYPE_FLOAT) {
        return obj->value.float_val;
    } else {
        fprintf(stderr, "Error: expected number, got type %d\n", obj->type);
        exit(1);
    }
}

typedef struct {
    char* name;
    LispObject* (*func)(LispObject*);
} FunctionEntry;

static FunctionEntry function_table[100];
static int function_count = 0;

void lisp_define(const char* name, LispObject* (*func)(LispObject*)) {
    function_table[function_count].name = strdup(name);
    function_table[function_count].func = func;
    function_count++;
}

LispObject* lisp_lookup(const char* name) {
    for (int i = 0; i < function_count; i++) {
        if (strcmp(function_table[i].name, name) == 0) {
            return make_function(function_table[i].func);
        }
    }
    return LISP_NIL;
}

LispObject* lisp_apply(LispObject* args) {
    LispObject* fn_obj = get_arg(0, args);
    LispObject* arg_list = get_arg(1, args);
    
    if (fn_obj->type != TYPE_FUNCTION) {
        fprintf(stderr, "Error: apply expects a function, got type %d\n", fn_obj->type);
        exit(1);
    }
    
    LispObject* (*func)(LispObject*) = fn_obj->value.func_val;
    return func(arg_list);
}

LispObject* lisp_add(LispObject* args) {
    if (args == LISP_NIL) return make_integer(0);
    
    double sum = 0.0;
    int is_int = 1;
    LispObject* current = args;
    
    while (current != LISP_NIL && current->type == TYPE_CONS) {
        LispObject* arg = car(current);
        sum += to_double(arg);
        if (arg->type != TYPE_INT) is_int = 0;
        current = cdr(current);
    }
    
    if (is_int && sum == (int)sum) {
        return make_integer((int)sum);
    }
    return make_float(sum);
}

LispObject* lisp_sub(LispObject* args) {
    int argc = length(args);
    if (argc == 0) {
        fprintf(stderr, "Error: - expects at least 1 argument\n");
        exit(1);
    }
    
    double result = to_double(get_arg(0, args));
    int is_int = (get_arg(0, args)->type == TYPE_INT);
    
    for (int i = 1; i < argc; i++) {
        LispObject* arg = get_arg(i, args);
        result -= to_double(arg);
        if (arg->type != TYPE_INT) is_int = 0;
    }
    
    if (is_int && result == (int)result) {
        return make_integer((int)result);
    }
    return make_float(result);
}

LispObject* lisp_mul(LispObject* args) {
    if (args == LISP_NIL) return make_integer(1);
    
    double product = 1.0;
    int is_int = 1;
    LispObject* current = args;
    
    while (current != LISP_NIL && current->type == TYPE_CONS) {
        LispObject* arg = car(current);
        product *= to_double(arg);
        if (arg->type != TYPE_INT) is_int = 0;
        current = cdr(current);
    }
    
    if (is_int && product == (int)product) {
        return make_integer((int)product);
    }
    return make_float(product);
}

LispObject* lisp_div(LispObject* args) {
    int argc = length(args);
    if (argc == 0) {
        fprintf(stderr, "Error: / expects at least 1 argument\n");
        exit(1);
    }
    
    double result = to_double(get_arg(0, args));
    int is_int = (get_arg(0, args)->type == TYPE_INT);
    
    for (int i = 1; i < argc; i++) {
        LispObject* arg = get_arg(i, args);
        double divisor = to_double(arg);
        if (divisor == 0.0) {
            fprintf(stderr, "Error: division by zero\n");
            exit(1);
        }
        result /= divisor;
        if (arg->type != TYPE_INT) is_int = 0;
    }
    
    if (is_int && result == (int)result) {
        return make_integer((int)result);
    }
    return make_float(result);
}

LispObject* lisp_gt(LispObject* args) {
    if (length(args) != 2) {
        fprintf(stderr, "Error: > expects 2 arguments\n");
        exit(1);
    }
    double a = to_double(get_arg(0, args));
    double b = to_double(get_arg(1, args));
    return make_boolean(a > b);
}

LispObject* lisp_ge(LispObject* args) {
    if (length(args) != 2) {
        fprintf(stderr, "Error: >= expects 2 arguments\n");
        exit(1);
    }
    double a = to_double(get_arg(0, args));
    double b = to_double(get_arg(1, args));
    return make_boolean(a >= b);
}

LispObject* lisp_lt(LispObject* args) {
    if (length(args) != 2) {
        fprintf(stderr, "Error: < expects 2 arguments\n");
        exit(1);
    }
    double a = to_double(get_arg(0, args));
    double b = to_double(get_arg(1, args));
    return make_boolean(a < b);
}

LispObject* lisp_le(LispObject* args) {
    if (length(args) != 2) {
        fprintf(stderr, "Error: <= expects 2 arguments\n");
        exit(1);
    }
    double a = to_double(get_arg(0, args));
    double b = to_double(get_arg(1, args));
    return make_boolean(a <= b);
}

LispObject* lisp_eq(LispObject* args) {
    if (length(args) != 2) {
        fprintf(stderr, "Error: == expects 2 arguments\n");
        exit(1);
    }
    double a = to_double(get_arg(0, args));
    double b = to_double(get_arg(1, args));
    return make_boolean(a == b);
}

void print_object(LispObject* obj) {
    switch (obj->type) {
        case TYPE_INT:
            printf("%d", obj->value.int_val);
            break;
        case TYPE_FLOAT:
            if (obj->value.float_val == (int)obj->value.float_val) {
                printf("%.1f", obj->value.float_val);
            } else {
                printf("%g", obj->value.float_val);
            }
            break;
        case TYPE_STRING:
            printf("%s", obj->value.str_val);
            break;
        case TYPE_BOOLEAN:
            printf("%s", obj->value.bool_val ? "t" : "nil");
            break;
        case TYPE_CONS:
            printf("(");
            LispObject* current = obj;
            while (current != LISP_NIL && current->type == TYPE_CONS) {
                print_object(car(current));
                current = cdr(current);
                if (current != LISP_NIL && current->type == TYPE_CONS) {
                    printf(" ");
                }
            }
            if (current != LISP_NIL) {
                printf(" . ");
                print_object(current);
            }
            printf(")");
            break;
        case TYPE_FUNCTION:
            printf("#<function>");
            break;
        default:
            printf("#<unknown>");
            break;
    }
}

LispObject* lisp_print(LispObject* args) {
    LispObject* obj = get_arg(0, args);
    print_object(obj);
    printf("\n");
    return obj;
}

LispObject* lisp_car(LispObject* args) {
    LispObject* list = get_arg(0, args);
    return car(list);
}

LispObject* lisp_cdr(LispObject* args) {
    LispObject* list = get_arg(0, args);
    return cdr(list);
}

LispObject* lisp_cons(LispObject* args) {
    LispObject* a = get_arg(0, args);
    LispObject* b = get_arg(1, args);
    return make_cons(a, b);
}

LispObject* lisp_null(LispObject* args) {
    LispObject* obj = get_arg(0, args);
    return make_boolean(obj == LISP_NIL);
}