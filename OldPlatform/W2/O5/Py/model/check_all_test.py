# ! /usr/bin/env python
# coding=utf-8
# Author: Liu Qiang
# Tel:    13811571784
# QQ:     386939142
'''
C:\Python27\python.exe C:\script\maya\check_all.py --cgsw "Maya" --ui 119768 --ti 5334090 --sfp "C:/Program Files/Autodesk/maya2014/bin/maya.exe" --proj "" --cgfile "G:/test_2014.mb" --cg_info_file "C:/WORK/helper/60156/analyse_net.txt" --pt 1005
'''
import os
import sys
import re
import subprocess
if sys.version_info[:2] == (2, 6):
    if sys.platform.startswith("win"):
        sys.path.append(r"\\10.50.5.29\o5\py\model\tim\py26")
    elif sys.platform.startswith("linux"):
        sys.path.append(r"/mnt_rayvision/o5/py/model/tim/")

import argparse

if "maya" in sys.executable.lower():
    if "mayapy" in sys.executable.lower() or \
            "python-bin" in sys.executable.lower():
        import maya.standalone as standalone
        standalone.initialize()
    import maya.cmds as cmds
    import maya.mel as mel

def RBcmd(cmdStr, continueOnErr = False, myShell = False):

    cmdp = subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
    cmdp.stdin.write('3/n')
    cmdp.stdin.write('4/n')
    exitcode = 0
    while cmdp.poll() == None:
        resultLine = cmdp.stdout.readline().strip()
        
        if resultLine != '':
            print resultLine
        if resultLine =="write cg_info_file":
            cmdp.kill()
        
    resultStr = cmdp.stdout.read()
    resultCode = cmdp.returncode

    
    
    if exitcode == -1:
        sys.exit(-1)

    if not continueOnErr:
        if resultCode != 0:
            sys.exit(resultCode)
    return resultStr


class Analyze(dict):

    def __init__(self, options):
        for i in options:
            self[i] = options[i]

    def run(self):
        ''

    def write_info_file(self):
        info_file_path=os.path.dirname(self["cg_info_file"])
        if not os.path.exists(info_file_path):
            os.makedirs(info_file_path)
        f = open(self["cg_info_file"], "w")
        f.write("Start::%s\n" % (self["start"]))
        f.write("End::%s\n" % (self["end"]))
        if "camera" in self:
            f.write("camera::%s\n" % (self["camera"]))
        if "render_layer" in self:
            f.write("render_layer::%s\n" % (self["render_layer"]))
        f.close()
        print "write cg_info_file"
        #mel.eval("quit -force;")
        #cmds.quit(force=True)
        os._exit()
        exit()
