#include <windows.h>
#include <iostream>
#include <tlhelp32.h>
#include <cwchar>
#include <psapi.h> // 用于校验进程位数
#pragma comment(lib, "kernel32.lib")
#pragma comment(lib, "psapi.lib")

using namespace std;

// 校验进程位数（x86/x64），避免位数不匹配崩溃
BOOL CheckProcessArch(DWORD pid, BOOL &isX64)
{
    HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, pid);
    if (!hProcess)
        return FALSE;

    BOOL isWow64 = FALSE;
    IsWow64Process(hProcess, &isWow64);

// 判断目标进程位数：当前注入器是x64时，!isWow64表示目标是x64；注入器是x86时，目标只能是x86
#ifdef _WIN64
    isX64 = !isWow64;
#else
    isX64 = FALSE;
    if (isWow64)
    { // 注入器x86，目标x64 → 位数不匹配
        CloseHandle(hProcess);
        return FALSE;
    }
#endif

    CloseHandle(hProcess);
    return TRUE;
}

// 获取进程PID（保留你的Unicode逻辑，修复无问题）
DWORD GetProcessIdByName(LPCWSTR processName)
{
    DWORD pid = 0;
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (hSnapshot == INVALID_HANDLE_VALUE)
    {
        wcout << L"Failed to create process snapshot, Error Code: " << GetLastError() << endl;
        return 0;
    }

    PROCESSENTRY32W pe32;
    pe32.dwSize = sizeof(PROCESSENTRY32W);

    if (Process32FirstW(hSnapshot, &pe32))
    {
        do
        {
            if (wcscmp(pe32.szExeFile, processName) == 0)
            {
                pid = pe32.th32ProcessID;
                break;
            }
        } while (Process32NextW(hSnapshot, &pe32));
    }
    else
    {
        wcout << L"Failed to iterate processes, Error Code: " << GetLastError() << endl;
    }

    CloseHandle(hSnapshot);
    return pid;
}

// 修复后的注入函数（核心修改）
BOOL InjectDll(DWORD pid, LPCSTR dllPath)
{
    // 1. 检查DLL文件是否存在
    if (GetFileAttributesA(dllPath) == INVALID_FILE_ATTRIBUTES)
    {
        cout << "Error: DLL file does not exist! Path: " << dllPath << endl;
        return FALSE;
    }

    // 2. 校验注入器与目标进程位数是否匹配
    BOOL isTargetX64 = FALSE;
    if (!CheckProcessArch(pid, isTargetX64))
    {
        cout << "Error: Injector and target process architecture mismatch (x86/x64)!" << endl;
        return FALSE;
    }
#ifdef _WIN64
    if (!isTargetX64)
    {
        cout << "Error: Injector is x64, target process is x86!" << endl;
        return FALSE;
    }
#else
    if (isTargetX64)
    {
        cout << "Error: Injector is x86, target process is x64!" << endl;
        return FALSE;
    }
#endif

    // 3. 打开进程：使用最小必要权限（关键修复）
    DWORD dwProcessAccess = PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION |
                            PROCESS_VM_OPERATION | PROCESS_VM_WRITE | PROCESS_VM_READ;
    HANDLE hProcess = OpenProcess(dwProcessAccess, FALSE, pid);
    if (hProcess == NULL)
    {
        cout << "Failed to open process, Error Code: " << GetLastError() << endl;
        cout << "Tip: Run injector as administrator!" << endl;
        return FALSE;
    }

    // 4. 分配远程内存（存储DLL路径）
    SIZE_T dllPathLen = strlen(dllPath) + 1;
    LPVOID pRemoteMem = VirtualAllocEx(hProcess, NULL, dllPathLen, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (pRemoteMem == NULL)
    {
        cout << "Failed to allocate remote memory, Error Code: " << GetLastError() << endl;
        CloseHandle(hProcess);
        return FALSE;
    }

    // 5. 写入DLL路径到目标进程
    SIZE_T writeSize = 0;
    BOOL ret = WriteProcessMemory(hProcess, pRemoteMem, dllPath, dllPathLen, &writeSize);
    if (!ret || writeSize != dllPathLen)
    {
        cout << "Failed to write to remote memory, Error Code: " << GetLastError() << endl;
        VirtualFreeEx(hProcess, pRemoteMem, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return FALSE;
    }

    // 6. 创建远程线程（不无限等待，关键修复）
    HANDLE hRemoteThread = CreateRemoteThread(hProcess, NULL, 0,
                                              (LPTHREAD_START_ROUTINE)LoadLibraryA,
                                              pRemoteMem, 0, NULL);
    if (hRemoteThread == NULL)
    {
        cout << "Failed to create remote thread, Error Code: " << GetLastError() << endl;
        VirtualFreeEx(hProcess, pRemoteMem, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return FALSE;
    }

    // 7. 缩短等待时间（5秒），不强制等待完成（避免卡住）
    DWORD waitResult = WaitForSingleObject(hRemoteThread, 5000);
    if (waitResult == WAIT_TIMEOUT)
    {
        cout << "Warning: Remote thread is still running (DLL loading may take time)!" << endl;
    }
    else if (waitResult == WAIT_FAILED)
    {
        cout << "Failed to wait for remote thread, Error Code: " << GetLastError() << endl;
    }

    // 8. 检查LoadLibraryA是否加载成功（获取线程退出码）
    DWORD exitCode = 0;
    if (GetExitCodeThread(hRemoteThread, &exitCode))
    {
        if (exitCode == NULL)
        {
            cout << "Failed to load DLL! LoadLibraryA returned NULL." << endl;
        }
        else
        {
            cout << "DLL injected successfully! LoadLibraryA return handle: 0x" << hex << exitCode << endl;
        }
    }

    // 9. 释放资源（延迟释放内存，避免崩溃）
    CloseHandle(hRemoteThread);
    // 注释：不立即释放pRemoteMem，进程退出后系统会自动回收，避免DLL加载时引用失效
    // VirtualFreeEx(hProcess, pRemoteMem, 0, MEM_RELEASE);
    CloseHandle(hProcess);

    return exitCode != NULL;
}

int main()
{
    // 设置控制台编码
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    // 目标进程名（宽字符）+ DLL绝对路径
    LPCWSTR targetProcess = L"FZU.exe";
    LPCSTR dllPath = "C:\\Users\\16413\\Documents\\GitHub\\FuckYouFZU\\Pee.dll";

    // 获取PID
    DWORD pid = GetProcessIdByName(targetProcess);
    if (pid == 0)
    {
        wcout << L"Process not found: " << targetProcess << endl;
        system("pause");
        return 1;
    }
    wcout << L"Process found, PID: " << dec << pid << endl;

    // 执行注入
    if (!InjectDll(pid, dllPath))
    {
        system("pause");
        return 1;
    }

    system("pause");
    return 0;
}