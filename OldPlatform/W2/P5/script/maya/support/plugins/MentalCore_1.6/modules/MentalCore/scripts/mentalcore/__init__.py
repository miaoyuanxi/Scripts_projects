#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com


## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
import sys, os, shutil, webbrowser
from functools import partial

try:
    import maya.cmds as cmds
    import maya.mel as mel
    from maya import OpenMaya

    import mlib
    import mapi
    import renderglobals
    import general
    import passes
    import callbacks
except:
    pass

## ------------------------------------------------------------------------
## GLOBAL VARIABLES
## ------------------------------------------------------------------------
VERSION = 1.6
VERSION_STR = "1.6v1"
FORCE_MV = False
MIN_SAMPLES = 0
MAX_SAMPLES = 0

## ------------------------------------------------------------------------
## STARTUP
## ------------------------------------------------------------------------
def startup():
    maya_ver = int(cmds.about(f=True))
    maya_batch = cmds.about(b=True)

    if maya_ver in (2012, 2013, 2014):
        print 'MentalCore(): MentalCore for Maya %s' % VERSION_STR
        
        # Set environment variables for gpu ao
        if sys.platform == 'win32': # Windows
            # Find MR bin directory
            for p in os.environ['MAYA_PLUG_IN_PATH'].split(';'):
                if 'mentalray' in p:
                    mr_bin = os.path.join(os.path.dirname(p), 'bin')
                    if os.path.exists(mr_bin):
                        # MI_LIBRARY_PATH
                        if os.environ.has_key('MI_LIBRARY_PATH'):
                            os.environ['MI_LIBRARY_PATH'] = '%s;%s' % (mr_bin, os.environ['MI_LIBRARY_PATH'])
                        else:
                            os.environ['MI_LIBRARY_PATH'] = mr_bin
                        break
    
        elif sys.platform == 'linux2': # Linux
            # Find MR bin directory
            for p in os.environ['MAYA_PLUG_IN_PATH'].split(':'):
                if 'mentalray' in p:
                    mr_bin = os.path.join(os.path.dirname(p), 'bin')
                    if os.path.exists(mr_bin):
                        # MI_LIBRARY_PATH
                        if os.environ.has_key('MI_LIBRARY_PATH'):
                            os.environ['MI_LIBRARY_PATH'] = '%s:%s' % (mr_bin, os.environ['MI_LIBRARY_PATH'])
                        else:
                            os.environ['MI_LIBRARY_PATH'] = mr_bin
                        break

        elif sys.platform == 'darwin': # Mac
            # Find MR bin directory
            for p in os.environ['MAYA_PLUG_IN_PATH'].split(':'):
                if 'mentalray' in p:
                    mr_bin = os.path.join(os.path.dirname(p), 'bin')
                    if os.path.exists(mr_bin):
                        # MI_LIBRARY_PATH
                        if os.environ.has_key('MI_LIBRARY_PATH'):
                            os.environ['MI_LIBRARY_PATH'] = '%s:%s' % (mr_bin, os.environ['MI_LIBRARY_PATH'])
                        else:
                            os.environ['MI_LIBRARY_PATH'] = mr_bin
                        break
    
        #mental core startup
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

        if not maya_batch: #not in batch mode
            cmds.scriptedPanelType('renderWindowPanel', e=True, addCallback='mc_renderview_extension')
            build_menu()
            
        #Load callbacks
        callbacks.loadCallbacks()
        
        #Add Extension Attributes
        #Render layer composite extension attribute
        cmds.addExtension(nodeType='renderLayer', longName='mc_composite', attributeType='message')
        #Hair shader override extenstion attribute
        cmds.addExtension(nodeType='pfxHair', longName='mc_shaderOverride', attributeType='message')

    else:
        print 'MentalCore(): This version of Maya is not support in MentalCore %s' % VERSION_STR
            
    
