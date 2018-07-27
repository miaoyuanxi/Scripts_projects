import os
import re
import pymel.core as pm
for i in pm.ls(type="VRaySettingsNode"):
    if i.hasAttr("srdml"):
        i.srdml.set(36000)
    if i.hasAttr("sys_distributed_rendering_on"):
        i.sys_distributed_rendering_on.set(False)
    if i.hasAttr("globopt_gi_dontRenderImage"):
        i.globopt_gi_dontRenderImage.set(False)