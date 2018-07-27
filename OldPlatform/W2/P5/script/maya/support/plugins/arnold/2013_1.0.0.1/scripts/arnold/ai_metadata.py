
from ctypes import *
from arnold_common import ai
from ai_node_entry import *

AiMetaDataGetBool = ai.AiMetaDataGetBool
AiMetaDataGetBool.argtypes = [POINTER(AtNodeEntry), c_char_p, c_char_p, POINTER(c_bool)]
AiMetaDataGetBool.restype = c_bool

AiMetaDataGetInt = ai.AiMetaDataGetInt
AiMetaDataGetInt.argtypes = [POINTER(AtNodeEntry), c_char_p, c_char_p, POINTER(c_int)]
AiMetaDataGetInt.restype = c_bool

AiMetaDataGetFlt = ai.AiMetaDataGetFlt
AiMetaDataGetFlt.argtypes = [POINTER(AtNodeEntry), c_char_p, c_char_p, POINTER(c_float)]
AiMetaDataGetFlt.restype = c_bool

AiMetaDataGetPnt = ai.AiMetaDataGetPnt
AiMetaDataGetPnt.argtypes = [POINTER(AtNodeEntry), c_char_p, c_char_p, POINTER(AtPoint)]
AiMetaDataGetPnt.restype = c_bool

AiMetaDataGetVec = ai.AiMetaDataGetVec
AiMetaDataGetVec.argtypes = [POINTER(AtNodeEntry), c_char_p, c_char_p, POINTER(AtVector)]
AiMetaDataGetVec.restype = c_bool

AiMetaDataGetPnt2 = ai.AiMetaDataGetPnt2
AiMetaDataGetPnt2.argtypes = [POINTER(AtNodeEntry), c_char_p, c_char_p, POINTER(AtPoint2)]
AiMetaDataGetPnt2.restype = c_bool

AiMetaDataGetRGB = ai.AiMetaDataGetRGB
AiMetaDataGetRGB.argtypes = [POINTER(AtNodeEntry), c_char_p, c_char_p, POINTER(AtColor)]
AiMetaDataGetRGB.restype = c_bool

AiMetaDataGetStr = ai.AiMetaDataGetStr
AiMetaDataGetStr.argtypes = [POINTER(AtNodeEntry), c_char_p, c_char_p, POINTER(c_char_p)]
AiMetaDataGetStr.restype = c_bool

AiMetaDataLoadFile = ai.AiMetaDataLoadFile
AiMetaDataLoadFile.argtypes = [c_char_p]
AiMetaDataLoadFile.restype = c_bool