## ------------------------------------------------------------------------
## MAYA MENU
## ------------------------------------------------------------------------
def build_menu():
    '''Builds the mentalcore menu'''
    #check maya version
    maya_ver = int(cmds.about(f=True))

    maya2014 = False
    if maya_ver >= 2014:
        maya2014 = True
    
    #main window
    mel.eval('global string $gMainWindow')
    mainWindow = mel.eval('$temp=$gMainWindow')
    
    if cmds.menu('mc_menu', q=True, exists=True):
        cmds.menu('mc_menu', e=True, dai=True)
        cmds.setParent('mc_menu', menu=True)
    else:
        cmds.menu('mc_menu', l='MentalCore', to=True, p=mainWindow)

    if mlib.is_license_valid():
        if not mlib.is_license_expired():
            cmds.menuItem(l='Create', sm=True)
            cmds.menuItem(l='Environment Light', c=partial(mapi.create_envlight, 'envLight1'))
            if maya2014:
                cmds.menuItem(l='Object Light From Selected', c=mapi.make_objlight)
            else:
                cmds.menuItem(l='Geolight From Selected', c=mapi.make_geolight)
            cmds.setParent('..', m=True)
            cmds.menuItem(l='Upgrade', sm=True)
            cmds.menuItem(l='Selected Shaders To Core', c=mapi.selected_shaders_to_core)
            cmds.menuItem(l='All Shaders To Core', c=mapi.all_shaders_to_core)
            cmds.setParent('..', m=True)
            cmds.menuItem(d=True)
            cmds.menuItem(l='Generate Low Res Textures', c='from mentalcore import ui; ui.LowResTexUI().show()')
            cmds.menuItem(d=True)
            cmds.menuItem(l='Install License', c=select_licence)
            cmds.menuItem(l='Reset Scene', c=partial(mapi.reset, True))           
            cmds.menuItem(d=True)
            cmds.menuItem(l='Documentation', c=open_docs)
            cmds.menuItem(l='Website', c=open_site)
        else:
            cmds.menuItem(l='License Expired', en=False)
            cmds.menuItem(l='Install License', c=select_licence)
            cmds.menuItem(d=True)
            cmds.menuItem(l='Documentation', c=open_docs)
            cmds.menuItem(l='Website', c=open_site)
    else:
        cmds.menuItem(l='No Valid License Found', en=False)
        cmds.menuItem(l='Install License', c=select_licence)
        cmds.menuItem(d=True)
        cmds.menuItem(l='Documentation', c=open_docs)
        cmds.menuItem(l='Website', c=open_site)
    
    
def open_docs(*args):
    webbrowser.open("http://core-cg.com/support-request/documentation/")
    
def open_site(*args):
    webbrowser.open("http://core-cg.com/")
    
def select_licence(*args):
    ret_lic = cmds.fileDialog2(fileFilter="Licence Files (*.lic)", dialogStyle=2, fm=1, cap='Select Licence File')
    if ret_lic:
        mlib.install_licence(str(ret_lic[0]))
    
## ------------------------------------------------------------------------
## RENDERVIEW EXTENSION
## ------------------------------------------------------------------------
def renderview_extension(editor):
    '''Extends the renderview with a pass selection option box'''
    mel.eval('addRenderWindowPanel "%s";' % editor)
    
    if cmds.objExists('mentalcoreGlobals') and cmds.getAttr('mentalcoreGlobals.enable'):
        cmds.setParent('renderViewToolbar')
        
        cmds.optionMenu('mc_renderview_passmenu', h=26, l='Preview Pass:', cc=set_preview_from_menu)
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.preview_pass', rebuild_renderview_menu], protected=True, parent='mc_renderview_passmenu')
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.output_mode', rebuild_renderview_menu], protected=True, parent='mc_renderview_passmenu')
        
        rebuild_renderview_menu()        

def rebuild_renderview_menu():
    if cmds.objExists('mentalcoreGlobals'):
        if cmds.control('mc_renderview_passmenu', q=True, exists=True):
            current_pass = mapi.get_preview()

            menu_items = cmds.optionMenu('mc_renderview_passmenu', q=True, itemListLong=True)
            if menu_items:
                for item in menu_items:
                    cmds.deleteUI(item)
            
            preview_index = 0
            cmds.menuItem(p='mc_renderview_passmenu', l='None')
            
            all_passes = cmds.ls(type='core_renderpass')
            if all_passes:
                j = 0
                for i in range(len(all_passes)):
                    rp = all_passes[i]
                    rp_type = cmds.getAttr('%s.type' % rp)
                    
                    #Skip the preview option for diagnostic passes
                    if rp_type >= 39 and rp_type <= 41:
                        continue
                    
                    cmds.menuItem(p='mc_renderview_passmenu', l=rp, c=partial(mapi.set_preview, rp))
                    
                    if current_pass == rp:
                        preview_index = j+1
                        
                    j += 1
                
            show_menu = False
            if cmds.getAttr('mentalcoreGlobals.output_mode') == 0:
                show_menu = True
                        
            cmds.optionMenu('mc_renderview_passmenu', e=True, sl=preview_index+1, vis=show_menu)
    else:
        if cmds.control('mc_renderview_passmenu', q=True, exists=True):
            cmds.optionMenu('mc_renderview_passmenu', e=True, vis=False)
    
def set_preview_from_menu(*args):
    cur_pass = cmds.optionMenu('mc_renderview_passmenu', q=True, v=True)
    mapi.set_preview(cur_pass)            

