import time
from ctypes import *

# ----------以下四种加载DLL方式皆可—————————
# pDLL = WinDLL("./myTest.dll")
# pDll = windll.LoadLibrary("./myTest.dll")
# pDll = cdll.LoadLibrary("./myTest.dll")

pDll = CDLL("Dll1.dll")
print('DLL加载成功')
while True:
    res = pDll.add(1, 2)
    print(res)
    time.sleep(1)
