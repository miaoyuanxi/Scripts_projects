#  Copyright (c)2013 Core CG
#  All rights reserved
#  www.core-cg.com

'''The MentalCore Python API provides various functions that allow MentalCore to be easily integrated into any pipeline.
It contains a variety of functions for creating, editing, linking render passes, as well as a few utility and helper functions.
As it is currently in beta, the api may change with each release.

It should be imported as follows:

>>> from mentalcore import mapi

To enable or disable MentalCore and create all necessary nodes, use the enable function:

>>> mapi.enable(True)

To get a list of all available render passes that can be created, use the AVALIABLE_PASSES global variable:

>>> print mapi.AVALIABLE_PASSES
... ['Beauty', 'Colour', 'Diffuse', 'Diffuse Raw', 'Shadow', 'Shadow Raw', 'Diffuse Without Shadows', 'Diffuse Without Shadows Raw', 'Ambient', 'Ambient Raw', 'Indirect', 'Indirect Raw', 'Ambient Occlusion', 'Translucency', 'Subsurface', 'Subsurface Front', 'Subsurface Mid', 'Subsurface Back', 'Incandesence', 'Specular', 'Reflection', 'Refraction', 'Bloom Source', 'Depth', 'Depth (Normalized)', 'Normal World', 'Normal World (Normalized)', 'Normal Camera', 'Normal Camera (Normalized)', 'Point World', 'Point Camera', 'Motion Vector', 'Motion Vector (Normalized)', 'Opacity', 'Facing Ratio', 'UV', 'Material ID', 'Object ID', 'Matte', 'Custom Colour', 'Custom Vector']

Render pass can be created as follows:

>>> mapi.create_pass('diffuse')
... diffuse

To get a list of all render passes associated to a specific layer:

>>> mapi.get_associated_passes('layer1')
... [u'ambient', u'colour', u'diffuse', u'matte_chair', u'matte_house', u'matte_tree']

To link the currently selected objects to a render pass:

>>> mapi.link_selected_to_pass('diffuse_raw', mapi.OBJECTS)

For more information, see the documentation below.
'''

## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
import sys, os
import subprocess
import pickle
import traceback
import shutil
import glob

try:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya.OpenMaya as om

    import mentalcore
    import mlib
    import passpresets
except:
    pass

## ------------------------------------------------------------------------
## GLOBAL VARIABLES
## ------------------------------------------------------------------------
AVALIABLE_PASSES = ['Beauty', 
                    'Colour', 
                    'Diffuse', 
                    'Diffuse Raw', 
                    'Shadow', 
                    'Shadow Raw', 
                    'Diffuse Without Shadows', 
                    'Diffuse Without Shadows Raw', 
                    'Ambient', 
                    'Ambient Raw', 
                    'Indirect', 
                    'Indirect Raw', 
                    'Ambient Occlusion', 
                    'Translucency', 
                    'Subsurface', 
                    'Subsurface Front', 
                    'Subsurface Mid', 
                    'Subsurface Back', 
                    'Incandescence', 
                    'Specular', 
                    'Reflection', 
                    'Refraction',
                    'Light Select',
                    'Bloom Source',
                    'Environment', 
                    'Depth', 
                    'Depth (Normalized)',
                    'Normal World',
                    'Normal World (Normalized)', 
                    'Normal Camera',
                    'Normal Camera (Normalized)',
                    'Point World', 
                    'Point Camera', 
                    'Motion Vector', 
                    'Motion Vector (Normalized)', 
                    'Opacity', 
                    'Facing Ratio', 
                    'UV', 
                    'Material ID', 
                    'Object ID', 
                    'Matte', 
                    'Custom Colour',
                    'Custom Vector',
                    'Diagnostic Samples',
                    'Diagnostic Error',
                    'Diagnostic Time']
OBJECTS, MATERIALS, LIGHTS = range(3)
IMF_COPY = None

## ------------------------------------------------------------------------
## DEFAULT NODES
## ------------------------------------------------------------------------
def create_default_nodes():
    '''Creates the default MentalCore nodes. This happens automatically when enabling MentalCore'''
    #check maya version
    maya_ver = int(cmds.about(f=True))
    
    #Maya version
    maya2014 = False
    if maya_ver >= 2014:
        maya2014 = True
    
    #create default mi nodes
    mel.eval('miCreateDefaultNodes')

    #create core globals
    if not cmds.objExists('mentalcoreGlobals'):
        cmds.createNode('core_globals', n='mentalcoreGlobals', ss=True)
        cmds.setAttr('mentalcoreGlobals.primary_group', 'beauty', type='string')
        
        cmds.addAttr('mentalcoreGlobals', ln='version', dt='string')
        cmds.setAttr('mentalcoreGlobals.version', '%.1f' % mentalcore.VERSION, type='string')
        cmds.setAttr('mentalcoreGlobals.version', lock=True)
        
        #Defaults for maya versions
        if maya2014:
            cmds.setAttr('mentalcoreGlobals.exr_comp', 5) # ZipS compression
        
        cmds.lockNode('mentalcoreGlobals', l=True)
    
    #create core lens
    if not cmds.objExists('mentalcoreLens'):
        cmds.createNode('core_lens', n='mentalcoreLens', ss=True)
        cmds.lockNode('mentalcoreLens', l=True)
        
    #set image format to exr
    cmds.setAttr('defaultRenderGlobals.imfPluginKey', 'exr', type='string')
    cmds.setAttr('defaultRenderGlobals.imageFormat', 51)

## ------------------------------------------------------------------------
## ENABLE TRIGGER
## ------------------------------------------------------------------------
def enable(state):
    '''Enables or disables MentalCore in a scene and creates necessary default nodes.
    
    >>> from mentalcore import mapi
    >>> mapi.enable(True)
    '''

    if state:
        create_default_nodes()
        
        cmds.setAttr('mentalcoreGlobals.enable', True)
    
        #Pre/Post render commands
        pre_mel = cmds.getAttr('defaultRenderGlobals.preMel')
        post_mel = cmds.getAttr('defaultRenderGlobals.postMel')

        if not pre_mel:
            pre_mel = ''
        if not post_mel:
            post_mel = ''

        mc_pre_mel = 'python("import mentalcore; mentalcore.pre_render()");'
        mc_post_mel = 'python("import mentalcore; mentalcore.post_render()");'

        if not mc_pre_mel in pre_mel:
            cmds.setAttr('defaultRenderGlobals.preRenderLayerMel', '%s%s' % (mc_pre_mel, pre_mel), type='string')
        if not mc_pre_mel in pre_mel:
            cmds.setAttr('defaultRenderGlobals.postRenderLayerMel', '%s%s' % (mc_post_mel, post_mel), type='string')

    else:
        cmds.setAttr('mentalcoreGlobals.enable', False)
    
        #Remove Pre/Post render commands
        pre_mel = cmds.getAttr('defaultRenderGlobals.preRenderLayerMel')
        post_mel = cmds.getAttr('defaultRenderGlobals.postRenderLayerMel')

        if not pre_mel:
            pre_mel = ''
        if not post_mel:
            post_mel = ''

        mc_pre_mel = 'python("import mentalcore; mentalcore.pre_render()");'
        mc_post_mel = 'python("import mentalcore; mentalcore.post_render()");'

        cmds.setAttr('defaultRenderGlobals.preRenderLayerMel', pre_mel.replace(mc_pre_mel, ''), type='string')
        cmds.setAttr('defaultRenderGlobals.postRenderLayerMel', post_mel.replace(mc_post_mel, ''), type='string')
            
            
