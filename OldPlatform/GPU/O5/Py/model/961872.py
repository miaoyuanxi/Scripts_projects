import re
import pymel.core as pm
import os


short_scene_name = os.path.splitext(os.path.basename(pm.sceneName()))[0]
r = re.findall(r"(?P<name>.*)LGT_(?P<path>.*)", short_scene_name)

if r:
    new_path = "{0}/%l/{1}%l".format(r[0][1], r[0][0])
    pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(new_path)
    print "New output path: " + str(pm.PyNode("defaultRenderGlobals").imageFilePrefix.get())
if not r:
	r = re.findall(r"(?P<name>.*)LGT_(?P<path>[A-Za-z_0-9]*)", short_scene_name)
	if r:
		new_path = "{0}/%l/{1}%l".format(r[0][1], r[0][0])
		pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(new_path)
		print "New output path: " + str(pm.PyNode("defaultRenderGlobals").imageFilePrefix.get())
if not r:
	print "short_scene_name: {}".format(short_scene_name)
	print "New output path: Failed"