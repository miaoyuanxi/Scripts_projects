#! /usr/bin/env python
#coding=utf-8
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
print "+++++++++++++++++++++++++++++++++the prerender strat++++++++++++++++++++++++++++++++++++++++++++++++"
maya_proj_paht = cmds.workspace(q=True, fullName=True)
source_path = "%s/sourceimages" % (maya_proj_paht)
scenes_path = "%s/scenes" % (maya_proj_paht)
render_node = pm.PyNode("defaultRenderGlobals")
yeti_load = cmds.pluginInfo("pgYetiMaya", query=True, loaded=True )
yeti_vray_load = cmds.pluginInfo("pgYetiVRayMaya", query=True, loaded=True )
shave_load = cmds.pluginInfo("shaveNode", query=True, loaded=True )
rep_path = ""
search = ""
dicts = {}


def rd_path():
    
    rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    render_node=pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()
    if render_name == "vray":
        rd_path = pm.PyNode("vraySettings").fnprx.get()
    print rd_path
    if rd_path is not None and type(rd_path) is type("a"):
        rd_path=rd_path.replace('\\','/').replace('//','/')
        p1=re.compile(r"^\w:/?")
        p2=re.compile(r"^/*")
        
        p3=re.compile(r"[^\w///<>. :]")
        p4=re.compile(r"//*")
        #print re.findall(p,rd_path)
        #p=re.compile("[.~!@#$%\^\+\*&/ \? \|:\.{}()<>';=\\"]")
        #print p.search(rd_path).group()
        #m=p.match(rd_path)
        rd_path=re.sub(p4,"/",rd_path)
        print rd_path
        rd_path = re.sub(p1,"",rd_path)
        print rd_path
        rd_path = re.sub(p2,"",rd_path)
        print rd_path
        rd_path = re.sub(p3,"",rd_path)
        rd_path = re.sub(" ","_",rd_path)
        sceneName = os.path.splitext(os.path.basename(pm.system.sceneName()))[0].strip()
        if '<Scene>' in rd_path:
            rd_path = rd_path.replace('<Scene>', sceneName)
        print "the output is %s " % rd_path
        pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(rd_path)
        if render_name == "vray":
            rd_path = pm.PyNode("vraySettings").fnprx.set(rd_path)
    else:
        pass

def change_path(node_type, attr_name, mapping, rep_path,dicts):
    print "the  node type  is %s" % (node_type)    
    maya_proj_paht = cmds.workspace(q=True, fullName=True)
    source_path = "%s/sourceimages" % (maya_proj_paht)
    scenes_path = "%s/scenes" % (maya_proj_paht)
    data_path = "%s/data" % (maya_proj_paht)
    all_node = pm.ls(type=node_type)
    if len(all_node) != 0:
        for node in all_node:
            if node.hasAttr(attr_name):
                #file_path = cmds.getAttr(node + "."+attr_name)
                refcheck = pm.referenceQuery(node, inr = True)
                print "refcheck %s " % (refcheck)
                if (refcheck == False):
                    try:              
                        node.attr(attr_name).set(l=0)
                    except Exception,error:
                        print Exception,":",error
                        pass
                file_path = node.attr(attr_name).get()
                if file_path != None and file_path.strip() !="" :
                    file_path = file_path.replace('\\', '/')
                    file_path = file_path.replace('<udim>', '1001')
                    file_path = file_path.replace('<UDIM>', '1001')
                    if os.path.exists(file_path) == 0:                        
                        asset_name = os.path.split(file_path)[1]
                        file_path_new = file_path
                        if rep_path:
                            file_path_new = "%s/%s" % (rep_path, asset_name)
                        if os.path.exists(file_path_new) == 0 and mapping:
                            for repath in mapping:
                                if mapping[repath] != repath:
                                    if file_path.find(repath) >= 0:
                                        file_path_new = file_path.replace(repath, mapping[repath])
                        
                        if os.path.exists(file_path_new) == 0:
                            file_path_new = "%s/%s" % (source_path, asset_name)
                        if os.path.exists(file_path_new) == 0:
                            file_path_new = "%s/%s" % (scenes_path, asset_name)
                        if os.path.exists(file_path_new) == 0 and dicts :
                            if asset_name in dicts:
                                file_path_new = dicts[asset_name]
                        
                        if os.path.exists(file_path_new) == 0:
                            print "the %s node %s  %s is not find ::: %s " % (node_type,node,attr_name,file_path)
                        else:
                            cmds.setAttr((node + "." + attr_name), file_path_new, type="string")

