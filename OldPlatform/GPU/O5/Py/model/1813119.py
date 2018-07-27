# # ! /usr/bin/env python
# # coding=utf-8
import os
import re
import pymel.core as pm
for i in pm.ls(type="VRaySettingsNode"):
    if i.hasAttr("srdml"):
        i.srdml.set(24000)
        i.vrscene_on.set(0)

        shot_scene_name = os.path.splitext(os.path.basename(pm.sceneName()))[0]
        r = re.findall(r'\w+_\w+_\d+_\w+_(v\d+).+', shot_scene_name, re.I)
        if r:
            version = r[0]

        if renderableCamera.lower().endswith("l"):
            resolution = "fullres_L"
        elif renderableCamera.lower().endswith("r"):
            resolution = "fullres_R"
        else:
            resolution = "fullres"

        new_path = "<Layer>/%s/%s/%s" % (version, resolution, shot_scene_name)
        print "Old output path: " + str(i.fileNamePrefix.get())
        i.fileNamePrefix.set(new_path)
        print "New output path: " + str(i.fileNamePrefix.get())
