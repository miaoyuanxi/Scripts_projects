
from ctypes import *
from arnold_common import ai
from ai_types import *

ai.AiGetVersion.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
ai.AiGetVersion.restype = c_char_p

# NOTE: The following two functions differ from Arnold API. They represent the functionality
#       of AiGetVersion() in a Python friendly way

# Returns version numbers as a 4-element list: [arch, major, minor, fix] 
def AiGetVersion():
   arch = create_string_buffer(10)
   major = create_string_buffer(10)
   minor = create_string_buffer(10)
   fix = create_string_buffer(20)
   ai.AiGetVersion(arch, major, minor, fix)
   return [arch.value, major.value, minor.value, fix.value]

def AiGetVersionString():
   arch = c_char_p()
   major = c_char_p()
   minor = c_char_p()
   fix = c_char_p()
   return ai.AiGetVersion(arch, major, minor, fix)

AiGetVersionInfo = ai.AiGetVersionInfo
AiGetVersionInfo.restype = c_char_p

AiGetCompileOptions = ai.AiGetCompileOptions
AiGetCompileOptions.restype = c_char_p

AiCheckAPIVersion = ai.AiCheckAPIVersion
AiCheckAPIVersion.argtypes = [c_char_p, c_char_p, c_char_p]
AiCheckAPIVersion.restype = c_bool

AiSetAppString = ai.AiSetAppString
AiSetAppString.argtypes = [c_char_p]