## ------------------------------------------------------------------------
## PRE/POST RENDER
## ------------------------------------------------------------------------
def disconnect_passes():
    '''Disconnects all passes from the mentalcore globals'''
    if cmds.objExists('mentalcoreGlobals'):
        pass_conn = cmds.listConnections('mentalcoreGlobals.renderpasses', c=True, p=True)
        if pass_conn:    
            for i in range(len(pass_conn)/2):
                rp_attr = pass_conn[i*2]
                global_attr = pass_conn[i*2+1]
                cmds.disconnectAttr(global_attr, rp_attr)

def connect_passes(layer):
    '''Connects all associated passes of the specified layer to the mentalcore globals'''
    if cmds.objExists(layer) and cmds.objExists('mentalcoreGlobals'):
        disconnect_passes()
        con_passes = mapi.get_associated_passes(layer)
        i = 0
        if con_passes:    
            for i in range(len(con_passes)):
                pass_attr = '%s.message' % con_passes[i]
                global_attr = 'mentalcoreGlobals.renderpasses[%i]' % i
                cmds.connectAttr(pass_attr, global_attr)
            i += 1
                
        if cmds.getAttr('mentalcoreGlobals.output_mode') == 0:
            preview_pass = mapi.get_preview()
            if preview_pass and not preview_pass in con_passes:
                global_attr = 'mentalcoreGlobals.renderpasses[%i]' % i
                cmds.connectAttr('%s.message' % preview_pass, global_attr)    
            
# -------------------------------------------------
# Spraytrace pre render command
# -------------------------------------------------
def spraytrace_pre_render():
    if not cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'mentalRay':
        return
        
    if cmds.objExists('mentalcoreGlobals') and cmds.getAttr('mentalcoreGlobals.enable'):		
        # -------------------------------------------------
        # maya version and batch mode
        maya_ver = int(cmds.about(f=True))
        maya_batch = cmds.about(b=True)
        
        # -------------------------------------------------
        # current render layer
        current_layer = cmds.editRenderLayerGlobals(q=True, crl=True)
        
        # -------------------------------------------------
        # connect camera shaders to all cameras
        env_shader = cmds.listConnections('mentalcoreGlobals.env_shader', s=True, d=False)
        if env_shader:
            env_shader = env_shader[0]
            
        photographic_shader = cmds.listConnections('mentalcoreGlobals.photographic_shader', s=True, d=False)
        if photographic_shader:
            photographic_shader = photographic_shader[0]
            
        dof_shader = cmds.listConnections('mentalcoreGlobals.dof_shader', s=True, d=False)
        if dof_shader:
            dof_shader = dof_shader[0]

        for cam in cmds.ls(type='camera'):
            if not cmds.listConnections('%s.message' % cam, type='projection'): #Skip projection cameras
                #lens
                try:
                    lens_conn = cmds.listConnections('%s.miLensShader' % cam, s=True, d=False, p=True)

                    if lens_conn:
                        cmds.disconnectAttr(lens_conn[0], '%s.miLensShader' % cam)
                    
                    cmds.connectAttr('mentalcoreLens.message', '%s.miLensShader' % cam, f=True)
                except:
                    pass
                
                #environment
                try:
                    if env_shader:
                        env_conn = cmds.listConnections('%s.miEnvironmentShader' % cam, s=True, d=False, p=True)

                        if env_conn:
                            cmds.disconnectAttr(env_conn[0], '%s.miEnvironmentShader' % cam)
                            
                        cmds.connectAttr('%s.message' % env_shader, '%s.miEnvironmentShader' % cam, f=True)
                except:
                    pass
                    
                #dof shader
                try:
                    if dof_shader:
                        shader_conn = cmds.listConnections('%s.message' % dof_shader, sh=True, d=True, s=False, type='camera')
                        if not shader_conn or not cam in shader_conn:
                            mlib.connect_next_avaliable('%s.message' % dof_shader, '%s.miLensShaderList' % cam)
                except:
                    pass
                    
                #photographic shader
                try:
                    if photographic_shader:
                        shader_conn = cmds.listConnections('%s.message' % photographic_shader, sh=True, d=True, s=False, type='camera')
                        if not shader_conn or not cam in shader_conn:
                            mlib.connect_next_avaliable('%s.message' % photographic_shader, '%s.miLensShaderList' % cam)
                except:
                    pass
                
        # -------------------------------------------------
        # connect up mia_envblur shader to core_environment
        env_shader = cmds.listConnections('mentalcoreGlobals.env_shader', s=True, d=False, type='core_environment')
        if env_shader:
            env_shader = env_shader[0]
                
            # -----------------------
            # Secondary Env mia_envblur
            conn = cmds.listConnections('%s.sec_envblur' % env_shader, s=True, d=False, type='mia_envblur')
            if conn:
                cmds.delete(conn[0])
            
            if cmds.getAttr('%s.sec_en' % env_shader):
                # Only create the env blur shader if needed
                if cmds.getAttr('%s.sec_mat_blur' % env_shader) or cmds.getAttr('%s.sec_blur' % env_shader):
                    #create envblur shader
                    blur_shader = cmds.createNode('mia_envblur', ss=True)
                    cmds.connectAttr('%s.message' % blur_shader, '%s.sec_envblur' % env_shader, f=True)
                    
                    #connect attributes
                    cmds.connectAttr('%s.sec_blur' % env_shader, '%s.blur' % blur_shader, f=True)
                    cmds.connectAttr('%s.sec_mat_blur' % env_shader, '%s.mia_material_blur' % blur_shader, f=True)
                    cmds.connectAttr('%s.sec_blur_res' % env_shader, '%s.resolution' % blur_shader, f=True)
                    
        # -------------------------------------------------
        # Set primary framebuffer settings
        set_primary_framebuffer()

        # -------------------------------------------------
        # Initialize string options
        init_string_options()

        # -------------------------------------------------
        # set to preview pass mode
        cmds.setAttr('mentalcoreGlobals.output_mode', 0)        

