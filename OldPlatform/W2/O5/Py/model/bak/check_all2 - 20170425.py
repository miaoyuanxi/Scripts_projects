# ! /usr/bin/env python
# coding=utf-8
# Author: Liu Qiang
# Tel:    13811571784
# QQ:     386939142

import os
import sys
import re
if "maya" in sys.executable.lower():
    import maya.cmds as cmds
    # import pymel.core as pm


class Analyze(dict):

    def __init__(self, options):
        for i in options:
            self[i] = options[i]

    def run(self):
        ''

    def write_info_file(self):
        info_file_path = os.path.dirname(self["cg_info_file"])
        if not os.path.exists(info_file_path):
            os.makedirs(info_file_path)

        with open(self["cg_info_file"], "w") as f:
            f.write("Start::%s\n" % (self["start"]))
            f.write("End::%s\n" % (self["end"]))
            if "camera" in self:
                f.write("camera::%s\n" % (self["camera"]))


class MayaAnalyze(Analyze):

    def __init__(self, options):
        super(MayaAnalyze, self).__init__(options)

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
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--cgfl", dest="cg_file", type=str)
    # parser.add_argument("--cgin", dest="cg_info_file", type=str)
    # parser.add_argument("--cgsw", dest="cg_software", type=str)
    # parser.add_argument("--ti", dest="task_id", type=int)
    #
    # options = parser.parse_args().__dict__
    options = {}
    options["cg_file"] = cg_file
    options["cg_info_file"] = cg_info_file
    options["cg_software"] = cg_software

    analyze = eval(options["cg_software"]+"Analyze(options)")
    analyze.run()
    analyze.write_info_file()
