#include <stdio.h>
#include <stdlib.h>

int factorial(int n) {
	//初始情况需要根据n变化方向、变化步长的最大值来决定
	if (n == 0) {
		return 1;
	}
	else {
		//可以看出n不断减小，每次减小1，必然命中n==0
		return n * factorial(n - 1);
	}
}

int Fibonacci(int n) {
	//初始情况包含0和1
	if (n <= 1) {
		return 1;
	}
	else {
		//n不断减小，n=2时下一次迭代对n=0和n=1进行处理
		//n=0和n=1满足初始情况，命中
		return Fibonacci(n - 1) + Fibonacci(n - 2);
	}
}

void perm(int list[], int k, int m, int length) {
	//所谓全排列，即是每一位数字分别和之后的每一位可排列数字交换得到
	if (k == m) {
		for (int i = 0; i < length; i++) {
			printf("%d ", list[i]);
		}
		printf("\n");
	}
	else
	{
		for (int i = k; i <= m; i++) {
			//对第i个数和第k个数进行交换，i是介于（包括）m到k之间的index
			//注意，如果i不取m，实际可交换（排列）的范围只有k到m-1
			//之前遇到的情况是1到3，m取不到的话实际只有1到2，也就是两个数排序
			int temp = list[i];
			list[i] = list[k];
			list[k] = temp;

			//对交换后得到的序列的剩下k+1到m之间的数继续排列
			perm(list, k + 1, m, length);

			//还原之前的交换操作以保证下次循环用的还是相同的list
			list[k] = list[i];
			list[i] = temp;
		}
	}
}


void main_Recursion() {
	int result = factorial(7);
	result = Fibonacci(9);
	int list[5] = { 0,1,2,3,4 };
	perm(list, 1, 3, 5);
}