# -------------------------------------------------
# Pre render command
# -------------------------------------------------
def pre_render():
    if not cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'mentalRay':
        return
        
    if cmds.objExists('mentalcoreGlobals') and cmds.getAttr('mentalcoreGlobals.enable'):
        print 'MentalCore(): Executing Pre Render Script'
    
        # -------------------------------------------------
        # maya version and batch mode
        maya_ver = int(cmds.about(f=True))
        maya_batch = cmds.about(b=True)
        
        #Check if we are exporting a scene to .mi
        if callbacks.EXPORT:
            maya_batch = True
    
        # -------------------------------------------------
        # current render layer
        current_layer = cmds.editRenderLayerGlobals(q=True, crl=True)
        
        # -------------------------------------------------
        # Connect Associated Passes
        connect_passes(current_layer)
        
        # -------------------------------------------------
        # override maya fur shaders
        try:
            init_fur_overrides()
        except:
            pass
            
        # -------------------------------------------------
        # init geo lights
        try:
            geo_light_init()
        except:
            pass
    
        # -------------------------------------------------
        # disable extra globals
        for node in cmds.ls(type='core_globals'):
            if not node == 'mentalcoreGlobals':
                cmds.setAttr('%s.enable' % node, False)
            
        # -------------------------------------------------
        # create core state
        if cmds.objExists('mentalcoreState'):
            mlib.disconnect_next_avaliable('mentalcoreState.message', 'miDefaultOptions.stateShaderList')
            cmds.delete('mentalcoreState')
            
        state_shader = cmds.createNode('core_state', n='mentalcoreState', ss=True)
        mlib.connect_next_avaliable('%s.message' % state_shader, 'miDefaultOptions.stateShaderList')
        
        cmds.setAttr('%s.enable' % state_shader, True)
        if maya_batch:
            cmds.setAttr('%s.lic_mode' % state_shader, 1)
            
        # -------------------------------------------------
        # create temp geo
        if cmds.objExists('mc_globals_geo'):
            cmds.delete('mc_globals_geo')
            
        temp_shape = cmds.createNode('mesh', ss=True)
        temp_parent = cmds.listRelatives(temp_shape, p=True)[0]
        cmds.rename(temp_parent, 'mc_globals_geo')
        
        cmds.setAttr('mc_globals_geo.miExportGeoShader', True)
        cmds.connectAttr('mentalcoreGlobals.message', 'mc_globals_geo.miGeoShader', f=True)
        
        #add to current render layer
        if current_layer != 'defaultRenderLayer':
            cmds.editRenderLayerMembers(current_layer, 'mc_globals_geo')
            
        #select temp geo if Maya is set to render selected objects
        if cmds.getAttr('defaultRenderGlobals.renderAll') == 0:
            cmds.select('mc_globals_geo', add=True)
                    
        # -------------------------------------------------
        # connect camera shaders to all cameras
        env_shader = cmds.listConnections('mentalcoreGlobals.env_shader', s=True, d=False)
        if env_shader:
            env_shader = env_shader[0]
            
        photographic_shader = cmds.listConnections('mentalcoreGlobals.photographic_shader', s=True, d=False)
        if photographic_shader:
            photographic_shader = photographic_shader[0]
            
        dof_shader = cmds.listConnections('mentalcoreGlobals.dof_shader', s=True, d=False)
        if dof_shader:
            dof_shader = dof_shader[0]

        for cam in cmds.ls(type='camera'):
            if not cmds.listConnections('%s.message' % cam, type='projection'): #Skip projection cameras
                #lens
                try:
                    lens_conn = cmds.listConnections('%s.miLensShader' % cam, s=True, d=False, p=True)

                    if lens_conn:
                        cmds.disconnectAttr(lens_conn[0], '%s.miLensShader' % cam)
                    
                    cmds.connectAttr('mentalcoreLens.message', '%s.miLensShader' % cam, f=True)
                except:
                    pass
                
                #environment
                try:
                    if env_shader:
                        env_conn = cmds.listConnections('%s.miEnvironmentShader' % cam, s=True, d=False, p=True)

                        if env_conn:
                            cmds.disconnectAttr(env_conn[0], '%s.miEnvironmentShader' % cam)
                            
                        cmds.connectAttr('%s.message' % env_shader, '%s.miEnvironmentShader' % cam, f=True)
                except:
                    pass
                    
                #dof shader
                try:
                    if dof_shader:
                        shader_conn = cmds.listConnections('%s.message' % dof_shader, sh=True, d=True, s=False, type='camera')
                        if not shader_conn or not cam in shader_conn:
                            mlib.connect_next_avaliable('%s.message' % dof_shader, '%s.miLensShaderList' % cam)
                except:
                    pass
                    
                #photographic shader
                try:
                    if photographic_shader:
                        shader_conn = cmds.listConnections('%s.message' % photographic_shader, sh=True, d=True, s=False, type='camera')
                        if not shader_conn or not cam in shader_conn:
                            mlib.connect_next_avaliable('%s.message' % photographic_shader, '%s.miLensShaderList' % cam)
                except:
                    pass
                
        # -------------------------------------------------
        # connect up mia_envblur shader to core_environment
        env_shader = cmds.listConnections('mentalcoreGlobals.env_shader', s=True, d=False, type='core_environment')
        if env_shader:
            env_shader = env_shader[0]
                
            # -----------------------
            # Secondary Env mia_envblur
            conn = cmds.listConnections('%s.sec_envblur' % env_shader, s=True, d=False, type='mia_envblur')
            if conn:
                cmds.delete(conn[0])
            
            if cmds.getAttr('%s.sec_en' % env_shader):
                # Only create the env blur shader if needed
                if cmds.getAttr('%s.sec_mat_blur' % env_shader) or cmds.getAttr('%s.sec_blur' % env_shader):
                    #create envblur shader
                    blur_shader = cmds.createNode('mia_envblur', ss=True)
                    cmds.connectAttr('%s.message' % blur_shader, '%s.sec_envblur' % env_shader, f=True)
                    
                    #connect attributes
                    cmds.connectAttr('%s.sec_blur' % env_shader, '%s.blur' % blur_shader, f=True)
                    cmds.connectAttr('%s.sec_mat_blur' % env_shader, '%s.mia_material_blur' % blur_shader, f=True)
                    cmds.connectAttr('%s.sec_blur_res' % env_shader, '%s.resolution' % blur_shader, f=True)
                
        # -------------------------------------------------
        # set to output all passes if in batch mode
        if maya_batch:
            cmds.setAttr('mentalcoreGlobals.output_mode', 2)
        
        # -------------------------------------------------
        # Set primary framebuffer settings
        set_primary_framebuffer()
            
        # -------------------------------------------------
        # Set framebuffer mode for 2012
        if maya_ver >= 2012:
            try:
                fb_mode = cmds.getAttr('mentalcoreGlobals.fb_mem_mode')
                cmds.setAttr('mentalrayGlobals.frameBufferMode', fb_mode)
            except:
                pass
                
        # -------------------------------------------------
        # Connect preview composite
        if cmds.getAttr('mentalcoreGlobals.output_mode') == 1:
            comp = general.get_composite(current_layer)
            if comp:
                cmds.connectAttr('%s.message' % comp, 'mentalcoreGlobals.preview_composite', f=True)

        # -------------------------------------------------
        # Initialize string options
        init_string_options()

        # -------------------------------------------------
        # Set filename and path for metadata
        scene_path = cmds.file(q=True, sn=True)
        if scene_path:
            scene_name = os.path.splitext(os.path.basename(scene_path))[0]

            cmds.setAttr('mentalcoreGlobals.maya_file_path', scene_path, type='string')
            cmds.setAttr('mentalcoreGlobals.maya_file_name', scene_name, type='string')

        # -------------------------------------------------
        # set force motion vectors?
        global FORCE_MV
        FORCE_MV = cmds.getAttr('miDefaultOptions.forceMotionVectors')
        
        if cmds.getAttr('mentalcoreGlobals.output_mode') == 0:
            preview_pass = mapi.get_preview()
            if preview_pass and cmds.getAttr('%s.type' % preview_pass) == 28:
                try:
                    cmds.setAttr('miDefaultOptions.forceMotionVectors', True)
                except:
                    pass
        else:
            associated_passes = mapi.get_associated_passes(current_layer)
            if associated_passes:
                for rp in associated_passes:
                    if cmds.getAttr('%s.type' % rp) == 28:
                        try:
                            cmds.setAttr('miDefaultOptions.forceMotionVectors', True)
                        except:
                            pass
                            
        # -------------------------------------------------
        # Post Only Mode?
        global MIN_SAMPLES
        global MAX_SAMPLES
        MIN_SAMPLES = cmds.getAttr('miDefaultOptions.minSamples')
        MAX_SAMPLES = cmds.getAttr('miDefaultOptions.maxSamples')
        
        if cmds.getAttr('mentalcoreGlobals.output_override') == 3:
            cmds.setAttr('miDefaultOptions.minSamples', 0)
            cmds.setAttr('miDefaultOptions.maxSamples', 0)
            
        # -------------------------------------------------
        # Make Ptex Textures Relative
        ptex_make_relative()
        
        # -------------------------------------------------
        # Make Alembic Shaders Relative
        alembic_make_relative()

