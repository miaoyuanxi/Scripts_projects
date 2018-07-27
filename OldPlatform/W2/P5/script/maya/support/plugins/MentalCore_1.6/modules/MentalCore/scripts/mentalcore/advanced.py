#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com

## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
from functools import partial

import maya.cmds as cmds
import maya.mel as mel

from mentalcore import mlib

## ------------------------------------------------------------------------
## GLOBAL VARIABLES
## ------------------------------------------------------------------------
ADVANCED_TAB = None

## ------------------------------------------------------------------------
## ADVANCED TAB
## ------------------------------------------------------------------------
class AdvancedTab():
    '''Creates the advanced tab of the mentalcore globals'''
    def __init__(self):
        global ADVANCED_TAB
        ADVANCED_TAB = self
        
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
        ## OUTPUT OVERRIDE
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Output', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
                
        #output override
        self.output_override = cmds.attrEnumOptionMenuGrp( l='Output Override', ei=[(0, 'Normal'),(1, 'Primary Holdout'),(9, 'Holdout'),(2, 'Matte'),(3, 'Post Passes Only'),(4, 'Core Materials Only'),(5, 'Mia Materials Only'),(6, 'Paint Materials Only'),(7, 'Hair Materials Only'),(8, 'Surface Shaders Only') ] )
 
        cmds.setParent(self.layout)
        
        ## ------------------------------------------------------------------------
        ## OPTIONS
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Options', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #light relative scale
        self.light_relative_scale = cmds.attrFieldSliderGrp( label='Light Relative Scale', min=0.0, max=1.0, fmx=10000, vis=maya2013 )
        #detail shadowmap contrast
        self.shadowmap_contrast = cmds.attrColorSliderGrp( l='Detail Shadow Contrast', vis=maya2013 )
        
        cmds.separator(vis=maya2013)
                
        #trace camera motion
        self.trace_cam_motion = cmds.checkBoxGrp( l1='Trace Camera Motion Vectors', vis=maya2013 and not maya2014 )
        #trace camera clip
        self.trace_cam_clip = cmds.checkBoxGrp( l1='Trace Camera Clip', vis=maya2013 and not maya2014 )
        #force proview profile for primary buffer
        self.preview_profile_pri_buffer = cmds.checkBoxGrp( l1='Use Preview Profile for Sampling Beauty Passes')
                
        cmds.separator(vis=maya2013 and not maya2014)
                
        #disable swatches
        cmds.checkBoxGrp(l1='Disable Swatch Rendering (Requires Restart)', cc=lambda *args: cmds.optionVar(iv=('MC_DISABLE_SWATCHES', args[0])), v1=cmds.optionVar(q='MC_DISABLE_SWATCHES'))
        #expose mip shaders
        cmds.checkBoxGrp(l1='Expose MIP Shaders (Requires Restart)', cc=lambda *args: cmds.optionVar(iv=('MIP_SHD_EXPOSE', args[0])), v1=int(cmds.optionVar(q='MIP_SHD_EXPOSE')))
        #expose map shaders
        cmds.checkBoxGrp(l1='Expose MAP Shaders (Requires Restart)', cc=lambda *args: cmds.optionVar(iv=('MAP_SHD_EXPOSE', args[0])), v1=int(cmds.optionVar(q='MAP_SHD_EXPOSE')))
                
        cmds.setParent(self.layout)
                
        ## ------------------------------------------------------------------------
        ## PERFORMANCE
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Performance', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #use proxy textures
        self.use_proxy_textures = cmds.checkBoxGrp( l1='Use Proxy Textures in Preview Mode' )
        #use proxy textures for secondary rays
        self.use_proxy_textures_sec = cmds.checkBoxGrp( l1='Use Proxy Textures for Seconday Rays' )
        #disable baked textures
        self.disable_baked_textures = cmds.checkBoxGrp( l1='Disable Baked Textures' )
        
        cmds.separator()
        
        #contrast all buffers
        self.contrast_buffers = cmds.checkBoxGrp( l1='Contrast All Buffers' )
        #ray differentials
        self.ray_differentials = cmds.checkBoxGrp( l1='Ray Differentials' )
        #finalgather legacy
        self.finalgather_legacy = cmds.checkBoxGrp( l1='Legacy Final Gather' )
        #hair mem mode
        self.hair_mem_mode = cmds.checkBoxGrp( l1='Hair Memory Mode' )
        #hair caps
        self.hair_caps = cmds.checkBoxGrp( l1='Hair Caps' )
        #nested assemblies
        self.nested_assemblies = cmds.checkBoxGrp( l1='Enable Nested Assemblies', vis=maya2014 )
                
        cmds.setParent(self.layout)
                
        ## ------------------------------------------------------------------------
        ## IMPORTANCE SAMPLING
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Importance Sampling', w=430, collapsable=True, collapse=False, vis=maya2013)
        cmds.columnLayout(rs=1, adj=True)
        
        self.light_is = cmds.attrEnumOptionMenuGrp( l='Light Importance Sampling', ei=[(0, 'Off'),(1, 'On'),(2, 'Always')], vis=maya2014 )
        self.light_is_variance = cmds.floatFieldGrp( label='Variance', vis=maya2014 )
        self.light_is_precomp = cmds.checkBoxGrp( l1='Presample', vis=maya2014 )
                
        cmds.separator(vis=maya2014)
                
        self.mis = cmds.checkBoxGrp( l1='Multiple Importance Sampling', vis=maya2014 )
                
        cmds.separator(vis=maya2014)
                
        self.finalgather_importance = cmds.attrEnumOptionMenuGrp( l='Finalgather Importance', ei=[(0, 'Off'),(1, 'Partial'),(2, 'Full') ] )
        
        cmds.setParent(self.layout)
                
        ## ------------------------------------------------------------------------
        ## SHUTTER EFFICIENCY
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Shutter Efficiency (Motion Blur)', w=430, collapsable=True, collapse=False, vis=maya2014)
        cmds.columnLayout(rs=1, adj=True)
        
        self.shutter_shape = cmds.attrEnumOptionMenuGrp( l='Shape', ei=[(0, 'None (Box)'),(1, 'Trapezoidal')] )
        self.shutter_efficiency = cmds.attrFieldSliderGrp( label='Efficiency', min=0.5, max=1.0, pre=2, fmx=1 )
                
                
        cmds.setParent(self.layout)


        cmds.setUITemplate(popTemplate=True)
        
                            
    def connect_controls(self):
        ## ------------------------------------------------------------------------
        ## OUTPUT
        ## ------------------------------------------------------------------------
        cmds.attrEnumOptionMenuGrp( self.output_override, e=True, at='mentalcoreGlobals.output_override' )
        
        ## ------------------------------------------------------------------------
        ## OPTIONS
        ## ------------------------------------------------------------------------
        cmds.attrFieldSliderGrp( self.light_relative_scale, e=True, at='mentalcoreGlobals.light_relative_scale' )
        cmds.attrColorSliderGrp( self.shadowmap_contrast, e=True, at='mentalcoreGlobals.detail_shadowmap_contrast' )
        cmds.connectControl( self.trace_cam_motion, 'mentalcoreGlobals.trace_camera_motion_vectors', index=2 )
        cmds.connectControl( self.trace_cam_clip, 'mentalcoreGlobals.trace_camera_clip', index=2 )
        cmds.connectControl( self.preview_profile_pri_buffer, 'mentalcoreGlobals.preview_profile_pri_buffer', index=2 )
        
        ## ------------------------------------------------------------------------
        ## PERFORMANCE
        ## ------------------------------------------------------------------------
        cmds.connectControl( self.use_proxy_textures, 'mentalcoreGlobals.use_proxy_textures', index=2 )
        cmds.connectControl( self.use_proxy_textures_sec, 'mentalcoreGlobals.use_proxy_textures_sec', index=2 )
        cmds.connectControl( self.disable_baked_textures, 'mentalcoreGlobals.disable_baked_textures', index=2 )
        cmds.connectControl( self.contrast_buffers, 'mentalcoreGlobals.contrast_all_buffers', index=2 )
        cmds.connectControl( self.ray_differentials, 'mentalcoreGlobals.ray_differentials', index=2 )
        cmds.connectControl( self.finalgather_legacy, 'mentalcoreGlobals.finalgather_legacy', index=2 )
        cmds.connectControl( self.hair_mem_mode, 'mentalcoreGlobals.hair_mem_mode', index=2 )
        cmds.connectControl( self.hair_caps, 'mentalcoreGlobals.hair_caps', index=2 )
        cmds.connectControl( self.nested_assemblies, 'mentalcoreGlobals.nested_assemblies', index=2 )
        
        ## ------------------------------------------------------------------------
        ## IMPORTANCE SAMPLING
        ## ------------------------------------------------------------------------
        cmds.attrEnumOptionMenuGrp( self.light_is, e=True, at='mentalcoreGlobals.light_importance_sampling' )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.light_importance_sampling', self.update_light_is], protected=True, parent=self.light_is)
        
        cmds.connectControl( self.light_is_variance, 'mentalcoreGlobals.light_importance_sampling_variance', index=2 )
        cmds.connectControl( self.light_is_precomp, 'mentalcoreGlobals.light_importance_sampling_precomp', index=2 )
        cmds.connectControl( self.mis, 'mentalcoreGlobals.multiple_importance_sampling', index=2 )
        cmds.attrEnumOptionMenuGrp( self.finalgather_importance, e=True, at='mentalcoreGlobals.finalgather_importance' )
        
        ## ------------------------------------------------------------------------
        ## SHUTTER EFFICIENCY
        ## ------------------------------------------------------------------------
        cmds.attrEnumOptionMenuGrp( self.shutter_shape, e=True, at='mentalcoreGlobals.shutter_shape' )
        cmds.attrFieldSliderGrp( self.shutter_efficiency, e=True, at='mentalcoreGlobals.shutter_efficiency' )

        #Update Controls
        self.update_light_is()

    ## ------------------------------------------------------------------------
    ## UPDATE FUNCTIONS
    ## ------------------------------------------------------------------------
    def update_light_is(self):
        if cmds.getAttr('mentalcoreGlobals.light_importance_sampling') > 0:
            cmds.control( self.light_is_variance, e=True, en=True )
            cmds.control( self.light_is_precomp, e=True, en=True )
        else:
            cmds.control( self.light_is_variance, e=True, en=False )
            cmds.control( self.light_is_precomp, e=True, en=False )