## ------------------------------------------------------------------------
## RESET MENTALCORE
## ------------------------------------------------------------------------
def reset(show_dialog=True, *args):
    '''Resets MentalCore and deletes all default nodes.'''
    
    if show_dialog:
        dialog_res = cmds.confirmDialog( title='Reset MentalCore', message='This will remove all MentalCore global nodes and settings, continue?', button=['Yes','No'], defaultButton='No', cancelButton='No', dismissString='No' )
    else:
        dialog_res = 'Yes'
    
    if dialog_res == 'Yes':
        try:
            enable(False)
            cmds.lockNode('mentalcoreGlobals', l=False)
            cmds.delete('mentalcoreGlobals')
        except:
            pass
            
        try:
            cmds.lockNode('mentalcoreLens', l=False)
            cmds.delete('mentalcoreLens')
        except:
            pass


## ------------------------------------------------------------------------
## RENDERPASS FUNCTIONS
## ------------------------------------------------------------------------
def create_pass(type, n=None):
    '''Creates a pass with the given type (one of mapi.AVALIABLE_PASSES)
    
    >>> mapi.create_pass('diffuse_raw')
    
    Optional argument 'n' is used to specify a name for the pass.
    
    >>> mapi.create_pass('diffuse_raw', n='myDiffusePass')
    
    Returns the name of the created renderpass.
    '''
    
    #Check pass type
    if not type in AVALIABLE_PASSES:
        raise Exception, '%s is not a valid render pass type. Must be one of mapi.AVALIABLE_PASSES' % type
    
    if n:
        pass_name = n
    else:
        pass_name = str(type)
        pass_name = pass_name.lower()
        pass_name = pass_name.replace(' ', '_')
        pass_name = pass_name.replace('(normalized)', 'norm')
        pass_name = pass_name.replace('without', 'no')
        pass_name = pass_name.replace('subsurface', 'sss')
        pass_name = pass_name.replace('ambient_occlusion', 'ao')
        pass_name = pass_name.replace('light_select', 'light')

    rp = cmds.createNode('core_renderpass', n=pass_name)
    passpresets.set_type(rp, type)
    
    return rp
    
def is_pass_associated(rp, layer):
    '''Checks if the renderpass is associated with the specified layer'''
    '''
    exist_conn = cmds.listConnections('%s.renderlayer' % rp)
    if exist_conn:
        if layer in exist_conn:
            return True
    return False
    '''
    if cmds.attributeQuery('mc_renderpasses', n=layer, exists=True):
        exist_conn = cmds.listConnections('%s.mc_renderpasses' % layer)
        if exist_conn:
            if rp in exist_conn:
                return True
    return False
    
def get_associated_passes(layer):
    '''List all render passes associated to the specified layer'''
    '''
    passes = cmds.listConnections('%s.message' % layer, type='core_renderpass')
    if passes:
        passes.sort()
        return passes
    else:
        return []
    '''
    if cmds.attributeQuery('mc_renderpasses', n=layer, exists=True):
        passes = cmds.listConnections('%s.mc_renderpasses' % layer, type='core_renderpass')
        if passes:
            passes.sort()
            return passes
    return []
    
def get_unassociated_passes(layer):
    '''Lists all passses not associated to the specified layer'''
    associated_passes = get_associated_passes(layer)
    all_passes = cmds.ls(type='core_renderpass')
    
    if associated_passes:
        unassociated_passes = []
        for rp in all_passes:
            if not rp in associated_passes:
                unassociated_passes.append(rp)
                
        unassociated_passes.sort()
        return unassociated_passes
    else:
        if all_passes:
            return all_passes
        else:
            return []
            
def get_all_passes():
    '''Lists all passes in the scene'''
    all_passes = cmds.ls(type='core_renderpass')
    return [rp for rp in all_passes if not ':' in rp]
            
    
def associate_pass(rp, layer):
    '''Associates a render pass with the specified render layer'''
    '''
    if cmds.objExists(rp) and cmds.objExists(layer): 
        if cmds.nodeType(rp) == 'core_renderpass' and cmds.nodeType(layer) == 'renderLayer':
            if not is_pass_associated(rp, layer):
                mlib.connect_next_avaliable('%s.message' % layer, '%s.renderlayer' % rp)
    '''
    if cmds.objExists(rp) and cmds.objExists(layer): 
        if cmds.nodeType(rp) == 'core_renderpass' and cmds.nodeType(layer) == 'renderLayer':
            if not is_pass_associated(rp, layer):
                if not cmds.attributeQuery('mc_renderpasses', n=layer, exists=True):
                    cmds.addAttr(layer, ln='mc_renderpasses', at='message', m=True)
                #Connect pass to layer
                mlib.connect_next_avaliable('%s.message' % rp, '%s.mc_renderpasses' % layer)
                
def unassociate_pass(rp, layer):
    '''Unassociates a render pass with the specified layer'''
    '''
    layer_conn = cmds.listConnections('%s.renderlayer' % rp, type='renderLayer', c=True, p=True)
    if layer_conn:    
        for i in range(len(layer_conn)/2):
            rp_attr = layer_conn[i*2]
            layer_attr = layer_conn[i*2+1]
            layer_name = layer_attr.split('.')[0]
            
            if layer_name == layer:
                cmds.disconnectAttr(layer_attr, rp_attr)
    '''
    pass_conn = cmds.listConnections('%s.mc_renderpasses' % layer, type='core_renderpass', c=True, p=True)
    if pass_conn:    
        for i in range(len(pass_conn)/2):
            layer_attr = pass_conn[i*2]
            pass_attr = pass_conn[i*2+1]
            pass_name = pass_attr.split('.')[0]
            
            if pass_name == rp:
                cmds.disconnectAttr(pass_attr, layer_attr)
                    
                    
def set_preview(rp):
    '''Sets the specified render pass as the current preview pass'''
    if cmds.objExists('mentalcoreGlobals'):
        cur_pass = get_preview()
        if cur_pass:
            cmds.disconnectAttr('%s.message' % cur_pass, 'mentalcoreGlobals.preview_pass')
        
        if rp and rp != 'None':
            cmds.connectAttr('%s.message' % rp, 'mentalcoreGlobals.preview_pass', f=True)

            
def get_preview():
    '''Returns the current prevew pass'''
    if cmds.objExists('mentalcoreGlobals'):
        preview_conn = cmds.listConnections('mentalcoreGlobals.preview_pass', type='core_renderpass')
        if preview_conn:
            return preview_conn[0]
                
            
## ------------------------------------------------------------------------
## RENDERPASS LINKING
## ------------------------------------------------------------------------
def _is_geo_transform(obj):
    if cmds.listRelatives(obj, s=True, type=['mesh', 'nurbsSurface', 'subdiv'], f=True):
        return True
    else:
        return False

def _get_selected_objects():
    '''Reurns a list of the selected objects that can be linked to a pass'''
    #selected transforms
    sel = cmds.ls(sl=True, type='transform')
    sel_objects = [obj for obj in sel if _is_geo_transform(obj)]
    
    #hierachy transforms
    trans = cmds.listRelatives(f=True, ad=True, type='transform')
    
    #find transforms with geo
    if trans:
        objects = [obj for obj in trans if cmds.listRelatives(obj, s=True, type=['mesh', 'nurbsSurface', 'subdiv'], f=True)]
        if objects:
            #add current selection
            if sel_objects:
                objects.extend(sel_objects)
            return objects
        else:
            #add current selection
            if sel_objects:
                return sel_objects
            else:
                return []
    else:
        #add current selection
        if sel_objects:
            return sel_objects
        else:
            return []
        
def _get_selected_materials():
    '''Reurns a list of the selected materials that can be linked to a pass'''
    selected = cmds.ls(sl=True)
    if selected:
        sg_list = []
        for node in selected:
            node_type = cmds.nodeType(node)
            if node_type == 'shadingEngine':
                sg_list.append(node)
            else:
                sg_conn = cmds.listConnections(node, type='shadingEngine')
                if sg_conn:
                    for sg in sg_conn:
                        sg_list.append(sg)
                        
        return sg_list
            
