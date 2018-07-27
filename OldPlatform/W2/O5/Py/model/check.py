# ! /usr/bin/env python
# coding=utf-8
# Author: Liu Qiang
# Tel:    13811571784
# QQ:     386939142

import argparse
import os
import sys
import maya.standalone as standalone
standalone.initialize()
import maya.cmds as cmds


def analyze_maya(kwargs):
    cmds.file(kwargs["cg_file"], o=1, force=1, ignoreVersion=1, prompt=0)

    start = int(cmds.getAttr("defaultRenderGlobals.startFrame"))
    end = int(cmds.getAttr("defaultRenderGlobals.endFrame"))

    net_file_path = os.path.dirname(kwargs["net_file"])
    if not os.path.exists(net_file_path):
        os.makedirs(net_file_path)

    with open(kwargs["net_file"], "w") as f:
        f.write("Start::%s\n" % (start))
        f.write("End::%s\n" % (end))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--cf", dest="cg_file", type=str)
    parser.add_argument("--nf", dest="net_file", type=str)

    kwargs = parser.parse_args().__dict__
    analyze_maya(kwargs)
