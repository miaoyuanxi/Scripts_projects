#  Copyright (c)2013 Core CG
#  All rights reserved
#  www.core-cg.com

## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
import traceback
import maya.cmds as cmds
from mentalcore import mapi
reload(mapi)

## ------------------------------------------------------------------------
## CALLBACKS
## ------------------------------------------------------------------------
class LowResTexUI(object):
    def __init__(self):
        # Maya UI name
        self.ui_name = 'MC_lowResTexUI'
        
        # Delete existing window
        if cmds.window(self.ui_name, exists=True):            
            cmds.deleteUI(self.ui_name)
            #cmds.windowPref(self.ui_name, remove=True)
            
        # Create window
        self.window = cmds.window(self.ui_name, title='Generate Low Res Textures', width=350, height=200, sizeable=False)
        
        # Create logo bar
        main_layout = cmds.columnLayout(adj=True)
        
        logo_form = cmds.formLayout(h=26)
    
        logo_left = cmds.picture(image='mc_titlebar_l.png', h=26, w=10)
        logo = cmds.picture(image='mc_titlebar.png', h=26, w=1, tl=1)
        logo_right = cmds.picture(image='texture_generator_logo.png', h=26, w=200)
            
        cmds.formLayout(logo_form, edit=True,
                        af=[(logo_left, 'top', 0),
                            (logo_left, 'left', 0),
                            (logo_left, 'bottom', 0),
                            (logo_right, 'top', 0),
                            (logo_right, 'right', 0),
                            (logo_right, 'bottom', 0),
                            (logo, 'top', 0),
                            (logo, 'bottom', 0)],
                        ac=[(logo, 'left', 0, logo_left),
                            (logo, 'right', 0, logo_right)])
        
        # Create layout
        cmds.setParent(main_layout)
        self.layout = cmds.columnLayout(columnAttach=('both', 5), adj=True)
        cmds.separator(h=5, w=350, style='none')
        
        # Setup remaining UI
        self.setup_ui()
        self.update_ui()
        
    def setup_ui(self):
        # Create proxy texture layout
        cmds.frameLayout( label='Low Res Proxy Textures', borderStyle='etchedIn' )        
        cmds.columnLayout(columnAttach=('both', 5), adj=True, rs=2)
        
        self.create_proxy = cmds.checkBoxGrp(l='', l1='Generate Proxy Textures', cw2=[140, 100], cc=self.update_ui, ann='Generate low resolution textures to speed up test renders.\nOriginal textures will be used during batch render.\nProxy textures can be disabled in the Advanced tab of the MentalCore render globals.')
        
        self.proxy_res = cmds.optionMenuGrp(label='Resolution')
        cmds.menuItem( label='1/2' )
        cmds.menuItem( label='1/4' )
        cmds.menuItem( label='1/8' )
        cmds.menuItem( label='1/16' )
        cmds.menuItem( label='1/32' )
        
        self.proxy_format = cmds.optionMenuGrp(label='Format')
        cmds.menuItem( label='png' )
        cmds.menuItem( label='jpg' )
        cmds.menuItem( label='tif' )
        
        self.delete_proxy = cmds.button(l='Delete Proxy Textures', h=20, c=self.delete_proxy_textures)
        
        cmds.separator(h=2, style='none')
        
        cmds.setParent(self.layout)
        
        # Create fg texture layout
        cmds.frameLayout( label='Low Res Finalgather Textures', borderStyle='etchedIn' )
        cmds.columnLayout(columnAttach=('both', 5), adj=True, rs=2)

        self.create_fg = cmds.checkBoxGrp(l='', l1='Generate Finalgather Textures', cw2=[140, 100], cc=self.update_ui, ann='Generate low resolution textures to speed upFinalgather calculation.')
        
        self.fg_res = cmds.optionMenuGrp(label='Resolution')
        cmds.menuItem( label='1/2' )
        cmds.menuItem( label='1/4' )
        cmds.menuItem( label='1/8' )
        cmds.menuItem( label='1/16' )
        cmds.menuItem( label='1/32' )
        cmds.optionMenuGrp(self.fg_res, e=True, v='1/8')
        
        self.fg_format = cmds.optionMenuGrp(label='Format')
        cmds.menuItem( label='png' )
        cmds.menuItem( label='jpg' )
        cmds.menuItem( label='tif' )
        
        self.delete_fg = cmds.button(l='Delete Finalgather Textures', h=20, c=self.delete_fg_textures)
        
        cmds.separator(h=2, style='none')
        
        cmds.setParent(self.layout)
        
        cmds.separator(h=5, style='none')
        
        # Generate buttom
        self.generate = cmds.button(l='Generate Low Res Textures', h=32, c=self.generate_textures)
        
        cmds.separator(h=5, style='none')
        
    def update_ui(self, *args):
        # Update proxy res
        if cmds.checkBoxGrp(self.create_proxy, q=True, v1=True):
            cmds.control(self.proxy_res, e=True, en=True)
            cmds.control(self.proxy_format, e=True, en=True)
        else:
            cmds.control(self.proxy_res, e=True, en=False)
            cmds.control(self.proxy_format, e=True, en=False)
        
        # Update fg res
        if cmds.checkBoxGrp(self.create_fg, q=True, v1=True):
            cmds.control(self.fg_res, e=True, en=True)
            cmds.control(self.fg_format, e=True, en=True)
        else:
            cmds.control(self.fg_res, e=True, en=False)
            cmds.control(self.fg_format, e=True, en=False)
        
    def generate_textures(self, *args):
        # Get options
        create_proxy = cmds.checkBoxGrp(self.create_proxy, q=True, v1=True)
        proxy_res = cmds.optionMenuGrp(self.proxy_res, q=True, v=True)
        proxy_format = cmds.optionMenuGrp(self.proxy_format, q=True, v=True)
        
        create_fg = cmds.checkBoxGrp(self.create_fg, q=True, v1=True)
        fg_res = cmds.optionMenuGrp(self.fg_res, q=True, v=True)
        fg_format = cmds.optionMenuGrp(self.fg_format, q=True, v=True)
        
        # Validate
        if not create_proxy and not create_fg:
            return cmds.confirmDialog( title='Warning', message='No options selected for conversion!', button=['Ok'])
        
        # Start conversion
        try:
            result = mapi.generate_low_res_textures(proxy=create_proxy, proxy_res=proxy_res, proxy_format=proxy_format, 
                                                    fg=create_fg, fg_res=fg_res, fg_format=fg_format,
                                                    create_nodes=True, progress=True)
            if not result:
                cmds.confirmDialog( title='Completed With Errors', message='There were some errors during processing, see script editor for details!', button=['Ok'])
        except:
            print traceback.format_exc()
            cmds.confirmDialog( title='Error', message='Error during texture conversion, see script editor for details!', button=['Ok'])
        
    def delete_proxy_textures(self, *args):
        prompt = cmds.confirmDialog( title='Delete Proxy Textures', message='This will delete all Proxy texture nodes from the scene.\nDo you also want to delete textures from disk as well?', button=['Yes, delete from disk', 'No, only from scene', 'Cancel'])
        try:
            if prompt == 'Yes, delete from disk':
                result = mapi.delete_low_res_textures(proxy=True, from_disk=True, progress=True)
                if not result:
                    cmds.confirmDialog( title='Completed With Errors', message='There were some errors during processing, see script editor for details!', button=['Ok'])
            elif prompt == 'No, only from scene':
                result = mapi.delete_low_res_textures(proxy=True, from_disk=False, progress=True)
                if not result:
                    cmds.confirmDialog( title='Completed With Errors', message='There were some errors during processing, see script editor for details!', button=['Ok'])
        except:
            print traceback.format_exc()
            cmds.confirmDialog( title='Error', message='Error deleting Proxy textures, see script editor for details!', button=['Ok'])
    
    def delete_fg_textures(self, *args):
        prompt = cmds.confirmDialog( title='Delete Finalgather Textures', message='This will delete all Finalgather texture nodes from the scene.\nDo you also want to delete textures from disk as well?', button=['Yes, delete from disk', 'No, only from scene', 'Cancel'])
        try:
            if prompt == 'Yes, delete from disk':
                result = mapi.delete_low_res_textures(fg=True, from_disk=True, progress=True)
                if not result:
                    cmds.confirmDialog( title='Completed With Errors', message='There were some errors during processing, see script editor for details!', button=['Ok'])
            elif prompt == 'No, only from scene':
                result = mapi.delete_low_res_textures(fg=True, from_disk=False, progress=True)
                if not result:
                    cmds.confirmDialog( title='Completed With Errors', message='There were some errors during processing, see script editor for details!', button=['Ok'])
        except:
            print traceback.format_exc()
            cmds.confirmDialog( title='Error', message='Error deleting Finalgather textures, see script editor for details!', button=['Ok'])
        
    def show(self):
        cmds.showWindow(self.window)
        
    def close(self):
        cmds.deleteUI(self.window)