def replace_path(node_type, attr_name,rep_path,repath_new):
    maya_proj_paht = cmds.workspace(q=True, fullName=True)
    source_path = "%s/sourceimages" % (maya_proj_paht)
    scenes_path = "%s/scenes" % (maya_proj_paht)
    data_path = "%s/data" % (maya_proj_paht)
    all_node = pm.ls(type=node_type)
    if all_node:
        for node in all_node:
            #file_path = cmds.getAttr(node + "."+attr_name)
            refcheck = pm.referenceQuery(node, inr = True)
            if (refcheck == False):                
                node.attr(attr_name).set(l=0)
            file_path = node.attr(attr_name).get()
            #print file_path
            if file_path != None and file_path.strip() !="" :
                file_path_new = file_path.replace(repath, repath_new)
                cmds.setAttr((node + "." + attr_name), file_path_new, type="string")
                
def file_dicts(search):
    dicts = {}
    for parents, dirnames, filenames in os.walk(search):
        for filename in filenames:
            dicts[filename] = os.path.join(parents, filename)
    return dicts

def rep_path_def(mapping,old_path):
    if mapping:
        file_path_new=old_path
        for repath in mapping:
            if mapping[repath] != repath:
                if old_path.find(repath) >= 0:
                    file_path_new = old_path.replace(repath, mapping[repath]) 
        if os.path.exists(file_path_new):           
            return file_path_new
        else:
            return old_path
    else:
        return old_path
def get_graph_path(node):
    return cmds.getAttr(node+'.cacheFileName')
def set_graph_path(node, path):
    cmds.setAttr(node+'.cacheFileName', path)
def get_texture_node(graph_node):
    mel_cmd = 'pgYetiGraph -listNodes -type "texture" %s' % str(graph_node)
    texture_nodes = mel.eval(mel_cmd)
    return texture_nodes

def get_texture_path(texture, graph):
    mel_cmd = 'pgYetiGraph -node "%s" -param "file_name" -getParamValue %s' %(str(texture), str(graph))
    path = mel.eval(mel_cmd)
    return path
    
def set_texture_path(path, node, graph):
    mel_cmd = 'pgYetiGraph -node "{node_name}" -param "file_name" -setParamValueString {path}  {graph}'\
    .format(node_name=str(node), path=str(path), graph=str(graph))
    print mel_cmd

def set_yeti_imageSearchPath(mapping):   
    all_yeti_nodes = cmds.ls(type='pgYetiMaya')
    if len(all_yeti_nodes) != 0:
        for node_name in all_yeti_nodes:
            #cache = get_graph_path(node_name)
            tnodes = get_texture_node(node_name)
            yeti_dict={}
            yeti_texs=[] 
            #print node_name
            if tnodes != None:
                if len(tnodes) != 0:
                    for tx_node in tnodes:
                        texs = get_texture_path(tx_node, node_name)
                        texs = texs.replace('\\', '/')
                        texs = texs.replace('<udim>', '1001')
                        texs = texs.replace('<UDIM>', '1001')
                        if os.path.exists(texs) == 0 and texs != "" and texs != None :
                            tex_new_path = rep_path_def(mapping,texs)
                            #print tex_new_path
                            if os.path.exists(tex_new_path) == 0:
                                print "the %s node %s   is not find :: %s" % (node_name,tx_node,texs)

                            
                            yeti_texs.append(os.path.dirname(tex_new_path) )
                             
                    cmds.setAttr(node_name+".imageSearchPath",l=0)
                    yeti_searchpath = ";".join(yeti_texs)
                    cmds.setAttr(node_name+".imageSearchPath",yeti_searchpath ,type='string')
   
    
