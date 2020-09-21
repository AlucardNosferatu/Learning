#include <cstdio>
#include <stdlib.h>


int main()
{
    char* name;
    char* path;

    name = getenv("LOGNAME");
    path = getenv("PWD");

    printf("logname = %s\n", name);
    printf("pwd = %s\n", path);

    return 0;
}