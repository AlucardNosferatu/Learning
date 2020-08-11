#include <stdio.h>
#include <stdlib.h>

int factorial(int n) {
	//��ʼ�����Ҫ����n�仯���򡢱仯���������ֵ������
	if (n == 0) {
		return 1;
	}
	else {
		//���Կ���n���ϼ�С��ÿ�μ�С1����Ȼ����n==0
		return n * factorial(n - 1);
	}
}

int Fibonacci(int n) {
	//��ʼ�������0��1
	if (n <= 1) {
		return 1;
	}
	else {
		//n���ϼ�С��n=2ʱ��һ�ε�����n=0��n=1���д���
		//n=0��n=1�����ʼ���������
		return Fibonacci(n - 1) + Fibonacci(n - 2);
	}
}

void perm(int list[], int k, int m, int length) {
	//��νȫ���У�����ÿһλ���ֱַ��֮���ÿһλ���������ֽ����õ�
	if (k == m) {
		for (int i = 0; i < length; i++) {
			printf("%d ", list[i]);
		}
		printf("\n");
	}
	else
	{
		for (int i = k; i <= m; i++) {
			//�Ե�i�����͵�k�������н�����i�ǽ��ڣ�������m��k֮���index
			//ע�⣬���i��ȡm��ʵ�ʿɽ��������У��ķ�Χֻ��k��m-1
			//֮ǰ�����������1��3��mȡ�����Ļ�ʵ��ֻ��1��2��Ҳ��������������
			int temp = list[i];
			list[i] = list[k];
			list[k] = temp;

			//�Խ�����õ������е�ʣ��k+1��m֮�������������
			perm(list, k + 1, m, length);

			//��ԭ֮ǰ�Ľ��������Ա�֤�´�ѭ���õĻ�����ͬ��list
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