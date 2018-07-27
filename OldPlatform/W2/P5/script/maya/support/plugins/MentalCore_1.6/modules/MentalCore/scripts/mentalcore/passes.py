#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com

## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
from functools import partial

import maya.cmds as cmds
import maya.mel as mel

import mentalcore as mc
import mlib
import mapi
import passpresets


## ------------------------------------------------------------------------
## GLOBAL VARIABLES
## ------------------------------------------------------------------------
PASSES_TAB = None

BEAUTY, COLOUR, DIFFUSE, DIFFUSE_RAW, SHADOW, SHADOW_RAW, DIFFUSE_NO_SHAD, DIFFUSE_NO_SHAD_RAW, AMBIENT, AMBIENT_RAW, INDIRECT, INDIRECT_RAW, AO, TRANSLUCENCY, SSS, SSS_FRONT, SSS_MID, SSS_BACK, INCANDESENCE, SPECULAR, REFLECTION, REFRACTION, BLOOM, DEPTH, NORMALW, NORMALC, POINTW, POINTC, MOTIONV, OPACITY, FACING, UV, MATID, OBJID, MATTE, CUSTOMC, CUSTOMV, ENVIRONMENT, LIGHTSELECT = range(39)
    

## ------------------------------------------------------------------------
## RENDERPASS TAB
## ------------------------------------------------------------------------
def refresh_passes_ui():
    global PASSES_TAB
    if PASSES_TAB:
        PASSES_TAB.refresh_all_passes()


