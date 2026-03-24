#ifndef RUNTIME_H
#define RUNTIME_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING,
    TYPE_BOOLEAN
} LispType;

typedef struct LispObject {
    LispType type;
    union {
        int int_val;
        double float_val;
        char* str_val;
        int bool_val;
    } value;
} LispObject;

extern LispObject LISP_NIL_OBJ;
extern LispObject LISP_T_OBJ;
#define LISP_NIL (&LISP_NIL_OBJ)
#define LISP_T (&LISP_T_OBJ)

LispObject* make_integer(int n);
LispObject* make_float(double f);
LispObject* make_string(const char* str);
LispObject* make_boolean(int b);

LispObject* lisp_add(LispObject* a, LispObject* b);
LispObject* lisp_sub(LispObject* a, LispObject* b);
LispObject* lisp_mul(LispObject* a, LispObject* b);
LispObject* lisp_div(LispObject* a, LispObject* b);

LispObject* lisp_print(LispObject* obj);

LispObject* lisp_gt(LispObject* a, LispObject* b);
LispObject* lisp_ge(LispObject* a, LispObject* b);
LispObject* lisp_lt(LispObject* a, LispObject* b);
LispObject* lisp_le(LispObject* a, LispObject* b);
LispObject* lisp_eq(LispObject* a, LispObject* b);

#endif