def pre_layer_mel():
    print '++++++++++++++++++pre_layer_mel +++++++++++++++++++++++++++++'
    if "pgYetiMaya" in plugins and "vrayformaya" in plugins:
        cmds.loadPlugin( "vrayformaya")
        cmds.loadPlugin( "pgYetiVRayMaya")   
    render_node=pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()
    yeti_load=cmds.pluginInfo("pgYetiMaya", query=True, loaded=True )
    print "the yeti load is %s " % yeti_load
    yeti_vray_load=cmds.pluginInfo("pgYetiVRayMaya", query=True, loaded=True )
    print "the yeti_vray_load load is %s " % yeti_vray_load
    shave_load=cmds.pluginInfo("shaveNode", query=True, loaded=True )
    print "the shave_load load is %s " % shave_load
    render_node.postMel.set(l=0)
    render_node.preRenderLayerMel.set(l=0)
    render_node.postRenderLayerMel.set(l=0)
    render_node.preRenderMel.set(l=0)
    render_node.postRenderMel.set(l=0)
    
    if render_name=="vray":
        print "++++++++++++++++ the renderer is vray+++++++++++++++++++++"
        if yeti_load and  yeti_vray_load and shave_load==False:
            mel.eval('pgYetiVRayPreRender;')
            #render_node.postMel.set("pgYetiVRayPostRende;")
            print render_node.postMel.get()
        if shave_load and yeti_load==False :
            mel.eval('shaveVrayPreRender;')
        if yeti_load and  yeti_vray_load and shave_load:
            mel.eval('shaveVrayPreRender;pgYetiVRayPreRender;')
        else:
            render_node.postMel.set("")
            render_node.preRenderLayerMel.set("")
            render_node.postRenderLayerMel.set("")
            render_node.preRenderMel.set("")
            render_node.postRenderMel.set("")
            
    elif render_name=="mentalRay":
        print "++++++++++++++++ the renderer is mentalRay++++++++++++++++++"
        if shave_load:
            #render_name = render_node.currentRenderer.get()
            
            render_node.preRenderMel.set("shave_MRFrameStart;")
            render_node.postRenderMel.set("shave_MRFrameEnd;")
            #mel.eval('shave_MRFrameStart')

            #render_node.preRenderLayerMel.set('python \"mel.eval(\\"pgYetiVRayPreRender\\")\"')
        else:
            render_node.preRenderMel.set("")
            render_node.postRenderMel.set("")
    else:
        print "++++++++++++++++ the renderer isnot vray mentalRay+++++++++++++++++++++++++"
        render_node.postMel.set("")
        render_node.preRenderLayerMel.set("")
        render_node.postRenderLayerMel.set("")
        render_node.preRenderMel.set("")
        render_node.postRenderMel.set("")
def del_node(node_name):     
    if pm.objExists(node_name):
        try:
            
            tran = pm.listTransforms(node_name)
             
            for a in tran:
                
                pm.delete(a) 
                print "the %s is del " % (a) 
        except:
            print "the %s dont del " % (node_name) 
            pass 

def set_cam_render(cams):
    print "multiple cams to cmd"
    cams_list = cams.split(',')
    
    cams_all = pm.ls(type='camera')
    for cam in cams_all:
        mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % cam)
        if cam not in cams_list:
            cmds.setAttr(cam + ".renderable", 0)
        else:
            cmds.setAttr(cam + ".renderable", 1)

def set_layer_render(layers):
    print "multiple render layer to cmd"
    layers_list = layers.split(',')
    
    layers_all = cmds.listConnections("renderLayerManager.renderLayerId")
    for layer in layers_all:
        mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % layer)
        if layer not in layers_list:
            cmds.setAttr(layer + ".renderable", 0)
        else:
            cmds.setAttr(layer + ".renderable", 1)
          
pre_layer_mel()
if rendersetting:
    if 'renderableLayer' in rendersetting :
        if "," in rendersetting['renderableLayer']:
            set_layer_render(rendersetting['renderableLayer'])

