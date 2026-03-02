#include <iostream>
#include <windows.h>
#pragma comment(lib, "user32.lib")
using namespace std;

int main()
{
    // 循环输出，让进程持续运行（方便注入）
    cout << "PID:" << GetCurrentProcessId() << endl;
    cout << "Press to quit..." << endl;
    while (true)
    {
        Sleep(1000); // 每秒循环一次
        cout << "Running..." << endl;
        if (GetAsyncKeyState(VK_ESCAPE) & 0x8000)
        { // 按ESC退出
            break;
        }
    }
    return 0;
}