#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re


pm.lockNode( 'defaultRenderGlobals', lock=False )

render_node = pm.PyNode("defaultRenderGlobals")
render_name = render_node.currentRenderer.get()


rep_path = ""
search = ""
dicts = {}

def resetup():
    default_globals = pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()

    print "Set Renumber frames   is off"
    print "get you scene attritubes>>>>>>>>>>>"
    for i in pm.ls(type="aiAOVDriver"):
        if i.hasAttr("append"):
            i.append.set(0)     
            print "set   Append   off"    
    for i in pm.ls(type="aiOptions"): 
        if i.hasAttr("log_verbosity"):
            log_verbosity = i.log_verbosity.get()
            i.log_verbosity.set(1)
    for i in pm.ls(type="pgYetiMaya"):
        if i.hasAttr("aiLoadAtInit"):
            i.aiLoadAtInit.set(1)       

    for i in pm.ls(type="aiStandIn"):
        if i.hasAttr("deferStandinLoad"):
            i.deferStandinLoad.set(0)
            print "set %s to 0" % (i.deferStandinLoad)
            

    sys.stdout.flush()
            
resetup()    


print "**********************************************the prerender end******************************************************"