import pymel.core as pm
from mtoa.ui.ae.shaderTemplate import ShaderAETemplate

class AEaiVolumeCollectorTemplate(ShaderAETemplate):
    def setup(self):
        self.beginScrollLayout()
        
        self.beginLayout('Attributes', collapse=False)
        self.addControl('scattering', label='Scattering')
        self.addControl('attenuation_mode', label='Attenuation Mode')
        self.addControl('attenuation', label='Attenuation')
        self.addControl('emission', label='Emission')
        self.addControl('phase', label='Phase Function Anisotropy')
        self.endLayout()
               
        pm.mel.AEdependNodeTemplate(self.nodeName)

        self.addExtraControls()
        self.endScrollLayout()
