#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com

## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
from functools import partial
import webbrowser

import maya.cmds as cmds
import maya.mel as mel

from mentalcore import mlib


## ------------------------------------------------------------------------
## GLOBAL VARIABLES
## ------------------------------------------------------------------------
OPTIONS_TAB = None


## ------------------------------------------------------------------------
## OPTIONS TAB
## ------------------------------------------------------------------------
class OptionsTab():
    def __init__(self):
        global OPTIONS_TAB
        OPTIONS_TAB = self
        
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
        ## ENVIRONMENT
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Environment', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #core environment
        self.env = mlib.NodeLinkWdget('Core Environment', 'core_environment', 'core_environment')
        
        cmds.setParent(self.layout)
        
        
        ## ------------------------------------------------------------------------
        ## IMAGE BASED LIGHTING
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Image Based Lighting', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #ibl mode
        self.ibl_mode = cmds.attrEnumOptionMenuGrp( l='Mode', ei=[(0, 'Off'),(1, 'Automatic'),(2, 'Approximate'),(3, 'Light') ] )
        #quality
        self.ibl_quality = cmds.attrFieldSliderGrp( label='Quality', min=0.0, max=1.0, fmx=1000 )
        #ibl scale
        self.ibl_scale = cmds.attrColorSliderGrp( l='Scale', sb=False )
        #shadows
        self.ibl_shadows = cmds.attrEnumOptionMenuGrp( l='Shadows', ei=[(0, 'Off'),(1, 'Solid'),(2, 'Transparent') ] )
    
        cmds.frameLayout(l='IBL Optimization', w=430, collapsable=True, collapse=True)
        cmds.columnLayout(rs=1, adj=True)
                
        #approx add samples
        self.ibl_approx_split = cmds.intFieldGrp( label='Approx Oversampling' )
        #approx vis rays
        self.ibl_approx_vis_rays = cmds.intFieldGrp( label='Approx Visibility Rays' )
        
        self.ibl_approx_sep = cmds.separator()
        
        #ibl env resolution
        self.ibl_env_res = cmds.intFieldGrp( label='Resolution' )
        #ibl env shadersamples
        self.ibl_env_shader_samples = cmds.intFieldGrp( label='Shader Samples' )
        #ibl env cache
        self.ibl_env_cache = cmds.checkBoxGrp( l1='Enable Environment Cache' )
        
        cmds.setParent(self.layout)
        
        
        ## ------------------------------------------------------------------------
        ## GLOBAL ENVIRONMENT LIGHT
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Global Environment Light', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #enable env light
        self.enable_env_light = cmds.checkBoxGrp( l1='Enable Global Environment Light' )
        #intensity
        self.env_intensity = cmds.attrFieldSliderGrp( label='Intensity', min=0.0, max=4.0, fmx=10000 )
        #blur
        self.env_blur = cmds.attrFieldSliderGrp( label='Blur', min=0.0, max=10.0, fmx=10000 )
        #blur resolution
        self.env_blur_res = cmds.attrFieldSliderGrp( label='Blur Resolution', min=0.0, max=1000.0, fmx=100000 )
        
        #enable flood colour
        self.env_flood = cmds.checkBoxGrp( l1='Enable Flood Colour' )
        #flood colour
        self.env_flood_colour = cmds.attrColorSliderGrp( l='Flood Colour', sb=False )
        
        cmds.setParent(self.layout)
        
        
        ## ------------------------------------------------------------------------
        ## AMBIENT OCCLUSION
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Ambient Occlusion', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #enable ao
        self.enable_ao = cmds.checkBoxGrp( l1='Enable Ambient Occlusion' )
                
        self.ao_non_gpu_layout = cmds.columnLayout(rs=1, adj=True)
                
        #ao colour
        self.ao_colour = cmds.attrColorSliderGrp( l='Colour', sb=False )
        #samples
        self.ao_samples = cmds.intFieldGrp( label='Samples' )
        #spread
        self.ao_spread = cmds.attrFieldSliderGrp( label='Spread', min=0.0, max=100.0 )
        #near clip
        self.ao_near = cmds.attrFieldSliderGrp( label='Min Distance', min=0.0, max=100.0, fmx=1000000 )
                
        cmds.setParent('..')
                
        #far clip
        self.ao_far = cmds.attrFieldSliderGrp( label='Max Distance', min=0.0, max=100.0, fmx=1000000 )
        #falloff
        self.ao_falloff = cmds.floatFieldGrp( label='Falloff' )
        
        self.ao_contib_layout = cmds.columnLayout(rs=1, adj=True)
        cmds.separator()
        
        #ambient occlusion
        self.ao_amb_occ = cmds.attrFieldSliderGrp( label='Ambient Occlusion', min=0.0, max=1.0 )
        #direct occlusion
        self.ao_direct_occ = cmds.attrFieldSliderGrp( label='Direct Occlusion', min=0.0, max=1.0 )
        
        cmds.setParent('..')
                
        self.ao_gpu_layout = cmds.columnLayout(rs=1, adj=True, vis=False)
        cmds.separator()
                
        #Override gpu ao quality
        self.ao_gpu_override_quality = cmds.checkBoxGrp( l1='Override GPU AO Quality' )
        # GPU Passes
        self.ao_gpu_passes = cmds.intFieldGrp( label='Passes' )
        # GPU Rays
        self.ao_gpu_rays = cmds.intFieldGrp( label='Rays' )
                
        cmds.setParent('..')
                
        ## ADVANCED OCCLUSION ##
        self.adv_ao_frame = cmds.frameLayout(l='Advanced Occlusion', w=430, collapsable=True, collapse=True)
        cmds.columnLayout(rs=1, adj=True)
        
        #ao mode
        if maya2014:
            self.ao_mode = cmds.attrEnumOptionMenuGrp( l='Mode', ei=[(0, 'MentalCore'),(1, 'Mentalray Built-in'),(2, 'Mentalray GPU') ] )
        else:
            self.ao_mode = cmds.attrEnumOptionMenuGrp( l='Mode', ei=[(0, 'MentalCore'),(1, 'Mentalray Built-in') ] )
        
            
        self.ao_adv_mc_layout = cmds.columnLayout(rs=1, adj=True)
                
        #use transparency
        self.ao_trans = cmds.checkBoxGrp( l1='Occlusion Transparency' )
        
        cmds.separator()
        
        #visible in Indirect
        self.ao_vis_indirect = cmds.checkBoxGrp( l1='Visible in Indirect' )
        #visible in Reflection
        self.ao_vis_refl = cmds.checkBoxGrp( l1='Visible in Reflection' )
        #visible in Refreaction
        self.ao_vis_refr = cmds.checkBoxGrp( l1='Visible in Refraction' )
        #visible in Transparency
        self.ao_vis_trans = cmds.checkBoxGrp( l1='Visible in Transparency' )
        
        cmds.separator()
        
        #include/exclude id
        self.ao_inclexcl_id = cmds.intFieldGrp( label='Include/Exclude ID' )
        #non self id
        self.ao_nonself_id = cmds.intFieldGrp( label='Non-self ID' )
        
        cmds.setParent('..')
        
        ## AO TRACE FLAGS ##
        self.ao_flags_frame = cmds.frameLayout(l='Occlusion Trace Flags', w=430, collapsable=True, collapse=True)
        cmds.columnLayout(rs=1, adj=True)
        
        cmds.text('Ambient Occlusion will only hit objects with the following rendering flags set:', h=22)
        
        self.ao_flag_visible = cmds.checkBoxGrp( l1='Primary Visibility' )
        self.ao_flag_shadow = cmds.checkBoxGrp( l1='Casts Shadows' )
        self.ao_flag_reflect = cmds.checkBoxGrp( l1='Visible in Reflections' )
        self.ao_flag_refract = cmds.checkBoxGrp( l1='Visible in Refractions' )
        self.ao_flag_transp = cmds.checkBoxGrp( l1='Visible in Transparency' )
        self.ao_flag_caustic = cmds.checkBoxGrp( l1='Caustics Enabled' )
        self.ao_flag_globillum = cmds.checkBoxGrp( l1='Global Illumination Enabled' )
        self.ao_flag_finalgather = cmds.checkBoxGrp( l1='Finalgather Enabled' )
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        ## OCCLUSION CACHING ##
        if not maya2014:
            self.cache_ao_frame = cmds.frameLayout(l='Occlusion Caching', w=430, collapsable=True, collapse=True, vis=not maya2014)
            cmds.columnLayout(rs=1, adj=True)
            
            #enable caching
            self.ao_caching = cmds.checkBoxGrp( l1='Enable Caching' )
            #cache density
            self.ao_cache_density = cmds.floatFieldGrp( label='Cache Density' )
            #cache points
            self.ao_cache_points = cmds.intFieldGrp( label='Cache Points' )

        cmds.setParent(self.layout)
        
        
        ## ------------------------------------------------------------------------
        ## INDIRECT
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Indirect Illumination', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        self.indirect_scale = cmds.attrFieldSliderGrp( label='Indirect Scale', min=0.0, max=4.0, fmx=1000 )
        self.indirect_occlusion = cmds.attrFieldSliderGrp( label='Indirect Occlusion', min=0.0, max=1.0 )
        
        cmds.setParent(self.layout)
        
        
        ## ------------------------------------------------------------------------
        ## LIGHT BLOOM
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Light Bloom', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #enable bloom
        self.enable_bloom = cmds.checkBoxGrp( l1='Enable Light Bloom' )
        #bloom source
        self.bloom_source = cmds.attrEnumOptionMenuGrp( l='Source', ei=[(0, 'Beauty'),(1, 'Specular'),(2, 'Reflections'),(2, 'Incandesence'),(4, 'All Highlights') ] )
        #bloom scale
        self.bloom_scale = cmds.attrFieldSliderGrp( l='Scale', min=0.0, max=4.0, fmx=1000 )
        #bloom threshold
        self.bloom_threshold = cmds.attrFieldSliderGrp( l='Threshold', min=0.0, max=4.0, fmx=1000 )
        #bloom saturation
        self.bloom_saturation = cmds.attrFieldSliderGrp( l='Saturation', min=0.0, max=4.0, fmx=1000 )
        
        cmds.setParent(self.layout)
        
        cmds.setUITemplate(popTemplate=True)
        
    
    def connect_controls(self):
        #check maya version
        maya_ver = int(cmds.about(f=True))
        
        maya2013 = False
        if maya_ver >= 2013:
            maya2013 = True
        
        maya2014 = False
        if maya_ver >= 2014:
            maya2014 = True
        
        ## ------------------------------------------------------------------------
        ## ENVIRONMENT
        ## ------------------------------------------------------------------------
        self.env.connect('mentalcoreGlobals.env_shader')
        
        ## ------------------------------------------------------------------------
        ## ENVIRONMENT LIGHT
        ## ------------------------------------------------------------------------
        cmds.connectControl( self.enable_env_light, 'mentalcoreGlobals.en_envl', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.en_envl', self.update_env_light], protected=True, parent=self.enable_env_light)
        
        cmds.attrFieldSliderGrp( self.env_intensity, e=True, at='mentalcoreGlobals.envl_scale' )
        cmds.attrFieldSliderGrp( self.env_blur, e=True, at='mentalcoreGlobals.envl_blur' )
        cmds.attrFieldSliderGrp( self.env_blur_res, e=True, at='mentalcoreGlobals.envl_blur_res' )
        cmds.connectControl( self.env_flood, 'mentalcoreGlobals.envl_en_flood_colour', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.envl_en_flood_colour', self.update_env_light], protected=True, parent=self.env_flood)
        
        cmds.attrColorSliderGrp( self.env_flood_colour, e=True, at='mentalcoreGlobals.envl_flood_colour' )

        ## ------------------------------------------------------------------------
        ## IMAGE BASED LIGHTING
        ## ------------------------------------------------------------------------
        cmds.attrEnumOptionMenuGrp( self.ibl_mode, e=True, at='mentalcoreGlobals.ibl_mode' )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.ibl_mode', self.update_ibl], protected=True, parent=self.ibl_mode)
        
        cmds.attrFieldSliderGrp( self.ibl_quality, e=True, at='mentalcoreGlobals.ibl_quality' )
        cmds.attrEnumOptionMenuGrp( self.ibl_shadows, e=True, at='mentalcoreGlobals.ibl_shadows' )
        cmds.attrColorSliderGrp( self.ibl_scale, e=True, at='mentalcoreGlobals.ibl_scale' )
        cmds.connectControl( self.ibl_approx_split, 'mentalcoreGlobals.ibl_approx_split', index=2 )
        cmds.connectControl( self.ibl_approx_vis_rays, 'mentalcoreGlobals.ibl_approx_split_vis', index=2 )
        
        cmds.connectControl( self.ibl_env_cache, 'mentalcoreGlobals.ibl_env_cache', index=2 )
        cmds.connectControl( self.ibl_env_res, 'mentalcoreGlobals.ibl_env_res', index=2 )
        cmds.connectControl( self.ibl_env_shader_samples, 'mentalcoreGlobals.ibl_env_shader_samples', index=2 )
        
        ## ------------------------------------------------------------------------
        ## AMBIENT OCCLUSION
        ## ------------------------------------------------------------------------
        cmds.connectControl( self.enable_ao, 'mentalcoreGlobals.en_ao', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.en_ao', self.update_occlusion], protected=True, parent=self.enable_ao)
        
        cmds.attrColorSliderGrp( self.ao_colour, e=True, at='mentalcoreGlobals.ao_colour' )
        cmds.connectControl( self.ao_samples, 'mentalcoreGlobals.ao_samples', index=2 )
        cmds.attrFieldSliderGrp( self.ao_spread, e=True, at='mentalcoreGlobals.ao_spread' )
        cmds.attrFieldSliderGrp( self.ao_near, e=True, at='mentalcoreGlobals.ao_near_clip' )
        cmds.attrFieldSliderGrp( self.ao_far, e=True, at='mentalcoreGlobals.ao_far_clip' )
        cmds.connectControl( self.ao_falloff, 'mentalcoreGlobals.ao_falloff', index=2 )
                
        cmds.attrFieldSliderGrp( self.ao_amb_occ, e=True, at='mentalcoreGlobals.ao_amt_amb_occ' )
        cmds.attrFieldSliderGrp( self.ao_direct_occ, e=True, at='mentalcoreGlobals.ao_amt_direct_occ' )
    
        cmds.connectControl( self.ao_gpu_override_quality, 'mentalcoreGlobals.ao_gpu_override_quality', index=2 )
        cmds.connectControl( self.ao_gpu_passes, 'mentalcoreGlobals.ao_gpu_passes', index=2 )
        cmds.connectControl( self.ao_gpu_rays, 'mentalcoreGlobals.ao_gpu_rays', index=2 )
        
        ## ADVANCED OCCLUSION ##
        cmds.attrEnumOptionMenuGrp( self.ao_mode, e=True, at='mentalcoreGlobals.ao_mode' )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.ao_mode', self.update_occlusion], protected=True, parent=self.ao_mode)
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.ao_mode', self.check_gpu_ao], protected=True, parent=self.ao_mode)
        
        cmds.connectControl( self.ao_trans, 'mentalcoreGlobals.ao_opacity', index=2 )
                
        cmds.connectControl( self.ao_vis_indirect, 'mentalcoreGlobals.ao_vis_indirect', index=2 )
        cmds.connectControl( self.ao_vis_refl, 'mentalcoreGlobals.ao_vis_refl', index=2 )
        cmds.connectControl( self.ao_vis_refr, 'mentalcoreGlobals.ao_vis_refr', index=2 )
        cmds.connectControl( self.ao_vis_trans, 'mentalcoreGlobals.ao_vis_trans', index=2 )
                
        #include/exclude id
        cmds.connectControl( self.ao_inclexcl_id, 'mentalcoreGlobals.ao_inclexcl_id', index=2 )
        cmds.connectControl( self.ao_nonself_id, 'mentalcoreGlobals.ao_nonself_id', index=2 )
        
        #AO Trace flags
        cmds.connectControl( self.ao_flag_visible, 'mentalcoreGlobals.ao_flag_visible', index=2 )
        cmds.connectControl( self.ao_flag_shadow, 'mentalcoreGlobals.ao_flag_shadow', index=2 )
        cmds.connectControl( self.ao_flag_reflect, 'mentalcoreGlobals.ao_flag_reflect', index=2 )
        cmds.connectControl( self.ao_flag_refract, 'mentalcoreGlobals.ao_flag_refract', index=2 )
        cmds.connectControl( self.ao_flag_transp, 'mentalcoreGlobals.ao_flag_transp', index=2 )
        cmds.connectControl( self.ao_flag_caustic, 'mentalcoreGlobals.ao_flag_caustic', index=2 )
        cmds.connectControl( self.ao_flag_globillum, 'mentalcoreGlobals.ao_flag_globillum', index=2 )
        cmds.connectControl( self.ao_flag_finalgather, 'mentalcoreGlobals.ao_flag_finalgather', index=2 )

        ## OCCLUSION CACHING ##
        if not maya2014:
            cmds.connectControl( self.ao_caching, 'mentalcoreGlobals.ao_caching', index=2 )
            cmds.scriptJob(attributeChange=['mentalcoreGlobals.ao_caching', self.update_occlusion], protected=True, parent=self.ao_caching)
            
            cmds.connectControl( self.ao_cache_density, 'mentalcoreGlobals.ao_cache_density', index=2 )
            cmds.connectControl( self.ao_cache_points, 'mentalcoreGlobals.ao_cache_points', index=2 )
        
        ## ------------------------------------------------------------------------
        ## INDIRECT
        ## ------------------------------------------------------------------------
        cmds.attrFieldSliderGrp( self.indirect_scale, e=True, at='mentalcoreGlobals.indirect_scale' )
        cmds.attrFieldSliderGrp( self.indirect_occlusion, e=True, at='mentalcoreGlobals.indirect_occlusion' )
        
        ## ------------------------------------------------------------------------
        ## LIGHT BLOOM
        ## ------------------------------------------------------------------------
        cmds.connectControl( self.enable_bloom, 'mentalcoreGlobals.en_bloom', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.en_bloom', self.update_bloom], protected=True, parent=self.enable_bloom)
        
        cmds.attrEnumOptionMenuGrp( self.bloom_source, e=True, at='mentalcoreGlobals.bloom_source' )
        cmds.attrFieldSliderGrp( self.bloom_scale, e=True, at='mentalcoreGlobals.bloom_scale' )
        cmds.attrFieldSliderGrp( self.bloom_threshold, e=True, at='mentalcoreGlobals.bloom_threshold' )
        cmds.attrFieldSliderGrp( self.bloom_saturation, e=True, at='mentalcoreGlobals.bloom_saturation' )
        
        #Update Controls
        self.update_env_light()
        self.update_ibl()
        self.update_occlusion()
        self.update_bloom()
        self.check_gpu_ao()
        
    ## ------------------------------------------------------------------------
    ## UPDATE FUNCTIONS
    ## ------------------------------------------------------------------------
    def update_ibl(self):
        if cmds.getAttr('mentalcoreGlobals.ibl_mode') > 0:
            cmds.control( self.ibl_quality, e=True, en=True )
            cmds.control( self.ibl_shadows, e=True, en=True )
            cmds.control( self.ibl_scale, e=True, en=True )
            cmds.control( self.ibl_approx_split, e=True, en=True )
            cmds.control( self.ibl_approx_vis_rays, e=True, en=True )
            cmds.control( self.ibl_env_cache, e=True, en=True )
            cmds.control( self.ibl_env_res, e=True, en=True )
            cmds.control( self.ibl_env_shader_samples, e=True, en=True )
        else:
            cmds.control( self.ibl_quality, e=True, en=False )
            cmds.control( self.ibl_shadows, e=True, en=False )
            cmds.control( self.ibl_scale, e=True, en=False )
            cmds.control( self.ibl_approx_split, e=True, en=False )
            cmds.control( self.ibl_approx_vis_rays, e=True, en=False )
            cmds.control( self.ibl_env_cache, e=True, en=False )
            cmds.control( self.ibl_env_res, e=True, en=False )
            cmds.control( self.ibl_env_shader_samples, e=True, en=False )

        if cmds.getAttr('mentalcoreGlobals.ibl_mode') == 2:
            cmds.control( self.ibl_approx_split, e=True, vis=True )
            cmds.control( self.ibl_approx_vis_rays, e=True, vis=True )
            cmds.separator( self.ibl_approx_sep, e=True, vis=True )
        else:
            cmds.control( self.ibl_approx_split, e=True, vis=False )
            cmds.control( self.ibl_approx_vis_rays, e=True, vis=False )
            cmds.separator( self.ibl_approx_sep, e=True, vis=False )
        
        
    def update_env_light(self):
        if cmds.getAttr('mentalcoreGlobals.en_envl'):
            cmds.control( self.env_intensity, e=True, en=True )
            cmds.control( self.env_blur, e=True, en=True )
            cmds.control( self.env_blur_res, e=True, en=True )
            cmds.control( self.env_flood, e=True, en=True )
            
            if cmds.getAttr('mentalcoreGlobals.envl_en_flood_colour'):
                cmds.control( self.env_flood_colour, e=True, en=True )
            else:
                cmds.control( self.env_flood_colour, e=True, en=False )
        else:
            cmds.control( self.env_intensity, e=True, en=False )
            cmds.control( self.env_blur, e=True, en=False )
            cmds.control( self.env_blur_res, e=True, en=False )
            cmds.control( self.env_flood, e=True, en=False )
            cmds.control( self.env_flood_colour, e=True, en=False )	
    
        
    def update_occlusion(self):
        #check maya version
        maya_ver = int(cmds.about(f=True))
            
        maya2013 = False
        if maya_ver >= 2013:
            maya2013 = True
        
        maya2014 = False
        if maya_ver >= 2014:
            maya2014 = True
    
        if cmds.getAttr('mentalcoreGlobals.en_ao'):
            cmds.control( self.ao_colour, e=True, en=True )
            cmds.control( self.ao_samples, e=True, en=True )
            cmds.control( self.ao_spread, e=True, en=True )
            cmds.control( self.ao_near, e=True, en=True )
            cmds.control( self.ao_far, e=True, en=True )
            cmds.control( self.ao_falloff, e=True, en=True )
            cmds.control( self.ao_amb_occ, e=True, en=True )
            cmds.control( self.ao_direct_occ, e=True, en=True )
            cmds.control( self.ao_mode, e=True, en=True )
            cmds.control( self.ao_trans, e=True, en=True )
            cmds.control( self.ao_vis_indirect, e=True, en=True )
            cmds.control( self.ao_vis_refl, e=True, en=True )
            cmds.control( self.ao_vis_refr, e=True, en=True )
            cmds.control( self.ao_vis_trans, e=True, en=True )
            cmds.control( self.ao_inclexcl_id, e=True, en=True )
            cmds.control( self.ao_nonself_id, e=True, en=True )
            
            cmds.control( self.adv_ao_frame, e=True, en=True )

            if not maya2014:
                cmds.control( self.cache_ao_frame, e=True, en=True )
            
            if cmds.getAttr('mentalcoreGlobals.ao_mode') == 0:
                # MentalCore AO
                cmds.columnLayout( self.ao_non_gpu_layout, e=True, vis=True )
                
                cmds.control( self.ao_near, e=True, vis=True )
                
                cmds.columnLayout( self.ao_contib_layout, e=True, vis=True )
                
                #cmds.columnLayout( self.ao_gpu_layout, e=True, vis=False )
                
                cmds.columnLayout( self.ao_adv_mc_layout, e=True, vis=True )
                
                cmds.control( self.ao_flags_frame, e=True, vis=True )
                
                if not maya2014:
                    cmds.control( self.cache_ao_frame, e=True, vis=False )
            
            elif cmds.getAttr('mentalcoreGlobals.ao_mode') == 1:
                # MI AO
                cmds.columnLayout( self.ao_non_gpu_layout, e=True, vis=True )

                cmds.control( self.ao_near, e=True, vis=False )
                
                cmds.columnLayout( self.ao_contib_layout, e=True, vis=True )
                
                #cmds.columnLayout( self.ao_gpu_layout, e=True, vis=False )
                
                cmds.columnLayout( self.ao_adv_mc_layout, e=True, vis=False )
                
                if maya2013:
                    cmds.control( self.ao_flags_frame, e=True, vis=True )
                else:
                    cmds.control( self.ao_flags_frame, e=True, vis=False )
                
                if not maya2014:
                    cmds.control( self.cache_ao_frame, e=True, vis=True )
                    if cmds.getAttr('mentalcoreGlobals.ao_caching'):
                        cmds.control( self.ao_cache_density, e=True, en=True )
                        cmds.control( self.ao_cache_points, e=True, en=True )
                    else:
                        cmds.control( self.ao_cache_density, e=True, en=False )
                        cmds.control( self.ao_cache_points, e=True, en=False )
            
            elif cmds.getAttr('mentalcoreGlobals.ao_mode') == 2:
                # GPU AO
                cmds.columnLayout( self.ao_non_gpu_layout, e=True, vis=False )
                
                cmds.columnLayout( self.ao_contib_layout, e=True, vis=False )
                
                #cmds.columnLayout( self.ao_gpu_layout, e=True, vis=True )
                
                cmds.columnLayout( self.ao_adv_mc_layout, e=True, vis=False )
                    
                cmds.control( self.ao_flags_frame, e=True, vis=False )
                
                
        else:
            cmds.control( self.ao_colour, e=True, en=False )
            cmds.control( self.ao_samples, e=True, en=False )
            cmds.control( self.ao_spread, e=True, en=False )
            cmds.control( self.ao_far, e=True, en=False )
            cmds.control( self.ao_falloff, e=True, en=False )
            cmds.control( self.ao_amb_occ, e=True, en=False )
            cmds.control( self.ao_direct_occ, e=True, en=False )
            cmds.control( self.ao_mode, e=True, en=False )
            cmds.control( self.ao_near, e=True, en=False )
            cmds.control( self.ao_trans, e=True, en=False )
            cmds.control( self.ao_vis_indirect, e=True, en=False )
            cmds.control( self.ao_vis_refl, e=True, en=False )
            cmds.control( self.ao_vis_refr, e=True, en=False )
            cmds.control( self.ao_vis_trans, e=True, en=False )
            cmds.control( self.ao_inclexcl_id, e=True, en=False )
            cmds.control( self.ao_nonself_id, e=True, en=False )
            
            if not maya2014:
                cmds.control( self.cache_ao_frame, e=True, en=False )
                cmds.control( self.ao_caching, e=True, en=False )
                cmds.control( self.ao_cache_density, e=True, en=False )
                cmds.control( self.ao_cache_points, e=True, en=False )
            
            cmds.control( self.adv_ao_frame, e=True, en=False )
            
    def check_gpu_ao(self):
        # Check if GPU AO has been enabled
        if cmds.getAttr('mentalcoreGlobals.ao_mode') == 2:
            # Check this message hasnt been displayed before
            if not cmds.optionVar( q='MC_GPUAO_INFO' ):
                # Set option var so we dont see this in future
                cmds.optionVar( iv=('MC_GPUAO_INFO', 1) )                
                # Display confirm dialog
                result = cmds.confirmDialog( title='GPU AO Warning', message='GPU Ambient Occlusion requires additional setup to work correctly.\nPlease see the documentation for more information', button=['Open Documentation', 'Dismiss'], icon='warning')
                if result == 'Open Documentation':
                    # Open docs
                    webbrowser.open("http://core-cg.com/documentation/gpu_ao.html")                    
                
            
    def update_bloom(self):
        if cmds.getAttr('mentalcoreGlobals.en_bloom'):
            cmds.control( self.bloom_source, e=True, en=True )
            cmds.control( self.bloom_scale, e=True, en=True )
            cmds.control( self.bloom_threshold, e=True, en=True )
            cmds.control( self.bloom_saturation, e=True, en=True )
        else:
            cmds.control( self.bloom_source, e=True, en=False )
            cmds.control( self.bloom_scale, e=True, en=False )
            cmds.control( self.bloom_threshold, e=True, en=False )
            cmds.control( self.bloom_saturation, e=True, en=False )
