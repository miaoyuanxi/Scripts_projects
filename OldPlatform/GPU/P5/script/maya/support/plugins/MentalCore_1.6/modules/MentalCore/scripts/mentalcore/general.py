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
GENERAL_TAB = None


## ------------------------------------------------------------------------
## FUNCTIONS
## ------------------------------------------------------------------------			
def get_composite(rl):
    '''Returns the composite for the specified render layer'''
    if cmds.objExists(rl) and cmds.objExists('mentalcoreGlobals'):
        if cmds.attributeQuery( 'mc_composite', node=rl, exists=True ):
            comp_conn = cmds.listConnections('%s.mc_composite' % rl, type='core_composite')
            if comp_conn:
                return comp_conn[0]
    
    
## ------------------------------------------------------------------------
## GENERAL TAB
## ------------------------------------------------------------------------
class GeneralTab():
    '''Creates the general tab of the mentalcore globals'''
    def __init__(self):
        global GENERAL_TAB
        GENERAL_TAB = self
        
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
        ## OUTPUT
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Output', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #output mode
        self.out_mode = cmds.attrEnumOptionMenuGrp( l='Output Mode', ei=[(0, 'Preview'), (1, 'Preview Composite'), (2, 'All Passes') ] )
        #output mode
        self.preview_pass = cmds.attrNavigationControlGrp( l='Preview Pass' )
        #composite
        self.composite = mlib.NodeLinkWdget('Layer Composite', 'core_composite', 'core_composite')
        #self.composite = cmds.attrNavigationControlGrp( l='Layer Composite' )
        
        cmds.setParent(self.layout)

        
        ## ------------------------------------------------------------------------
        ## FILE OUTPUT
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='File Output', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #file mode
        self.file_mode = cmds.attrEnumOptionMenuGrp( l='File Mode', ei=[(0, 'Separate Files'),(1, 'Grouped EXR'), (2, 'Single EXR') ] )
        #fb mem mode
        self.fb_mode = cmds.attrEnumOptionMenuGrp( l='Framebuffer Mode', ei=[(0, 'Disabled'),(1, 'Memory Mapped'), (2, 'Cached') ] )
        #exr compression
        if maya2014:
            self.exr_comp = cmds.attrEnumOptionMenuGrp( l='Exr Compression', ei=[(0, 'None'),(1, 'Run Length Encoding'), (2, 'Zip (16 Scanlines)'), (5, 'ZipS (1 Scanline)'), (3, 'Piz-Based Wavelet Compression'), (4, 'Lossy 24Bit Float Compression') ] )
        else:
            self.exr_comp = cmds.attrEnumOptionMenuGrp( l='Exr Compression', ei=[(0, 'None'),(1, 'Run Length Encoding'), (2, 'Zip (16 Scanlines)'), (3, 'Piz-Based Wavelet Compression'), (4, 'Lossy 24Bit Float Compression') ] )
        #exr format
        self.exr_format = cmds.attrEnumOptionMenuGrp( l='Exr Format', ei=[(0, 'Scanline'),(1, 'Tiled')], vis=maya2013 )
        
        cmds.setParent(self.layout)
        
        
        ## ------------------------------------------------------------------------
        ## COLOUR MANAGEMENT
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Colour Management', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
        #enable cm
        self.enable_cm = cmds.checkBoxGrp( l1='Enable Colour Management' )
        #in profile
        self.in_profile = cmds.attrEnumOptionMenuGrp( l='In Profile', ei=[(0, 'Linear'),(1, 'sRGB'),(2, 'Rec. 709') ] )
        #out profile
        self.out_profile = cmds.attrEnumOptionMenuGrp( l='Out Profile', ei=[(0, 'Linear'),(1, 'sRGB'),(2, 'Rec. 709') ] )
        #preview profile
        self.preview_profile = cmds.attrEnumOptionMenuGrp( l='Preview Profile', ei=[(0, 'Linear'),(1, 'sRGB'),(2, 'Rec. 709') ] )
        
        cmds.setParent(self.layout)
        

        ## ------------------------------------------------------------------------
        ## UNIFIED SAMPLING
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Unified Sampling', w=430, collapsable=True, collapse=False, vis=not maya2014)
        cmds.columnLayout(rs=1, adj=True)
        
        #Unified Sampling
        self.unified = cmds.checkBoxGrp( l1='Unified Sampling' )
        #samples min
        self.u_min_samples = cmds.attrFieldSliderGrp( label='Min Samples', min=0, max=100, fmx=1000 ) 
        #samples max
        self.u_max_samples = cmds.attrFieldSliderGrp( label='Max Samples', min=0, max=100, fmx=1000 ) 
        #quality
        self.u_quality = cmds.attrFieldSliderGrp( label='Quality', min=0, max=2, fmx=1000 ) 
        #error cutoff
        self.u_error_cutoff = cmds.attrFieldSliderGrp( label='Error Cutoff', min=0, max=1 ) 
        #Samples per object
        self.u_per_object = cmds.checkBoxGrp( l1='Per Object Samples' )
        
        cmds.setParent(self.layout)
        
        
        ## ------------------------------------------------------------------------
        ## PROGRESSIVE RENDERING
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Progressive Rendering', w=430, collapsable=True, collapse=False, vis=not maya2014)
        cmds.columnLayout(rs=1, adj=True)
        
        #Progressive
        self.progressive = cmds.checkBoxGrp( l1='Progressive Rendering' )
        #subsample size
        self.p_subsamp_size = cmds.intFieldGrp( label='Subsampling Size' ) 
        #subsample mode
        self.p_subsamp_mode = cmds.attrEnumOptionMenuGrp( l='Subsampling Mode', ei=[(0, 'Sparse'),(1, 'Detail') ] )
        #subsample pattern
        self.p_subsamp_pattern = cmds.attrEnumOptionMenuGrp( l='Subsampling Pattern', ei=[(0, 'Linear'),(1, 'Scatter') ] )
        #max time
        self.p_max_time = cmds.floatFieldGrp( label='Max Time' ) 
        #min samples
        self.p_min_samples = cmds.attrFieldSliderGrp( label='Min Samples', min=0, max=100, fmx=1000 ) 
        #max samples
        self.p_max_samples = cmds.attrFieldSliderGrp( label='Max Samples', min=0, max=100, fmx=1000 ) 
        #error threshold
        self.p_error_threshold = cmds.floatFieldGrp( label='Error Threshold' ) 
        
        #Progressive Occlusion Cache
        self.p_ao_cache_frame = cmds.frameLayout(l='Progressive Occlusion Cache', w=430, collapsable=True, collapse=True)
        cmds.columnLayout(rs=1, adj=True)
        
        #AO Cache
        self.p_ao_cache = cmds.checkBoxGrp( l1='Progressive Occlusion Cache' )
        #cache points
        self.p_cache_points = cmds.intFieldGrp( label='Cache Points' ) 
        #cache rays
        self.p_cache_rays = cmds.intFieldGrp( label='Cache Rays' ) 
        #cache max frame
        self.p_cache_maxf = cmds.intFieldGrp( label='Cache Max Frame' ) 
        #cache exclude
        self.p_cache_exclude = cmds.intFieldGrp( label='Cache Exclude' ) 
        
        cmds.setParent(self.layout)
        
        
        ## ------------------------------------------------------------------------
        ## CAMERA
        ## ------------------------------------------------------------------------
        cmds.frameLayout(l='Camera', w=430, collapsable=True, collapse=False)
        cmds.columnLayout(rs=1, adj=True)
        
            
        self.lens = cmds.attrEnumOptionMenuGrp( l='Lens Type', ei=[(0, 'Standard'),(1, 'Spherical'), (2, 'Fish Eye') ] )
        #fish eye distortion
        self.fe_distortion = cmds.attrFieldSliderGrp( l='Distortion' )
        #fish eye mask
        self.fe_mask = cmds.checkBoxGrp( l1='Mask' )
        
        cmds.separator()
        
        #affect env
        self.affect_env = cmds.checkBoxGrp( l1='Affect Environment' )
        #exposure
        self.exposure = cmds.attrFieldSliderGrp( l='Exposure', min=0, max=4, fmx=1000 )
        #saturation
        self.saturation = cmds.attrFieldSliderGrp( l='Saturation', min=0, max=4, fmx=1000 )
        #filter amount
        self.filter_amount = cmds.attrFieldSliderGrp( l='Filter Amount', min=0, max=1 )
        #filter colour
        self.filter_colour = cmds.attrColorSliderGrp( l='Filter Colour' )
        #grade shader
        self.grade = mlib.NodeLinkWdget('Colour Grade', 'core_colour_grade', 'camera_grade')
                
        cmds.separator()
        
        #overlay
        self.overlay = cmds.attrColorSliderGrp( l='Overlay' )
        #overlay
        self.background = cmds.attrColorSliderGrp( l='Background' )
        
        cmds.separator()
        
        #photographic lens shader
        def create_ph_lens(node):
            cmds.setAttr('%s.film_iso' % node, 0)
            cmds.setAttr('%s.gamma' % node, 1)
        
        self.photographic_shader = mlib.NodeLinkWdget('Photographic Lens', 'mia_exposure_photographic', 'mia_exposure_photographic')
        self.photographic_shader.create_hook = create_ph_lens
        #dof lens shader
        self.dof_shader = mlib.NodeLinkWdget('Bokeh DOF Lens', 'mia_lens_bokeh', 'mia_lens_bokeh')
                
        
        ## TONEMAPPING ##
        cmds.frameLayout(l='Tonemapping', w=430, collapsable=True, collapse=True)
        cmds.columnLayout(rs=1, adj=True)
        
        #enable tonemap
        self.enable_tm = cmds.checkBoxGrp( l1='Enable Exponential Tonemapper' )
        #tm gain
        self.tm_gain = cmds.attrFieldSliderGrp( l='Gain', min=0, max=4, fmx=1000 )
        #tm exposure
        self.tm_exposure = cmds.attrFieldSliderGrp( l='Exposure', min=0, max=4, fmx=1000 )
        #tm blend
        self.tm_blend = cmds.attrFieldSliderGrp( l='Blend', min=0, max=1 )
        
        cmds.setParent('..')
        cmds.setParent('..')
        
        ## STEREO RENDERING ##
        cmds.frameLayout(l='Stereo Rendering', w=430, collapsable=True, collapse=True)
        cmds.columnLayout(rs=1, adj=True)
        
        #stereo rendering
        self.stereo_rendering = cmds.checkBoxGrp( l1='Stereo Rendering' )
        #stereo method
        self.stereo_method = cmds.attrEnumOptionMenuGrp( l='Stereo Method', ei=[(0, 'Toe In'),(1, 'Off Axis'),(2, 'Offset') ] )
        #eye separation
        self.eye_separation = cmds.floatFieldGrp( label='Eye Separation' )
        #parallax distance
        self.parallax_distance = cmds.floatFieldGrp( label='Parallax Distance' )
        
        cmds.setParent(self.layout)
        
        
        cmds.setUITemplate(popTemplate=True)
        
                            
    def connect_controls(self):
        ## ------------------------------------------------------------------------
        ## OUTPUT
        ## ------------------------------------------------------------------------
        cmds.attrEnumOptionMenuGrp( self.out_mode, e=True, at='mentalcoreGlobals.output_mode' )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.output_mode', self.update_output], protected=True, parent=self.out_mode)
        
        cmds.attrNavigationControlGrp( self.preview_pass, e=True, at='mentalcoreGlobals.preview_pass' )
        
        cmds.scriptJob(e=['renderLayerManagerChange', self.update_layer_composite], protected=True, parent=self.out_mode)
        self.update_layer_composite()
        #cmds.attrNavigationControlGrp( self.composite, e=True, at='mentalcoreGlobals.preview_composite' )

        ## ------------------------------------------------------------------------
        ## FILE OUTPUT
        ## ------------------------------------------------------------------------
        cmds.attrEnumOptionMenuGrp( self.file_mode, e=True, at='mentalcoreGlobals.file_mode' )
        cmds.attrEnumOptionMenuGrp( self.fb_mode, e=True, at='mentalcoreGlobals.fb_mem_mode' )
        cmds.attrEnumOptionMenuGrp( self.exr_comp, e=True, at='mentalcoreGlobals.exr_comp' )
        cmds.attrEnumOptionMenuGrp( self.exr_format, e=True, at='mentalcoreGlobals.exr_format' )
        
        ## ------------------------------------------------------------------------
        ## COLOUR MANAGEMENT
        ## ------------------------------------------------------------------------
        cmds.connectControl( self.enable_cm, 'mentalcoreGlobals.en_colour_management', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.en_colour_management', self.update_cm], protected=True, parent=self.enable_cm)
        
        cmds.attrEnumOptionMenuGrp( self.in_profile, e=True, at='mentalcoreGlobals.in_cprofile' )
        cmds.attrEnumOptionMenuGrp( self.out_profile, e=True, at='mentalcoreGlobals.out_cprofile' )
        cmds.attrEnumOptionMenuGrp( self.preview_profile, e=True, at='mentalcoreGlobals.preview_cprofile' )

        ## ------------------------------------------------------------------------
        ## CAMERA
        ## ------------------------------------------------------------------------
        cmds.attrEnumOptionMenuGrp( self.lens, e=True, at='mentalcoreLens.lens' )
        cmds.scriptJob(attributeChange=['mentalcoreLens.lens', self.update_lens], protected=True, parent=self.lens)
        
        cmds.attrFieldSliderGrp( self.fe_distortion, e=True, at='mentalcoreLens.fe_distortion' )
        cmds.connectControl( self.fe_mask, 'mentalcoreLens.fe_mask', index=2 )
        
        cmds.connectControl( self.affect_env, 'mentalcoreLens.affect_env', index=2 )
        cmds.attrFieldSliderGrp( self.exposure, e=True, at='mentalcoreLens.exposure' )
        cmds.attrFieldSliderGrp( self.saturation, e=True, at='mentalcoreLens.saturation' )
        cmds.attrFieldSliderGrp( self.filter_amount, e=True, at='mentalcoreLens.filter_amt' )
        cmds.attrColorSliderGrp( self.filter_colour, e=True, at='mentalcoreLens.filter_col' )
        
        self.grade.connect('mentalcoreLens.grade_shader')
        self.photographic_shader.connect('mentalcoreGlobals.photographic_shader')
        self.dof_shader.connect('mentalcoreGlobals.dof_shader')
                
        cmds.attrColorSliderGrp( self.overlay, e=True, at='mentalcoreLens.overlay' )
        cmds.attrColorSliderGrp( self.background, e=True, at='mentalcoreLens.background' )

        cmds.connectControl( self.enable_tm, 'mentalcoreLens.en_tonemap', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreLens.en_tonemap', self.update_tonemapping], protected=True, parent=self.enable_tm)
        
        cmds.attrFieldSliderGrp( self.tm_gain, e=True, at='mentalcoreLens.tm_gain' )
        cmds.attrFieldSliderGrp( self.tm_exposure, e=True, at='mentalcoreLens.tm_exposure' )
        cmds.attrFieldSliderGrp( self.tm_blend, e=True, at='mentalcoreLens.tm_blend' )

        cmds.connectControl( self.stereo_rendering, 'mentalcoreGlobals.en_stereo_rendering', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.en_stereo_rendering', self.update_stereo], protected=True, parent=self.stereo_rendering)
        
        cmds.attrEnumOptionMenuGrp( self.stereo_method, e=True, at='mentalcoreGlobals.stereo_method' )
        cmds.connectControl( self.eye_separation, 'mentalcoreGlobals.eye_separation', index=2 )
        cmds.connectControl( self.parallax_distance, 'mentalcoreGlobals.parallax_distance', index=2 )
        

        ## ------------------------------------------------------------------------
        ## UNIFIED SAMPLING
        ## ------------------------------------------------------------------------
        cmds.connectControl( self.unified, 'mentalcoreGlobals.unified_sampling', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.unified_sampling', self.update_unified], protected=True, parent=self.unified)
        
        cmds.attrFieldSliderGrp( self.u_min_samples, e=True, at='mentalcoreGlobals.samples_min' )
        cmds.attrFieldSliderGrp( self.u_max_samples, e=True, at='mentalcoreGlobals.samples_max' )
        cmds.attrFieldSliderGrp( self.u_quality, e=True, at='mentalcoreGlobals.samples_quality' )
        cmds.attrFieldSliderGrp( self.u_error_cutoff, e=True, at='mentalcoreGlobals.samples_error_cutoff' )
        cmds.connectControl( self.u_per_object, 'mentalcoreGlobals.samples_per_object', index=2 )
        
        
        ## ------------------------------------------------------------------------
        ## PROGRESSIVE RENDERING
        ## ------------------------------------------------------------------------
        cmds.connectControl( self.progressive, 'mentalcoreGlobals.progressive', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.progressive', self.update_progressive], protected=True, parent=self.progressive)
        
        cmds.connectControl( self.p_subsamp_size, 'mentalcoreGlobals.prog_subsamp_size', index=2 )
        cmds.attrEnumOptionMenuGrp( self.p_subsamp_mode, e=True, at='mentalcoreGlobals.prog_subsamp_mode' )
        cmds.attrEnumOptionMenuGrp( self.p_subsamp_pattern, e=True, at='mentalcoreGlobals.prog_subsamp_pattern' )
        cmds.attrFieldSliderGrp( self.p_min_samples, e=True, at='mentalcoreGlobals.prog_min_samples' )
        cmds.attrFieldSliderGrp( self.p_max_samples, e=True, at='mentalcoreGlobals.prog_max_samples' )
        cmds.connectControl( self.p_max_time, 'mentalcoreGlobals.prog_max_time', index=2 )
        cmds.connectControl( self.p_error_threshold, 'mentalcoreGlobals.prog_error_threshold', index=2 )
        
        cmds.connectControl( self.p_ao_cache, 'mentalcoreGlobals.prog_ao_cache', index=2 )
        cmds.scriptJob(attributeChange=['mentalcoreGlobals.prog_ao_cache', self.update_progressive], protected=True, parent=self.p_ao_cache)
        
        cmds.connectControl( self.p_cache_points, 'mentalcoreGlobals.prog_ao_cache_points', index=2 )
        cmds.connectControl( self.p_cache_rays, 'mentalcoreGlobals.prog_ao_cache_rays', index=2 )
        cmds.connectControl( self.p_cache_maxf, 'mentalcoreGlobals.prog_ao_cache_max_frame', index=2 )
        cmds.connectControl( self.p_cache_exclude, 'mentalcoreGlobals.prog_ao_cache_exclude', index=2 )
        

        # Update controls
        self.update_output()
        self.update_cm()
        self.update_lens()
        self.update_tonemapping()
        self.update_stereo()
        self.update_unified()
        self.update_progressive()

    ## ------------------------------------------------------------------------
    ## UPDATE FUNCTIONS
    ## ------------------------------------------------------------------------
    def update_output(self):
        if cmds.getAttr('mentalcoreGlobals.output_mode') == 0: #Preview
            cmds.attrNavigationControlGrp( self.preview_pass, e=True, vis=True )
            self.composite.set_visible(False)
        elif cmds.getAttr('mentalcoreGlobals.output_mode') == 1: #Composite
            cmds.attrNavigationControlGrp( self.preview_pass, e=True, vis=False )
            self.composite.set_visible(True)
        elif cmds.getAttr('mentalcoreGlobals.output_mode') == 2: #All Passes
            cmds.attrNavigationControlGrp( self.preview_pass, e=True, vis=False )
            self.composite.set_visible(False)
            
    def update_layer_composite(self):
        rl = cmds.editRenderLayerGlobals(q=True, crl=True)
        
        if not cmds.attributeQuery( 'mc_composite', node=rl, exists=True ):
            cmds.addAttr(rl, ln='mc_composite', at='message')
        
        if rl == 'defaultRenderLayer':
            self.composite.node_name = 'default_composite'
        else:
            self.composite.node_name = '%s_composite' % rl
        self.composite.connect('%s.mc_composite' % rl)
        #cmds.attrNavigationControlGrp( self.composite, e=True, at='%s.mc_composite' % rl )
    
    def update_cm(self):
        if cmds.getAttr('mentalcoreGlobals.en_colour_management'):
            cmds.control( self.in_profile, e=True, en=True )
            cmds.control( self.out_profile, e=True, en=True )
            cmds.control( self.preview_profile, e=True, en=True )
        else:
            cmds.control( self.in_profile, e=True, en=False )
            cmds.control( self.out_profile, e=True, en=False )
            cmds.control( self.preview_profile, e=True, en=False )	

    def update_lens(self):
        value = cmds.getAttr('mentalcoreLens.lens')
        if value > 0:
            cmds.setAttr('miDefaultOptions.scanline', 0)
        
        if value == 2:
            cmds.control( self.fe_distortion, e=True, vis=True )
            cmds.control( self.fe_mask, e=True, vis=True )
        else:
            cmds.control( self.fe_distortion, e=True, vis=False )
            cmds.control( self.fe_mask, e=True, vis=False )
            
    def update_tonemapping(self):
        if cmds.getAttr('mentalcoreLens.en_tonemap'):
            cmds.control( self.tm_gain, e=True, en=True )
            cmds.control( self.tm_exposure, e=True, en=True )
            cmds.control( self.tm_blend, e=True, en=True )
        else:
            cmds.control( self.tm_gain, e=True, en=False )
            cmds.control( self.tm_exposure, e=True, en=False )
            cmds.control( self.tm_blend, e=True, en=False )
        
            
    def update_stereo(self):
        if cmds.getAttr('mentalcoreGlobals.en_stereo_rendering'):
            cmds.control( self.stereo_method, e=True, en=True )
            cmds.control( self.eye_separation, e=True, en=True )
            cmds.control( self.parallax_distance, e=True, en=True )
        else:
            cmds.control( self.stereo_method, e=True, en=False )
            cmds.control( self.eye_separation, e=True, en=False )
            cmds.control( self.parallax_distance, e=True, en=False )
            
            
    def update_unified(self):	
        if cmds.getAttr('mentalcoreGlobals.unified_sampling'):
            cmds.control( self.u_min_samples, e=True, en=True )
            cmds.control( self.u_max_samples, e=True, en=True )
            cmds.control( self.u_quality, e=True, en=True )
            cmds.control( self.u_error_cutoff, e=True, en=True )
            cmds.control( self.u_per_object, e=True, en=True )
        
            cmds.control( self.p_min_samples, e=True, en=False )
            cmds.control( self.p_max_samples, e=True, en=False )
            cmds.control( self.p_error_threshold, e=True, en=False )
        else:
            cmds.control( self.u_min_samples, e=True, en=False )
            cmds.control( self.u_max_samples, e=True, en=False )
            cmds.control( self.u_quality, e=True, en=False )
            cmds.control( self.u_error_cutoff, e=True, en=False )
            cmds.control( self.u_per_object, e=True, en=False )
        
            if cmds.getAttr('mentalcoreGlobals.progressive'):
                cmds.control( self.p_min_samples, e=True, en=True )
                cmds.control( self.p_max_samples, e=True, en=True )
                cmds.control( self.p_error_threshold, e=True, en=True )
            
            
    def update_progressive(self):
        if cmds.getAttr('mentalcoreGlobals.progressive'):
            cmds.control( self.p_subsamp_size, e=True, en=True )
            cmds.control( self.p_subsamp_mode, e=True, en=True )
            cmds.control( self.p_subsamp_pattern, e=True, en=True )
            cmds.control( self.p_max_time, e=True, en=True )
            cmds.control( self.p_ao_cache, e=True, en=True )
            cmds.control( self.p_ao_cache_frame, e=True, en=True )
            
            if not cmds.getAttr('mentalcoreGlobals.unified_sampling'):
                cmds.control( self.p_min_samples, e=True, en=True )
                cmds.control( self.p_max_samples, e=True, en=True )
                cmds.control( self.p_error_threshold, e=True, en=True )
                
            if cmds.getAttr('mentalcoreGlobals.prog_ao_cache'):
                cmds.control( self.p_cache_points, e=True, en=True )
                cmds.control( self.p_cache_rays, e=True, en=True )
                cmds.control( self.p_cache_maxf, e=True, en=True )
                cmds.control( self.p_cache_exclude, e=True, en=True )
            else:
                cmds.control( self.p_cache_points, e=True, en=False )
                cmds.control( self.p_cache_rays, e=True, en=False )
                cmds.control( self.p_cache_maxf, e=True, en=False )
                cmds.control( self.p_cache_exclude, e=True, en=False )
                
        else:
            cmds.control( self.p_subsamp_size, e=True, en=False )
            cmds.control( self.p_subsamp_mode, e=True, en=False )
            cmds.control( self.p_subsamp_pattern, e=True, en=False )
            cmds.control( self.p_max_time, e=True, en=False )
            cmds.control( self.p_min_samples, e=True, en=False )
            cmds.control( self.p_max_samples, e=True, en=False )
            cmds.control( self.p_error_threshold, e=True, en=False )
            
            cmds.control( self.p_ao_cache, e=True, en=False )
            cmds.control( self.p_cache_points, e=True, en=False )
            cmds.control( self.p_cache_rays, e=True, en=False )
            cmds.control( self.p_cache_maxf, e=True, en=False )
            cmds.control( self.p_cache_exclude, e=True, en=False )
            
            cmds.control( self.p_ao_cache_frame, e=True, en=False )
