#ifndef RUNTIME_H
#define RUNTIME_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING,
    TYPE_BOOLEAN,
    TYPE_CONS
} LispType;

typedef struct LispObject {
    LispType type;
    union {
        int int_val;
        double float_val;
        char* str_val;
        int bool_val;
        struct {
            struct LispObject* car;
            struct LispObject* cdr;
        } cons;
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
LispObject* make_cons(LispObject* car, LispObject* cdr);

LispObject* car(LispObject* obj);
LispObject* cdr(LispObject* obj);
int length(LispObject* list);
LispObject* get_arg(int n, LispObject* args);
double to_double(LispObject* obj);

LispObject* lisp_add(LispObject* args);
LispObject* lisp_sub(LispObject* args);
LispObject* lisp_mul(LispObject* args);
LispObject* lisp_div(LispObject* args);

LispObject* lisp_gt(LispObject* args);
LispObject* lisp_ge(LispObject* args);
LispObject* lisp_lt(LispObject* args);
LispObject* lisp_le(LispObject* args);
LispObject* lisp_eq(LispObject* args);

LispObject* lisp_print(LispObject* args);

LispObject* lisp_car(LispObject* args);
LispObject* lisp_cdr(LispObject* args);
LispObject* lisp_cons(LispObject* args);
LispObject* lisp_null(LispObject* args);

#endif