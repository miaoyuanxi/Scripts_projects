
# # ! /usr/bin/env python
# # coding=utf-8
import os
import re
import pymel.core as pm
import maya.mel as mel
import maya.cmds as cmds
import sys

short_scene_name = os.path.splitext(os.path.basename(pm.sceneName()))[0]

short_scene_name = short_scene_name.replace(" ","")
# print short_scene_name
r = re.findall(r"(.*)LGT_(.*)", short_scene_name)
if r:
    #new_path = "{0}/%l/{1}%l".format(r[0][1], r[0][0])
    new_path = "{0}/<RenderLayer>/{1}<RenderLayer>".format(r[0][1], r[0][0])
    pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(new_path)
    print "New output path: " + str(pm.PyNode("defaultRenderGlobals").imageFilePrefix.get())
    
if not r:
    r = re.findall(r"(.*)LGT_([A-Za-z_0-9]*)", short_scene_name)
    if r:
        #new_path = "{0}/%l/{1}%l".format(r[0][1], r[0][0])
        new_path = "{0}/<RenderLayer>/{1}<RenderLayer>".format(r[0][1], r[0][0])
        pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(new_path)
        print "New output path: " + str(pm.PyNode("defaultRenderGlobals").imageFilePrefix.get())
if not r:
    print "scene_name: {0} ".format(short_scene_name)
    print "New output path: Failed"

#mel.eval('source "//10.60.100.102/td/clientFiles/1812148/meshShapeAttrSet.mel"')
## from //10.50.1.22/td/clientFiles/1812148/meshShapeAttrSet.mel
#for i in pm.ls(type="mesh"):
#    if i.hasAttr("dsm"):
#        i.dsm.set(2)
for i in pm.ls(type="aiOptions"):

    if i.hasAttr("log_verbosity"):
        i.log_verbosity.set(1)
    if i.hasAttr("autotx"):
        i.autotx.set(False)
    if i.hasAttr("textureMaxMemoryMB"):
        org_arnold_texturecache = cmds.getAttr(i+".textureMaxMemoryMB")
        print "org arnold texturecache to %s MB " % org_arnold_texturecache
        i.textureMaxMemoryMB.set(40960)
        print "set arnold texturecache to 40960 MB"
def change_path_mapping(node_type, attr_name, mapping):
    print "the  node type  is %s" % (node_type)    
    maya_proj_paht = cmds.workspace(q=True, fullName=True)
    source_path = "%s/sourceimages" % (maya_proj_paht)
    scenes_path = "%s/scenes" % (maya_proj_paht)
    data_path = "%s/data" % (maya_proj_paht)
    all_node = pm.ls(type=node_type)
    if len(all_node) != 0:
        for node in all_node:
            if node.hasAttr(attr_name):
                #file_path = cmds.getAttr(node + "."+attr_name)
                refcheck = pm.referenceQuery(node, inr = True)
                
                if (refcheck == False):
                    try:              
                        node.attr(attr_name).set(l=0)
                    except Exception,error:
                        print Exception,":",error
                        pass
                file_path = node.attr(attr_name).get()
                if file_path != None and file_path.strip() !="" :
                    file_path = file_path.replace('\\', '/')
                    if os.path.exists(file_path) == 0:                        
                        asset_name = os.path.split(file_path)[1]
                        file_path_new = file_path
                        print file_path_new
                        if os.path.exists(file_path_new) == 0 and mapping:
                            for repath in mapping:
                                if mapping[repath] != repath:
                                    if file_path.find(repath) >= 0:
                                        file_path_new = file_path.replace(repath, mapping[repath])
                                        print file_path_new                        
                                        cmds.setAttr((node + "." + attr_name), file_path_new, type="string")
#change_path_mapping("AlembicNode", "abc_File",mapping)
# print "the mode++++++"
# print cmds.evaluationManager( query=True ,mode =1 )
# print "the mode++++++"
if user_id in [1812148]:
    print "the user_id is 1812148"
    if cmds.about(v=True)=="2017":
        #mel.eval("source \"B:/custom_config/1812148/XgmTools/preRenderMEL.mel\";")
        #mel.eval("B:/custom_config/1812148/XgmTools/xgmTools/preRenderMEL.mel")
        mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
        pyDir = "B:/custom_config/1812148/XgmTools"
        if pyDir not in sys.path:
            sys.path.append(pyDir)
        import xgmTools.description as xd
        xd.pre_render_routine()

cmds.refresh()