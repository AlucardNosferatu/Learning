#include <stdio.h>
#include <stdlib.h>

typedef struct complex {
    float im;
    float re;
} cx;
typedef cx *Cx;


Cx Init(float re, float im) {
    Cx cx_instance = malloc(sizeof(cx));
    if (cx_instance)
    {
        cx_instance->im = im;
        cx_instance->re = re;
        return cx_instance;
    }
    else {
        return NULL;
    }
}


Cx Add(Cx Cx_A, Cx Cx_B) {
    Cx cx_instance = malloc(sizeof(cx));
    if (cx_instance)
    {
        cx_instance->im = Cx_A->im + Cx_B->im;
        cx_instance->re = Cx_A->re + Cx_B->re;
        return cx_instance;
    }
    else {
        return NULL;
    }
}

Cx Minus(Cx Cx_A, Cx Cx_B) {
    Cx cx_instance = malloc(sizeof(cx));
    if (cx_instance)
    {
        cx_instance->im = Cx_A->im - Cx_B->im;
        cx_instance->re = Cx_A->re - Cx_B->re;
        return cx_instance;
    }
    else {
        return NULL;
    }
}

Cx Mult(Cx Cx_A, Cx Cx_B) {
    Cx cx_instance = malloc(sizeof(cx));
    if (cx_instance)
    {
        float a = Cx_A->re;
        float b = Cx_A->im;
        float c = Cx_B->re;
        float d = Cx_B->im;
        cx_instance->im = (a * d + b * c);
        cx_instance->re = (a * c - b * d);
        return cx_instance;
    }
    else {
        return NULL;
    }
}

Cx Divi(Cx Cx_A, Cx Cx_B) {
    Cx cx_instance = malloc(sizeof(cx));
    if (cx_instance)
    {
        float a = Cx_A->re;
        float b = Cx_A->im;
        float c = Cx_B->re;
        float d = Cx_B->im;
        cx_instance->im = (b * c - a * d) / (c * c + d * d);
        cx_instance->re = (a * c + b * d) / (c * c + d * d);
        return cx_instance;
    }
    else {
        return NULL;
    }
}

void main() {
    Cx Cx_A = Init(1.0, 2.0);
    Cx Cx_B = Init(3.0, 7.0);
    Cx Cx_C = Divi(Cx_A, Cx_B);
    printf("re:%f im:%f",Cx_C->re,Cx_C->im);
    free(Cx_A);
    free(Cx_B);
    free(Cx_C);
    Cx_A = NULL;
    Cx_B = NULL;
    Cx_C = NULL;
}