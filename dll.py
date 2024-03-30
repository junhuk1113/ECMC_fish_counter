import ctypes                           # 파이썬 extension을 사용하기 위한 모듈
import platform                         # 파이썬 아키텍처를 확인하기 위한 모듈

if 'Windows' == platform.system() :     # 윈도우 운영체제에서 c 모듈 로드
    path = 'D:\VSCODE\ECMC_fish_counter\Dll2.dll'
    print("d")
    c_module = ctypes.windll.LoadLibrary(path)
elif 'Linux' == platform.system() :     # 리눅스 운영체제에서 c 모듈 로드
    path = "./libc_module.so"
    c_module = ctypes.cdll.LoadLibrary(path)
else :
    raise OSError()
    
print(c_module)

# int add(int a, int b)
add = c_module.add
print(add)   # <_FuncPtr object at 0x000002196BFE9860>
add.argtypes = (ctypes.c_int, ctypes.c_int)
add.restype = ctypes.c_int

res = add(1, 2)
print(res)   # 3

# void sub(double a, double b, double* result)
sub = c_module.sub
sub.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_double))
sub.restype = None
outparam = ctypes.c_double()

sub(3.2, 2.2, outparam)
print(outparam.value)  # 1.0/t

# 3. 배열 파라메터를 사용하는 예
accumulate = c_module.accumulate
accumulate.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.c_int)
accumulate.restype = ctypes.c_int

s = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
arr = (ctypes.c_int * len(s))(*s)

res = accumulate(arr, len(s))
print(res)
ctypes.c_char