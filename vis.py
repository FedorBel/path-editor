from ctypes import *

dll = CDLL("./libhack.so")
dll.foo.restype = py_object
a = [1.0, 2.0, 3.0]

print(dll.foo(py_object(a)))
