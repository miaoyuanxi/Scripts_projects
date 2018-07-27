#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

# 2017/9/21-16:27-2017
#"C:\Program Files\Autodesk\Maya2014\bin\mayapy.exe" E:\PycharmProjects\work\test_del\an_maya.py --ui "123" --ti "456" --proj "E:\fang\fagng" --cgfile "E:\fang\fagng\scenes\pre_test_2014.mb" --taskjson "d:\task.json"
#"C:/Program Files/Autodesk/maya2014/bin/mayabatch.exe" -command "python \"options={'cg_file': 'E:/fang/fagng/scenes/pre_test_2014.mb', 'user_id': 123, 'cg_project': 'E:/fang/fagng', 'task_id': 456, 'task_json': 'd:/task.json'};import sys;sys.path.insert(0, 'E:/PycharmProjects/work/test_del');from an_maya import *;analyze = maya_an(options);analyze.run();analyze.write_info_file();\""


import os
import sys
import re
import subprocess
import json
import argparse

if "maya" in sys.executable.lower():
    if "mayapy" in sys.executable.lower() or \
            "python-bin" in sys.executable.lower():
        import maya.standalone as standalone
        standalone.initialize()
    import maya.cmds as cmds
    import maya.mel as mel
    import pymel.core as pm





class Analyze(dict):
    def __init__(self, options):
        print options
        for i in options:
            print i
            self[i] = options[i]
        
    
    def write_info_file(self):
        info_file_path = os.path.dirname(self["task_json"])
        print "write info to task.json"
        if not os.path.exists(info_file_path):
            os.makedirs(info_file_path)
        try:
            info_file = self["task_json"]
            #print inof_json_path

            with open(info_file, 'r') as f:
                print "read info file"
                json_src = json.load(f)
            print type(json_src)
            json_src["scene_info"] = self.scene_info_dict
            # json_src.setdefault("scene_info",[]).append(self.scene_info_dict)
            print json_src
            with open(info_file, 'w') as f:
                print "write info file"
                f.write(json.dumps(json_src))
                print "88888888888888888888888888"
                # f.close()
        except Exception as err:
            print  err
            pass

    def run(self):
        self.scene_info_dict={}
        scene_info_common_dict = {}
        print "[Rayvision]: open maya file " + self["cg_file"]
        try:
            cmds.file(self["cg_file"], o=1, force=1, ignoreVersion=1, prompt=0)
        except:
            pass
        print "[Rayvision]: open maya ok."
        
        pm.lockNode( 'defaultRenderGlobals', lock=False )
        render_node = pm.PyNode("defaultRenderGlobals")
        
        self.scene_info_dict['renderer'] =  cmds.getAttr("defaultRenderGlobals.currentRenderer")

        scene_info_common_dict['imageFilePrefix'] =  str(cmds.getAttr("defaultRenderGlobals.imageFilePrefix"))
        scene_info_common_dict['Start'] =  int(cmds.getAttr("defaultRenderGlobals.startFrame"))
        scene_info_common_dict['End'] = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
        scene_info_common_dict['all_camera'] = ",".join(cmds.ls(type="camera")) 
        scene_info_common_dict['render_camera'] = ",".join([i.name() for i in pm.ls(type="camera") if i.renderable.get()]) 
        scene_info_common_dict['all_layer'] = ",".join([i.name() for i in pm.PyNode("renderLayerManager.renderLayerId").outputs() if i.type() == "renderLayer"])
        scene_info_common_dict['render_layer'] = ",".join([i.name() for i in pm.PyNode("renderLayerManager.renderLayerId").outputs() if i.type() == "renderLayer"  if i.renderable.get()] )
        
        scene_info_common_dict['imageFormat'] =  str(cmds.getAttr("defaultRenderGlobals.imfkey"))
        
        scene_info_common_dict['width'] =  int(cmds.getAttr("defaultResolution.width"))
        scene_info_common_dict['height'] =  int(cmds.getAttr("defaultResolution.height"))
        scene_info_common_dict['preMel'] = str(self.get_pre()[0])
        scene_info_common_dict['postMel'] = str(self.get_pre()[1])
        scene_info_common_dict['preRenderLayerMel'] = str(self.get_pre()[2])
        scene_info_common_dict['postRenderLayerMel'] = str(self.get_pre()[3])
        scene_info_common_dict['preRenderMel'] = str(self.get_pre()[4])
        scene_info_common_dict['postRenderMel'] = str(self.get_pre()[5])
        
        self.scene_info_dict['common'] = scene_info_common_dict
        print self.scene_info_dict

    
    def get_pre(self):
        render_node = pm.PyNode("defaultRenderGlobals")
        preMel = render_node.preMel.get()
        postMel = render_node.postMel.get()
        preRenderLayerMel = render_node.preRenderLayerMel.get()
        postRenderLayerMel = render_node.postRenderLayerMel.get()
        preRenderMel = render_node.preRenderMel.get()
        postRenderMel = render_node.postRenderMel.get()
        return preMel, postMel, preRenderLayerMel, postRenderLayerMel, preRenderMel, postRenderMel
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='maya check python')
    parser.add_argument("--ui", dest="user_id", type=int)
    parser.add_argument("--ti", dest="task_id", type=int)
    parser.add_argument("--proj", dest="cg_project", type=str)
    parser.add_argument("--cgfile", dest="cg_file", type=str)
    parser.add_argument("--taskjson", dest="task_json", type=str)
    options = parser.parse_args().__dict__
    print options
    print "77777777777777777777777777777777777"
    analyze = Analyze(options)
    analyze.run()
    analyze.write_info_file()
    print "success"