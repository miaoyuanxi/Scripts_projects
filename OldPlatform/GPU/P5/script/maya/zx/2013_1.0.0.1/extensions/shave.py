import pymel.core as pm
import mtoa.ui.ae.templates as templates
from mtoa.ui.ae.templates import AttributeTemplate, ShapeMixin, registerTranslatorUI
from mtoa.ui.ae.shaderTemplate import ShaderMixin

class ShaveHairTemplate(AttributeTemplate, ShapeMixin, ShaderMixin):
    def setup(self):
        self.addControl("primaryVisibility")
        self.addControl("castsShadows")
        self.addControl("visibleInReflections")
        self.addControl("visibleInRefractions")
        self.addSeparator()
        self.commonShapeAttributes()        
        self.addSeparator()

        self.addControl("aiOverrideHair")
        self.addControl("aiHairShader")
    
        self.addSeparator()
    
        self.addControl("aiMinPixelWidth")
        self.addControl("aiMode")

        self.addSeparator()

        self.addControl("aiDiffuseCache")
        self.addControl("aiIndirect")
        self.addControl("aiDirectDiffuse")
        
        self.addControl("aiExportHairColors")
        self.addControl("aiExportHairIDs")

        self.addAOVLayout()

templates.registerTranslatorUI(ShaveHairTemplate, "shaveHair", "shave")