'''
        with open(self["cg_info_file"], "w") as f:
            f.write("Start::%s\n" % (self["start"]))
            f.write("End::%s\n" % (self["end"]))
            if "camera" in self:
                f.write("camera::%s\n" % (self["camera"]))
            if "render_layer" in self:
                f.write("render_layer::%s\n" % (self["render_layer"]))
            print "write cg_info_file"
            mel.eval("quit -force;")
            cmds.quit(force=True)
        cmds.quit(force=True)
'''

        
class MayaAnalyze(Analyze):

    def __init__(self, options):
        super(MayaAnalyze, self).__init__(options)
    def get_info(self):
        if self["user_id"]:
          
            if int(str(self["user_id"])[-3:]) >= 500:
                fileId = str(self["user_id"] - int(str(self["user_id"])[-3:]) + 500)
            else:
                fileId = str(self["user_id"] - int(str(self["user_id"])[-3:]))
        else:
            print "don't find user_id"
        if self["platform"] == 1000:
            plugin_config = r"//10.60.100.105/stg_data/input/p5/config/%s/%s/%s/plugins.json" % (fileId, self["user_id"], self["task_id"])
            custom_config = r"\\10.60.100.102\td\custom_config"
            model = r"//10.60.100.105/stg_data/input/o5/py/model"
        if self["platform"] == 1002:
            plugin_config = r"//10.60.100.101/p5/config/%s/%s/%s/plugins.json" % (fileId, self["user_id"], self["task_id"])
            custom_config = r"\\10.60.100.102\td\custom_config"
            model = r"//10.60.100.101/o5/py/model"
        if self["platform"] == 1005:      
            plugin_config = r"//10.50.244.116/p5/config/%s/%s/%s/plugins.json" % (fileId, self["user_id"], self["task_id"])
            custom_config = r"\\10.50.1.22\td\custom_config"
            model = "//10.50.5.29/o5/py/model"       

        self["model"] = model
        self["plugin_config"] = plugin_config
        self["custom_config"] = custom_config
        maya_batch = os.path.split(self["cg_software_path"])[0]+"\mayabatch.exe"
        self["cg_software_path"] =maya_batch
        self['cmdStr']="\"%(cg_software_path)s\" -command \"python \\\"options={'cg_file':  '%(cg_file)s' , 'cg_info_file': '%(cg_info_file)s', 'cg_software': 'Maya','cg_project':'%(cg_project)s'};import sys;sys.path.insert(0, '%(model)s');from check_all import *;analyze = eval(options['cg_software']+'Analyze(options)');analyze.run();analyze.write_info_file();\\\"\"" % (self)
        return self
    def load_plugins(self):
        sys.path.append(self["model"])
        import RayvisionPluginsLoader
        custom_file = self["custom_config"] + "/" + str(self["user_id"]) + "/RayvisionCustomConfig.py"
        print self["plugin_config"]
        plginLd = RayvisionPluginsLoader.RayvisionPluginsLoader()
        plginLd.RayvisionPluginsLoader(self["plugin_config"], [custom_file])

        with open(self["plugin_config"], 'r') as file:
            file_str = file.read()
            plugis_dict = dict(eval(file_str))
            
            if plugis_dict:
                renderSoftware = plugis_dict['renderSoftware']
                softwareVer = plugis_dict['softwareVer']
                plugis_list_dict = plugis_dict['plugins']
                print plugis_list_dict
    
    def run(self):
        print "[Rayvision]: open maya file " + self["cg_file"]
        try:
            cmds.file(self["cg_file"], o=1, force=1, ignoreVersion=1, prompt=0)
        except:
            pass
        print "[Rayvision]: open maya ok."

        self["start"] = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
        self["end"] = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
        self["camera"] = ",".join(cmds.ls(type="camera"))
        self["render_layer"] = ",".join(cmds.listConnections("renderLayerManager.renderLayerId"))

class LightWaveAnalyze(Analyze):

    def __init__(self, options):
        super(LightWaveAnalyze, self).__init__(options)

    def run(self):
        start_re = re.compile(r'FirstFrame +(\d+)', re.I)
        end_re = re.compile(r'LastFrame +(\d+)', re.I)

        output_re_list = [re.compile(r'SaveAnimationName +(.+)\\.+?\.avi$', re.I),
                          re.compile(r'SaveRGBImagesPrefix +(.+)[/\\][\w ]+$', re.I),
                          re.compile(r'SaveAlphaImagesPrefix +(.+)[/\\][\w ]+$', re.I)]

        ok_file = os.path.splitext(self["cg_file"])[0] + "_rayvision.lws"
        output = r"c:\work\render\%s\output" % (self["task_id"])

        with open(self["cg_file"]) as f:
            with open(ok_file, "w") as f_ok:
                for line in f:
                    if line and line.strip():
                        if start_re.findall(line):
                            self["start"] = start_re.findall(line)[0]
                        elif end_re.findall(line):
                            self["end"] = end_re.findall(line)[0]

                    for i_re in output_re_list:
                        if i_re.findall(line):
                            print "Old: " + line
                            sys.stdout.flush()
                            line = line.replace(i_re.findall(line)[0], output)
                            print "New: " + line
                            sys.stdout.flush()
                            break
                    f_ok.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'rayvision web submit check python')
    parser.add_argument("--cgsw", dest="cg_software", type=str)
    parser.add_argument("--ui", dest="user_id", type=int)
    parser.add_argument("--ti", dest="task_id", type=int)
    parser.add_argument("--sfp", dest="cg_software_path", type=str)
    parser.add_argument("--proj", dest="cg_project", type=str)
    parser.add_argument("--cgfile", dest="cg_file", type=str)
    parser.add_argument("--cg_info_file", dest="cg_info_file", type=str)
    parser.add_argument("--pt", dest="platform", type=int)
    
    options = parser.parse_args().__dict__
    analyze = eval(options["cg_software"]+"Analyze(options)")
    if options["cg_software"] == "Maya":
        opt= analyze.get_info()
        analyze.load_plugins() 
        RBcmd(opt['cmdStr'],False,False)    
    else:
        analyze.run()
        analyze.write_info_file()
