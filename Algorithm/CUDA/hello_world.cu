#include <stdio.h>
#include "cuda_runtime.h"

__global__ void hello_from_gpu()
{
    printf("Hello World!\n");
}

int main(void)
{
    hello_from_gpu<<<2, 2>>>();
    cudaDeviceSynchronize();
    return 0;
}