def _get_selected_lights():
    '''Reurns a list of the selected lights that can be linked to a pass'''
    lights = cmds.listRelatives(f=True, ad=True, type=['light'])
    if lights:
        light_list = []
        for light in lights:
            transform = cmds.listRelatives(light, p=True, f=True)
            if transform:
                light_list.append(transform[0])
                
        return light_list
        
# -------------------------------------------------------------------------
    

def link_selected_to_pass(rp, type, *args):
    '''Links the selected instances of the specified type to to the renderpass or list of renderpasses.
    
    Type must be one of mapi.OBJECTS, mapi.MATERIALS or mapi.LIGHTS
    
    >>> mapi.link_selected_to_pass('diffuse_raw', mapi.OBJECTS)
    '''
    if type == OBJECTS:
        objects = _get_selected_objects()
        if objects:
            if rp.__class__ == list:
                for renderpass in rp:
                    link_to_pass(objects, renderpass, type)
            else:
                link_to_pass(objects, rp, type)
                
    elif type == MATERIALS:
        sg_list = _get_selected_materials()
        if sg_list:
            if rp.__class__ == list:
                for renderpass in rp:
                    link_to_pass(sg_list, renderpass, type)
            else:
                link_to_pass(sg_list, rp, type)
                    
    elif type == LIGHTS:
        light_list = _get_selected_lights()
        if light_list:
            if rp.__class__ == list:
                for renderpass in rp:
                    link_to_pass(light_list, renderpass, type)
            else:
                link_to_pass(light_list, rp, type)
        

def link_to_pass(list, rp, type, *args):
    '''Links the specifed list of nodes of the specified type to the renderpass.
    
    Type must be one of mapi.OBJECTS, mapi.MATERIALS or mapi.LIGHTS
    
    >>> mapi.link_to_pass(['pSphere1', 'pCube1'], 'diffuse_raw', mapi.OBJECTS)
    '''
    if list:
        if type == OBJECTS:
            #Enable object linking
            cmds.setAttr('%s.en_obj_linking' % rp, True)
            
            #link objects
            for node in list:
                node_type = cmds.nodeType(node)
                if node_type == 'transform':
                    exist_conn = cmds.listConnections(node, type='core_renderpass')
                    if not exist_conn or not rp in exist_conn:
                        mlib.connect_next_avaliable('%s.message' % node, '%s.linked_objs' % rp)
                    
        elif type == MATERIALS:
            #Enable material linking
            cmds.setAttr('%s.en_obj_linking' % rp, True)
                        
            #link materials
            for node in list:
                node_type = cmds.nodeType(node)
                if node_type == 'shadingEngine':
                    exist_conn = cmds.listConnections(node, type='core_renderpass')
                    if not exist_conn or not rp in exist_conn:
                        mlib.connect_next_avaliable('%s.message' % node, '%s.linked_mats' % rp)
    
        elif type == LIGHTS:
            #Enable light linking
            cmds.setAttr('%s.en_light_linking' % rp, True)
                        
            #link lights
            for node in list:
                shape = cmds.listRelatives(node, s=True, f=True)
                if shape:
                    node_type = cmds.nodeType(shape[0], i=True)
                    if 'light' in node_type:
                        exist_conn = cmds.listConnections(node, type='core_renderpass')
                        if not exist_conn or not rp in exist_conn:
                            mlib.connect_next_avaliable('%s.message' % node, '%s.linked_lights' % rp)
                            
# -------------------------------------------------------------------------
                            
def unlink_selected_from_pass(rp, type, *args):
    '''Unlinks the selected instances of the specified type to to the renderpass or list of renderpasses.
    
    Type must be one of mapi.OBJECTS, mapi.MATERIALS or mapi.LIGHTS
    
    >>> mapi.unlink_selected_from_pass('diffuse_raw', mapi.MATERIALS)
    '''
    if type == OBJECTS:
        objects = _get_selected_objects()
        if objects:
            if rp.__class__ == list:
                for renderpass in rp:
                    unlink_from_pass(objects, renderpass, type)
                    _updated_linked_enable(renderpass, type)
            else:
                unlink_from_pass(objects, rp, type)
                _updated_linked_enable(rp, type)
                
    elif type == MATERIALS:
        sg_list = _get_selected_materials()
        if sg_list:
            if rp.__class__ == list:
                for renderpass in rp:
                    unlink_from_pass(sg_list, renderpass, type)
                    _updated_linked_enable(renderpass, type)
            else:
                unlink_from_pass(sg_list, rp, type)
                _updated_linked_enable(rp, type)
                    
    elif type == LIGHTS:
        light_list = _get_selected_lights()
        if light_list:
            if rp.__class__ == list:
                for renderpass in rp:
                    unlink_from_pass(light_list, renderpass, type)
                    _updated_linked_enable(renderpass, type)
            else:
                unlink_from_pass(light_list, rp, type)
                _updated_linked_enable(rp, type)
        

def unlink_from_pass(list, rp, type, *args):
    '''Unlinks the specifed list of nodes of the specified type from the renderpass.
    Type must be one of: 
    
    Type must be one of mapi.OBJECTS, mapi.MATERIALS or mapi.LIGHTS
    
    >>> mapi.unlink_from_pass(['core_material1', 'core_material2'], 'diffuse_raw', mapi.MATERIALS)
    '''
    if list:
        for node in list:
            exist_conn = cmds.listConnections(node, type='core_renderpass', p=True)
            if exist_conn:
                for conn in exist_conn:
                    try:
                        cmds.disconnectAttr('%s.message' % node, conn)
                    except:
                        pass
                        
# -------------------------------------------------------------------------
                        
def unlink_all_from_pass(rp, type, *args):
    '''Unlinks all instances of the specified type from the renderpass or list of renderpasses.
    
    Type must be one of mapi.OBJECTS, mapi.MATERIALS or mapi.LIGHTS
    
    >>> mapi.unlink_all_from_pass('diffuse_raw', mapi.LIGHTS)
    '''
    def unlink_pass(rp, type):
        exist_conn = []
        if type == OBJECTS:
            exist_conn = cmds.listConnections('%s.linked_objs' % rp, c=True, p=True)
        elif type == MATERIALS:
            exist_conn = cmds.listConnections('%s.linked_mats' % rp, c=True, p=True)
        elif type == LIGHTS:
            exist_conn = cmds.listConnections('%s.linked_lights' % rp, c=True, p=True)
        
        if exist_conn:
            for i in range(len(exist_conn)/2):
                rp_attr = exist_conn[i*2]
                obj_attr = exist_conn[i*2+1]
                cmds.disconnectAttr(obj_attr, rp_attr)
        
    if rp.__class__ == list:
        for renderpass in rp:
            unlink_pass(renderpass, type)
            _updated_linked_enable(renderpass, type)
    else:
        unlink_pass(rp, type)
        _updated_linked_enable(rp, type)
        
        
def _updated_linked_enable(rp, type):
    '''Enables or disables object/material/light linking on a pass if no links exist'''
    if type in (OBJECTS, MATERIALS):
        exist_obj_conn = cmds.listConnections('%s.linked_objs' % rp)
        exist_mat_conn = cmds.listConnections('%s.linked_mats' % rp)
        
        if not exist_obj_conn and not exist_mat_conn:
            cmds.setAttr('%s.en_obj_linking' % rp, False)
        else:
            cmds.setAttr('%s.en_obj_linking' % rp, True)
    else:
        exist_light_conn = cmds.listConnections('%s.linked_lights' % rp)
        
        if not exist_light_conn:
            cmds.setAttr('%s.en_light_linking' % rp, False)
        else:
            cmds.setAttr('%s.en_light_linking' % rp, True)
            
# -------------------------------------------------------------------------
            