# -------------------------------------------------
# Post render command
# -------------------------------------------------
def post_render():
    if not cmds.getAttr('defaultRenderGlobals.currentRenderer') == 'mentalRay':
        return
        
    # -------------------------------------------------
    # remove temp state shader
    if cmds.objExists('mentalcoreState'):
        mlib.disconnect_next_avaliable('mentalcoreState.message', 'miDefaultOptions.stateShaderList')
        cmds.delete('mentalcoreState')
        
    # -------------------------------------------------
    # remove temp geo
    if cmds.objExists('|mc_globals_geo'):
        cmds.delete('|mc_globals_geo')
        
    # -------------------------------------------------
    # remove temp fur overrides
    if cmds.objExists('mcFurOverrides'):
        cmds.delete('mcFurOverrides')
    if cmds.objExists('|AFurTemp'):
        cmds.delete('|AFurTemp')
        
    if cmds.objExists('mentalcoreGlobals'):
        # -------------------------------------------------
        # cleanup geo lights
        try:
            geo_light_cleanup()
        except:
            pass
        
        # -------------------------------------------------
        # Disconnect Associated Passes
        disconnect_passes()
        
        # -------------------------------------------------
        # Disconnect preview composite
        comp_conn = cmds.listConnections('mentalcoreGlobals.preview_composite', c=True, p=True)
        if comp_conn:    
            cmds.disconnectAttr(comp_conn[1], comp_conn[0])
            
        # -------------------------------------------------
        # cleanup mia_envblur shader
        env_shader = cmds.listConnections('mentalcoreGlobals.env_shader', s=True, d=False, type='core_environment')
        if env_shader:
            env_shader = env_shader[0]

            conn = cmds.listConnections('%s.sec_envblur' % env_shader, s=True, d=False, type='mia_envblur')
            if conn:
                try:	
                    cmds.delete(conn[0])
                except:
                    pass

        # -------------------------------------------------
        # Cleanup settings if mentalcore is enabled
        if cmds.getAttr('mentalcoreGlobals.enable'):
            # -------------------------------------------------
            # Reset force motion vectors
            global FORCE_MV
            cmds.setAttr('miDefaultOptions.forceMotionVectors', FORCE_MV)
            
            # -------------------------------------------------
            # Post Only Mode?
            global MIN_SAMPLES
            global MAX_SAMPLES
            
            if cmds.getAttr('mentalcoreGlobals.output_override') == 3:
                cmds.setAttr('miDefaultOptions.minSamples', MIN_SAMPLES)
                cmds.setAttr('miDefaultOptions.maxSamples', MAX_SAMPLES)

