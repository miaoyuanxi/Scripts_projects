
from ctypes import *
from arnold_common import ai

AiMalloc_func = ai.AiMalloc_func
AiMalloc_func.argtypes = [c_ulong, c_char_p, c_int, c_char_p]
AiMalloc_func.restype = c_void_p

def AiMalloc(size):
   return AiMalloc_func(size, '', 0, '')

AiRealloc_func = ai.AiRealloc_func
AiRealloc_func.argtypes = [c_void_p, c_ulong, c_char_p, c_int, c_char_p]
AiRealloc_func.restype = c_void_p

def AiRealloc(addr, size):
   return AiRealloc_func(addr, size, '', 0, '')

AiFree_func = ai.AiFree_func
AiFree_func.argtypes = [c_void_p, c_char_p, c_int, c_char_p]

def AiFree(addr):
   AiFree_func(addr, '', 0, '')
 