def select_pass_linked(rp, type, *args):
    '''Selects all objects of a specified type linked to a renderpass or list of renderpasses.
    
    Type must be one of mapi.OBJECTS, mapi.MATERIALS or mapi.LIGHTS
    
    >>> mapi.select_pass_linked('diffuse_raw', mapi.LIGHTS)
    '''
    def select_linked(rp, type):
        if type == OBJECTS:
            exist_conn = cmds.listConnections('%s.linked_objs' % rp)
            if exist_conn:
                for node in exist_conn:
                    if not cmds.nodeType(node) == 'transform':
                        transform = cmds.listRelatives(node, p=True, f=True)
                        if transform:
                            cmds.select(transform, add=True)
                    else:
                        cmds.select(node, add=True)
        elif type == MATERIALS:
            exist_conn = cmds.listConnections('%s.linked_mats' % rp)
            if exist_conn:
                for node in exist_conn:
                    cmds.select(node, add=True)
        elif type == LIGHTS:
            exist_conn = cmds.listConnections('%s.linked_lights' % rp)
            if exist_conn:
                for node in exist_conn:
                    cmds.select(node, add=True)
        
    cmds.select(cl=True)
        
    if rp.__class__ == list:
        for renderpass in rp:
            select_linked(renderpass, type)
    else:
        select_linked(rp, type)
        

## ------------------------------------------------------------------------
## PRESETS
## ------------------------------------------------------------------------

def _collect_preset_info(*args):
    '''Collects a list of render passes and all their attributes. Used to save presets.'''
    passes_info = []
    for rp in get_all_passes():
        rp_attrs = {}    
        for attr in cmds.listAttr(rp, se=True, hd=True):
            if not attr in ('caching', 'isHistoricallyInteresting', 'nodeState', 'miFactoryNode', 'miForwardDefinition', 'binMembership'):
                try:
                    rp_attrs[attr] = cmds.getAttr('%s.%s' % (rp, attr))
                except:
                    pass
                 
        passes_info.append({'pass':rp, 'attrs':rp_attrs})

    return passes_info
    
def _apply_preset_info(preset_info, *args):
    '''Applies preset into to the scene to recreate render passes. Used to load presets.'''
    for rp_info in preset_info:
        print 'MentalCore(): Loading renderpass: "%s"' % rp_info['pass']
        rp = cmds.createNode('core_renderpass', n=rp_info['pass'])

        for attr, value in rp_info['attrs'].items():
            try:
                if type(value) in (str, unicode):
                    cmds.setAttr('%s.%s' % (rp, attr), value, type='string')
                else:
                    cmds.setAttr('%s.%s' % (rp, attr), value)
            except:
                print 'MentalCore(): Error applying renderpass attribute "%s.%s"' % (rp, attr)

def save_preset(*args):
    '''Brings up a file dialog where a render pass preset can be saved.'''
    #collect preset info
    preset_info = _collect_preset_info()

    #preset directory
    project_dir = cmds.workspace(q=True, rd=True)
    preset_dir = os.path.join(project_dir, 'presets', 'mentalcore')

    #check preset dir exists
    if not os.path.exists(preset_dir):
        os.makedirs(preset_dir)

    #file dialog
    preset_file = cmds.fileDialog2(fileFilter="MentalCore Preset (*.mcp)", dialogStyle=2, fm=0, dir=preset_dir)

    if preset_file:
        preset_file = preset_file[0]

        #dump pickle
        f = open(preset_file, 'wb')
        pickle.dump( preset_info, f )
        f.close()
                
        print 'MentalCore(): Preset saved to: "%s"' % preset_file
        
        
def load_preset(*args):
    '''Brings up a file dialog where a render pass preset can be loaded'''
    #preset directory
    project_dir = cmds.workspace(q=True, rd=True)
    preset_dir = os.path.join(project_dir, 'presets', 'mentalcore')

    #check preset dir exists
    if not os.path.exists(preset_dir):
        os.makedirs(preset_dir)

    #file dialog
    preset_file = cmds.fileDialog2(fileFilter="MentalCore Preset (*.mcp)", dialogStyle=2, fm=1, dir=preset_dir)

    if preset_file:
        preset_file = preset_file[0]

        #load pickle
        f = open(preset_file, 'rb')
        preset_info = pickle.load( f )
        f.close()

        #apply preset
        if preset_info:
            print 'MentalCore(): Loading Renderpass Preset: "%s"' % preset_file
        
            _apply_preset_info(preset_info)
            
            print 'MentalCore(): Preset Loaded'


## ------------------------------------------------------------------------
## ENVIRONMENT LIGHTS
## ------------------------------------------------------------------------
def create_envlight(name='envLight1', show=True, *args):
    '''Creates a new environment light. Returns the new light'''
    # First create area light
    al = cmds.shadingNode('areaLight', asLight=True)
    al = cmds.rename(al, name)
    
    cmds.setAttr('%s.areaLight' % al, True)
    cmds.setAttr('%s.areaType' % al, 4)
    cmds.setAttr('%s.areaHiSamples' % al, 1)
    cmds.setAttr('%s.miExportMrLight' % al, True)
    
    #now create the env light shader
    envShader = cmds.createNode('core_env_light', n='%sShader' % name, ss=True)
    cmds.connectAttr('%s.message' % envShader, '%s.miLightShader' % al, f=True)
    
    #update light locator
    mlib.update_envlight_loc(envShader)
    
    #show in AE
    cmds.select(al)
    if show:
        mel.eval('evalDeferred("showEditor \\"%s\\"")' % envShader)
    
    #return new light
    return str(al)
    
        
## ------------------------------------------------------------------------
## GEOMETRY LIGHTS
## ------------------------------------------------------------------------
def make_geolight(*args):
    '''Converts the selected geometries to a MentalCore geometry light'''
    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            if cmds.listRelatives(obj, s=True, f=True):
                if not cmds.listConnections('%s.message' % obj, type='core_geo_light') :      
                    light_node = cmds.createNode('core_geo_light', n='%s_geo_light' % obj)
                    cmds.connectAttr('%s.message' % obj, '%s.source_geo' % light_node, f=True)
                    
                    light = cmds.shadingNode('mib_light_point', asLight=True, n='%s_light' % obj)
                    cmds.connectAttr('%s.message' % light, '%s.light_shader' % light_node, f=True)
                    
                    cmds.select(light_node, r=True)

def make_objlight(*args):
    '''For Maya 2014+. Converts the selected geometries to a MR 3.11 object light'''
    sel = cmds.ls(sl=True)
    if sel:
        for obj in sel:
            shape = cmds.listRelatives(obj, s=True, f=True)
            if shape and cmds.nodeType(shape[0]) in ['mesh', 'nurbsSurface']:
                sg = cmds.listConnections(shape[0], type='shadingEngine')
                if sg:
                    mat = cmds.listConnections('%s.miMaterialShader' % sg[0], type='builtin_object_light')
                    if mat:
                        # Check for existing object light shader
                        cmds.warning('Object "%s" already has a object light shader assigned!' % obj)
                        continue
                    else:
                        # Create new object light shader
                        shader = cmds.shadingNode('builtin_object_light', asShader=True, ss=True, n='%s_lightShader' % obj)
                        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name='%s_SG' % shader)
                        cmds.setAttr('%s.miExportShadingEngine' % sg, False)
                        cmds.connectAttr('%s.message' % shader, '%s.miMaterialShader' % sg)
                        cmds.sets(shape[0], e=True, fe=sg)
                        
                        # Create new area light
                        light = cmds.shadingNode('areaLight', asLight=True, ss=True, n='%s_areaLight' % obj)
                        light_shape = cmds.listRelatives(light, s=True, f=True)[0]
                        cmds.connectAttr('%s.message' % light, '%s.light' % shader)
                        cmds.parent(light, obj, r=True)
                        
                        # Set geo render stats
                        cmds.setAttr('%s.castsShadows' % shape[0], False)
                        cmds.setAttr('%s.receiveShadows' % shape[0], False)
                        
                        # Set area light attributes
                        cmds.setAttr('%s.areaLight' % light, True)
                        cmds.setAttr('%s.areaVisible' % light, True)
                        cmds.setAttr('%s.useRayTraceShadows' % light, True)

                        cmds.select(light, r=True)

