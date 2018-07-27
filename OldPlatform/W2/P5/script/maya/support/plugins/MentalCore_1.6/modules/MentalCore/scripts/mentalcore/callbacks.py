#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com


## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
import os, shutil, webbrowser
from functools import partial

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMaya

import mlib
import mapi
import renderglobals
import general
import passes

## ------------------------------------------------------------------------
## GLOBAL VARIABLES
## ------------------------------------------------------------------------
DISABLE_CALLBACK = False
EXPORT = False

## ------------------------------------------------------------------------
## CALLBACKS
## ------------------------------------------------------------------------
def loadCallbacks():
    #load callback trigger
    mrLoadCallback = OpenMaya.MSceneMessage.addStringArrayCallback(OpenMaya.MSceneMessage.kAfterPluginLoad, mentalrayLoadCallbacks)
    
    #Trigger callbacks immediately if plugins are already loaded
    if cmds.pluginInfo('Maytomr', q=True, loaded=True):
        mentalrayLoadCallbacks([None, 'Maytomr'])
        
    if cmds.pluginInfo('Fur', q=True, loaded=True):
        mentalrayLoadCallbacks([None, 'Fur'])

def mentalrayLoadCallbacks(strs, clientData=None):
    '''Sets up callbacks and overrides scripts when the mr plugin is loaded'''
    #Get Maya version
    maya_ver = int(cmds.about(f=True))
    maya_batch = cmds.about(b=True)
    
    if strs[1] == 'Mayatomr':
        if maya_ver == 2012:
            mel.eval('source "mc_registerMentalRayRenderer.mel"')
            mel.eval('source "mc_mentalrayCustomNodeClass_2012.mel"')
            mel.eval('source "mc_connectNodeToAttrOverride.mel"')
            mel.eval('source "mc_mrCreateCustomNode.mel"')
            mel.eval('source "mc_mrFurDescription.mel"')
            mel.eval('source "mc_AEpfxHairTemplate.mel"')
        elif maya_ver == 2013:
            mel.eval('source "mc_registerMentalRayRenderer.mel"')
            mel.eval('source "mc_mentalrayCustomNodeClass_2013.mel"')
            mel.eval('source "mc_connectNodeToAttrOverride.mel"')
            mel.eval('source "mc_mrCreateCustomNode.mel"')
        elif maya_ver == 2014:
            mel.eval('source "mc_registerMentalRayRenderer_2014.mel"')
            mel.eval('source "mc_mentalrayCustomNodeClass_2014.mel"')
            mel.eval('source "mc_connectNodeToAttrOverride.mel"')
            mel.eval('source "mc_mrCreateCustomNode.mel"')
    
        #AE Extensions
        if int(maya_ver) >= 2013 and not maya_batch: # Maya 2013+ and not in batch mode
            cmds.callbacks(addCallback=mcAExtension, hook='AETemplateCustomContent', owner='mayaToMr')
    
        #Add Callbacks
        if not maya_batch: #not in batch mode
            OpenMaya.MDGMessage.addConnectionCallback ( shaderConnectionCB )
            
            OpenMaya.MDGMessage.addNodeAddedCallback ( shaderCreateCB, 'core_hair' )
            OpenMaya.MDGMessage.addNodeAddedCallback ( shaderCreateCB, 'core_material' )
            OpenMaya.MDGMessage.addNodeAddedCallback ( shaderCreateCB, 'core_geo_light' )
            
            OpenMaya.MDGMessage.addNodeAddedCallback ( shaderCreateCB, 'core_renderpass' )
            OpenMaya.MDGMessage.addNodeRemovedCallback ( shaderDeleteCB, 'core_renderpass' )
            
            OpenMaya.MDGMessage.addNodeAddedCallback ( shaderCreateCB, 'renderLayer' )
            OpenMaya.MDGMessage.addNodeRemovedCallback ( shaderDeleteCB, 'renderLayer' )
            
        #Scene Upgrade Callback
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kBeforeOpen, beforeOpenCB, None)
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterOpen, afterOpenCB, None)    
        
        #Scene Export Callback
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kBeforeExport, beforeExportCB, None)
        OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterExport, afterExportCB, None)
        
    elif strs[1] == 'Fur':
        #Fur shader override extenstion attribute
        cmds.addExtension( nodeType='FurDescription', longName='mc_shaderOverride', attributeType='message' )
        
        
