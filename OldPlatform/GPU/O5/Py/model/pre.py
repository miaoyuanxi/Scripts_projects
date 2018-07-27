import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

def main():
    RenderNode = pm.PyNode("defaultRenderGlobals")
    Renderer_name = RenderNode.currentRenderer.get()
    print("Current renderner: %s"%Renderer_name)
    print("Current Outpu setting: %s"%RenderNode.attr("imageFilePrefix").get())
    print("Current Outpu format: %s"%RenderNode.attr("imageFormat").get())
    if Renderer_name == "redshift":
        aiop = pm.PyNode("redshiftOptions")
        aiop.attr("percentageOfGPUMemoryToUse").set(90)
        aiop.attr("maxNumGPUMBForIrradiancePointCloudHierarchy").set(128)
        aiop.attr("maxNumGPUMBForForICPHierarchy").set(128)
        aiop.attr("percentageOfFreeMemoryUsedForTextureCache").set(15)
        aiop.attr("maxNumGPUMBForTextureCache").set(256)