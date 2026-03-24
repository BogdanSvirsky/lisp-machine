#include "runtime.h"

LispObject LISP_NIL_OBJ = {
    .type = TYPE_BOOLEAN,
    .value.bool_val = 0
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

static double to_double(LispObject* obj) {
    if (obj->type == TYPE_INT) {
        return (double)obj->value.int_val;
    } else if (obj->type == TYPE_FLOAT) {
        return obj->value.float_val;
    } else {
        fprintf(stderr, "Error: expected number, got type %d\n", obj->type);
        exit(1);
    }
}

LispObject* lisp_add(LispObject* a, LispObject* b) {
    double da = to_double(a);
    double db = to_double(b);
    double result = da + db;
    
    if (a->type == TYPE_INT && b->type == TYPE_INT && result == (int)result) {
        return make_integer((int)result);
    }
    return make_float(result);
}

LispObject* lisp_sub(LispObject* a, LispObject* b) {
    double da = to_double(a);
    double db = to_double(b);
    double result = da - db;
    
    if (a->type == TYPE_INT && b->type == TYPE_INT && result == (int)result) {
        return make_integer((int)result);
    }
    return make_float(result);
}

LispObject* lisp_mul(LispObject* a, LispObject* b) {
    double da = to_double(a);
    double db = to_double(b);
    double result = da * db;
    
    if (a->type == TYPE_INT && b->type == TYPE_INT && result == (int)result) {
        return make_integer((int)result);
    }
    return make_float(result);
}

LispObject* lisp_div(LispObject* a, LispObject* b) {
    double da = to_double(a);
    double db = to_double(b);
    
    if (db == 0.0) {
        fprintf(stderr, "Error: division by zero\n");
        exit(1);
    }
    
    double result = da / db;
    
    if (a->type == TYPE_INT && b->type == TYPE_INT && result == (int)result) {
        return make_integer((int)result);
    }
    return make_float(result);
}

LispObject* lisp_print(LispObject* obj) {
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
        default:
            printf("#<unknown>");
            break;
    }
    printf("\n");
    return obj;
}