# # ! /usr/bin/env python
# # coding=utf-8
import os
import re
import pymel.core as pm
import maya.mel as mel


short_scene_name = os.path.splitext(os.path.basename(pm.sceneName()))[0]
r = re.findall(r"(.*)LGT_(.*)", short_scene_name)
if r:
    new_path = "{0}/%l/{1}%l".format(r[0][1], r[0][0])
    pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(new_path)
    print "New output path: " + str(pm.PyNode("defaultRenderGlobals").imageFilePrefix.get())
    
if not r:
    r = re.findall(r"(.*)LGT_([A-Za-z_0-9]*)", short_scene_name)
    if r:
        new_path = "{0}/%l/{1}%l".format(r[0][1], r[0][0])
        pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(new_path)
        print "New output path: " + str(pm.PyNode("defaultRenderGlobals").imageFilePrefix.get())
if not r:
    print "scene_name: {0} ".format(short_scene_name)
    print "New output path: Failed"

mel.eval('source "//10.50.1.22/td/clientFiles/1812148/meshShapeAttrSet.mel"')
## from //10.50.1.22/td/clientFiles/1812148/meshShapeAttrSet.mel
#for i in pm.ls(type="mesh"):
#    if i.hasAttr("dsm"):
#        i.dsm.set(2)


