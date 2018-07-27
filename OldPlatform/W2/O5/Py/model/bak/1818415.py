#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
print "+++++++++++++++++++++++++++++++++the prerender strat++++++++++++++++++++++++++++++++++++++++++++++++"

def pre_layer_mel():
    print '++++++++++++++++++pre_layer_mel +++++++++++++++++++++++++++++'
    # if "pgYetiMaya" in plugins and "vrayformaya" in plugins:
        # cmds.loadPlugin( "vrayformaya")
        # cmds.loadPlugin( "pgYetiVRayMaya")   
    render_node=pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()
    yeti_load=cmds.pluginInfo("pgYetiMaya", query=True, loaded=True )
    print "the yeti load is %s " % yeti_load
    yeti_vray_load=cmds.pluginInfo("pgYetiVRayMaya", query=True, loaded=True )
    print "the yeti_vray_load load is %s " % yeti_vray_load
    shave_load=cmds.pluginInfo("shaveNode", query=True, loaded=True )
    print "the shave_load load is %s " % shave_load
    pm.lockNode( 'defaultRenderGlobals', lock=False )
    render_node.postMel.set(l=0)
    render_node.preRenderLayerMel.set(l=0)
    render_node.postRenderLayerMel.set(l=0)
    render_node.preRenderMel.set(l=0)
    render_node.postRenderMel.set(l=0)
    
    if render_name=="vray":
        print "++++++++++++++++ the renderer is vray+++++++++++++++++++++"
        if yeti_load and  yeti_vray_load and shave_load==False:
            mel.eval('pgYetiVRayPreRender;')
            #render_node.postMel.set("pgYetiVRayPostRende;")
            print render_node.postMel.get()
        if shave_load and yeti_load==False :
            mel.eval('shaveVrayPreRender;')
        if yeti_load and  yeti_vray_load and shave_load:
            mel.eval('shaveVrayPreRender;pgYetiVRayPreRender;')
        else:
            render_node.postMel.set("")
            render_node.preRenderLayerMel.set("")
            render_node.postRenderLayerMel.set("")
            render_node.preRenderMel.set("")
            render_node.postRenderMel.set("")
            
    elif render_name=="mentalRay":
        print "++++++++++++++++ the renderer is mentalRay++++++++++++++++++"
        if shave_load:
            #render_name = render_node.currentRenderer.get()
            
            render_node.preRenderMel.set("shave_MRFrameStart;")
            render_node.postRenderMel.set("shave_MRFrameEnd;")
            #mel.eval('shave_MRFrameStart')

            #render_node.preRenderLayerMel.set('python \"mel.eval(\\"pgYetiVRayPreRender\\")\"')
        else:
            render_node.preRenderMel.set("")
            render_node.postRenderMel.set("")
    else:
        print "++++++++++++++++ the renderer isnot vray mentalRay+++++++++++++++++++++++++"
        render_node.preMel.set("")
        render_node.postMel.set("")
        render_node.preRenderLayerMel.set("")
        render_node.postRenderLayerMel.set("")
        render_node.preRenderMel.set("")
        render_node.postRenderMel.set("") 
        

print "clear pre mel---------------"
pre_layer_mel()
for i in pm.ls(type="aiOptions"):
    if i.hasAttr("log_verbosity"):
        i.log_verbosity.set(1)
    if i.hasAttr("autotx"):
        i.autotx.set(False)
    if i.hasAttr("textureMaxMemoryMB"):
        i.textureMaxMemoryMB.set(20480)
        print "set arnold textureMaxMemoryMB 20480 "
print "**********************************************the prerender end******************************************************"        