def mcAExtension(node):
    node_type = cmds.nodeType(node)
    if node_type == 'pfxHair':
        mel.eval('AEmentalcorePfxHair "%s"' % node)
    elif node_type == 'FurDescription':
        mel.eval('AEmentalcoreFurDescription "%s"' % node)
        
        
def shaderConnectionCB(srcPlug, destPlug, made, clientData):
    '''Disconnects the mia materials bump correctly when a texture is disconnected'''
    node = OpenMaya.MFnDependencyNode(destPlug.node())
        
    nodeName = node.name()
    nodeType = node.typeName()
    
    if not made:
        if nodeType == 'core_mia_material':
            plugName = destPlug.name();
            attr = plugName.split('.')[-1]

            if attr in ('overall_bump', 'standard_bump'):
                try:
                    cmds.setAttr(plugName, 0, 0, 0)
                except:
                    pass
            
    else:
        if nodeType == 'core_texture_blur':
            plugName = destPlug.name();
            attr = plugName.split('.')[-1]

            if attr == 'tex':
                file_tex = cmds.listConnections(plugName, s=True, d=False, type='file')
                if file_tex:
                    try:
                        cmds.setAttr('%s.filterType' % file_tex[0], 0);
                    except:
                        pass
    
    
def shaderCreateCB(node, clientData):
    '''Run whenever a dg node is created'''
    if not DISABLE_CALLBACK:
        node = OpenMaya.MFnDependencyNode(node)
        
        nodeName = node.name()
        nodeType = node.typeName()
        
        if cmds.objExists(nodeName):
            if nodeType == 'core_hair':
                if not cmds.listAttr(nodeName, m=True, v=True, c=True, st='colour'):
                    cmds.setAttr('%s.colour[0].col_color' % nodeName, .25, .18, .15, type='double3')
                    cmds.setAttr('%s.colour[0].col_position' % nodeName, 0)
                    
                    cmds.setAttr('%s.colour[1].col_color' % nodeName, .4, .3, .2, type='double3')
                    cmds.setAttr('%s.colour[1].col_position' % nodeName, 1)
                
            elif nodeType == 'core_material':
                if not cmds.listAttr(nodeName, m=True, v=True, c=True, st='rspec_col'):
                    cmds.setAttr('%s.rspec_col[0].rspec_col_color' % nodeName, 1, 1, 1, type='double3')
                    cmds.setAttr('%s.rspec_col[0].rspec_col_position' % nodeName, 0)
            
                if not cmds.listAttr(nodeName, m=True, v=True, c=True, st='rspec_falloff'):
                    cmds.setAttr('%s.rspec_falloff[0].rspec_falloff_value' % nodeName, .6)
                    cmds.setAttr('%s.rspec_falloff[0].rspec_falloff_position' % nodeName, 0)
                    
                    cmds.setAttr('%s.rspec_falloff[1].rspec_falloff_value' % nodeName, 1)
                    cmds.setAttr('%s.rspec_falloff[1].rspec_falloff_position' % nodeName, 1)
                
                if not cmds.listAttr(nodeName, m=True, v=True, c=True, st='refl_curve'):
                    cmds.setAttr('%s.refl_curve[0].refl_curve_value' % nodeName, .2)
                    cmds.setAttr('%s.refl_curve[0].refl_curve_position' % nodeName, 0)
                    
                    cmds.setAttr('%s.refl_curve[1].refl_curve_value' % nodeName, 1)
                    cmds.setAttr('%s.refl_curve[1].refl_curve_position' % nodeName, 1)
                    
            elif nodeType == 'core_geo_light':
                if not cmds.listConnections('%s.time' % nodeName, s=True, d=False):
                    cmds.connectAttr('time1.outTime', '%s.time' % nodeName, f=True)

            elif nodeType == 'core_renderpass':
                if passes.PASSES_TAB and cmds.control(passes.PASSES_TAB.scene_passes, q=True, exists=True):
                    passes.PASSES_TAB.connect_pass(nodeName)
                    passes.refresh_passes_ui()
                    
            '''
            elif nodeType == 'renderLayer':
                if nodeName != 'defaultRenderLayer' and passes.PASSES_TAB and cmds.control(passes.PASSES_TAB.scene_passes, q=True, exists=True):
                    passes.PASSES_TAB.connect_layer(nodeName)
                    passes.refresh_passes_ui()
            '''

