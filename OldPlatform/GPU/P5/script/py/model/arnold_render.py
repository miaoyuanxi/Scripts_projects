#! /usr/bin/env python
#coding=utf-8
import os
import subprocess
import _subprocess
import pprint
import sys
import shutil
import filecmp
import re

class Render(object):

    def __init__(self, task_id, start, end, by):
        self.task_id = task_id
        self.user_id = None
        self.cfg_path = self.get_cfg_path()
        self.cfg_info = self.get_cfg_info()

        if self.cfg_info:
            self.cfg_info["start"] = start
            self.cfg_info["end"] = end
            self.cfg_info["by"] = by

            self.cfg_info["output"] = "c:/work/render/%s/output/" % (self.task_id)
            if not os.path.exists(self.cfg_info["output"]):
                os.makedirs(self.cfg_info["output"])

            self.user_id = self.cfg_info["user_id"]

        self.pre_render()

    def pre_render(self):
        print "Start default pre render process..."
        self.clean_network()
        self.mapping_network()

    def post_render(self):
        print "Start default post render process..."
#        self.clean_network()

    def clean_network(self):
        result = self.call_command("net use * /delete /y")
        if result == 0:
            print "clean mapping network successfully."
        else:
            print "clean mapping network failed."

    def mapping_network(self):
#        mapping = {"x:": r"\\10.50.1.6\d\inputdata8\maya\21000\21293\X",
#                   "z:": r"\\192.168.0.88\3dsoft\temp"}

        if self.cfg_info:
            for i in self.cfg_info["mappings"]:
                if i.endswith(":"):
                    #on windows, we must use '\' slash when mount, not '/'
                    path = self.cfg_info["mappings"][i].replace("/", "\\")
                    if self.call_command("net use %s %s" % (i, path)):
                        print "can not mapping %s to %s" % (i, path)
                    else:
                        print "Mapping %s to %s" % (i, path)
                    sys.stdout.flush()

        self.call_command("net use")

    def get_cfg_path(self):
        if self.user_id:
            cfg = r"\\20.1.0.18\d\ninputdata5\%s\%s\temp" % \
                (self.user_id, self.task_id)
        else:
            cfg = r"\\20.1.0.18\d\ninputdata5\%s\temp" % \
                (self.task_id)

        cfg = cfg.replace("\\", "/")

        if os.path.exists(cfg):
            return cfg

    def get_cfg_info(self):
        if self.cfg_path:
            cfg_file = os.path.join(self.cfg_path, "server.cfg")
            if os.path.exists(cfg_file):
                return eval(open(cfg_file).read())

    def get_plugin_info(self):
        if self.cfg_path:
            plugin_file = os.path.join(self.cfg_path, "plugins.cfg")
            if os.path.exists(plugin_file):
                return eval(open(plugin_file).read())

    def copytree(self, src, dst):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            if os.path.isdir(s):
                if not os.path.exists(d):
                    os.makedirs(d)
                self.copytree(s, d)
            else:
                if os.path.exists(d):
                    if not filecmp.cmp(s, d):
                        print "copy %s to %s" % (s, d)
                        shutil.copy2(s, d)
                else:
                    print "copy %s to %s" % (s, d)
                    shutil.copy2(s, d)

    def call_command(self, cmd):
        return subprocess.call(cmd, shell=1)

    def run_command(self, cmd):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = _subprocess.SW_HIDE

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, startupinfo=startupinfo)

        while 1:
            #returns None while subprocess is running
            return_code = p.poll()
            if return_code == 0:
                break
            elif return_code == 1:
                raise Exception(cmd + " was terminated for some reason.")
            elif return_code != None:
                print "exit return code is: " + str(return_code)
                raise Exception(cmd + " was crashed for some reason.")
            line = p.stdout.readline()
            yield line


