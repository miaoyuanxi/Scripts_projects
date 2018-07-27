#! /usr/bin/env python
#coding=utf-8
import pymel.core as pm
import maya.cmds as cmds
import os
mapping={u'//192.168.80.222/MayaFiles/LZSH': u'N:', u'N:': u'N:'}
print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
print mapping
print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"

if mapping:
    all_vray_mesh = cmds.ls(exactType ="VRayMesh")
    if len(all_vray_mesh) != 0:
        for file_a in all_vray_mesh:
            file_path = cmds.getAttr(file_a+".fileName")
            file_path=file_path.replace('\\','/')
            for repath in mapping:
                if mapping[repath]!=repath:
                    if file_path.find(repath)>=0:
                        file_path_new=file_path.replace(repath,mapping[repath])
                        cmds.setAttr((file_a+".fileName"),file_path_new,type = "string")    
    
    
    all_file = cmds.ls(exactType ="file")
    if len(all_file) != 0:
        for file_a in all_file:
            file_path = cmds.getAttr(file_a+".fileTextureName")
            file_path=file_path.replace('\\','/')
            for repath in mapping:
                if mapping[repath]!=repath:
                    if file_path.find(repath)>=0:
                        file_path_new=file_path.replace(repath,mapping[repath])
                        cmds.setAttr((file_a+".fileTextureName"),file_path_new,type = "string") 

for i in pm.ls(type="VRaySettingsNode"):
    if i.hasAttr("srdml"):
        i.srdml.set(60000)
    if i.hasAttr("sys_distributed_rendering_on"):
        i.sys_distributed_rendering_on.set(False)
    if i.hasAttr("globopt_gi_dontRenderImage"):
        i.globopt_gi_dontRenderImage.set(False)
