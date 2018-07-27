
# TODO: Implement bounding box functions
 
from ctypes import *
from arnold_common import ai
from ai_types import *
from ai_vector import *

class AtBBox(Structure):
   _fields_ = [("min", AtPoint),
               ("max", AtPoint)]

class AtBBox2(Structure):
   _fields_ = [("minx", c_int),
               ("miny", c_int),
               ("maxx", c_int),
               ("maxy", c_int)]

# unit bounding-box
#
AI_BBOX_UNIT = AtBBox((0, 0, 0), (1, 1, 1))

# zero-width bounding-box
#
AI_BBOX_ZERO = AtBBox((0, 0, 0), (0, 0, 0))
