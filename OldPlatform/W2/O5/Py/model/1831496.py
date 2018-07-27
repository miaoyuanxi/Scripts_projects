import pymel.core as pm
import maya.cmds as cmds
import os
for i in pm.ls(type="aiOptions"):
    print "defaultArnoldRenderOptions.abortOnError 0"
    i.abortOnError.set(0)
    i.log_verbosity.set(1)
    if i.hasAttr("autotx"):
        i.autotx.set(False)
    i.absoluteTexturePaths.set(0)
    i.absoluteProceduralPaths.set(0)
    print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
    #setAttr "defaultArnoldRenderOptions.absoluteProceduralPaths" 0;
    i.procedural_searchpath.set(r"N:\cg_custom_setup\network\arnold\htoa-1.11.1_r1692_houdini-15.0.393_windows\arnold\procedurals")
    i.shader_searchpath.set(r"N:\cg_custom_setup\network\arnold\htoa-1.11.1_r1692_houdini-15.0.393_windows\arnold\plugins")
    #setAttr -type "string" defaultArnoldRenderOptions.procedural_searchpath ;

    #setAttr -type "string" defaultArnoldRenderOptions.shader_searchpath "B:\\custom_config\\1831496\\htoa-1.11.1_r1692_houdini-15.0.393\\arnold\\plugins";
    i.renderType.set(0)