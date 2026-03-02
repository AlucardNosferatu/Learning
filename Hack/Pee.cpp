#pragma execution_character_set("utf-8")
#include <Windows.h>
#include <string>
#include <cstring>
#include <ImageHlp.h>
#pragma comment(lib, "ImageHlp.lib")

// Define WriteFile function type
typedef BOOL(WINAPI *PFN_WriteFile)(
    HANDLE hFile,
    LPCVOID lpBuffer,
    DWORD nNumberOfBytesToWrite,
    LPDWORD lpNumberOfBytesWritten,
    LPOVERLAPPED lpOverlapped);

// Global variable: save original WriteFile address
PFN_WriteFile g_pOriginalWriteFile = nullptr;

// Core Hook function: only modify cout output
BOOL WINAPI MyWriteFile(
    HANDLE hFile,
    LPCVOID lpBuffer,
    DWORD nNumberOfBytesToWrite,
    LPDWORD lpNumberOfBytesWritten,
    LPOVERLAPPED lpOverlapped)
{
    // Only process console standard output
    if (hFile != GetStdHandle(STD_OUTPUT_HANDLE) || !lpBuffer || nNumberOfBytesToWrite == 0)
    {
        return g_pOriginalWriteFile(hFile, lpBuffer, nNumberOfBytesToWrite, lpNumberOfBytesWritten, lpOverlapped);
    }

    // Safe string conversion (avoid overflow)
    char buffer[1024] = {0};
    memcpy(buffer, lpBuffer, min(nNumberOfBytesToWrite, (DWORD)sizeof(buffer) - 1));
    std::string output = buffer;

    // Replace "Running..." with "Injected!!!"
    size_t pos = output.find("Running...");
    if (pos != std::string::npos)
    {
        output.replace(pos, 9, "Injected!!!");
    }

    // Call original function
    return g_pOriginalWriteFile(hFile, output.c_str(), output.length(), lpNumberOfBytesWritten, lpOverlapped);
}

// Correct IAT Hook logic (fix IMAGE_IMPORT_DESCRIPTOR type error)
BOOL HookIAT_WriteFile()
{
    // Get current process module base address
    HMODULE hModule = GetModuleHandle(NULL);
    if (!hModule)
        return FALSE;

    ULONG ulSize = 0;
    // Fix: Use PIMAGE_IMPORT_DESCRIPTOR (not PIMAGE_THUNK_DATA)
    PIMAGE_IMPORT_DESCRIPTOR pImportDesc = (PIMAGE_IMPORT_DESCRIPTOR)ImageDirectoryEntryToData(
        hModule, TRUE, IMAGE_DIRECTORY_ENTRY_IMPORT, &ulSize);
    if (!pImportDesc)
        return FALSE;

    // Traverse all imported DLLs
    while (pImportDesc->Name != 0)
    { // Fix: Use Name instead of Characteristics (more reliable)
        // Get DLL name
        char *szDllName = (char *)((BYTE *)hModule + pImportDesc->Name);
        if (_stricmp(szDllName, "kernel32.dll") == 0)
        {
            // Fix: Correctly get OriginalFirstThunk/FirstThunk from IMAGE_IMPORT_DESCRIPTOR
            PIMAGE_THUNK_DATA pOriginalThunk = (PIMAGE_THUNK_DATA)((BYTE *)hModule + pImportDesc->OriginalFirstThunk);
            PIMAGE_THUNK_DATA pFirstThunk = (PIMAGE_THUNK_DATA)((BYTE *)hModule + pImportDesc->FirstThunk);

            // Traverse imported functions of kernel32.dll
            while (pOriginalThunk->u1.AddressOfData != 0)
            {
                PIMAGE_IMPORT_BY_NAME pImportName = (PIMAGE_IMPORT_BY_NAME)((BYTE *)hModule + pOriginalThunk->u1.AddressOfData);
                if (_stricmp((char *)pImportName->Name, "WriteFile") == 0)
                {
                    // Save original function address
                    g_pOriginalWriteFile = (PFN_WriteFile)pFirstThunk->u1.Function;

                    // Modify IAT (safe memory write)
                    DWORD dwOldProtect = 0;
                    VirtualProtect(&pFirstThunk->u1.Function, sizeof(DWORD_PTR), PAGE_EXECUTE_READWRITE, &dwOldProtect);
                    pFirstThunk->u1.Function = (DWORD_PTR)MyWriteFile;
                    VirtualProtect(&pFirstThunk->u1.Function, sizeof(DWORD_PTR), dwOldProtect, &dwOldProtect);

                    return TRUE;
                }
                pOriginalThunk++;
                pFirstThunk++;
            }
        }
        pImportDesc++;
    }
    return FALSE;
}

// Worker thread (no GUI, avoid crash)
DWORD WINAPI WorkerThread(LPVOID)
{
    HookIAT_WriteFile();
    while (true)
        Sleep(1000);
    return 0;
}

// DLL entry (minimal logic)
BOOL APIENTRY DllMain(HMODULE hMod, DWORD reason, LPVOID)
{
    if (reason == DLL_PROCESS_ATTACH)
    {
        DisableThreadLibraryCalls(hMod);
        CreateThread(nullptr, 0, WorkerThread, nullptr, 0, nullptr);
    }
    return TRUE;
}