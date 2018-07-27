import pymel.core as pm
import mtoa.utils as utils
import mtoa.ui.ae.utils as aeUtils
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate


class AEaiSkinSssTemplate(ShaderAETemplate):

    def setup(self):
        self.addSwatch()
        
        self.beginScrollLayout()
        
        self.addCustom('message', 'AEshaderTypeNew', 'AEshaderTypeReplace')

        self.beginLayout("Matte", collapse=True)
        self.addControl("aiEnableMatte", label="Enable Matte")
        self.addControl("aiMatteColor", label="Matte Color")
        self.addControl("aiMatteColorA", label="Matte Opacity")
        self.endLayout()
        
        self.beginLayout("Diffuse", collapse=False)     
        self.addControl("diffuse_color",  label="Color", annotation="Diffuse Color")
        self.addControl("diffuse_weight", label="Weight")
        self.addControl("diffuse_roughness", label="Roughness")
        self.endLayout()
        
        self.beginLayout("SSS", collapse=False)
        self.addControl("sss_weight", label="SSS Weight")
        self.endLayout()

        self.beginLayout("Shallow Scatter", collapse=False)
        self.addControl("shallow_scatter_color", label="Color")
        self.addControl("shallow_scatter_weight", label="Weight")
        self.addControl("shallow_scatter_radius", label="Radius")
        self.endLayout()
        
        self.beginLayout("Mid Scatter", collapse=False)
        self.addControl("mid_scatter_color", label="Color")
        self.addControl("mid_scatter_weight", label="Weight")
        self.addControl("mid_scatter_radius", label="Radius")
        self.endLayout()
        
        self.beginLayout("Deep Scatter", collapse=False)
        self.addControl("deep_scatter_color", label="Color")
        self.addControl("deep_scatter_weight", label="Weight")
        self.addControl("deep_scatter_radius", label="Radius")
        self.endLayout()
        
        self.beginLayout("Primary Reflection", collapse=False)
        self.addControl("primary_reflection_color", label="Color")
        self.addControl("primary_reflection_weight", label="Weight")
        self.addControl("primary_reflection_roughness", label="Roughness")
        self.addControl("primary_reflection_specular_weight", label="Specular Weight")
        self.addControl("primary_reflection_reflection_weight", label="Reflection Weight")
        self.addControl("primary_reflection_enable_fresnel_falloff", label="Enable Fresnel Falloff")
        self.addControl("primary_reflection_fresnel_coefficient", label="Reflectance at normal incidence")
        self.endLayout()
        
        self.beginLayout("Secondary Reflection", collapse=False)
        self.addControl("secondary_reflection_color", label="Color")
        self.addControl("secondary_reflection_weight", label="Weight")
        self.addControl("secondary_reflection_roughness", label="Roughness")
        self.addControl("secondary_reflection_specular_weight", label="Specular Weight")
        self.addControl("secondary_reflection_reflection_weight", label="Reflection Weight")
        self.addControl("secondary_reflection_enable_fresnel_falloff", label="Enable Fresnel Falloff")
        self.addControl("secondary_reflection_fresnel_coefficient", label="Reflectance at normal incidence")
        self.endLayout()
        
        self.beginLayout("Options", collapse=True)
        self.addControl("global_sss_radius_multiplier", label="SSS Radius Multiplier")
        self.addControl("use_screen_compositing_for_colors", label="Use Screen Compositing")
        self.addControl("sample_sss_only_in_gi_rays", label="Sample only SSS in GI rays")
        self.addControl("sample_sss_only_in_glossy_rays", label="Sample only SSS in Glossy rays")
        self.endLayout()

        self.addBumpLayout()
        
        self.beginLayout("Hardware Texturing", collapse=True)
        pm.mel.eval('AEhardwareTextureTemplate "%s"' % self.nodeName + r'("color")')
        self.endLayout()

        self.addAOVLayout()
        
        # include/call base class/node attributes
        pm.mel.AEdependNodeTemplate(self.nodeName)
        
        self.addExtraControls()
        
        self.endScrollLayout()
