
from ctypes import *
from arnold_common import ai, NullToNone
from ai_color import *
from ai_matrix import *
from ai_node_entry import *
from ai_vector import *
from ai_types import *

class AtNode(Structure):
   pass

class AtUserParamIterator(Structure):
   pass

_AiNode = ai.AiNode
_AiNode.argtypes = [c_char_p]
_AiNode.restype = c_void_p

def AiNode(name):
   return NullToNone(_AiNode(name), POINTER(AtNode)) 

_AiNodeLookUpByName = ai.AiNodeLookUpByName
_AiNodeLookUpByName.argtypes = [c_char_p]
_AiNodeLookUpByName.restype = c_void_p 

def AiNodeLookUpByName(name):
   return NullToNone(_AiNodeLookUpByName(name), POINTER(AtNode)) 

AiNodeReset = ai.AiNodeReset
AiNodeReset.argtypes = [POINTER(AtNode)]

_AiNodeClone = ai.AiNodeClone
_AiNodeClone.argtypes = [POINTER(AtNode)]
_AiNodeClone.restype = c_void_p

def AiNodeClone(node):
   return NullToNone(_AiNodeClone(node), POINTER(AtNode)) 

AiNodeDestroy = ai.AiNodeDestroy
AiNodeDestroy.argtypes = [POINTER(AtNode)]
AiNodeDestroy.restype = c_bool

AiNodeIs = ai.AiNodeIs
AiNodeIs.argtypes = [POINTER(AtNode), c_char_p]
AiNodeIs.restype = c_bool

AiNodeDeclare = ai.AiNodeDeclare
AiNodeDeclare.argtypes = [POINTER(AtNode), c_char_p, c_char_p]
AiNodeDeclare.restype = c_bool

AiNodeLink = ai.AiNodeLink
AiNodeLink.argtypes = [POINTER(AtNode), c_char_p, POINTER(AtNode)]
AiNodeLink.restype = c_bool

AiNodeLinkOutput = ai.AiNodeLinkOutput
AiNodeLinkOutput.argtypes = [POINTER(AtNode), c_char_p, POINTER(AtNode), c_char_p]
AiNodeLinkOutput.restype = c_bool

AiNodeUnlink = ai.AiNodeUnlink
AiNodeUnlink.argtypes = [POINTER(AtNode), c_char_p]
AiNodeUnlink.restype = c_bool

AiNodeIsLinked= ai.AiNodeIsLinked
AiNodeIsLinked.argtypes = [POINTER(AtNode), c_char_p]
AiNodeIsLinked.restype = c_bool

_AiNodeGetLink = ai.AiNodeGetLink
_AiNodeGetLink.argtypes = [POINTER(AtNode), c_char_p, POINTER(c_int)]
_AiNodeGetLink.restype = c_void_p

def AiNodeGetLink(node, input, comp = None):
   return NullToNone(_AiNodeGetLink(node, input, comp), POINTER(AtNode))

AiNodeGetName = ai.AiNodeGetName
AiNodeGetName.argtypes = [POINTER(AtNode)]
AiNodeGetName.restype = c_char_p

_AiNodeGetNodeEntry = ai.AiNodeGetNodeEntry
_AiNodeGetNodeEntry.argtypes = [POINTER(AtNode)]
_AiNodeGetNodeEntry.restype = c_void_p

def AiNodeGetNodeEntry(node):
   return NullToNone(_AiNodeGetNodeEntry(node), POINTER(AtNodeEntry)) 

AiNodeGetLocalData = ai.AiNodeGetLocalData
AiNodeGetLocalData.argtypes = [POINTER(AtNode)]
AiNodeGetLocalData.restype = c_void_p

AiNodeSetLocalData = ai.AiNodeSetLocalData
AiNodeSetLocalData.argtypes = [POINTER(AtNode), c_void_p]

_AiNodeLookUpUserParameter = ai.AiNodeLookUpUserParameter
_AiNodeLookUpUserParameter.argtypes = [POINTER(AtNode), c_char_p]
_AiNodeLookUpUserParameter.restype = c_void_p

def AiNodeLookUpUserParameter(node, param):
   return NullToNone(_AiNodeLookUpUserParameter(node, param), POINTER(AtUserParamEntry)) 

_AiNodeGetUserParamIterator = ai.AiNodeGetUserParamIterator
_AiNodeGetUserParamIterator.argtypes = [POINTER(AtNode)]
_AiNodeGetUserParamIterator.restype = c_void_p

def AiNodeGetUserParamIterator(node):
   return NullToNone(_AiNodeGetUserParamIterator(node), POINTER(AtUserParamIterator)) 

AiUserParamIteratorDestroy = ai.AiUserParamIteratorDestroy
AiUserParamIteratorDestroy.argtypes = [POINTER(AtUserParamIterator)]

_AiUserParamIteratorGetNext = ai.AiUserParamIteratorGetNext
_AiUserParamIteratorGetNext.argtypes = [POINTER(AtUserParamIterator)]
_AiUserParamIteratorGetNext.restype = c_void_p