## ------------------------------------------------------------------------
## SHADER CONVERSION
## ------------------------------------------------------------------------
def core_node_cast(old_shader, new_shader):
    '''Replaces settings and connections between two similar shaders with identical attributes where possible'''
    #copy attribte values
    for attr in cmds.listAttr(old_shader, multi=True, write=True, scalar=True, visible=True, hasData=True):
        try:
            value = cmds.getAttr(old_shader + '.' + attr)
            cmds.setAttr(new_shader + '.' + attr, value)
        except:
            pass

    #restore input connections
    input_connections = []
    conn_buffer = []
    conn_list = cmds.listConnections(old_shader, s=True, d=False, p=True, c=True)

    if conn_list:
        for i in range(len(conn_list)):
            if i % 2:
                conn_buffer.insert(0, conn_list[i])
                input_connections.append(conn_buffer)
            else:
                conn_buffer = [conn_list[i]]
                
        for src, dest in input_connections:
            try:
                cmds.connectAttr(src, dest.replace(old_shader, new_shader), f=True)
            except:
                pass
            
    #restore output connections
    ouput_connections = []
    conn_buffer = []
    conn_list = cmds.listConnections(old_shader, s=False, d=True, p=True, c=True)

    if conn_list:
        for i in range(len(conn_list)):
            if i % 2:
                conn_buffer.append(conn_list[i])
                ouput_connections.append(conn_buffer)
            else:
                conn_buffer = [conn_list[i]]        
                
        for src, dest in ouput_connections:
            try:
                cmds.connectAttr(src.replace(old_shader, new_shader), dest, f=True)
            except:
                pass
            
            

def sss_shader_to_core(shader, material):
    '''Converts the specified sss shader to MentalCore shader where possible.

    >>> mapi.sss_shader_to_core('misss_fast_skin1', 'blinn1')
    '''
    sss_type = cmds.nodeType(shader)
    if sss_type == 'misss_fast_skin_maya':
        #create mentalcore sss node
        mc_shader = cmds.shadingNode('core_skin_sss', asShader=True)

        #swap nodes
        core_node_cast(shader, mc_shader)
        
        #diffuse weight
        has_diffuse_weight = False
        conn = cmds.listConnections(shader + '.diffuse_weight', s=True, d=False, p=True)
        if conn:
            cmds.connectAttr(conn[0], material + '.diffuse_weight', f=True)
            has_diffuse_weight = True
        else:
            dif = cmds.getAttr(shader + '.diffuse_weight')
            if dif != 0:
                cmds.setAttr(material + '.diffuse_weight', dif)
                has_diffuse_weight = True
        
        #diffuse color
        if not cmds.listConnections(material + '.diffuse', s=True, d=False):
            conn = cmds.listConnections(shader + '.diffuse_color', s=True, d=False, p=True)
            if conn and has_diffuse_weight:
                cmds.connectAttr(conn[0], material + '.diffuse', f=True)
            else:
                col = cmds.getAttr(shader + '.diffuse_color')[0]
                if col[0] != 1.0 or col[1] != 1.0 or col[2] != 1.0 and has_diffuse_weight:
                    cmds.setAttr(material + '.diffuse', col[0], col[1], col[2])
                
        #overall color
        conn = cmds.listConnections(shader + '.overall_color', s=True, d=False, p=True)
        if conn:
            overall_shader = cmds.shadingNode('core_texture_merge', asShader=True)
            cmds.setAttr('%s.operation' % overall_shader, 2)
            cmds.connectAttr(conn[0], overall_shader + '.input_a', f=True)

            conn_diff = cmds.listConnections(material + '.diffuse', s=True, d=False, p=True)
            if conn_diff:
                cmds.connectAttr(conn_diff[0], overall_shader + '.input_b', f=True)
            else:
                col = cmds.getAttr(material + '.diffuse')[0]
                cmds.setAttr(overall_shader + '.input_b', col[0], col[1], col[2])

            cmds.connectAttr('%s.outColor' % overall_shader, material + '.diffuse', f=True)
           
        else:
            col = cmds.getAttr(shader + '.overall_color')[0]
            if col[0] != 1.0 or col[1] != 1.0 or col[2] != 1.0:
                overall_shader = cmds.shadingNode('core_texture_merge', asShader=True)
                cmds.setAttr('%s.operation' % overall_shader, 2)
                cmds.setAttr('%s.input_a' % overall_shader, col[0], col[1], col[2])

                conn_diff = cmds.listConnections(material + '.diffuse', s=True, d=False, p=True)
                if conn_diff:
                    cmds.connectAttr(conn_diff[0], overall_shader + '.input_b', f=True)
                else:
                    col = cmds.getAttr(material + '.diffuse')[0]
                    cmds.setAttr(overall_shader + '.input_b', col[0], col[1], col[2])

                cmds.connectAttr('%s.outColor' % overall_shader, material + '.diffuse', f=True)

        #delete old shader and rename
        cmds.delete(shader)
        cmds.rename(mc_shader, shader)

        return True
        
    elif sss_type in ['misss_fast_simple_maya','misss_fast_shader', 'misss_fast_shader_x', 'misss_fast_shader_x_passes']:
        #create mentalcore sss node
        mc_shader = cmds.shadingNode('core_simple_sss', asShader=True)

        #swap nodes
        core_node_cast(shader, mc_shader)

        #diffuse weight
        has_diffuse_weight = False
        conn = cmds.listConnections(shader + '.diffuse_weight', s=True, d=False, p=True)
        if conn:
            cmds.connectAttr(conn[0], material + '.diffuse_weight', f=True)
            has_diffuse_weight = True
        else:
            dif = cmds.getAttr(shader + '.diffuse_weight')
            if dif != 0:
                cmds.setAttr(material + '.diffuse_weight', dif)
                has_diffuse_weight = True
        
        #diffuse color
        if not cmds.listConnections(material + '.diffuse', s=True, d=False):
            conn = cmds.listConnections(shader + '.diffuse_color', s=True, d=False, p=True)
            if conn and has_diffuse_weight:
                cmds.connectAttr(conn[0], material + '.diffuse', f=True)
            else:
                col = cmds.getAttr(shader + '.diffuse_color')[0]
                if col[0] != 1.0 or col[1] != 1.0 or col[2] != 1.0 and has_diffuse_weight:
                    cmds.setAttr(material + '.diffuse', col[0], col[1], col[2])
                
        #overall color
        if sss_type == 'misss_fast_simple_maya':
            conn = cmds.listConnections(shader + '.overall_color', s=True, d=False, p=True)
            if conn:
                overall_shader = cmds.shadingNode('core_texture_merge', asShader=True)
                cmds.setAttr('%s.operation' % overall_shader, 2)
                cmds.connectAttr(conn[0], overall_shader + '.input_a', f=True)

                conn_diff = cmds.listConnections(material + '.diffuse', s=True, d=False, p=True)
                if conn_diff:
                    cmds.connectAttr(conn_diff[0], overall_shader + '.input_b', f=True)
                else:
                    col = cmds.getAttr(material + '.diffuse')[0]
                    cmds.setAttr(overall_shader + '.input_b', col[0], col[1], col[2])

                cmds.connectAttr('%s.outColor' % overall_shader, material + '.diffuse', f=True)
               
            else:
                col = cmds.getAttr(shader + '.overall_color')[0]
                if col[0] != 1.0 or col[1] != 1.0 or col[2] != 1.0:
                    overall_shader = cmds.shadingNode('core_texture_merge', asShader=True)
                    cmds.setAttr('%s.operation' % overall_shader, 2)
                    cmds.setAttr('%s.input_a' % overall_shader, col[0], col[1], col[2])

                    conn_diff = cmds.listConnections(material + '.diffuse', s=True, d=False, p=True)
                    if conn_diff:
                        cmds.connectAttr(conn_diff[0], overall_shader + '.input_b', f=True)
                    else:
                        col = cmds.getAttr(material + '.diffuse')[0]
                        cmds.setAttr(overall_shader + '.input_b', col[0], col[1], col[2])

                    cmds.connectAttr('%s.outColor' % overall_shader, material + '.diffuse', f=True)
            
        #delete old shader and rename
        cmds.delete(shader)
        cmds.rename(mc_shader, shader)

        return True

