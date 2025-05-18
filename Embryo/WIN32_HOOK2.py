import ctypes as c
from ctypes import wintypes as w

import win32api
import win32con as wcon
import win32process as wproc


class MODULEINFO(c.Structure):
    _fields_ = [
        ("lpBaseOfDll", c.c_void_p),
        ("SizeOfImage", w.DWORD),
        ("EntryPoint", c.c_void_p),
    ]


pid = 14692  # Minesweeper

k32 = c.windll.kernel32

GetLastError = k32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = w.DWORD

CloseHandle = k32.CloseHandle
CloseHandle.argtypes = [w.HANDLE]
CloseHandle.restype = w.BOOL

get_module_information_func_name = "GetModuleInformation"
GetModuleInformation = getattr(
    c.WinDLL("kernel32"),
    get_module_information_func_name,
    getattr(
        c.WinDLL("psapi"),
        get_module_information_func_name
    )
)
GetModuleInformation.argtypes = [w.HANDLE, w.HMODULE, c.POINTER(MODULEINFO), w.DWORD]
GetModuleInformation.restype = w.BOOL

processHandle = win32api.OpenProcess(wcon.PROCESS_ALL_ACCESS, False, pid)

memory_info = wproc.GetProcessMemoryInfo(processHandle)
module_handles = wproc.EnumProcessModules(processHandle)
module_info = MODULEINFO()
for i in range(len(module_handles)):
    module_handle = module_handles[i]
    module_file_name = wproc.GetModuleFileNameEx(processHandle, module_handle)

    if module_file_name.endswith('KERNEL32.DLL'):
        mh = win32api.GetModuleHandle(module_file_name)
        CloseHandle_address = win32api.GetProcAddress(mh, b'CloseHandle')
        GetLastError_address = win32api.GetProcAddress(mh, b'GetLastError')

    res = GetModuleInformation(int(processHandle), module_handle, c.byref(module_info), c.sizeof(module_info))
    print("ModuleName: {}".format(module_file_name))
    print("EntryPoint: {}".format(module_info.EntryPoint))
    print("SizeOfImage: {}".format(module_info.SizeOfImage))
    print("lpBaseOfDll: {}".format(module_info.lpBaseOfDll))
    print()
