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
import json
if sys.version_info[:2] == (2, 6):
    if sys.platform.startswith("win"):
        sys.path.append(r"\\10.60.100.101\o5\py\model\tim\py26")
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
    import pymel.core as pm

def RBcmd(cmdStr, continueOnErr = False, myShell = False):
    print cmdStr
    an_task_id = options['cg_info_file'].split('/')[3]
    user_id = options['user_id']

    if user_id in [119768]:
        G_JOB_NAME=os.environ.get('G_JOB_NAME')
        print an_task_id,user_id,G_JOB_NAME
        render_log = "d:/log/helper/%s/%s.log" % (an_task_id,G_JOB_NAME)
        with open(render_log,"wb") as l:
            l.write('render cmd info: \n')
            l.write(cmdStr)
            l.flush()
            cmdp = subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
            cmdp.stdin.write('3/n')
            cmdp.stdin.write('4/n')
            exitcode = 0
            
            while cmdp.poll() is None:
                resultLine = cmdp.stdout.readline().strip()
                
                if resultLine != '':            
                    l.write(resultLine+'\n')
                    l.flush()
                    print resultLine
                if resultLine =="write cg_info_file":
                    cmdp.kill()
                        
            resultStr = cmdp.stdout.read()
            resultCode = cmdp.returncode
    else:
        cmdp = subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
        cmdp.stdin.write('3/n')
        cmdp.stdin.write('4/n')
        exitcode = 0
        while cmdp.poll() is None:
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
        try:
            inof_json_path=  os.path.splitext(self["cg_info_file"])[0]+".json"
            print inof_json_path
            with open(inof_json_path, 'w') as f:
                f.write(json.dumps(self))
                f.close()
        except Exception as err:
            print  err
            pass
            
            
        with open(self["cg_info_file"], "w") as f:
            f.write("Start::%s\n" % (self["Start"]))
            f.flush()
            f.write("End::%s\n" % (self["End"]))
            f.flush()
            if "camera" in self:
                f.write("camera::%s\n" % (self["camera"]))
                f.flush()
            if "render_layer" in self:
                f.write("render_layer::%s\n" % (self["render_layer"]))
                f.flush()
            f.flush()
            print "write cg_info_file"            
            cmds.quit(force=True)
        cmds.quit(force=True)
    def write_dict_info(self):
        print "write_dict_info is start "
        info_file_path=os.path.dirname(self["cg_info_file"])
        if not os.path.exists(info_file_path):
            os.makedirs(info_file_path)
        with open(self["cg_info_file"], "w") as f:
            for key in self:
                str_w = '%s::%s' % (key, self[key])
                f.write(str_w)
                f.write('\n')
                f.flush()
            print "write cg_info_file"
            cmds.quit(force=True)
        cmds.quit(force=True)
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
        currentPath = os.path.split(os.path.realpath(__file__))[0].replace('\\', '/')
        info_json = eval(open(currentPath + '\\info.json').read())
        if self["platform"] in info_json:
            cfg_path = info_json[self['platform']]['cfg_path']
            json_path = info_json[self['platform']]['json_path']
            custom_config = info_json[self['platform']]['custom_config']
            py_path = info_json[self['platform']]['py_path']
            bat_path = info_json[self['platform']]['bat_path']
            auto_plugins = info_json[self['platform']]['auto_plugins']
            #print cfg_path, json_path, custom_config, py_path, bat_path, auto_plugins
        else:
            raise Exception("Can not find  Current platform info form info.json")
        plugin_config = r"%s/%s/%s/%s/plugins.json" % (json_path,fileId, self["user_id"], self["task_id"])

        self["model"] = py_path
        self["plugin_config"] = plugin_config
        self["custom_config"] = custom_config
        maya_batch = os.path.split(self["cg_software_path"])[0]+"\mayabatch.exe"
        self["cg_software_path"] =maya_batch
        

        print "*"*30
        if  self['user_id'] in [119768]:
            self['cmdStr'] = "\"%(cg_software_path)s\" -command \"python \\\"options={'cg_file':  '%(cg_file)s' , 'cg_info_file': '%(cg_info_file)s', 'cg_software': 'Maya','cg_project':'%(cg_project)s'};import sys;sys.path.insert(0, '%(model)s');from check_all import *;analyze = eval(options['cg_software']+'Analyze(options)');analyze.run();analyze.write_dict_info();\\\"\"" % ( self)
        else:
            self['cmdStr'] = "\"%(cg_software_path)s\" -command \"python \\\"options={'cg_file':  '%(cg_file)s' , 'cg_info_file': '%(cg_info_file)s', 'cg_software': 'Maya','cg_project':'%(cg_project)s'};import sys;sys.path.insert(0, '%(model)s');from check_all import *;analyze = eval(options['cg_software']+'Analyze(options)');analyze.run();analyze.write_info_file();\\\"\"" % (self)
        print "+"*30
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

        #self["start"] = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
        self["Start"] = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
        #self["end"] = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
        self["End"] = int(cmds.getAttr("defaultRenderGlobals.endFrame"))
        self["camera"] = ",".join(cmds.ls(type="camera"))
        self["render_layer"] = ",".join(cmds.listConnections("renderLayerManager.renderLayerId"))
        self['preMel'] = self.get_pre()[0]
        self['postMel'] = self.get_pre()[1]
        self['preRenderLayerMel'] = self.get_pre()[2]
        self['postRenderLayerMel'] = self.get_pre()[3]
        self['preRenderMel'] = self.get_pre()[4]
        self['postRenderMel'] = self.get_pre()[5]
        
        print self
    def get_pre(self):
        render_node = pm.PyNode("defaultRenderGlobals")
        preMel = render_node.preMel.get()
        postMel = render_node.postMel.get()
        preRenderLayerMel = render_node.preRenderLayerMel.get()
        postRenderLayerMel = render_node.postRenderLayerMel.get()
        preRenderMel = render_node.preRenderMel.get()
        postRenderMel = render_node.postRenderMel.get()
        return preMel,postMel,preRenderLayerMel,postRenderLayerMel,preRenderMel,postRenderMel


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
    print "*"*30
    print options['user_id']
    print "*"*30
    analyze = eval(options["cg_software"]+"Analyze(options)")
    if options["cg_software"] == "Maya":
        opt= analyze.get_info()
        analyze.load_plugins() 
        RBcmd(opt['cmdStr'],False,False)    
    else:
        analyze.run()
        analyze.write_info_file()