def shader_to_core(shader):
    '''Converts the specified shader to MentalCore shader where possible.

    >>> mapi.shader_to_core('blinn1')
    '''

    #Maya shaders
    valid_types = ['lambert', 'blinn', 'phong']
    type = cmds.nodeType(shader)
    if type in valid_types and not shader == 'lambert1':
        #create core shader
        mc_shader = cmds.shadingNode('core_material', asShader=True)

        #disable spec by default
        cmds.setAttr(mc_shader + '.en_blinn', False)
                
        #colour
        conn = cmds.listConnections(shader + '.color', s=True, d=False, p=True)
        if conn:
            cmds.connectAttr(conn[0], mc_shader + '.diffuse', f=True)
        else:
            col = cmds.getAttr(shader + '.color')[0]
            cmds.setAttr(mc_shader + '.diffuse', col[0], col[1], col[2])
            
        #diffuse
        conn = cmds.listConnections(shader + '.diffuse', s=True, d=False, p=True)
        if conn:
            cmds.connectAttr(conn[0], mc_shader + '.diffuse_weight', f=True)
        else:
            dif = cmds.getAttr(shader + '.diffuse')
            cmds.setAttr(mc_shader + '.diffuse_weight', dif)
            
        #transparency
        conn = cmds.listConnections(shader + '.transparency', s=True, d=False, p=True)
        if conn:
            cmds.connectAttr(conn[0]+'R', mc_shader + '.transparency', f=True)
        else:
            col = cmds.getAttr(shader + '.transparency')[0]
            cmds.setAttr(mc_shader + '.transparency', col[0])

        #incandesence
        conn = cmds.listConnections(shader + '.incandescence', s=True, d=False, p=True)
        if conn:
            cmds.connectAttr(conn[0], mc_shader + '.incandesence', f=True)
        else:
            col = cmds.getAttr(shader + '.incandescence')[0]
            cmds.setAttr(mc_shader + '.incandesence', col[0], col[1], col[2])
            
        #bumpmap
        conn = cmds.listConnections(shader + '.normalCamera', s=True, d=False, p=True)
        if conn:
            cmds.connectAttr(conn[0], mc_shader + '.standard_bump', f=True)

        if type == 'blinn':
            #spec type
            cmds.setAttr(mc_shader + '.en_blinn', True)
            
            #eccentricity
            conn = cmds.listConnections(shader + '.eccentricity', s=True, d=False, p=True)
            if conn:
                cmds.connectAttr(conn[0], mc_shader + '.blinn_ecc', f=True)
            else:
                value = cmds.getAttr(shader + '.eccentricity')
                cmds.setAttr(mc_shader + '.blinn_ecc', value)
                
            #rolloff
            conn = cmds.listConnections(shader + '.specularRollOff', s=True, d=False, p=True)
            if conn:
                cmds.connectAttr(conn[0], mc_shader + '.blinn_rloff', f=True)
            else:
                value = cmds.getAttr(shader + '.specularRollOff')
                cmds.setAttr(mc_shader + '.blinn_rloff', value)
                
            #spec colour
            conn = cmds.listConnections(shader + '.specularColor', s=True, d=False, p=True)
            if conn:
                cmds.connectAttr(conn[0], mc_shader + '.blinn_col', f=True)
            else:
                col = cmds.getAttr(shader + '.specularColor')[0]
                cmds.setAttr(mc_shader + '.blinn_col', col[0], col[1], col[2])
                
            #reflectivity
            conn = cmds.listConnections(shader + '.reflectivity', s=True, d=False, p=True)
            if conn:
                cmds.setAttr(mc_shader + '.en_refl', True)
                cmds.connectAttr(conn[0], mc_shader + '.reflectivity', f=True)
            else:
                value = cmds.getAttr(shader + '.reflectivity')
                if value:
                    cmds.setAttr(mc_shader + '.en_refl', True)
                    cmds.setAttr(mc_shader + '.reflectivity', value)

        elif type == 'phong':
            #spec type            
            cmds.setAttr(mc_shader + '.en_phong', True)
                
            #phong exponent
            conn = cmds.listConnections(shader + '.cosinePower', s=True, d=False, p=True)
            if conn:
                cmds.connectAttr(conn[0], mc_shader + '.phong_exp', f=True)
            else:
                value = cmds.getAttr(shader + '.cosinePower')
                cmds.setAttr(mc_shader + '.phong_exp', value)

            #spec colour
            conn = cmds.listConnections(shader + '.specularColor', s=True, d=False, p=True)
            if conn:
                cmds.connectAttr(conn[0], mc_shader + '.phong_col', f=True)
            else:
                col = cmds.getAttr(shader + '.specularColor')[0]
                cmds.setAttr(mc_shader + '.phong_col', col[0], col[1], col[2])
                
            #reflectivity
            conn = cmds.listConnections(shader + '.reflectivity', s=True, d=False, p=True)
            if conn:
                cmds.setAttr(mc_shader + '.en_refl', True)
                cmds.connectAttr(conn[0], mc_shader + '.reflectivity', f=True)
            else:
                value = cmds.getAttr(shader + '.reflectivity')
                if value:
                    cmds.setAttr(mc_shader + '.en_refl', True)
                    cmds.setAttr(mc_shader + '.reflectivity', value)
                    
        #connect shader to sg
        sg_conn = cmds.listConnections(shader + '.outColor', s=False, d=True, type='shadingEngine')
        sg_plug = cmds.listConnections(shader + '.outColor', s=False, d=True, p=True, type='shadingEngine')

        cmds.disconnectAttr(shader + '.outColor', sg_plug[0])

        cmds.connectAttr(mc_shader + '.message', sg_conn[0] + '.miMaterialShader', f=True)
        cmds.connectAttr(mc_shader + '.message', sg_conn[0] + '.miShadowShader', f=True)
        cmds.connectAttr(mc_shader + '.message', sg_conn[0] + '.miPhotonShader', f=True)

        #delete old shader and rename
        cmds.delete(shader)
        cmds.rename(mc_shader, shader)
        
    #MiaX Shaders
    if type == 'mia_material_x' or type == 'mia_material_x_passes':
        #create core shader
        mc_shader = cmds.shadingNode('core_mia_material', asShader=True)

        #swap nodes
        core_node_cast(shader, mc_shader)

        #convert any sss/incandesence shaders
        add_shader = cmds.listConnections('%s.additional_color' % shader, s=True, d=False)
        if add_shader:
            new_sss_shader = sss_shader_to_core(add_shader[0], mc_shader)
            if new_sss_shader:
                #connect sss shader to subsurface shot
                cmds.connectAttr('%s.message' % add_shader[0], '%s.subsurface' % mc_shader)

                #Check for lightmap node to replace
                sg_conn = cmds.listConnections(mc_shader + '.message', s=False, d=True, type='shadingEngine')
                if sg_conn:
                    sg = sg_conn[0]
                    lmap = cmds.listConnections(sg, s=True, d=False, type='misss_fast_lmap_maya')

                    if lmap:
                        #create core shader
                        mc_lmap = cmds.createNode('core_fast_lmap')

                        #swap nodes
                        core_node_cast(lmap[0], mc_lmap)

                        #delete old shader
                        cmds.delete(lmap[0])
            else:
                #incandesence
                conn = cmds.listConnections(shader + '.additional_color', s=True, d=False, p=True)
                cmds.connectAttr(conn[0], mc_shader + '.incandesence', f=True)
        else:
            #incandesence
            col = cmds.getAttr(shader + '.additional_color')[0]
            cmds.setAttr(mc_shader + '.incandesence', col[0], col[1], col[2])

        #delete old shader and rename
        cmds.delete(shader)
        cmds.rename(mc_shader, shader)
            