# -------------------------------------------------
# Init string options
# -------------------------------------------------
def init_string_options():
    #check maya version
    maya_ver = int(cmds.about(f=True))
    
    maya2013 = False
    if maya_ver >= 2013:
        maya2013 = True
    
    maya2014 = False
    if maya_ver >= 2014:
        maya2014 = True
    
    # -------------------------------------------------
    # IBL mode
    ibl_mode = cmds.getAttr('mentalcoreGlobals.ibl_mode')
    ibl_quality = cmds.getAttr('mentalcoreGlobals.ibl_quality')
    if ibl_mode == 0: #off
        mlib.MiStringOption('environment lighting mode').value = 'off'
    elif ibl_mode == 1: #automatic
        mlib.MiStringOption('environment lighting mode').value = 'automatic'
        mlib.MiStringOption('environment lighting quality').value = ibl_quality
    elif ibl_mode == 2: #approximate
        mlib.MiStringOption('environment lighting mode').value = 'approximate'
        mlib.MiStringOption('environment lighting quality').value = ibl_quality
    elif ibl_mode == 3: #Light
        mlib.MiStringOption('environment lighting mode').value = 'light'
        mlib.MiStringOption('environment lighting quality').value = ibl_quality

    # -------------------------------------------------
    # Light Relative Scale
    light_rel_scale = cmds.getAttr('mentalcoreGlobals.light_relative_scale')
    mlib.MiStringOption('light relative scale').value = light_rel_scale

    # -------------------------------------------------
    # Shutter Efficiency
    if maya2014:
        # Shutter Shape
        shape = cmds.getAttr('mentalcoreGlobals.shutter_shape')
        if shape == 1:
            mlib.MiStringOption('shutter shape function').value = "mi_trapezoidal_shutter"
        else:
            mlib.MiStringOption('shutter shape function').value = ""
        
        # Shutter Efficiency
        efficiency = cmds.getAttr('mentalcoreGlobals.shutter_efficiency')
        open = cmds.getAttr('miDefaultOptions.shutterDelay')
        close = cmds.getAttr('miDefaultOptions.shutter')

        efficiency = (1.0 - efficiency) * (close - open)
        open += efficiency
        close -= efficiency

        mlib.MiStringOption('shutter full open').value = mlib.clamp_precision(open, 2)
        mlib.MiStringOption('shutter full close').value = mlib.clamp_precision(close, 2)
        