class KickRender(Render):

    def __init__(self, task_id, start, end, by=1):
        Render.__init__(self, task_id, start, end, by)
        if self.cfg_info:
            self.get_kick_info()
            self.render()
        else:
            print "The cfg file of task %s doesn't exists." % self.task_id

        print "\n"

    def get_kick_info(self):
        self.cfg_info["kick_exe"] = None
        self.cfg_info["shader_path"] = None

        if int(self.cfg_info["user_id"]) in [100001]:
            self.cfg_info["kick_exe"] = '//10.50.24.10/mili/plugins/arnold/bin/kick.exe'
            self.cfg_info["shader_path"] = '//10.50.24.10/mili/plugins/arnold/shaders'

            self.call_command("NET USE %s %s" % ("N:", r"\\10.50.24.10\mili\N"))

            hasEnv = False
            host = r"C:/Windows/system32/drivers/etc/hosts"
            with open(host, "a+" ) as f:
                lines = f.readlines()
                for line in lines:
                    if "20.1.0.18 hnas02" == line.strip():
                        hasEnv = True
                if not hasEnv:
                    f.write( '\n' )
                    f.write( "20.1.0.18 hnas02" )
                    f.write( '\n' )

        elif int(self.cfg_info["user_id"]) in [961900]:
            self.cfg_info["kick_exe"] = '//10.222.1.10/d/plugins/961900/arnold/bin/kick.exe'
            self.cfg_info["shader_path"] = '//10.222.1.10/d/plugins/961900/arnold/shaders'

            hasEnv = False
            host = r"C:/Windows/system32/drivers/etc/hosts"
            with open(host, "a+" ) as f:
                lines = f.readlines()
                for line in lines:
                    if "10.222.1.10 hnas02" == line.strip():
                        hasEnv = True
                if not hasEnv:
                    f.write( '\n' )
                    f.write( "10.222.1.10 hnas02" )
                    f.write( '\n' )

            os.environ["PATH"] += ";"
            os.environ["PATH"] += "//10.222.1.10/d/plugins/961900/Yeti/bin"


        else:
            ass_start = self.get_ass_file(self.cfg_info["start"])
            self.cfg_info["arnold_version"] = self.get_arnold_version(ass_start)

    def get_arnold_version(self, ass):
        result = {"arnold_version": None,
                  "sys": None,
                  "host_app": None,
                  "host_version": None,
                  "software": None,
                  "software_version": None}

        if os.path.exists(ass):
            with open(ass, "r") as f:
                while 1:
                    line = f.readline()
                    if line.startswith("### from"):
                        result["arnold_version"], result["sys"] = line.split()[3:5]
                        continue
                    if line.startswith("### host app"):
                        line_split = line.split()
                        result["host_app"] = line_split[3]
                        result["host_version"] = line_split[4]
                        result["software"] = line_split[-3]
                        result["software_version"] = " ".join(line_split[-2:])
                        break

        return result

    def get_ass_file(self, frame):
        return self.cfg_info["ass_path"] + "/" + self.cfg_info["ass_head"] + \
            str(frame).zfill(self.cfg_info["ass_padding"]) + \
            self.cfg_info["ass_tail"]

    def render(self):
        if self.cfg_info:
            pprint.pprint(self.cfg_info)

            for i in range(int(self.cfg_info["start"]), int(self.cfg_info["end"])+1):
                print "start to render frame: " + str(i)
                self.render_frame(i)

    def render_frame(self, frame):
        input = self.get_ass_file(frame)
        output = os.path.join(self.cfg_info["output"],
                              os.path.basename(input.replace(".ass", ".exr")))

#        cmd = "\"%s\" -g 2.2 -nstdin -dw -dp -nocrashpopup -v 2 -t 0 -l %s " \
#              "-i %s" % (self.cfg_info["kick_exe"],
#                               self.cfg_info["shader_path"],
#                               self.get_ass_file(frame))

        cmd = "\"%s\" -g 2.2 -nstdin -dw -dp -nocrashpopup -v 2 -t 0 -l %s " \
              "-i %s -o %s" % (self.cfg_info["kick_exe"],
                               self.cfg_info["shader_path"],
                               input,
                               output)

        print "Info: Run render ass file command:"
        print cmd

        images = []
        RE_ALL = re.compile(r'writing.+file `?(.+?)[ \']')
        for line in self.run_command(cmd):
            if line.strip():
                print line.strip()
                if "Arnold shutdown" in line:
                    break
                elif RE_ALL.findall(line, re.I):
                    images.append(RE_ALL.findall(line, re.I)[0])
                elif re.findall(r'.+driver_exr.+Cannot open image file',
                                line, re.I):
                    kill_all()
                    raise Exception("Can't find output image path")
                elif "[kick] Can't read input file" in line:
                    kill_all()
                    raise Exception("Can't read input ass file")
#                elif "[texturesys] Could not open file" in line:
#                    kill_all()
#                    raise Exception("Can't read sourceimage file")

#        for i in images:
#            self.copy_file(i)

    def copy_file(self, src):
        dst = os.path.join(self.cfg_info["output"],
                           src.split("data")[1].lstrip("/"))
        dst_dir = os.path.dirname(dst)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        shutil.copy2(src, dst)
        print "Info: copy to " + dst


