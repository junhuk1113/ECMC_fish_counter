import ctypes                           # 파이썬 extension을 사용하기 위한 모듈
import platform   
import time

path = 'C:\\Users\\PMKJun\\source\\repos\\logLoader\\x64\\Debug\\logLoader.dll'

c_module = ctypes.windll.LoadLibrary(path)

print(c_module)

filesizeLoad = c_module.filesizeLoad
filesizeLoad.argtypes = [ctypes.c_char_p]
filesizeLoad.restype = ctypes.c_long

tempst = "C:/Users/PMKJun/AppData/Roaming/.minecraft/logs/latest.log"
filepath = tempst.encode("euc-kr")
outparam = filesizeLoad(filepath)
filesize = outparam
print(filesize)

readFish = c_module.readFish
rp = ctypes.c_long()
readFish.argtypes = (ctypes.c_char_p,ctypes.c_long,ctypes.POINTER(ctypes.c_long))
readFish.restype = ctypes.c_char_p

while 1:
    outparam=readFish(filepath,filesize,rp)
    result = outparam.decode('euc-kr',errors='ignore')
    filesize=rp.value
    if result ==' ':
        continue
    print(result)
    
    
    