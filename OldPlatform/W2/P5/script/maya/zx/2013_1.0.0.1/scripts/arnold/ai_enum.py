
from ctypes import *
from arnold_common import ai
from ai_types import *

AtEnum = POINTER(c_char_p)

AiEnumGetValue = ai.AiEnumGetValue
AiEnumGetValue.argtypes = [AtEnum, c_char_p]
AiEnumGetValue.restype = c_int

AiEnumGetString = ai.AiEnumGetString
AiEnumGetString.argtypes = [AtEnum, c_int]
AiEnumGetString.restype = c_char_p
