import pymel.core as pm
import maya.cmds as cmds
import os
for i in pm.ls(type="aiOptions"):
    print "defaultArnoldRenderOptions.abortOnError 0"
    i.abortOnError.set(0)
    i.log_verbosity.set(1)
    if i.hasAttr("autotx"):
        i.autotx.set(False)