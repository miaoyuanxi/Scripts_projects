#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com

## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
from functools import partial
import webbrowser
from datetime import date

import maya.cmds as cmds
import maya.mel as mel

import mentalcore as mc
import mlib
import mapi

import general 
import options
import passes
import advanced

## ------------------------------------------------------------------------
## GLOBAL VARIABLES
## ------------------------------------------------------------------------
GLOBALS = None


## ------------------------------------------------------------------------
## RENDERGLOBALS TAB
## ------------------------------------------------------------------------
def build():
    '''Builds the render globals tab'''
    global GLOBALS
    GLOBALS = RenderGlobals()
        
def update():
    '''Updates the render globals tab'''
    global GLOBALS
    if GLOBALS:
        GLOBALS.update()


#Create globals tab
class RenderGlobals():
    '''Creates the mentalcore render globals tab'''
    def __init__(self):
        self.create()

    def update(self):
        #update metal core
        self.update_enable()


    def create(self):
        #create globals tab
        parent_form = cmds.setParent(q=True)
        cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)

        #check if shaders installed
        if not cmds.getClassification('core_globals')[0]:
            def open_docs(*args):
                webbrowser.open("http://core-cg.com/docs/index.html")
            
            msg = cmds.text(l='MentalCore Shaders Not Installed Correctly')
            link = cmds.button(l='Open Documentation', c=open_docs)
            
            cmds.formLayout(parent_form, edit=True,
                attachForm=[(msg, 'left', 0),
                            (msg, 'right', 0),
                            (link, 'left', 20),
                            (link, 'right', 20)],
                attachPosition=[(msg, 'bottom', 0, 50)],
                attachControl=[(link, 'top', 5, msg)])
        
            return None
            
        #check if license exists or is expired
        if not mlib.is_license_valid():
            def open_docs(*args):
                webbrowser.open("http://core-cg.com/docs/licensing.html")
        
            msg = cmds.text(l='No valid license found, see documentation for help')
            link = cmds.button(l='Open Documentation', c=open_docs)
            
            cmds.formLayout(parent_form, edit=True,
                attachForm=[(msg, 'left', 0),
                            (msg, 'right', 0),
                            (link, 'left', 20),
                            (link, 'right', 20)],
                attachPosition=[(msg, 'bottom', 0, 50)],
                attachControl=[(link, 'top', 5, msg)])
        
            return None
            
        elif mlib.is_license_expired():	
            def open_site(*args):
                webbrowser.open("http://core-cg.com")
        
            msg = cmds.text(l='License Expired, visit www.core-cg.com to purchase')
            link = cmds.button(l='Open Website', c=open_site)
            
            cmds.formLayout(parent_form, edit=True,
                attachForm=[(msg, 'left', 0),
                            (msg, 'right', 0),
                            (link, 'left', 20),
                            (link, 'right', 20)],
                attachPosition=[(msg, 'bottom', 0, 50)],
                attachControl=[(link, 'top', 5, msg)])
            
            return None
        
        
        # ----------------------------------------
        # MENTALCORE
        # ----------------------------------------
        
        #core logo
        bar_left = cmds.picture(image='mc_titlebar_l.png', h=26, w=10)
        bar = cmds.picture(image='mc_titlebar.png', h=26, w=1, tl=True)
        bar_right = cmds.picture(image='mc_globals_logo.png', h=26, w=120)
        

        #enable mc
        cmds.separator(style='none', h=2)
        self.enable_check = cmds.checkBoxGrp(l1='  Enable MentalCore  ', ann='Enable or disable MentalCore', cc=self.enable_toggle)
        #cmds.connectControl(en_check, 'defaultMentalCoreGlobals.enable_mental_core', index=2)
        
        #Tabs
        self.tab_layout = cmds.tabLayout('mc_globals_tabs', innerMarginWidth=5, innerMarginHeight=5, cr=True, scr=True)
        
        #General Tab
        general_layout = cmds.columnLayout('mc_general_col', rs=1, adj=True)
        self.general_tab = general.GeneralTab()
        cmds.setParent(self.tab_layout)
        
        #Optons Tab
        options_layout = cmds.columnLayout('mc_options_col', rs=1, adj=True)
        self.options_tab = options.OptionsTab()
        cmds.setParent(self.tab_layout)
        
        #Passes Tab
        passes_layout = cmds.columnLayout('mc_passes_col', rs=1, adj=True)
        self.passes_tab = passes.PassesTab()
        cmds.setParent(self.tab_layout)
    
        #Advanced Tab
        advanced_layout = cmds.columnLayout('mc_advanced_col', rs=1, adj=True)
        self.advanced_tab = advanced.AdvancedTab()
        cmds.setParent(self.tab_layout)
        
        cmds.tabLayout( self.tab_layout, edit=True, tabLabel=((general_layout, 'General'), (options_layout, 'Options'), (passes_layout, 'Render Passes'), (advanced_layout, 'Advanced')) )
        
        #set form layout
        cmds.setUITemplate(popTemplate=True)
        
        cmds.formLayout(parent_form, edit=True,
            attachForm=[(bar_left, 'top', 0),
                        (bar_left, 'left', 0),
                        (bar, 'top', 0),
                        (bar_right, 'top', 0),
                        (bar_right, 'right', 0),
                        (self.enable_check, 'left', 0),
                        (self.enable_check, 'right', 0),
                        (self.tab_layout, 'left', 0),
                        (self.tab_layout, 'right', 0),
                        (self.tab_layout, 'bottom', 0)],
            attachControl=[	(bar, 'left', 0, bar_left), 
                            (bar, 'right', 0, bar_right), 
                            (self.enable_check, 'top', 4, bar_right), 
                            (self.tab_layout, 'top', 0, self.enable_check)])
                            
        #remaining days message
        license_expiry = mlib.get_license_expiry()
        if license_expiry:
            cmds.setParent(parent_form)
            
            #remaining days
            diff = license_expiry - date.today()
            msg = cmds.text(l='License expires in %i days' % diff.days, en=False)
            
            cmds.formLayout(parent_form, edit=True,
                attachForm=[(msg, 'right', 12)],
                attachControl=[	(msg, 'top', 2, bar_right), 
                                (self.enable_check, 'top', 2, msg)])
            
            
        #check if mc is already enabled
        if cmds.objExists('mentalcoreGlobals'):
            cmds.scriptJob(attributeChange=['mentalcoreGlobals.enable', self.update_enable], protected=True, parent=self.enable_check)
            self.general_tab.connect_controls()
            self.options_tab.connect_controls()
            self.passes_tab.connect_controls()
            self.advanced_tab.connect_controls()
            
            if cmds.getAttr('mentalcoreGlobals.enable'):
                cmds.layout(self.tab_layout, e=True, en=True)
        
        self.update_enable()
        
    ## ------------------------------------------------------------------------
    ## UPDATE FUNCTIONS
    ## ------------------------------------------------------------------------	
    def update_enable(self):
        if cmds.objExists('mentalcoreGlobals'):
            enabled = cmds.getAttr('mentalcoreGlobals.enable')
            cmds.checkBoxGrp(self.enable_check, e=True, v1=enabled)
            if enabled:
                cmds.layout(self.tab_layout, e=True, en=True)
            else:
                cmds.layout(self.tab_layout, e=True, en=False)
        else:
            cmds.checkBoxGrp(self.enable_check, e=True, v1=False)
            cmds.layout(self.tab_layout, e=True, en=False)

    
    def enable_toggle(self, *args):
        if cmds.checkBoxGrp(self.enable_check, q=True, v1=True):
        
            init = False
            if not cmds.objExists('mentalcoreGlobals'):
                init = True
        
            #enable mentalcore
            mapi.enable(True)
        
            if init:
                cmds.scriptJob(attributeChange=['mentalcoreGlobals.enable', self.update_enable], protected=True, parent=self.enable_check)
                self.general_tab.connect_controls()
                self.options_tab.connect_controls()
                self.passes_tab.connect_controls()
                self.advanced_tab.connect_controls()
                
            cmds.setAttr('mentalcoreGlobals.enable', True)
            cmds.layout(self.tab_layout, e=True, en=True)
        else:
            mapi.enable(False)
            cmds.layout(self.tab_layout, e=True, en=False)