def AiUserParamIteratorGetNext(iter):
   return NullToNone(_AiUserParamIteratorGetNext(iter), POINTER(AtUserParamEntry)) 

AiUserParamIteratorFinished = ai.AiUserParamIteratorFinished
AiUserParamIteratorFinished.argtypes = [POINTER(AtUserParamIterator)]
AiUserParamIteratorFinished.restype = c_bool

# Parameter Writers
#
AiNodeSetByte = ai.AiNodeSetByte
AiNodeSetByte.argtypes = [POINTER(AtNode), c_char_p, AtByte]

AiNodeSetInt = ai.AiNodeSetInt
AiNodeSetInt.argtypes = [POINTER(AtNode), c_char_p, c_int]

AiNodeSetUInt = ai.AiNodeSetUInt
AiNodeSetUInt.argtypes = [POINTER(AtNode), c_char_p, c_uint]

AiNodeSetBool = ai.AiNodeSetBool
AiNodeSetBool.argtypes = [POINTER(AtNode), c_char_p, c_bool]

AiNodeSetFlt = ai.AiNodeSetFlt
AiNodeSetFlt.argtypes = [POINTER(AtNode), c_char_p, c_float]

AiNodeSetRGB = ai.AiNodeSetRGB
AiNodeSetRGB.argtypes = [POINTER(AtNode), c_char_p, c_float, c_float, c_float]

AiNodeSetRGBA = ai.AiNodeSetRGBA
AiNodeSetRGBA.argtypes = [POINTER(AtNode), c_char_p, c_float, c_float, c_float, c_float]

AiNodeSetVec = ai.AiNodeSetVec
AiNodeSetVec.argtypes = [POINTER(AtNode), c_char_p, c_float, c_float, c_float]

AiNodeSetPnt = ai.AiNodeSetPnt
AiNodeSetPnt.argtypes = [POINTER(AtNode), c_char_p, c_float, c_float, c_float]

AiNodeSetPnt2 = ai.AiNodeSetPnt2
AiNodeSetPnt2.argtypes = [POINTER(AtNode), c_char_p, c_float, c_float]

AiNodeSetStr = ai.AiNodeSetStr
AiNodeSetStr.argtypes = [POINTER(AtNode), c_char_p, c_char_p]

AiNodeSetPtr = ai.AiNodeSetPtr
AiNodeSetPtr.argtypes = [POINTER(AtNode), c_char_p, c_void_p]

AiNodeSetArray = ai.AiNodeSetArray
AiNodeSetArray.argtypes = [POINTER(AtNode), c_char_p, POINTER(AtArray)]

AiNodeSetMatrix = ai.AiNodeSetMatrix
AiNodeSetMatrix.argtypes = [POINTER(AtNode), c_char_p, POINTER(AtMatrix)]

# Parameter Readers
#

AiNodeGetByte = ai.AiNodeGetByte
AiNodeGetByte.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetByte.restype = AtByte

AiNodeGetInt = ai.AiNodeGetInt
AiNodeGetInt.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetInt.restype = c_int

AiNodeGetUInt = ai.AiNodeGetUInt
AiNodeGetUInt.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetUInt.restype = c_uint

AiNodeGetBool = ai.AiNodeGetBool
AiNodeGetBool.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetBool.restype = c_bool

AiNodeGetFlt = ai.AiNodeGetFlt
AiNodeGetFlt.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetFlt.restype = c_float

AiNodeGetRGB = ai.AiNodeGetRGB
AiNodeGetRGB.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetRGB.restype = AtRGB

AiNodeGetRGBA = ai.AiNodeGetRGBA
AiNodeGetRGBA.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetRGBA.restype = AtRGBA

AiNodeGetVec = ai.AiNodeGetVec
AiNodeGetVec.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetVec.restype = AtVector

AiNodeGetPnt = ai.AiNodeGetPnt
AiNodeGetPnt.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetPnt.restype = AtPoint

AiNodeGetPnt2 = ai.AiNodeGetPnt2
AiNodeGetPnt2.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetPnt2.restype = AtPoint2

AiNodeGetStr = ai.AiNodeGetStr
AiNodeGetStr.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetStr.restype = c_char_p

AiNodeGetPtr = ai.AiNodeGetPtr
AiNodeGetPtr.argtypes = [POINTER(AtNode), c_char_p]
AiNodeGetPtr.restype = c_void_p

_AiNodeGetArray = ai.AiNodeGetArray
_AiNodeGetArray.argtypes = [POINTER(AtNode), c_char_p]
_AiNodeGetArray.restype = c_void_p

def AiNodeGetArray(node, param):
   return NullToNone(_AiNodeGetArray(node, param), POINTER(AtArray)) 

AiNodeGetMatrix = ai.AiNodeGetMatrix
AiNodeGetMatrix.argtypes = [POINTER(AtNode), c_char_p, POINTER(AtMatrix)]

AiNodeSetAttributes = ai.AiNodeSetAttributes
AiNodeSetAttributes.argtypes = [POINTER(AtNode), c_char_p]
