
from ctypes import *
from arnold_common import ai

AiLoadPlugins = ai.AiLoadPlugins
AiLoadPlugins.argtypes = [c_char_p]

AiLoadPlugin = ai.AiLoadPlugin
AiLoadPlugin.argtypes = [c_char_p]
