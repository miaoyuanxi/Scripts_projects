#! /usr/bin/env python
#coding=utf-8
import pymel.core as pm
import maya.cmds as cmds
import os,sys,re
maya_proj_paht = cmds.workspace(q=True, fullName=True)
render_node=pm.PyNode("defaultRenderGlobals")
def rd_path():
    rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    
    render_name = render_node.currentRenderer.get()
    if render_name=="vray":
        rd_path = pm.PyNode("vraySettings").fnprx.get()
    print rd_path
    rd_path=rd_path.replace('\\','/').replace('//','/')
    p1=re.compile(r"^\w:/?")
    p2=re.compile(r"^/*")
    
    p3=re.compile(r"[^\w///<> :]")
    p4=re.compile(r"//*")
    #print re.findall(p,rd_path)
    #p=re.compile("[.~!@#$%\^\+\*&/ \? \|:\.{}()<>';=\\"]")
    #print p.search(rd_path).group()
    #m=p.match(rd_path)
    rd_path=re.sub(p4,"/",rd_path)
    print rd_path
    rd_path= re.sub(p1,"",rd_path)
    print rd_path
    rd_path=re.sub(p2,"",rd_path)
    print rd_path
    rd_path=re.sub(p3,"",rd_path)
    rd_path=re.sub(" ","_",rd_path)
    print rd_path
    pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(rd_path)



if user_id in [962413]:
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad)        
print user_id


if user_id in [1017637]:
    print plugins
    print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
    print mapping
    print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
    print user_id
    if mapping:
        all_file = cmds.ls(exactType ="VRayMesh")
        if len(all_file) != 0:
            for file_a in all_file:
                file_path = cmds.getAttr(file_a+".fileName")
                file_path=file_path.replace('\\','/')
                for repath in mapping:
                    if mapping[repath]!=repath:
                        if file_path.find(repath)>=0:
                            file_path_new=file_path.replace(repath,mapping[repath])
                            cmds.setAttr((file_a+".fileName"),file_path_new,type = "string")    
        all_file = cmds.ls(exactType ="aiStandIn")
        if len(all_file) != 0:
            for file_a in all_file:
                file_path = cmds.getAttr(file_a+".dso")
                file_path=file_path.replace('\\','/')
                for repath in mapping:
                    if mapping[repath]!=repath:
                        if file_path.find(repath)>=0:
                            file_path_new=file_path.replace(repath,mapping[repath])
                            cmds.setAttr((file_a+".dso"),file_path_new,type = "string")
        all_file = cmds.ls(exactType ="aiImage")
        if len(all_file) != 0:
            for file_a in all_file:
                file_path = cmds.getAttr(file_a+".filename")
                file_path=file_path.replace('\\','/')
                for repath in mapping:
                    if mapping[repath]!=repath:
                        if file_path.find(repath)>=0:
                            file_path_new=file_path.replace(repath,mapping[repath])
                            cmds.setAttr((file_a+".filename"),file_path_new,type = "string")                            
    if "pgYetiMaya" not in plugins or "vrayformaya" not in plugins:
        render_node.postMel.set("")
    
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            #dml = 48000
            dml =i.srdml.get()
            print "the scene vray srdml %s MB" %(dml)

        if i.hasAttr("sys_distributed_rendering_on"):
            i.sys_distributed_rendering_on.set(False)
        if i.hasAttr("globopt_gi_dontRenderImage"):
            i.globopt_gi_dontRenderImage.set(False)
            
        if i.hasAttr("imap_fileName"):
            file_path = cmds.getAttr(i+".imap_fileName")
            if file_path != None:
                file_path=file_path.replace('\\','/')
                for repath in mapping:
                    if mapping[repath]!=repath:
                        if file_path.find(repath)>=0:
                            file_path_new=file_path.replace(repath,mapping[repath])
                            cmds.setAttr((i+".imap_fileName"),file_path_new,type = "string")
        if i.hasAttr("fileName"):
            file_path = cmds.getAttr(i+".fileName")
            if file_path != None:
                file_path=file_path.replace('\\','/')
                for repath in mapping:
                    if mapping[repath]!=repath:
                        if file_path.find(repath)>=0:
                            file_path_new=file_path.replace(repath,mapping[repath])
                            cmds.setAttr((i+".fileName"),file_path_new,type = "string")
                        
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(1)
        i.log_verbosity.set(0)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        i.absoluteTexturePaths.set(0)
        i.absoluteProceduralPaths.set(0)
        
        print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
        #setAttr "defaultArnoldRenderOptions.absoluteProceduralPaths" 0;
        #i.procedural_searchpath.set(r"N:\cg_custom_setup\network\arnold\htoa-1.11.1_r1692_houdini-15.0.393_windows\arnold\procedurals")
        source_path="%s/sourceimages" % (maya_proj_paht)
        i.shader_searchpath.set(source_path)
        i.texture_searchpath.set(source_path)
        #setAttr -type "string" defaultArnoldRenderOptions.procedural_searchpath ;
                