# -------------------------------------------------
# Set Primary Framebuffer Settings
# -------------------------------------------------
def set_primary_framebuffer():
    # Get channels and bit depth
    channels = cmds.getAttr('mentalcoreGlobals.primary_channels')
    bit_depth = cmds.getAttr('mentalcoreGlobals.primary_bit_depth')

    # Set primary framebuffer setting
    if channels == 0: # 3 Channels
        if bit_depth == 0: # 8 Bit Integer
            cmds.setAttr('miDefaultFramebuffer.datatype', 0)
        elif bit_depth == 1: # 16 Bit Integer
            cmds.setAttr('miDefaultFramebuffer.datatype', 1)
        elif bit_depth == 2: # 16 Bit Float
            cmds.setAttr('miDefaultFramebuffer.datatype', 17)
        elif bit_depth == 3: # 32 Bit Float
            cmds.setAttr('miDefaultFramebuffer.datatype', 4)
    elif channels == 1: # 4 Channels
        if bit_depth == 0: # 8 Bit Integer
            cmds.setAttr('miDefaultFramebuffer.datatype', 2)
        elif bit_depth == 1: # 16 Bit Integer
            cmds.setAttr('miDefaultFramebuffer.datatype', 3)
        elif bit_depth == 2: # 16 Bit Float
            cmds.setAttr('miDefaultFramebuffer.datatype', 16)
        elif bit_depth == 3: # 32 Bit Float
            cmds.setAttr('miDefaultFramebuffer.datatype', 5)

# -------------------------------------------------
# Setup fur and hair shader overrides
# -------------------------------------------------
def init_fur_overrides():
    #Get node types to override
    node_types = ['pfxHair']
    if cmds.pluginInfo('Fur', q=True, l=True):
        node_types.append('FurDescription')
    
    #Find nodes to override
    override_nodes = cmds.ls(type=node_types)
    if override_nodes:
        #delete existing override shader
        if cmds.objExists('mcFurOverrides'):
            cmds.delete('mcFurOverrides')
    
        overrides = {}
        override_nodes = set(override_nodes)
        for node in override_nodes:
            nodetype = cmds.nodeType(node)
            if cmds.objExists(node + ".mc_shaderOverride"):
                material = None
                sg = cmds.listConnections(node + ".mc_shaderOverride")
                if sg:
                    mat_type = cmds.nodeType(sg[0])
                    if mat_type == 'shadingEngine':
                        material = sg[0]
                    else:
                        shader = sg[0]
                        sg = cmds.listConnections(shader, s=False, d=True, type='shadingEngine')
                        if sg:
                            material = sg[0]
                        else:
                            material = cmds.sets(r=True, n='%sSG' % shader)
                            cmds.connectAttr('%s.message' % shader, '%s.miMaterialShader' % material, f=True)
                            cmds.connectAttr('%s.message' % shader, '%s.miShadowShader' % material, f=True)
                
                if material:
                    if nodetype == 'FurDescription':
                        ff_nodes = cmds.listConnections(node, type='FurFeedback')
                        if ff_nodes:
                            if overrides.has_key(material):
                                overrides[material].append(ff_nodes[0])
                            else:
                                overrides[material] = [ff_nodes[0]]
                    elif nodetype == 'pfxHair':
                        hairTrans = cmds.listRelatives(node, p=True)
                        if hairTrans:
                            if overrides.has_key(material):
                                overrides[material].append(hairTrans[0])
                            else:
                                overrides[material] = [hairTrans[0]]
        if overrides:
            mat_ovr_node = cmds.createNode('core_material_override', n='mcFurOverrides', ss=True)
            
            i = 0
            for mat, objs in overrides.items():
                for obj in objs:
                    print 'MentalCore(): Overriding "%s" with material "%s"' % (obj, material)
                    cmds.connectAttr(mat + '.message', mat_ovr_node + '.override[' + str(i) + '].material', f=True)
                    cmds.connectAttr(obj + '.message', mat_ovr_node + '.override[' + str(i) + '].object', f=True)
                    i += 1
                            
            # -------------------------------------------------
            # create temp geo
            if cmds.objExists('AFurTemp'):
                cmds.delete('AFurTemp')
                
            temp_shape = cmds.createNode('mesh', ss=True)
            temp_parent = cmds.listRelatives(temp_shape, p=True)[0]
            cmds.rename(temp_parent, 'AFurTemp')
            
            cmds.setAttr('AFurTemp.miExportGeoShader', True)
            cmds.connectAttr('mcFurOverrides.message', 'AFurTemp.miGeoShader', f=True)
            
            #add to current render layer
            current_layer = cmds.editRenderLayerGlobals(q=True, crl=True)
            if current_layer != 'defaultRenderLayer':
                cmds.editRenderLayerMembers(current_layer, 'AFurTemp')
        
