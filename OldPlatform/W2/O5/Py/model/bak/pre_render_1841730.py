#! /usr/bin/env python
#coding=utf-8
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
def set_layer_render(layers):
    layers_list = layers.split(',')
    print "multiple render layer to cmd"
    print layers_list
    layers_all = cmds.listConnections("renderLayerManager.renderLayerId")
    for layer in layers_all:
        mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % layer)
        if layer not in layers_list:
            cmds.setAttr(layer + ".renderable", 0)
        else:
            cmds.setAttr(layer + ".renderable", 1)
if rendersetting:
    if 'renderableLayer' in rendersetting :
        if "," in rendersetting['renderableLayer']:
            set_layer_render(rendersetting['renderableLayer'])
