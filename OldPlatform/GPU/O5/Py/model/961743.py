import pymel.core as pm
import maya.cmds as cmds
import os
# cmds.setAttr("redshiftOptions.maxNumGPUMBForForICPHierarchy",256) 
print "3333333333333333333333333333333333"
print "set VRAM"
for i in pm.ls(type='RedshiftOptions'):
    if i.hasAttr("maxNumGPUMBForIrradiancePointCloudHierarchy"):
        print "Irradiance Point Cloud is 1024"
        i.maxNumGPUMBForIrradiancePointCloudHierarchy.set(1024)
    if i.hasAttr("maxNumGPUMBForForICPHierarchy"):
        print "Irradiance cache is 1024"
        i.maxNumGPUMBForForICPHierarchy.set(1024)
# cmds.setAttr("redshiftOptions.maxNumGPUMBForForICPHierarchy",1024)
rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
# if "<RenderLayer>" not in  rd_path:        
    # rd_path += "/<RenderLayer>"
    # print rd_path
    # pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(rd_path)