attr_list = [{"VRayMesh": "fileName"}, {"AlembicNode": "abc_File"},{"pgYetiMaya": "groomFileName"},{"pgYetiMaya": "cacheFileName"},\
            {"aiImage": "filename"},{"RMSGeoLightBlocker": "Map"},{"PxrStdEnvMapLight": "Map"},{"VRaySettingsNode": "imap_fileName2"},\
            {"VRaySettingsNode": "pmap_file2"},{"VRaySettingsNode": "lc_fileName"},{"VRaySettingsNode": "shr_file_name"},{"VRaySettingsNode": "causticsFile2"},\
            {"VRaySettingsNode": "shr_file_name"},{"VRaySettingsNode": "imap_fileName"},{"VRaySettingsNode": "pmap_file"},{"VRaySettingsNode": "fileName"},\
            {"VRaySettingsNode": "shr_file_name"},{"VRayLightIESShape": "iesFile"},{"diskCache": "cacheName"},{"miDefaultOptions": "finalGatherFilename"},\
            {"RealflowMesh": "Path"},{"aiStandIn": "dso"},{"mip_binaryproxy": "object_filename"},{"mentalrayLightProfile": "fileName"},{"aiPhotometricLight": "ai_filename"},\
            {"VRayVolumeGrid": "inFile"},{"file":"fileTextureName"},{"RedshiftDomeLight":"tex0"},{"RedshiftSprite":"tex0"},{"ExocortexAlembicXform":"fileName"},{"ffxDyna":"output_path"},\
            {"ffxDyna":"wavelet_output_path"},{"ffxDyna":"postprocess_output_path"},{"RedshiftIESLight":"profile"},{"RedshiftDomeLight":"tex1"},\
            {"RedshiftEnvironment":"tex0"},{"RedshiftEnvironment":"tex1"},{"RedshiftEnvironment":"tex2"},{"RedshiftEnvironment":"tex3"},{"RedshiftEnvironment":"tex4"},{"RedshiftLensDistortion":"LDimage"},\
            {"RedshiftLightGobo":"tex0"},{"RedshiftNormalMap":"tex0"},{"RedshiftOptions":"irradianceCacheFilename"},{"RedshiftOptions":"photonFilename"}, {"RedshiftOptions":"irradiancePointCloudFilename"},{"RedshiftOptions":"subsurfaceScatteringFilename"},\
            {"RedshiftProxyMesh":"fileName"},{"RedshiftVolumeShape":"fileName"},{"RedshiftBokeh":"dofBokehImage"},{"RedshiftCameraMap":"tex0"},{"RedshiftDisplacement":"texMap"}]
            #,{"houdiniAsset":"otlFilePath"}]    

pre_layer_mel()             
if user_id in [1850226]:
    print start
    if start:
        cmds.currentTime(int(start),edit=True)
if user_id in [1852657]:
    mel.eval('source "C:/Program Files/Domemaster3D/maya/common/scripts/domeRender.mel"; domemaster3DPreRenderMEL();')
if user_id in [962413,1844068]:
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad) 

print user_id
if user_id in [1818411]:
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad)
if user_id in [963567]:
    print plugins
    print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
    print mapping
    print "rendersetting"
    print rendersetting
    print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
    print user_id

    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)
