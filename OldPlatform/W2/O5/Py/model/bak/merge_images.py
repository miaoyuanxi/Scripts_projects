#! /usr/bin/env python
# coding=utf-8
import sys
import os
import nuke
import pprint
if sys.version_info[:2] == (2, 5):
    if sys.platform.startswith("win"):
        sys.path.append(os.path.join(os.path.dirname(__file__), "tim", "py25"))

import argparse

def set_format(width,height ):
    newFormat = nuke.addFormat('%s %s 1 new' % (width,height))
    nuke.Root()['format'].setValue(newFormat)

def create_read(file_path):
    node = nuke.createNode('Read')
    node['file'].fromUserText(file_path)
    return node

def merge(kwargs):
    # pprint.pprint(kwargs)

    #set_format(kwargs["width"],kwargs["height"])
    
    read_nodes = []
    for i in kwargs["tile_files"]:
        read_nodes.append(create_read(i))

    # for i in read_nodes:
    #     i['selected'].setValue(True)

    # merge = nuke.nodes.Merge2(inputs = read_nodes)

    merge = nuke.createNode('Merge2')
    x=0
    for i in read_nodes:
        if x==2:
            x+=1
            #print i.name()
            merge.setInput(x,i)
            x+=1
        else:
            merge.setInput(x,i)
            x+=1
    merge["operation"].setValue("max")
    merge["also_merge"].setValue("all")

    tile_output_folder = os.path.dirname(kwargs["tile_output"])
    if not os.path.exists(tile_output_folder):
        os.makedirs(tile_output_folder)

    write = nuke.nodes.Write(inputs=[merge], file=kwargs["tile_output"])
    write["channels"].setValue("all")
    nuke.execute(write.name(), 1, 1, 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Liu Qiang || MMmaomao')
    parser.add_argument("-tiles", dest="tiles", type=int)
    parser.add_argument("-tile_files", dest="tile_files", type=str)
    parser.add_argument("-tile_output", dest="tile_output", type=str)
    parser.add_argument("-width", dest="width", type=int)
    parser.add_argument("-height", dest="height", type=int)

    kwargs = parser.parse_args().__dict__

    kwargs["tile_files"] = eval(kwargs["tile_files"])
    merge(kwargs)
