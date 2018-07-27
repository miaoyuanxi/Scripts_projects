#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com

## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
import maya.cmds as cmds

## ------------------------------------------------------------------------
## RENDER PASSES
## ------------------------------------------------------------------------
def set_type(rp, type):
    if type == 'Beauty':
        cmds.setAttr('%s.type' % rp, 0)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Colour':
        cmds.setAttr('%s.type' % rp, 1)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Diffuse':
        cmds.setAttr('%s.type' % rp, 2)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Diffuse Raw':
        cmds.setAttr('%s.type' % rp, 3)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Shadow':
        cmds.setAttr('%s.type' % rp, 4)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Shadow Raw':
        cmds.setAttr('%s.type' % rp, 5)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Diffuse Without Shadows':
        cmds.setAttr('%s.type' % rp, 6)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Diffuse Without Shadows Raw':
        cmds.setAttr('%s.type' % rp, 7)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Ambient':
        cmds.setAttr('%s.type' % rp, 8)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Ambient Raw':
        cmds.setAttr('%s.type' % rp, 9)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Indirect':
        cmds.setAttr('%s.type' % rp, 10)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Indirect Raw':
        cmds.setAttr('%s.type' % rp, 11)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Ambient Occlusion':
        cmds.setAttr('%s.type' % rp, 12)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Translucency':
        cmds.setAttr('%s.type' % rp, 13)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Subsurface':
        cmds.setAttr('%s.type' % rp, 14)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Subsurface Front':
        cmds.setAttr('%s.type' % rp, 15)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Subsurface Mid':
        cmds.setAttr('%s.type' % rp, 16)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Subsurface Back':
        cmds.setAttr('%s.type' % rp, 17)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Incandesence':
        cmds.setAttr('%s.type' % rp, 18)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Incandescence':
        cmds.setAttr('%s.type' % rp, 18)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Specular':
        cmds.setAttr('%s.type' % rp, 19)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Reflection':
        cmds.setAttr('%s.type' % rp, 20)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Refraction':
        cmds.setAttr('%s.type' % rp, 21)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Bloom Source':
        cmds.setAttr('%s.type' % rp, 22)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Depth':
        cmds.setAttr('%s.type' % rp, 23)
        cmds.setAttr('%s.channels' % rp, 0)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Depth (Normalized)':
        cmds.setAttr('%s.type' % rp, 23)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.scale' % rp, 0.001)
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Normal World':
        cmds.setAttr('%s.type' % rp, 24)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Normal World (Normalized)':
        cmds.setAttr('%s.type' % rp, 24)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.scale' % rp, 0.5)
        cmds.setAttr('%s.offset' % rp, 0.5)
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Normal Camera':
        cmds.setAttr('%s.type' % rp, 25)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Normal Camera (Normalized)':
        cmds.setAttr('%s.type' % rp, 25)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.scale' % rp, 0.5)
        cmds.setAttr('%s.offset' % rp, 0.5)
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Point World':
        cmds.setAttr('%s.type' % rp, 26)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Point Camera':
        cmds.setAttr('%s.type' % rp, 27)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Motion Vector':
        cmds.setAttr('%s.type' % rp, 28)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Motion Vector (Normalized)':
        cmds.setAttr('%s.type' % rp, 28)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.scale' % rp, 0.01)
        cmds.setAttr('%s.offset' % rp, 0.5)
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Opacity':
        cmds.setAttr('%s.type' % rp, 29)
        cmds.setAttr('%s.channels' % rp, 0)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.vis_in_trans' % rp, 0)
    elif type == 'Facing Ratio':
        cmds.setAttr('%s.type' % rp, 30)
        cmds.setAttr('%s.channels' % rp, 0)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
    elif type == 'UV':
        cmds.setAttr('%s.type' % rp, 31)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
        cmds.setAttr('%s.filtering' % rp, False)
    elif type == 'Material ID':
        cmds.setAttr('%s.type' % rp, 32)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
    elif type == 'Object ID':
        cmds.setAttr('%s.type' % rp, 33)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
    elif type == 'Matte':
        cmds.setAttr('%s.type' % rp, 34)
        cmds.setAttr('%s.channels' % rp, 0)
        cmds.setAttr('%s.group' % rp, 'matte', type='string')
    elif type == 'Custom Colour':
        cmds.setAttr('%s.type' % rp, 35)
        cmds.setAttr('%s.group' % rp, 'custom', type='string')
    elif type == 'Custom Vector':
        cmds.setAttr('%s.type' % rp, 36)
        cmds.setAttr('%s.group' % rp, 'custom', type='string')
    elif type == 'Environment':
        cmds.setAttr('%s.type' % rp, 37)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Light Select':
        cmds.setAttr('%s.type' % rp, 38)
        cmds.setAttr('%s.group' % rp, 'beauty', type='string')
    elif type == 'Diagnostic Samples':
        cmds.setAttr('%s.type' % rp, 39)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
    elif type == 'Diagnostic Error':
        cmds.setAttr('%s.type' % rp, 40)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
    elif type == 'Diagnostic Time':
        cmds.setAttr('%s.type' % rp, 41)
        cmds.setAttr('%s.group' % rp, 'post', type='string')
