#include <iostream>
#include <windows.h>
// 引入 Detours 头文件（需确保 detours/include 路径正确）
#include "Detours/detours.h"
using namespace std;

// 1. 禁止函数内联（避免编译器优化导致挂钩失效）
__declspec(noinline) void funcA()
{
    cout << "This is func A" << endl;
}

__declspec(noinline) void funcB()
{
    cout << "This is func B" << endl;
}

// 2. 声明函数指针：保存 funcB 的原始地址
typedef void (*FUNC_VOID)();
FUNC_VOID pOriginalFuncB = nullptr; // 原始 funcB 地址
bool isHooked = false;              // 标记是否已完成挂钩（避免重复操作）

// 3. 挂钩后的替换函数：直接调用 funcA
void HookedFuncB()
{
    // 跳转到 funcA（无需调用原始 funcB）
    funcA();
}

// 4. 执行 Detours 自挂钩的函数
void HookFuncBToFuncA()
{
    if (isHooked)
        return; // 已挂钩则直接返回

    // 初始化 Detours 事务（自挂钩核心）
    DetourTransactionBegin();
    // 更新当前线程（自挂钩只需挂起当前线程）
    DetourUpdateThread(GetCurrentThread());
    // 将 funcB 挂钩到 HookedFuncB
    DetourAttach((PVOID *)&pOriginalFuncB, HookedFuncB);
    // 提交挂钩事务
    LONG lError = DetourTransactionCommit();

    if (lError == NO_ERROR)
    {
        isHooked = true;
    }
    else
    {
        cout << "FAILED:" << lError << endl;
    }
}

int main()
{
    int i = 0;
    int count = 0; // 循环计数器
    // 初始化原始 funcB 地址（自挂钩直接取函数地址即可）
    pOriginalFuncB = funcB;

    while (true)
    {
        count++; // 每次循环计数器+1
        cout << "Count:" << count << endl;

        if (i == 0)
        {
            funcA();
        }
        else
        {
            funcB();
        }

        // 5. 计数器超过10次时触发挂钩
        if (count > 10 && !isHooked)
        {
            HookFuncBToFuncA();
        }

        i = 1 - i;
        Sleep(1000); // 每秒循环一次
    }
    return 0;
}