if user_id in [1833080]:
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad)  
if user_id in [1833042]:
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad)         
if user_id in [1833047]:
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad)

# if user_id in [1820999]:
    # print "set vray srdml "
    # print taskid
    # for i in pm.ls(type="VRaySettingsNode"):
        # if i.hasAttr("srdml"):
            # dml = 20000            
            # if taskid in [9183335,9183346,9183337,9183224]:
                # dml = 32000
            # i.srdml.set(dml)
            # print "set vray srdml %s MB" %(dml)

if user_id in [1832764]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(48000)
        if i.hasAttr("sys_distributed_rendering_on"):
            i.sys_distributed_rendering_on.set(False)
        if i.hasAttr("globopt_gi_dontRenderImage"):
            i.globopt_gi_dontRenderImage.set(False)
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad)
        
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(1)
        i.log_verbosity.set(1)
    for i in pm.ls(type="pgYetiMaya"):
        print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
        
if user_id in [1843698]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(32000)
        if i.hasAttr("sys_distributed_rendering_on"):
            i.sys_distributed_rendering_on.set(False)
        if i.hasAttr("globopt_gi_dontRenderImage"):
            i.globopt_gi_dontRenderImage.set(False)
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
                          
if user_id in [964311]:

    if mapping:
        all_file = cmds.ls(exactType ="file")
        if len(all_file) != 0:
            #print all_file
            for file_a in all_file:
                file_path = cmds.getAttr(file_a+".fileTextureName")
                file_path=file_path.replace('\\','/')
                for repath in mapping:
                    if mapping[repath]!=repath:
                        if file_path.find(repath)>=0:
                            file_path_new=file_path.replace(repath,mapping[repath])
                            cmds.setAttr((file_a+".fileTextureName"),file_path_new,type = "string")
        all_file = cmds.ls(exactType ="RedshiftDomeLight")
        if len(all_file) != 0:
            for file_a in all_file:
                file_path = cmds.getAttr(file_a+".tex0")
                file_path=file_path.replace('\\','/')
                for repath in mapping:
                    if mapping[repath]!=repath:
                        if file_path.find(repath)>=0:
                            file_path_new=file_path.replace(repath,mapping[repath])
                            cmds.setAttr((file_a+".tex0"),file_path_new,type = "string")
        all_file = cmds.ls(exactType ="RedshiftSprite")
        if len(all_file) != 0:
            print all_file
            for file_a in all_file:
                file_path = cmds.getAttr(file_a+".tex0")
                file_path=file_path.replace('\\','/')
                for repath in mapping:
                    if mapping[repath]!=repath:
                        if file_path.find(repath)>=0:
                            file_path_new=file_path.replace(repath,mapping[repath])
                            cmds.setAttr((file_a+".tex0"),file_path_new,type = "string") 
if user_id in [961743]:
    print "  "
    cmds.setAttr("redshiftOptions.maxNumGPUMBForForICPHierarchy",256)                            
if user_id in [1844953,1847323]:
    for i in pm.ls(type='aiOptions'):
        if i.hasAttr("autotx"):
            print "autotx is false"
            i.autotx.set(False)

if user_id in [1819610]:
    print "  "
    rd_path()
    
    cmds.setAttr("redshiftOptions.maxNumGPUMBForForICPHierarchy",256)  