if user_id in [1017637]:

    print plugins
    print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
    print mapping
    print "rendersetting"
    print rendersetting
    print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
    print user_id

    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)
                            
    if "pgYetiMaya" not in plugins or "vrayformaya" not in plugins:
        render_node.postMel.set("")

    del_node('SGFC_sc05_sh01_ly_yong:SGFC_ch010001SwimsuitGirl_l_msAnim:Facial_PanelShape')
    del_node("SGFC_ch008001Policeman1_h_msAnim:Facial_PanelShape")
    del_node("aiAreaLightShape1309")
    del_node("Facial_PanelShape")
    
    del_node("aiAreaLightShape1309")
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad)  

    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("imap_multipass"):
            if taskid in [9350799]:
                i.attr('imap_multipass').set(0)
                print "set imap_multipass to false" 

                
        
        if i.hasAttr("srdml"):
            #dml = 48000
            dml =i.srdml.get()
            print "the scene vray srdml %s MB" %(dml)
            if taskid in [9350799]:
                print taskid
                i.srdml.set(20000)
                print "change vray srdml to  %s MB" %(i.srdml.get())
        if rendersetting:
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(rendersetting['width'])
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(rendersetting['height'])            

        if i.hasAttr("sys_distributed_rendering_on"):
            i.sys_distributed_rendering_on.set(False)
        if i.hasAttr("globopt_gi_dontRenderImage"):
            i.globopt_gi_dontRenderImage.set(False)  
    # all_image = cmds.ls(exactType ="cacheFile")
    # if len(all_image) != 0:
        # for a in all_image:        
            # b = cmds.getAttr(a+".cacheName")
            # c = cmds.getAttr(a+".cachePath")
            # print (c+"/"+b+".xml")
            # cmds.setAttr((a+".cachePath"),r"X:/data",type="string")


                        
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(1)
        i.log_verbosity.set(0)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(10240)
        i.absoluteTexturePaths.set(0)
        i.absoluteProceduralPaths.set(0)
        
        print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
        #setAttr "defaultArnoldRenderOptions.absoluteProceduralPaths" 0;
        #i.procedural_searchpath.set(r"N:\cg_custom_setup\network\arnold\htoa-1.11.1_r1692_houdini-15.0.393_windows\arnold\procedurals")
        
        i.shader_searchpath.set(source_path)
        i.texture_searchpath.set(source_path)
        #setAttr -type "string" defaultArnoldRenderOptions.procedural_searchpath ;
if user_id in [1840038]:
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(1)
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(40960)
        i.absoluteTexturePaths.set(0)
        i.absoluteProceduralPaths.set(0)
        print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ") 
if user_id in [1840793]:
    for i in pm.ls(type="VRaySettingsNode"):
        if rendersetting:
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(rendersetting['width'])
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(rendersetting['height'])     
    # if i.hasAttr("srdml"):
        # if taskid in [9277600,9277601]:
            # dml = 2500
        # i.srdml.set(dml)
        # print "set vray srdml %s MB" %(dml)
    if taskid in [9289969]:
        mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")                
if user_id in [1846319]:
    for i in pm.ls(type="resolution"):
        if rendersetting:
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(int(rendersetting['width']))
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(int(rendersetting['height']))  

if user_id in [1848725]:
    for i in pm.ls(type="VRaySettingsNode"):
        if rendersetting:
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(rendersetting['width'])
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(rendersetting['height'])    

                
if user_id in [1818014]:
    for i in pm.ls(type="VRaySettingsNode"):
        if rendersetting:
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(rendersetting['width'])
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(rendersetting['height'])
                
if user_id in [1855835]:
    for i in pm.ls(type="VRaySettingsNode"):
        if rendersetting:
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(rendersetting['width'])
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(rendersetting['height'])
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
if user_id in [1843589]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(32000)
if user_id in [1852550]:
    for i in pm.ls(type="pgYetiMaya"):
        print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(0)
        print "abortOnError off"
if user_id in [1844577,1857698,1853469]:
    for i in pm.ls(type="pgYetiMaya"):
        print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)        
if user_id in [1300061]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(30000)
            print "set vray srdml 30000"
        # if i.hasAttr("sys_distributed_rendering_on"):
            # i.sys_distributed_rendering_on.set(False)
        # if i.hasAttr("globopt_gi_dontRenderImage"):
            # i.globopt_gi_dontRenderImage.set(False)
            
if user_id in [1805679]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(30000)
            print "set vray srdml 30000"
            
if user_id in [1843088]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(30000)
            print "set vray srdml 30000"
# if user_id in [1843589]:
    # print "set vray srdml "
    # for i in pm.ls(type="VRaySettingsNode"):
        # if i.hasAttr("srdml"):
            # i.srdml.set(0)
            # print "set vray srdml 0"
if user_id in [1814431]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
if user_id in [1820999]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
# if user_id in [1858637]:
    # print start
    # if start:
        # cmds.currentTime(int(start),edit=True)
if user_id in [830123]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(50000)
            print "set vray srdml 0"            
if user_id in [1844577]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(55000)
            print "set vray srdml 55000"

if user_id in [963260]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
            
