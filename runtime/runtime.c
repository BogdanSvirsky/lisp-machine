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

LispObject* lisp_add(LispObject* a, LispObject* b) {
    if (a->type != TYPE_INT || b->type != TYPE_INT) {
        fprintf(stderr, "Error: + expects integer arguments\n");
        exit(1);
    }
    return make_integer(a->value.int_val + b->value.int_val);
}

LispObject* lisp_sub(LispObject* a, LispObject* b) {
    if (a->type != TYPE_INT || b->type != TYPE_INT) {
        fprintf(stderr, "Error: - expects integer arguments\n");
        exit(1);
    }
    return make_integer(a->value.int_val - b->value.int_val);
}

LispObject* lisp_mul(LispObject* a, LispObject* b) {
    if (a->type != TYPE_INT || b->type != TYPE_INT) {
        fprintf(stderr, "Error: * expects integer arguments\n");
        exit(1);
    }
    return make_integer(a->value.int_val * b->value.int_val);
}

LispObject* lisp_div(LispObject* a, LispObject* b) {
    if (a->type != TYPE_INT || b->type != TYPE_INT) {
        fprintf(stderr, "Error: / expects integer arguments\n");
        exit(1);
    }
    if (b->value.int_val == 0) {
        fprintf(stderr, "Error: division by zero\n");
        exit(1);
    }
    return make_integer(a->value.int_val / b->value.int_val);
}

LispObject* lisp_print(LispObject* obj) {
    switch (obj->type) {
        case TYPE_INT:
            printf("%d", obj->value.int_val);
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