class PassesTab():
    '''Creates the mentalcore passes tab'''
    def __init__(self):
        global PASSES_TAB
        PASSES_TAB = self
        
        self.layout = cmds.setParent(q=True)
        self.create()
        

    def create(self):
        cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)
        
        #check maya version
        maya_ver = int(cmds.about(f=True))
            
        maya2013 = False
        if maya_ver >= 2013:
            maya2013 = True
        
        maya2014 = False
        if maya_ver >= 2014:
            maya2014 = True
            
        ## ------------------------------------------------------------------------
        ## RENDER PASSES
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Render Passes', w=465, collapsable=True, collapse=False)
        pass_layout = cmds.columnLayout(rs=4, w=50, adj=True)
        
        self.split_layout = cmds.paneLayout( configuration='right3', w=460, h=550 )
        

        ## ------------------------------------------------------------------------
        ## AVALIABLE PASSES
        ## ------------------------------------------------------------------------
        avail_form = cmds.formLayout(w=135)
        
        avail_label = cmds.text( label='Avaliable Passes', align='center' )
        self.avail_passes = cmds.textScrollList( ams=True, append=mapi.AVALIABLE_PASSES, dcc=self.add_pass )
        
        self.add_pass_b = cmds.button(l='>>', h=32, c=self.add_pass)
        self.remove_pass_b = cmds.button(l='<<', h=32, c=self.remove_pass)
        
        cmds.formLayout(avail_form, edit=True,
            attachForm=[(avail_label, 'top', 1),
                        (avail_label, 'left', 1),
                        (self.avail_passes, 'left', 1),
                        (self.avail_passes, 'bottom', 1),
                        (self.add_pass_b, 'right', 1),
                        (self.add_pass_b, 'top', 21),
                        (self.remove_pass_b, 'right', 1)],
            attachControl=[	(self.avail_passes, 'top', 5, avail_label), 
                            (self.avail_passes, 'right', 6, self.add_pass_b),
                            (avail_label, 'right', 6, self.add_pass_b),
                            (self.remove_pass_b, 'top', 1, self.add_pass_b)])
        
        cmds.setParent(self.split_layout)
        
        ## ------------------------------------------------------------------------
        ## SCENE PASSES
        ## ------------------------------------------------------------------------
        scene_form = cmds.formLayout(w=50)

        scene_label = cmds.text( label='Scene Passes', align='center' )
        self.scene_passes = cmds.textScrollList( h=50, ams=True, dcc=self.select_scene_pass, dkc=self.remove_pass )
        
        scene_menu = cmds.popupMenu( parent=self.scene_passes )
        cmds.popupMenu( scene_menu, e=True, pmc=partial(self.build_pass_menu, scene_menu, 'scene_passes') )
        
        self.associate = cmds.button(l='Add To Render Layer', h=26, c=self.associate_pass)
        
        cmds.formLayout(scene_form, edit=True,
            attachForm=[(scene_label, 'top', 1),
                        (scene_label, 'left', 4),
                        (scene_label, 'right', 1),
                        (self.scene_passes, 'left', 4),
                        (self.scene_passes, 'right', 1),
                        (self.associate, 'left', 4),
                        (self.associate, 'right', 1),
                        (self.associate, 'bottom', 1)],
            attachControl=[	(self.scene_passes, 'top', 5, scene_label), 
                            (self.scene_passes, 'bottom', 4, self.associate)])
        
        cmds.setParent(self.split_layout)
        
        ## ------------------------------------------------------------------------
        ## ASSOCIATED PASSES
        ## ------------------------------------------------------------------------
        associated_form = cmds.formLayout(w=50)
        
        associated_label = cmds.text( label='Associated Passes', align='center' )
        self.associated_passes = cmds.textScrollList( h=50, ams=True, dcc=self.select_layer_pass, dkc=self.unassociate_pass )
        
        layer_menu = cmds.popupMenu( parent=self.associated_passes )
        cmds.popupMenu( layer_menu, e=True, pmc=partial(self.build_pass_menu, layer_menu, 'layer_passes') )
        
        self.desociate = cmds.button(l='Remove', h=26, c=self.unassociate_pass )
        
        cmds.formLayout(associated_form, edit=True,
            attachForm=[(associated_label, 'top', 5),
                        (associated_label, 'left', 4),
                        (associated_label, 'right', 1),
                        (self.associated_passes, 'left', 4),
                        (self.associated_passes, 'right', 1),
                        (self.desociate, 'left', 4),
                        (self.desociate, 'right', 1),
                        (self.desociate, 'bottom', 1)],
            attachControl=[	(self.associated_passes, 'top', 5, associated_label), 
                            (self.associated_passes, 'bottom', 4, self.desociate)])
                            
        cmds.setParent(self.layout)
        

        ## ------------------------------------------------------------------------
        ## SETTINGS
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Settings', w=460, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)

        # Enable global clamp
        self.en_global_clamp = cmds.checkBoxGrp( l1='Clamp Beauty Passes' )
        # Global clamp
        self.global_clamp = cmds.floatFieldGrp( label='Clamp' )
        
        cmds.separator()
        
        #beauty passes
        self.beauty_passes = cmds.checkBoxGrp( l1='Enable Beauty Passes' )
        #post passes
        self.post_passes = cmds.checkBoxGrp( l1='Enable Post Passes' )
        #matte passes
        self.matte_passes = cmds.checkBoxGrp( l1='Enable Matte Passes' )
        #custom passes
        self.custom_passes = cmds.checkBoxGrp( l1='Enable Custom Passes' )
        
        cmds.setParent(self.layout)
        
        ## ------------------------------------------------------------------------
        ## PRIMARY BUFFER
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Primary Framebuffer', w=460, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #channels
        self.channels = cmds.attrEnumOptionMenuGrp( l='Channels', ei=[(0, '3'),(1, '4') ] )
        #bit depth
        self.bit_depth = cmds.attrEnumOptionMenuGrp( l='Bit Depth', ei=[(0, '8 Bit Integer'),(1, '16 Bit Integer'),(2, '16 Bit Float'),(3, '32 Bit Float') ] )
        #group
        self.group = cmds.textFieldGrp( label='Pass Group', cc=self.set_pass_group )
        
        ## ------------------------------------------------------------------------
        ## METADATA
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Metadata', w=430, collapsable=True, collapse=True, vis=maya2013)
        cmds.columnLayout(rs=1, adj=True)
        
        meta_add = cmds.button(l='Add Metadata', c=self.create_metadata)
        
        cmds.separator()

        cmds.columnLayout('mc_meta_layout', rs=1, adj=True)
        
        cmds.setParent(self.layout)
        
                        
        cmds.setUITemplate(popTemplate=True)
        
    
    def connect_controls(self):
        ## ------------------------------------------------------------------------
        ## RENDERPASSES
        ## ------------------------------------------------------------------------
        cmds.scriptJob(e=['renderLayerManagerChange', self.refresh_all_passes], protected=True, parent=self.scene_passes)
    
        for rp in cmds.ls(type='core_renderpass'):
            self.connect_pass(rp)
        
    
        ## ------------------------------------------------------------------------
        ## SETTINGS
        ## ------------------------------------------------------------------------
        cmds.connectControl( self.en_global_clamp, 'mentalcoreGlobals.en_global_clamp', index=2 )
        cmds.connectControl( self.global_clamp, 'mentalcoreGlobals.global_clamp', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.en_global_clamp', self.update_clamp], protected=True, parent=self.en_global_clamp)
        
        cmds.connectControl( self.beauty_passes, 'mentalcoreGlobals.en_beauty_passes', index=2 )
        cmds.connectControl( self.post_passes, 'mentalcoreGlobals.en_post_passes', index=2 )
        cmds.connectControl( self.matte_passes, 'mentalcoreGlobals.en_matte_passes', index=2 )
        cmds.connectControl( self.custom_passes, 'mentalcoreGlobals.en_custom_passes', index=2 )
        
        
        ## ------------------------------------------------------------------------
        ## PRIMARY BUFFER
        ## ------------------------------------------------------------------------
        cmds.attrEnumOptionMenuGrp( self.channels, e=True, at='mentalcoreGlobals.primary_channels' )
        cmds.attrEnumOptionMenuGrp( self.bit_depth, e=True, at='mentalcoreGlobals.primary_bit_depth' )	
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.primary_group', self.update_pass_group], protected=True, parent=self.group)
        self.update_pass_group()
        
        #Update controls
        self.update_metadata()
        self.refresh_all_passes()
        self.update_clamp()        
                
    ## ------------------------------------------------------------------------
    ## UPDATE FUNCTIONS
    ## ------------------------------------------------------------------------
    def update_pass_group(self, *args):
        group = cmds.getAttr('mentalcoreGlobals.primary_group')
        cmds.textFieldGrp( self.group, e=True, text=group )
        
    def set_pass_group(self, *args):
        group = cmds.textFieldGrp( self.group, q=True, text=True )
        cmds.setAttr('mentalcoreGlobals.primary_group', group, type='string')
	
    def update_clamp(self):
        value = cmds.getAttr('mentalcoreGlobals.en_global_clamp')
        if value:
            cmds.control( self.global_clamp, e=True, en=True )
        else:
            cmds.control( self.global_clamp, e=True, en=False )
        
    ## ------------------------------------------------------------------------
    ## RENDER PASS FUNCTIONS
    ## ------------------------------------------------------------------------
    def build_pass_menu(self, menu, type, *args):
        '''Builds the right click renderpass menu on demand based on pass selection'''
        cmds.setParent( menu, menu=True )
        cmds.popupMenu(menu, e=True, dai=True)
        
        #Scene passes
        preview_mi = None
        sel_passes = None
        if type == 'scene_passes':
            sel_passes = cmds.textScrollList( self.scene_passes, q=True, si=True )
            
            if not sel_passes:
                #preset menu options
                if type == 'scene_passes':
                    cmds.menuItem(d=True)
                    cmds.menuItem(l='Presets', sm=True)
                    cmds.menuItem(l='Basic Pass Setup', c=partial(default_pass_preset, 'basic'))
                    cmds.menuItem(l='Basic Pass Setup With Shadow Pass', c=partial(default_pass_preset, 'basic_shad'))
                    cmds.menuItem(l='Raw Pass Setup', c=partial(default_pass_preset, 'raw'))
                    cmds.menuItem(l='Raw Pass Setup With Shadow Pass', c=partial(default_pass_preset, 'raw_shad'))
                    cmds.menuItem(d=True)
                    cmds.menuItem(l='Save Preset', c=partial(mapi.save_preset))
                    cmds.menuItem(l='Load Preset', c=partial(mapi.load_preset))
                    cmds.setParent('..', menu=True)
                return
            
            cmds.menuItem(l='Select', c=self.select_scene_pass)
            cmds.menuItem(l='Rename', c=self.rename_scene_pass)
            cmds.menuItem(d=True)
            cmds.menuItem(l='Add Selected To Render Layer', c=self.associate_pass)
            preview_mi = cmds.menuItem(l='Preview Selected Pass', c=self.preview_scene_pass)
            
        #Layer passes
        elif type == 'layer_passes':
            sel_passes = cmds.textScrollList( self.associated_passes, q=True, si=True )
            
            if not sel_passes:
                cmds.menuItem(l='No Pass Selected', en=False)
                return
            
            cmds.menuItem(l='Select', c=self.select_layer_pass)
            cmds.menuItem(l='Rename', c=self.rename_layer_pass)
            cmds.menuItem(d=True)
            cmds.menuItem(l='Remove Selected From Layer', c=self.unassociate_pass)
            preview_mi = cmds.menuItem(l='Preview Selected Pass', c=self.preview_layer_pass)
            
        #Check its not a diag pass and make preview option avaliable
        diag_pass = False
        if sel_passes:
            base_type = cmds.getAttr('%s.type' % sel_passes[0])
            if base_type >= 39 and base_type <= 41:
                diag_pass = True
                
        if diag_pass and preview_mi:
            cmds.menuItem(preview_mi, e=True, en=False)
            
        #Check types of selected passes to see if light linking should be avaliable
        sel_types = []
        show_light_linking = True
        for rp in sel_passes:
            sel_types.append(cmds.getAttr('%s.type' % rp))
            for pass_type in sel_types:
                if pass_type not in (DIFFUSE, DIFFUSE_RAW, DIFFUSE_NO_SHAD, DIFFUSE_NO_SHAD_RAW, SHADOW, SHADOW_RAW, SPECULAR, LIGHTSELECT):
                    show_light_linking = False
            
        #Link menu items
        cmds.menuItem(d=True)
        
        cmds.menuItem(l='Linked Objects', sm=True)
        cmds.menuItem(l='Link Selected Objects', c=partial(mapi.link_selected_to_pass, sel_passes, mapi.OBJECTS))
        cmds.menuItem(l='Unlink Selected Objects', c=partial(mapi.unlink_selected_from_pass, sel_passes, mapi.OBJECTS))
        cmds.menuItem(l='Unlink All Objects', c=partial(mapi.unlink_all_from_pass, sel_passes, mapi.OBJECTS))
        cmds.menuItem(d=True)
        cmds.menuItem(l='Select Linked Objects', c=partial(mapi.select_pass_linked, sel_passes, mapi.OBJECTS))
        cmds.setParent('..', menu=True)
        
        cmds.menuItem(l='Linked Materials', sm=True)		
        cmds.menuItem(l='Link Selected Materials', c=partial(mapi.link_selected_to_pass, sel_passes, mapi.MATERIALS))
        cmds.menuItem(l='Unlink Selected Materials', c=partial(mapi.unlink_selected_from_pass, sel_passes, mapi.MATERIALS))
        cmds.menuItem(l='Unlink All Materials', c=partial(mapi.unlink_all_from_pass, sel_passes, mapi.MATERIALS))
        cmds.menuItem(d=True)
        cmds.menuItem(l='Select Linked Materials', c=partial(mapi.select_pass_linked, sel_passes, mapi.MATERIALS))
        cmds.setParent('..', menu=True)
        
        if show_light_linking:
            cmds.menuItem(l='Linked Lights', sm=True)
            cmds.menuItem(l='Link Selected Lights', c=partial(mapi.link_selected_to_pass, sel_passes, mapi.LIGHTS))
            cmds.menuItem(l='Unlink Selected Lights', c=partial(mapi.unlink_selected_from_pass, sel_passes,mapi.LIGHTS))
            cmds.menuItem(l='Unlink All Lights', c=partial(mapi.unlink_all_from_pass, sel_passes, mapi.LIGHTS))
            cmds.menuItem(d=True)
            cmds.menuItem(l='Select Linked Lights', c=partial(mapi.select_pass_linked, sel_passes, mapi.LIGHTS))
            cmds.setParent('..', menu=True)
            
        #preset menu options
        if type == 'scene_passes':
            cmds.menuItem(d=True)
            cmds.menuItem(l='Presets', sm=True)
            cmds.menuItem(l='Basic Pass Setup', c=partial(default_pass_preset, 'basic'))
            cmds.menuItem(l='Basic Pass Setup With Shadow Pass', c=partial(default_pass_preset, 'basic_shad'))
            cmds.menuItem(l='Raw Pass Setup', c=partial(default_pass_preset, 'raw'))
            cmds.menuItem(l='Raw Pass Setup With Shadow Pass', c=partial(default_pass_preset, 'raw_shad'))
            cmds.menuItem(d=True)
            cmds.menuItem(l='Save Preset', c=partial(mapi.save_preset))
            cmds.menuItem(l='Load Preset', c=partial(mapi.load_preset))
            cmds.setParent('..', menu=True)
    
    
    def connect_pass(self, rp):
        cmds.scriptJob(nodeNameChanged=[str(rp), self.refresh_all_passes], protected=True, parent=self.scene_passes)
        cmds.scriptJob(connectionChange=['%s.message' % rp, self.refresh_all_passes], protected=True, parent=self.scene_passes)
        
        
    def refresh_all_passes(self):
        if cmds.control(self.scene_passes, q=True, exists=True):
            self.refresh_scene_passes()
            self.refresh_layer_passes()
        mc.rebuild_renderview_menu()
        
        
    def refresh_scene_passes(self):
        try:
            selected = cmds.textScrollList( self.scene_passes, q=True, si=True )
            cmds.textScrollList( self.scene_passes, e=True, ra=True )
            
            current_layer = cmds.editRenderLayerGlobals(q=True, crl=True)
            
            unassociated_passes = mapi.get_unassociated_passes(current_layer)
            if unassociated_passes:
                for rp in unassociated_passes:
                    cmds.textScrollList( self.scene_passes, e=True, append=rp )
                
                if selected:
                    for sel in selected:
                        if sel in unassociated_passes:
                            cmds.textScrollList( self.scene_passes, e=True, si=sel )
        except:
            pass
                        

    def refresh_layer_passes(self):
        try:
            selected = cmds.textScrollList( self.associated_passes, q=True, si=True )
            cmds.textScrollList( self.associated_passes, e=True, ra=True )
            
            current_layer = cmds.editRenderLayerGlobals(q=True, crl=True)
            
            associated_passes = mapi.get_associated_passes(current_layer)
            if associated_passes:
                for rp in associated_passes:
                    cmds.textScrollList( self.associated_passes, e=True, append=rp )
            
                if selected:
                    for sel in selected:
                        if sel in associated_passes:
                            cmds.textScrollList( self.associated_passes, e=True, si=sel )
        except:
            pass
                        
    def preview_scene_pass(self, *args):
        sel_passes = cmds.textScrollList( self.scene_passes, q=True, si=True )
        if sel_passes:
            mapi.set_preview(sel_passes[0])
            cmds.setAttr('mentalcoreGlobals.output_mode', 0)

    def preview_layer_pass(self, *args):
        sel_passes = cmds.textScrollList( self.associated_passes, q=True, si=True )
        if sel_passes:
            mapi.set_preview(sel_passes[0])
            cmds.setAttr('mentalcoreGlobals.output_mode', 0)
        
    def add_pass(self, *args):
        sel_passes = cmds.textScrollList( self.avail_passes, q=True, si=True )
        if sel_passes:
            for rp_type in sel_passes:
                rp = mapi.create_pass(rp_type)
                
            
    def remove_pass(self, *args):
        sel_passes = cmds.textScrollList( self.scene_passes, q=True, si=True )
        if sel_passes:
            for rp in sel_passes:
                try:
                    cmds.delete(rp)
                except:
                    pass
                    
    
    def select_scene_pass(self, *args):
        sel_passes = cmds.textScrollList( self.scene_passes, q=True, si=True )
        cmds.select(sel_passes, r=True)
        
    def select_layer_pass(self, *args):
        sel_passes = cmds.textScrollList( self.associated_passes, q=True, si=True )
        cmds.select(sel_passes, r=True)
        
        
    def rename_layer_pass(self, *args):
        sel_passes = cmds.textScrollList( self.associated_passes, q=True, si=True )
    
        if sel_passes:
            result = cmds.promptDialog(title='Rename', message='Enter Name:', text=sel_passes[0], button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel')
            
            if result == 'OK':
                new_name = cmds.promptDialog(q=True, text=True)
                for rp in sel_passes:
                    cmds.rename(rp, new_name)
        
    def rename_scene_pass(self, *args):
        sel_passes = cmds.textScrollList( self.scene_passes, q=True, si=True )
        if sel_passes:
            result = cmds.promptDialog(title='Rename', message='Enter Name:', text=sel_passes[0], button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel')
            
            if result == 'OK':
                new_name = cmds.promptDialog(q=True, text=True)
                for rp in sel_passes:
                    cmds.rename(rp, new_name)
    
        
    def associate_pass(self, *args):
        current_layer = cmds.editRenderLayerGlobals(q=True, crl=True)
    
        sel_passes = cmds.textScrollList( self.scene_passes, q=True, si=True )
        if sel_passes:
            for rp in sel_passes:
                mapi.associate_pass(rp, current_layer)

                
    def unassociate_pass(self, *args):
        current_layer = cmds.editRenderLayerGlobals(q=True, crl=True)
    
        sel_passes = cmds.textScrollList( self.associated_passes, q=True, si=True )
        if sel_passes:
            for rp in sel_passes:
                mapi.unassociate_pass(rp, current_layer)
                
    ## ------------------------------------------------------------------------
    ## METADATA FUNCTIONS
    ## ------------------------------------------------------------------------		
    def update_metadata(self):
        #check maya version
        maya_ver = int(cmds.about(f=True))
            
        maya2013 = False
        if maya_ver >= 2013:
            maya2013 = True
            
        if not maya2013:
            return
    
        #Set parent
        cmds.setParent('mc_meta_layout')
        
        #Delete existing children
        child_array = cmds.layout('mc_meta_layout', q=True, ca=True)
        if child_array:
            for child in child_array:
                cmds.deleteUI(child)
        
        #List all meta data attributes
        meta_attrs = cmds.listAttr('mentalcoreGlobals', m=True, v=True, c=True, st='metadata')
        
        if meta_attrs:
            for attr in meta_attrs:
                #Full metadata attribute
                full_attr = 'mentalcoreGlobals.%s' % attr
                   
                #Row layout
                cmds.rowLayout(nc=6, adj=6, cw6=[25, 18, 80, 100, 34, 100], dtg=attr)

                #Delete data
                cmds.iconTextButton(l='', mw=0, mh=0, h=24, image='smallTrash.png', c=partial(self.delete_metadata, attr))

                #Enable data
                en_check = cmds.checkBox(l='')
                cmds.connectControl(en_check, '%s.meta_enable' % full_attr)
                
                cmds.scriptJob(attributeChange=['%s.meta_enable' % full_attr, partial(self.update_metadata_enable, attr)], 
                                protected=True, 
                                parent=en_check)
                
                #Data Type
                meta_type = cmds.attrEnumOptionMenuGrp( l='',
                                cw=[1, 1],
                                at='%s.meta_type' % full_attr,
                                ei=[(0, 'String'),(1, 'Boolean'), (2, 'Integer'), (3, 'Scalar'), (4, 'Vector') ] )
                                
                cmds.scriptJob(attributeChange=['%s.meta_type' % full_attr, partial(self.update_metdata_type, attr)], 
                                protected=True, 
                                parent=meta_type)
                
                #Data Key
                key_field = cmds.textFieldGrp(l='Key:', cw2=[22, 70])
                cmds.connectControl(key_field, '%s.meta_key' % full_attr, index=2)
                
                #Value
                cmds.text(l='Value:')
                
                data_layout = cmds.columnLayout(rs=0, adj=True)
                
                #Data Controls
                string_data = cmds.textField(vis=False)
                cmds.connectControl(string_data, '%s.meta_string' % full_attr)
                
                bool_data = cmds.checkBoxGrp(l='', cw=[1,0], vis=False)
                cmds.connectControl(bool_data, '%s.meta_bool' % full_attr, index=2)
                
                int_data = cmds.intField(vis=False)
                cmds.connectControl(int_data, '%s.meta_int' % full_attr)
                
                scalar_data = cmds.floatField(vis=False)
                cmds.connectControl(scalar_data, '%s.meta_scalar' % full_attr)
                
                vector_data = cmds.floatFieldGrp(l='', nf=3, cw4=[0,58,58,58], vis=False)
                cmds.connectControl(vector_data, '%s.meta_vectorX' % full_attr, index=2)
                cmds.connectControl(vector_data, '%s.meta_vectorY' % full_attr, index=3)
                cmds.connectControl(vector_data, '%s.meta_vectorZ' % full_attr, index=4)
                
                cmds.setParent('..')
                
                #Update meta data
                self.update_metadata_enable(attr)
                self.update_metdata_type(attr)
                
                cmds.setParent('..')
                
    def update_metadata_enable(self, attr):
        #find matching metadata ui
        full_attr = 'mentalcoreGlobals.%s' % attr
        child_array = cmds.layout('mc_meta_layout', q=True, ca=True)
        
        for child in child_array:
            if attr == cmds.layout(child, q=True, dtg=True): #Found
                #Find matching control, hide others
                enabled = cmds.getAttr('%s.meta_enable' % full_attr)
                grandchildren = cmds.layout(child, q=True, ca=True)[2:]
                
                for control in grandchildren:
                    cmds.control(control, e=True, en=enabled)
                    
                break
                
    def update_metdata_type(self, attr):
        #find matching metadata ui
        full_attr = 'mentalcoreGlobals.%s' % attr
        child_array = cmds.layout('mc_meta_layout', q=True, ca=True)
        
        for child in child_array:
            if attr == cmds.layout(child, q=True, dtg=True): #Found
                #Find matching control, hide others
                type = cmds.getAttr('%s.meta_type' % full_attr)
                type_layout = cmds.layout(child, q=True, ca=True)[-1]
                type_controls = cmds.layout(type_layout, q=True, ca=True)
                match_control = None
                
                for i in range(len(type_controls)):
                    control = type_controls[i]
                    if type == i:
                        match_control = control
                    else:
                        cmds.control(control, e=True, vis=False)
                  
                #Show matched control
                if match_control:     
                    cmds.control(match_control, e=True, vis=True)
                
                break
                
    def create_metadata(self, *args):
        #find next attribute
        meta_attrs = cmds.listAttr('mentalcoreGlobals', m=True, v=True, c=True, st='metadata')
        if meta_attrs:
            last_attr = meta_attrs[-1]
            last_attr = last_attr.replace('metadata[', '')
            last_attr = last_attr.replace(']', '')
            
            cmds.getAttr('mentalcoreGlobals.metadata[%i].meta_enable' % (int(last_attr) + 1))
        else:
            cmds.getAttr('mentalcoreGlobals.metadata[0].meta_enable')
        
        #update metadata ui
        self.update_metadata()
                
    def delete_metadata(self, attr):
        #find matching metadata ui
        full_attr = 'mentalcoreGlobals.%s' % attr
        child_array = cmds.layout('mc_meta_layout', q=True, ca=True)
        
        for child in child_array:
            if attr == cmds.layout(child, q=True, dtg=True): #Found
                cmds.deleteUI(child)
                break
                
        cmds.removeMultiInstance(full_attr)

    
## ------------------------------------------------------------------------
## UTILITY FUNCTIONS
## ------------------------------------------------------------------------
def default_pass_preset(preset, *args):
    '''Default preset pass setups'''
    if preset == 'basic':
        mapi.create_pass('Diffuse')
        mapi.create_pass('Ambient')
        mapi.create_pass('Indirect')
        mapi.create_pass('Ambient Occlusion')
        mapi.create_pass('Subsurface')
        mapi.create_pass('Incandescence')
        mapi.create_pass('Specular')
        mapi.create_pass('Reflection')
        mapi.create_pass('Refraction')
        mapi.create_pass('Depth')
        mapi.create_pass('Motion Vector')
        mapi.create_pass('Material ID')
        mapi.create_pass('Object ID')
    elif preset == 'basic_shad':
        mapi.create_pass('Diffuse Without Shadows')
        mapi.create_pass('Shadow')
        mapi.create_pass('Ambient')
        mapi.create_pass('Indirect')
        mapi.create_pass('Ambient Occlusion')
        mapi.create_pass('Subsurface')
        mapi.create_pass('Incandescence')
        mapi.create_pass('Specular')
        mapi.create_pass('Reflection')
        mapi.create_pass('Refraction')
        mapi.create_pass('Depth')
        mapi.create_pass('Motion Vector')
        mapi.create_pass('Material ID')
        mapi.create_pass('Object ID')
    elif preset == 'raw':
        mapi.create_pass('Colour')
        mapi.create_pass('Diffuse Raw')
        mapi.create_pass('Ambient Raw')
        mapi.create_pass('Indirect Raw')
        mapi.create_pass('Ambient Occlusion')
        mapi.create_pass('Subsurface Front')
        mapi.create_pass('Subsurface Mid')
        mapi.create_pass('Subsurface Back')
        mapi.create_pass('Incandescence')
        mapi.create_pass('Specular')
        mapi.create_pass('Reflection')
        mapi.create_pass('Refraction')
        mapi.create_pass('Depth')
        mapi.create_pass('Normal World')
        mapi.create_pass('Point World')
        mapi.create_pass('Motion Vector')
        mapi.create_pass('Material ID')
        mapi.create_pass('Object ID')
    elif preset == 'raw_shad':
        mapi.create_pass('Colour')
        mapi.create_pass('Shadow Raw')
        mapi.create_pass('Diffuse Without Shadows Raw')
        mapi.create_pass('Ambient Raw')
        mapi.create_pass('Indirect Raw')
        mapi.create_pass('Ambient Occlusion')
        mapi.create_pass('Subsurface Front')
        mapi.create_pass('Subsurface Mid')
        mapi.create_pass('Subsurface Back')
        mapi.create_pass('Incandescence')
        mapi.create_pass('Specular')
        mapi.create_pass('Reflection')
        mapi.create_pass('Refraction')
        mapi.create_pass('Depth')
        mapi.create_pass('Normal World')
        mapi.create_pass('Point World')
        mapi.create_pass('Motion Vector')
        mapi.create_pass('Material ID')
        mapi.create_pass('Object ID')