# -------------------------------------------------
# Geo light init
# -------------------------------------------------
def geo_light_init():
    for node in cmds.ls(type='core_geo_light'):
        conn_geo = cmds.listConnections('%s.source_geo' % node, s=True, d=False)
        if conn_geo:
            conn_geo = conn_geo[0]
            if cmds.getAttr('%s.visibility' % conn_geo):
                try:
                    dup_geo = cmds.duplicate(conn_geo, rr=True, n='_%s' % conn_geo)[0]

                    cmds.setAttr('%s.miExportGeoShader' % dup_geo, True)
                    cmds.connectAttr('%s.message' % node, '%s.miGeoShader' % dup_geo, f=True)

                    cmds.connectAttr('%s.translate' % conn_geo, '%s.translate' % dup_geo, f=True)
                    cmds.connectAttr('%s.rotate' % conn_geo, '%s.rotate' % dup_geo, f=True)
                    cmds.connectAttr('%s.scale' % conn_geo, '%s.scale' % dup_geo, f=True)
                except:
                    pass

# -------------------------------------------------
# Geo light cleanup
# -------------------------------------------------
def geo_light_cleanup():
    for node in cmds.ls(type='core_geo_light'):
        conn_geo = cmds.listConnections('%s.message' % node, s=False, d=True, p=True)
        if conn_geo:
            conn_geo = conn_geo[0]
            if 'miGeoShader' in conn_geo:
                try:
                    name, attr = conn_geo.split('.')
                    cmds.delete(name)
                except:
                    pass
                    
# -------------------------------------------------
# Ptex Make Relative
# -------------------------------------------------
def ptex_make_relative():
    #check maya version
    maya_ver = int(cmds.about(f=True))
    maya2013 = False
    if maya_ver >= 2013:
        maya2013 = True
        
    if not maya2013:
        return
        
    #Get proj directory
    proj_dir = os.path.normpath(cmds.workspace(q=True, rd=True))
    
    #Look ptex shaders and make paths relative
    for ptex in cmds.ls(type='mib_ptex_lookup'):
        filename = cmds.getAttr('%s.filename' % ptex)
        if filename:
            filename = filename.replace('\\', '/')
            splitname = filename.split('//')
            if splitname and len(splitname) == 2:
                if proj_dir != os.path.normpath(splitname[0]):
                    newname = '%s//%s' % (proj_dir, splitname[1])
                    if os.path.exists(newname):
                        cmds.setAttr('%s.filename' % ptex, newname, type='string')
                        
# -------------------------------------------------
# Alembic Make Relative
# -------------------------------------------------
def alembic_make_relative():
    #check maya version
    maya_ver = int(cmds.about(f=True))
    maya2013 = False
    if maya_ver >= 2013:
        maya2013 = True
        
    if not maya2013:
        return
        
    #Get proj directory
    proj_dir = os.path.normpath(cmds.workspace(q=True, rd=True))
    
    #Look alembic shaders and make paths relative
    for ptex in cmds.ls(type='abcimport'):
        filename = cmds.getAttr('%s.filename' % ptex)
        if filename:
            filename = filename.replace('\\', '/')
            splitname = filename.split('//')
            if splitname and len(splitname) == 2:
                if proj_dir != os.path.normpath(splitname[0]):
                    newname = '%s//%s' % (proj_dir, splitname[1])
                    if os.path.exists(newname):
                        cmds.setAttr('%s.filename' % ptex, newname, type='string')