class MayaBatchRender(Render):

    def __init__(self, task_id, user_id=None):
        Render.__init__(self, task_id, user_id)
        if self.cfg_info:
            self.plugin_info = self.get_plugin_info()
            self.get_maya_info()
            self.create_setup_file()
            self.set_variables()
            self.set_plugins()
        else:
            print "The cfg file of task %s doesn't exists." % self.task_id

        print "\n"

    def get_maya_info(self):
        self.cfg_info["render_exe"] = "C:/Program Files/Autodesk/" \
            "maya%s/bin/render.exe" % (self.cfg_info["maya_version"])
        self.cfg_info["mayabatch_exe"] = "C:/Program Files/Autodesk/" \
            "maya%s/bin/mayabatch.exe" % (self.cfg_info["maya_version"])
        self.cfg_info["output"] = "c:/work/render/%s/output/" % (self.task_id)
        if not os.path.exists(self.cfg_info["output"]):
            os.makedirs(self.cfg_info["output"])

    def create_setup_file(self):
        if self.cfg_info["mappings"]:
            self.cfg_info["tmp"] = os.path.join(os.environ["tmp"],
                str(self.task_id))
            if not os.path.exists(self.cfg_info["tmp"]):
                os.makedirs(self.cfg_info["tmp"])

            self.cfg_info["setup_file"] = os.path.join(self.cfg_info["tmp"],
                "usersetup.mel")

            with open(self.cfg_info["setup_file"], "w") as f:
                f.write("dirmap -en true;\n")
                for i in self.cfg_info["mappings"]:
                    f.write("dirmap -m \"%s\" \"%s\";\n" % (i.encode("gb2312"),
                        self.cfg_info["mappings"][i]))

    def set_variables(self):
        for i in self.cfg_info["variables"]:
            os.environ[i] = self.cfg_info["variables"][i]

        if self.cfg_info["mappings"]:
            os.environ.setdefault("MAYA_SCRIPT_PATH", "")
            if os.environ["MAYA_SCRIPT_PATH"]:
                os.environ["MAYA_SCRIPT_PATH"] += ";"
            os.environ["MAYA_SCRIPT_PATH"] += self.cfg_info["tmp"]

    def set_plugins(self):
        if "mtoa" in self.plugin_info:
            print "set mtoa plugin"
            modules_path = r'C:\users\enfuzion\Documents\maya\%s-x64\modules' % (self.cfg_info["maya_version"])
            self.create_mtoa_module(modules_path)

            env_path = r'C:\users\enfuzion\Documents\maya\%s-x64' % (self.cfg_info["maya_version"])
            self.create_mtoa_env(env_path)

        if self.user_id in [100001, 300133, 961624]:
            self.copytree(r"\\10.50.8.16\td\zhaoxiaofei\300133\Autodesk",
                         r"C:\Program Files\Autodesk")

        if "vrayformaya" in self.plugin_info:
            print "set vrayformay plugin"
            os.environ["VRAY_FOR_MAYA2015_MAIN_x64"] = "//192.168.0.88/test/Maya 2015 for x64"
            os.environ["VRAY_FOR_MAYA2015_PLUGINS_x64"] = os.environ["VRAY_FOR_MAYA2015_MAIN_x64"] + "/vrayplugins"
            os.environ["VRAY_OSL_PATH_MAYA2015_x64"] = os.environ["VRAY_FOR_MAYA2015_MAIN_x64"] + "/include/opensl"
            os.environ["VRAY_TOOLS_MAYA2015_x64"] = os.environ["VRAY_FOR_MAYA2015_MAIN_x64"] + "/bin"

    def create_mtoa_module(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        with open(os.path.join(path, "mtoa.mod"), "w") as f:
            f.write(r"+ mtoa any C:\solidangle\mtoadeploy\%s_%s" % (self.cfg_info["maya_version"],
                    self.plugin_info["mtoa"]))
            f.write("\r\n")
            f.write(r"PATH +:= bin")

    def create_mtoa_env(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        with open(os.path.join(path, "Maya.env"), "w") as f:
            f.write(r"MAYA_RENDER_DESC_PATH = C:\solidangle\mtoadeploy\%s_%s" % (self.cfg_info["maya_version"],
                    self.plugin_info["mtoa"]))
            f.write("\r\n")
            f.write(r"PATH = %s;C:\solidangle\mtoadeploy\%s_%s\bin" % ("%PATH%",
                    self.cfg_info["maya_version"], self.plugin_info["mtoa"]))

    def render(self, start, end, by=1):
        self.pre_render()

        if self.cfg_info:
            self.cfg_info["start"] = start
            self.cfg_info["end"] = end
            self.cfg_info["by"] = by

            pprint.pprint(self.cfg_info)
#            for i in os.environ:
#                print i, os.environ[i]

            print "start maya render process..."
            if self.cfg_info["user_id"] in [961743]:
                cmd = "\"%(render_exe)s\" -s %(start)s -e %(end)s -b %(by)s " \
                    "-preRender \"setAttr \\\"miDefaultOptions.maxSamples\\\" 2;" \
                    "setAttr \\\"miDefaultOptions.finalGather\\\" 1;" \
                    "setAttr \\\"miDefaultOptions.finalGatherRays\\\" 200;" \
                    "setAttr \\\"miDefaultOptions.finalGatherPresampleDensity\\\" 2;" \
                    "setAttr \\\"miDefaultOptions.finalGatherPoints\\\" 30;\" " \
                    "-proj \"%(project)s\" -rd \"%(output)s\" -mr:art -mr:aml " \
                    "\"%(maya_file)s\"" % self.cfg_info
            else:
                cmd = "\"%(render_exe)s\" -s %(start)s -e %(end)s -b %(by)s " \
                    "-proj \"%(project)s\" -rd \"%(output)s\" -mr:art -mr:aml " \
                    "\"%(maya_file)s\"" % self.cfg_info

            print cmd
            sys.stdout.flush()

            if "single_frames" in self.cfg_info:
                if self.cfg_info["single_frames"]:
                    if self.cfg_info["start"] in self.cfg_info["single_frames"]:
                        print "Render this single frame."
                        subprocess.call(cmd)
                        return 0
                    else:
                        print "This frame doesn't need to be rendered."
                        return 0

            subprocess.call(cmd)


if __name__ == '__main__':
    KickRender(*sys.argv[1:])