def selected_shaders_to_core(*args):
    '''Converts the selected shaders to MentalCore shaders where possible.

    >>> mapi.selected_shaders_to_core()
    '''
    for shader in cmds.ls(sl=True):
        shader_to_core(shader)
        
        
def all_shaders_to_core(*args):
    '''Converts all shaders to MentalCore shaders where possible.

    >>> mapi.all_shaders_to_core()
    '''
    for sg in cmds.ls(type='shadingEngine'):
        if sg != 'initialShadingGroup' and sg != 'initialParticleSE':
            conn_shaders = cmds.listConnections(sg + '.miMaterialShader', s=True, d=False)
            if conn_shaders:
                shader_to_core(conn_shaders[0])
                continue

            conn_shaders = cmds.listConnections(sg + '.surfaceShader', s=True, d=False,)
            if conn_shaders:
                shader_to_core(conn_shaders[0])
                continue
            
            
## ------------------------------------------------------------------------
## LOW RES TEXTURE CONVERSION
## ------------------------------------------------------------------------
def generate_low_res_textures(proxy=False, proxy_res='1/2', proxy_format='png', fg=False, fg_res='1/8', fg_format='png', create_nodes=True, progress=False):
    '''Generates low res proxy and finalgather textures to speed up rendering.
    Only textures connected to a MentalCore core_texture_lookup2 shader will be used during conversion.
    If a converted texture already exists, it will only be regenerated if the original texture is newer.
    
    Arguments:
        proxy (bool) - Generate proxy textures?
        proxy_res (string) - Proxy texture resolution, either 1/2, 1/4, 1/8 or 1/16.
        proxy_format (string) - Proxy texture format, either jpg or png.
        fg (bool) - Generate finalgather textures?
        fg_res (string) - Finalgather texture resolution, either 1/2, 1/4, 1/8 or 1/16.
        fg_format (string) - Finalgather texture format, either jpg or png.
        create_nodes (bool) - If True, create and attach mentalrayTexture nodes.
        progress (bool) - If True, show a progress bar.
    '''
    if not proxy and not fg:
        return
    
    # Build texture node list
    tex_list = []
    for lookup_node in cmds.ls(type='core_texture_lookup2'):
        tex_conn = cmds.listConnections('%s.texture' % lookup_node, type='mentalrayTexture')
        if tex_conn and not tex_conn[0] in tex_list:
            if cmds.getAttr('%s.fileTextureName' % tex_conn[0]) and not cmds.getAttr('%s.miWritable' % tex_conn[0]):
                tex_list.append(tex_conn[0])
            
    # Create progress window
    if progress:
        max = len(tex_list)
        if proxy and fg:
            max *= 2        
        cmds.progressWindow(title='Processing Textures',
                            progress=0,
                            max=max,
                            status='Processing Texture 1 of %d' % max,
                            isInterruptable=True )
        
    print '-----------------------------------------'
    print 'MentalCore(): Generating Low Res Textures'
    print '-----------------------------------------'
        
    j = 0
    has_error = False
        
    # Process textures    
    for i in range(len(tex_list)):
        # Texture node
        tex = tex_list[i]
        tex_path = cmds.getAttr('%s.fileTextureName' % tex)
        tex_file, tex_ext = os.path.splitext(tex_path)
        print 'Processing Texture: %s' % tex_path 
        
        if not os.path.exists(tex_path):
            print '\tSkipping, file does not exist!'
        
        # Process Proxy Texture
        if proxy:
            # Update progress window
            if progress:
                # Check if the dialog has been cancelled
                if cmds.progressWindow( query=True, isCancelled=True ):
                    cmds.progressWindow(endProgress=True)
                    return
                
                j += 1
                cmds.progressWindow(e=True,
                                    step=1,
                                    status='Processing Texture %d of %d' % (j, max))
            
            # Check for proxy texture
            proxy_path = os.path.join('%s_Proxy.%s' % (tex_file, proxy_format))
            
            if ((not os.path.exists(proxy_path)) or
                os.path.getmtime(proxy_path) < os.path.getmtime(tex_path)):
                print '\t- Generating Proxy texture: %s' % os.path.basename(proxy_path)
                
                try:
                    # Resize image
                    _resize_image(tex_path, proxy_path, proxy_res, proxy_format)
                                                       
                except:
                    print '\t- Error converting Proxy texture, skipped! See error below.'
                    print traceback.format_exc(5)
                    has_error = True
            else:
                print '\t- Proxy texture already up to date, skipping!'
                
            # Create texture node
            if create_nodes:
                # Find texture lookup node
                tex_lookup = cmds.listConnections('%s.message' % tex, type='core_texture_lookup2')
                if tex_lookup:
                    for lookup in tex_lookup:
                        # Find proxy texture node, if it exists
                        proxy_tex = cmds.listConnections('%s.proxy_texture' % lookup, type='mentalrayTexture')
                        if proxy_tex:
                            # Proxy texture node already exists
                            proxy_tex = proxy_tex[0]
                        else:
                            # Create new proxy texture node
                            proxy_tex = cmds.shadingNode('mentalrayTexture', asTexture=True, n='%s_Proxy' % tex)  
                            cmds.connectAttr('%s.message' % proxy_tex, '%s.proxy_texture' % lookup, f=True) 
                                
                        # Set proxy texture path                                 
                        cmds.setAttr('%s.fileTextureName' % proxy_tex, proxy_path, type='string') 
                
        # Process FG Texture
        if fg:
            # Update progress window
            if progress:
                # Check if the dialog has been cancelled
                if cmds.progressWindow( query=True, isCancelled=True ):
                    cmds.progressWindow(endProgress=True)
                    return
                
                j += 1
                cmds.progressWindow(e=True,
                                    step=1,
                                    status='Processing Texture %d of %d' % (j, max))
                
            # Check for fg texture
            fg_path = os.path.join('%s_FG.%s' % (tex_file, fg_format))
            
            if ((not os.path.exists(fg_path)) or
                os.path.getmtime(fg_path) < os.path.getmtime(tex_path)):
                print '\t- Generating FG texture: %s' % os.path.basename(fg_path)                
                
                try:
                    # Resize image
                    _resize_image(tex_path, fg_path, fg_res, fg_format)
                except:
                    print '\t- Error converting FG texture, skipped! See error below.'
                    print traceback.format_exc(5)
                    has_error = True
            else:
                print '\t- FG texture already up to date, skipping!'
                
            # Create texture node
            if create_nodes:
                # Find texture lookup node
                tex_lookup = cmds.listConnections('%s.message' % tex, type='core_texture_lookup2')
                if tex_lookup:
                    for lookup in tex_lookup:
                        # Find fg texture node, if it exists
                        fg_tex = cmds.listConnections('%s.fg_texture' % lookup, type='mentalrayTexture')
                        if fg_tex:
                            # FG texture node already exists
                            fg_tex = fg_tex[0]
                        else:
                            # Create new fg texture node
                            fg_tex = cmds.shadingNode('mentalrayTexture', asTexture=True, n='%s_FG' % tex)
                            cmds.connectAttr('%s.message' % fg_tex, '%s.fg_texture' % lookup, f=True) 
                                
                        # Set fg texture path                                 
                        cmds.setAttr('%s.fileTextureName' % fg_tex, fg_path, type='string')  
    
    # End progress window
    if progress:
        cmds.progressWindow(endProgress=True)
        
    # Return True if it was successful with no errors
    return not has_error
        