def shaderDeleteCB(node, clientData):
    '''Run whenever a dg node is deleted'''
    node = OpenMaya.MFnDependencyNode(node)
    
    nodeName = node.name()
    nodeType = node.typeName()

    if nodeType == 'core_renderpass' or nodeType == 'renderLayer':
        cmds.evalDeferred(passes.refresh_passes_ui)

def beforeOpenCB(*args):
    '''Run before a scene is opened'''
    global DISABLE_CALLBACK
    DISABLE_CALLBACK = True

def afterOpenCB(*args):
    '''Run whenever a scene is finished opening. This is used to upgrade existing MentalCore scenes'''
    global DISABLE_CALLBACK
    DISABLE_CALLBACK = False
    
    if cmds.objExists('mentalcoreGlobals'):
        import mentalcore
        
        # Get current scene version
        version = 1.4
        if cmds.attributeQuery('version', n='mentalcoreGlobals', exists=True):
            temp_ver = cmds.getAttr('mentalcoreGlobals.version')
            if temp_ver:
                try:
                    version = float(temp_ver)
                except:
                    pass
                    
        if version < mentalcore.VERSION:
            print 'MentalCore(): Upgrading scene from version %.1f to %.1f' % (version, mentalcore.VERSION)
                        
            # >1.5 UPGRADE
            if version <= 1.4:
                # ------------------ #
                # Reassociate Passes #
                # ------------------ #
                pass_associations = {}
                for layer in cmds.ls(type='renderLayer'):
                    #Store associated passes
                    pass_associations[layer] = cmds.listConnections('%s.message' % layer, type='core_renderpass', s=False, d=True)
                    
                    #Disconnect asociated passes (old style)
                    pass_conn = cmds.listConnections('%s.message' % layer, type='core_renderpass', c=True, p=True)
                    if pass_conn:    
                        for i in range(len(pass_conn)/2):
                            layer_attr = pass_conn[i*2]
                            pass_attr = pass_conn[i*2+1]
                            pass_name = pass_attr.split('.')[0]
                            
                            cmds.disconnectAttr(layer_attr, pass_attr)
                            
                # Reassociate Passes
                for layer, passes in pass_associations.items():
                    if layer and passes:
                        for rp in passes:
                            mapi.associate_pass(rp, layer)
                            
        #Update version number on mentalcoreGlobals
        try:
            cmds.lockNode('mentalcoreGlobals', l=False)
            cmds.setAttr('mentalcoreGlobals.version', lock=False)
            cmds.setAttr('mentalcoreGlobals.version', '%.1f' % mentalcore.VERSION, type='string')
            cmds.setAttr('mentalcoreGlobals.version', lock=True)
            cmds.lockNode('mentalcoreGlobals', l=True)
        except:
            pass

    ## Upgrade Shaders ##
    
    # Upgrade to core_texture_lookup2
    to_upgrade = cmds.ls(type='core_texture_lookup')
    if to_upgrade:
        print 'MentalCore(): Upgrading core_texture_lookup shaders to core_texture_lookup2'
        for shader in to_upgrade:
            if cmds.objExists(shader):
                new_shader = None
                try:
                    new_shader = cmds.shadingNode('core_texture_lookup2', asTexture=True)
                    mel.eval('upgradeMentalRayShader("%s", "%s", true, "");' % (shader, new_shader))
                except:
                    print 'MentalCore(): Error upgrading shader "%s"' % shader
                    if new_shader:
                        cmds.delete(new_shader)

    # Upgrade to core_carpaint2
    to_upgrade = cmds.ls(type='core_carpaint')
    if to_upgrade:
        print 'MentalCore(): Upgrading core_carpaint shaders to core_carpaint2'
        for shader in to_upgrade:
            if cmds.objExists(shader):
                new_shader = None
                try:
                    new_shader = cmds.shadingNode('core_carpaint2', asShader=True)
                    mel.eval('upgradeMentalRayShader("%s", "%s", true, "");' % (shader, new_shader))
                except:
                    print 'MentalCore(): Error upgrading shader "%s"' % shader
                    if new_shader:
                        cmds.delete(new_shader)


def beforeExportCB(*args):
    '''Run whenever a export operation begins. Used to catch MR export events'''
    global EXPORT
    EXPORT = True
    
def afterExportCB(*args):
    '''Run whenever a export operation finishes. Used to catch MR export events'''
    global EXPORT
    EXPORT = False