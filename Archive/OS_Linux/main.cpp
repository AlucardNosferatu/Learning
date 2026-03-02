#include <cstdio>
#include <stdlib.h>
#include <sys/utsname.h>

int main()
{
    char* name;
    char* path;

    name = getenv("LOGNAME");
    path = getenv("PWD");

    printf("logname = %s\n", name);
    printf("pwd = %s\n", path);


    struct utsname buf;

    if (uname(&buf))
    {
        perror("uname");
        exit(1);
    }

    //printf("sysname:%s\n", buf.sysname);
    //printf("nodename:%s\n", buf.nodename);
    printf("release:%s\n", buf.release);
    printf("version:%s\n", buf.version);
    printf("machine:%s\n", buf.machine);

    return 0;
}