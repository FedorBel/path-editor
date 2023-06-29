from ctypes import *

dll = CDLL("./libhack.so")
dll.foo.restype = py_object
print(dll.foo("foo"))