if user_id in [1843698]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(32000)
        if i.hasAttr("sys_distributed_rendering_on"):
            i.sys_distributed_rendering_on.set(False)
        if i.hasAttr("globopt_gi_dontRenderImage"):
            i.globopt_gi_dontRenderImage.set(False)
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts) 
            
if user_id in [1859047]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(48000)
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")                          
if user_id in [964311]:
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)  
                          
if user_id in [1816685]:
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)  

if user_id in [1832581]:
    print mapping
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)
if user_id in [1848484]:
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)  
            
if user_id in [1848680]:
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)
if user_id in [962539]:
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)
    for i in pm.ls(type="aiOptions"):
        #print "defaultArnoldRenderOptions.abortOnError 0"
        #i.abortOnError.set(1)
        i.log_verbosity.set(0)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        i.absoluteTexturePaths.set(0)
        i.absoluteProceduralPaths.set(0)
        source_path="%s/sourceimages" % (maya_proj_paht)
        i.shader_searchpath.set(source_path)
        i.texture_searchpath.set(source_path)
        
        
if user_id in [965281]:
    print start
    if start:
        cmds.currentTime(int(start),edit=True)
if user_id in [1834714]:
    mel.eval('setUpAxis \"Y\";')
    print start
    if start:
        cmds.currentTime(int(start),edit=True)
if user_id in [963909]:
    mel.eval('setUpAxis \"Z\";')
    print start
    if start:
        cmds.currentTime(int(start),edit=True)
if user_id in [963447]:
    print start
    if start:
        cmds.currentTime(int(start),edit=True)
    for i in pm.ls(type="pgYetiMaya"):
        print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
    # for i in pm.ls(type="aiOptions"):
        # i.motion_blur_enable.set(0)
        # print "defaultArnoldRenderOptions.motion_blur_enable 0"

if user_id in [961743,1844765]:
    print "  "
    cmds.setAttr("redshiftOptions.maxNumGPUMBForForICPHierarchy",256)
    rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    if "<RenderLayer>" not in  rd_path:        
        rd_path += "/<RenderLayer>"
        print rd_path
        pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(rd_path)
if user_id in [1844953,1847323,1831205]:
    for i in pm.ls(type='aiOptions'):
        if i.hasAttr("autotx"):
            print "autotx is false"
            i.autotx.set(False)
if user_id in [1848099]:
    for i in pm.ls(type='aiOptions'):
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        print "autotx is OFF"
if user_id in [1819610]:
    print "  "
    rd_path()
    
    cmds.setAttr("redshiftOptions.maxNumGPUMBForForICPHierarchy",256)  
    
if user_id in [1814856]:
    print user_id
    print plugins
    print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
    print mapping
    print "+++++++++++++++++++++++mapping+++++++++++++++++++++++"
    render_node.postMel.set(l=0)
    render_node.postMel.set("")
    render_node.preRenderLayerMel.set(l=0)
    render_node.preRenderLayerMel.set("")
    render_node.postRenderLayerMel.set(l=0)
    render_node.postRenderLayerMel.set("")
    render_node.preRenderMel.set(l=0)
    render_node.preRenderMel.set("")
    render_node.postRenderMel.set(l=0)
    render_node.postRenderMel.set("")
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)
    set_yeti_imageSearchPath(mapping)        
if user_id in [1815272]:
    rd_path()
    pre_layer_mel()
    # for i in pm.ls(type="aiOptions"):
        # i.abortOnError.set(0)
        # print 'abortOnError-off'
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        print 'abortOnError-off'
if user_id in [1016752]:
    rd_path()
    pre_layer_mel()

if user_id in [1848903]:
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)
if user_id in [1852464]:
    if taskid in [5347743]:
        for i in pm.ls(type="aiOptions"):
            i.abortOnError.set(0)
            print "abort On Error turn off"
if user_id in [9271787]:
    mel.eval("optionVar  -iv \"miUseMayaAlphaDetection\" 1; ")
if user_id in [1814593,119602]:
    mel.eval("optionVar  -iv \"renderSetupEnable\" 0;")
if user_id in [1813119]:
    render_node.preRenderLayerMel.set("")
    render_node.postRenderLayerMel.set("")
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
if user_id in [1859072,1859047]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
print "**********************************************the prerender end******************************************************"