def _resize_image(src_path, dest_path, res, format):
    # Files and extension
    src_file, src_ext = os.path.splitext(src_path)
    dest_file, dest_ext = os.path.splitext(dest_path)
    
    if src_ext in ('.exr', '.hdr'):
        imf_copy = _find_imf_copy()
        
        if not imf_copy:
            raise Exception, 'Could not find imf_copy!'
        
        proc = subprocess.Popen([imf_copy, src_path, dest_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE
                                )
        
        # Get stdout and stderr
        stdout, stderr = proc.communicate()
        proc.wait()
        
        if not proc.returncode == 0:
            raise Exception, 'Error converting file! %s' % src_path
        
        # Set new src path
        src_path = dest_path
    
    # Read Image
    if not os.path.exists(src_path):
        raise Exception, 'File does not exist! %s' % src_path
    
    img = om.MImage()
    img.readFromFile(src_path)
    
    # Get width/height
    scriptUtil = om.MScriptUtil()
    
    widthPtr = scriptUtil.asUintPtr()
    heightPtr = scriptUtil.asUintPtr()     
               
    scriptUtil.setUint( widthPtr, 0 )
    scriptUtil.setUint( heightPtr, 0 )     
               
    img.getSize( widthPtr, heightPtr )
    
    width = scriptUtil.getUint(widthPtr)
    height = scriptUtil.getUint(heightPtr) 
    
    # Calculate new width/height
    factor = 1
    if res == '1/2':
        factor = 0.5
    elif res == '1/4':
        factor = 0.25
    elif res == '1/8':
        factor = 0.125
    elif res == '1/16':
        factor = 0.0625
    elif res == '1/32':
        factor = 0.03125
    
    new_width = int(width * factor)
    new_height = int(height * factor)
    
    # Resize image
    img.resize(new_width, new_height)
    
    # Write to file
    img.writeToFile(dest_path, format)
    
    # Release Image
    img.release()

def _find_imf_copy():
    global IMF_COPY
    if not IMF_COPY:
        maya_ver = int(cmds.about(f=True))
        
        # Find MR bin directory
        if maya_ver == 2012:
            if os.environ.has_key('MAYA_LOCATION'):
                IMF_COPY = os.path.join(os.environ['MAYA_LOCATION'], 'bin', 'imf_copy')
        else:            
            splitter = ';'
            if not sys.platform == 'win32':
                splitter = ':'            
            for p in os.environ['MAYA_PLUG_IN_PATH'].split(splitter):
                if 'mentalray' in p:
                    mr_bin = os.path.join(os.path.dirname(p), 'bin')
                    if os.path.exists(mr_bin):
                        IMF_COPY = os.path.join(mr_bin, 'imf_copy')
                    
    return IMF_COPY

def delete_low_res_textures(proxy=False, fg=False, from_disk=False, progress=False):
    '''Deletes low res proxy and finalgather textures from the scene and optionally from the disk.
    
    Arguments:
        proxy (bool) - Delete proxy textures?
        fg (bool) - Delete finalgather textures?
        from_disk (bool) - If True, also delete the textures from disk.
        progress (bool) - If True, show a progress bar.
    '''
    if not proxy and not fg:
        return

    # Build texture node list
    tex_list = []
    for lookup_node in cmds.ls(type='core_texture_lookup2'):
        tex_conn = cmds.listConnections('%s.texture' % lookup_node, type='mentalrayTexture')
        if tex_conn and not tex_conn[0] in tex_list:
            if cmds.getAttr('%s.fileTextureName' % tex_conn[0]) and not cmds.getAttr('%s.miWritable' % tex_conn[0]):
                tex_list.append(tex_conn[0])
            
    # Create progress window
    if progress:
        max = len(tex_list)
        if proxy and fg:
            max *= 2        
        cmds.progressWindow(title='Cleaning Up Textures',
                            progress=0,
                            max=max,
                            status='Deleting Texture 1 of %d' % max,
                            isInterruptable=True )
        
    j = 0
    has_error = False
        
    # Process textures    
    for i in range(len(tex_list)):
        # Texture node
        tex = tex_list[i]
        tex_path = cmds.getAttr('%s.fileTextureName' % tex)
        tex_file, tex_ext = os.path.splitext(tex_path)
        
        # Delete Proxy Texture
        if proxy:
            # Update progress window
            if progress:
                # Check if the dialog has been cancelled
                if cmds.progressWindow( query=True, isCancelled=True ):
                    cmds.progressWindow(endProgress=True)
                    return
                
                j += 1
                cmds.progressWindow(e=True,
                                    step=1,
                                    status='Deleting Texture %d of %d' % (j, max))
                
            # Find proxy texture node
            tex_lookup = cmds.listConnections('%s.message' % tex, type='core_texture_lookup2')
            if tex_lookup:
                for lookup in tex_lookup:
                    proxy_tex = cmds.listConnections('%s.proxy_texture' % lookup, type='mentalrayTexture')
                    if proxy_tex:
                        proxy_tex = proxy_tex[0]
                        proxy_path = cmds.getAttr('%s.fileTextureName' % proxy_tex)
                        
                        # Delete proxy texture node
                        print 'Deleting Proxy texture node: %s' % proxy_tex
                        try:           
                            cmds.delete(proxy_tex)
                        except:
                            print '\t- Error: Could not delete texture node!'
                            has_error = True
                        
                        # Delete proxy texture from disk
                        if os.path.exists(proxy_path) and from_disk:
                            print 'Deleting Proxy texture from disk: %s' % proxy_path
                            try:
                                os.remove(proxy_path)
                            except:
                                print '\t- Error: Could not delete texture file, skipped! See error below.'
                                print traceback.format_exc(5)
                                has_error = True
            
            # Delete proxy texture file, if it wasnt previously deleted
            if from_disk:
                for proxy_path in glob.glob('%s_Proxy.*' % tex_file):
                    print 'Deleting Proxy texture from disk: %s' % proxy_path 
                    try:
                        os.remove(proxy_path)
                    except:
                        print '\t- Error: Could not delete texture file, skipped! See error below.'
                        print traceback.format_exc(5)
                        has_error = True
            
        # Delete FG Texture
        if fg:
            # Update progress window
            if progress:
                # Check if the dialog has been cancelled
                if cmds.progressWindow( query=True, isCancelled=True ):
                    cmds.progressWindow(endProgress=True)
                    return
                
                j += 1
                cmds.progressWindow(e=True,
                                    step=1,
                                    status='Deleting Texture %d of %d' % (j, max))
                
            # Find fg texture node
            tex_lookup = cmds.listConnections('%s.message' % tex, type='core_texture_lookup2')
            if tex_lookup:
                for lookup in tex_lookup:
                    fg_tex = cmds.listConnections('%s.fg_texture' % lookup, type='mentalrayTexture')
                    if fg_tex:
                        fg_tex = fg_tex[0]
                        fg_path = cmds.getAttr('%s.fileTextureName' % fg_tex)
                        
                        # Delete fg texture node
                        print 'Deleting Finalgather texture node: %s' % fg_tex
                        try:           
                            cmds.delete(fg_tex)
                        except:
                            print '\t- Error: Could not delete texture node!'
                            has_error = True
                        
                        # Delete fg texture from disk
                        if os.path.exists(fg_path) and from_disk:
                            print 'Deleting Finalgather texture from disk: %s' % fg_path 
                            try:
                                os.remove(fg_path)
                            except:
                                print '\t- Error: Could not delete texture file, skipped! See error below.'
                                print traceback.format_exc(5)
                                has_error = True
            
            # Delete fg texture file, if it wasnt previously deleted
            if from_disk:
                for fg_path in glob.glob('%s_FG.*' % tex_file):
                    print 'Deleting Finalgather texture from disk: %s' % fg_path 
                    try:
                        os.remove(fg_path)
                    except:
                        print '\t- Error: Could not delete texture file, skipped! See error below.'
                        print traceback.format_exc(5)
                        has_error = True
    
    # End progress window
    if progress:
        cmds.progressWindow(endProgress=True)
        
    # Return True if it was successful with no errors
    return not has_error
    