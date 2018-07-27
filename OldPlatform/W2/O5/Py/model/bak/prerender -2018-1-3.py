#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
print "+++++++++++++++++++++++++++++++++the prerender strat++++++++++++++++++++++++++++++++++++++++++++++++"
pm.lockNode( 'defaultRenderGlobals', lock=False )
maya_proj_paht = cmds.workspace(q=True, fullName=True)
source_path = "%s/sourceimages" % (maya_proj_paht)
scenes_path = "%s/scenes" % (maya_proj_paht)
render_node = pm.PyNode("defaultRenderGlobals")
render_name = render_node.currentRenderer.get()
yeti_load = cmds.pluginInfo("pgYetiMaya", query=True, loaded=True )
yeti_vray_load = cmds.pluginInfo("pgYetiVRayMaya", query=True, loaded=True )
shave_load = cmds.pluginInfo("shaveNode", query=True, loaded=True )

rep_path = ""
search = ""
dicts = {}

def resetup():
    default_globals = pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()
    if render_name=="vray":        
        vraySettings = pm.PyNode("vraySettings")    
        dynMemLimit = vraySettings.sys_rayc_dynMemLimit.get()
        print "dynMemLimit  is : %s" % str(dynMemLimit)    
    #-------Renumber frames   is off-----
    default_globals.modifyExtension.set(0)
    print "Set Renumber frames   is off"
    print "get you scene attritubes>>>>>>>>>>>"
    for i in pm.ls(type="aiAOVDriver"):
        if i.hasAttr("append"):
            i.append.set(0)     
            print "set   Append   off"    
    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("textureMaxMemoryMB"):
            textureMaxMemoryMB = i.textureMaxMemoryMB.get()
            print "Scene textureMaxMemoryMB is :%s" % str(textureMaxMemoryMB)        
        if i.hasAttr(" Scene abortOnError"):
            abortOnError = i.abortOnError.get()
            print "Scene abortOnError is : %s" % str(abortOnError)
        if i.hasAttr("log_verbosity"):
            log_verbosity = i.log_verbosity.get()
            print "Scene log_verbosity  is: %s" % str(log_verbosity)
            i.log_verbosity.set(1)
            print "set log_verbosity to 1"
        if i.hasAttr("autotx"):
            autotx = i.autotx.get()
            print "Scene autotx is : %s" % str(autotx)
            i.autotx.set(False)
            print "set autotx to False"
    print "get you scene attritubes end >>>>>>>>>>>"
    for i in pm.ls(type="pgYetiMaya"):
        if i.hasAttr("aiLoadAtInit"):
            i.aiLoadAtInit.set(1)
            print "%s .aiLoadAtInit 1" % (i)
            
    # for i in pm.ls(type="VRaySettingsNode"):
        # if i.hasAttr("srdml"):
            # i.srdml.set(0)
            # print "set vray srdml 0"            
                    
    for i in pm.ls(type="aiStandIn"):
        if i.hasAttr("deferStandinLoad"):
            i.deferStandinLoad.set(0)
            print "set %s to 0" % (i.deferStandinLoad) 
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    sys.stdout.flush()
    #------set Frame/Animation ext: name.#.ext---
    #mel.eval("setMayaSoftwareFrameExt(3,0);")


def rd_path():
    
    rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    render_node=pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()
    if render_name == "vray":
        rd_path = pm.PyNode("vraySettings").fnprx.get()
    print rd_path
    if rd_path is not None:
        print "change output path"
        rd_path=rd_path.replace('\\','/').replace('//','/')
        p1=re.compile(r"^\w:/?")
        p2=re.compile(r"^/*")
        
        p3=re.compile(r"[^\w///<>.% :]")
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
        print rd_path
        sceneName = os.path.splitext(os.path.basename(pm.system.sceneName()))[0].strip()
        if '<Scene>' in rd_path:
            rd_path = rd_path.replace('<Scene>', sceneName)
        if '%s' in rd_path:
            rd_path = rd_path.replace('%s', sceneName)
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
                #print "refcheck %s " % (refcheck)
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
def change_path_mapping(node_type, attr_name, mapping):
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
                
                if (refcheck == False):
                    try:              
                        node.attr(attr_name).set(l=0)
                    except Exception,error:
                        print Exception,":",error
                        pass
                file_path = node.attr(attr_name).get()
                if file_path != None and file_path.strip() !="" :
                    file_path = file_path.replace('\\', '/')
                    if os.path.exists(file_path) == 0:                        
                        asset_name = os.path.split(file_path)[1]
                        file_path_new = file_path
                        print file_path_new
                        if os.path.exists(file_path_new) == 0 and mapping:
                            for repath in mapping:
                                if mapping[repath] != repath:
                                    if file_path.find(repath) >= 0:
                                        file_path_new = file_path.replace(repath, mapping[repath])
                                        print file_path_new                        
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
            print file_path
            if file_path != None and file_path.strip() !="" :
                file_path_new = file_path.replace(rep_path, repath_new)
                print file_path_new
                cmds.setAttr((node + "." + attr_name), file_path_new, type="string")
                print "%s %s %s " % (node,attr_name,file_path_new)
                
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

def del_cam(cams):
    print "multiple cams to cmd"
    cams_all = pm.ls(type='camera')
    if cams:
        cams_list = cams.split(',')    
    
        for cam in cams_all:
            mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % cam)
            if cam not in cams_list:
                try:                    
                    del_node(cam)
                    
                except:
                    print "the %s dont del " % (cam) 
                    pass 
            else:
                print "the cam %s is render" % (cam)
    else:
        for cam in cams_all:
            mel.eval('removeRenderLayerAdjustmentAndUnlock("%s.renderable")' % cam)
            if cmds.getAttr(cam + ".renderable")==0:
                try:
                    del_node(cam)
                    
                except:
                    print "the %s dont del " % (cam) 
                    pass 
            else:
                print "the cam %s is render" % (cam)
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

def GetCurrentRenderer():
    """Returns the current renderer."""
    renderer=str(pm.mel.currentRenderer())
    if renderer == "_3delight":
        renderer="3delight"
        
    return renderer




def unicode_to_str(str1,str_encode = 'system'):
    if isinstance(str1,unicode):
        try:
            if str_encode.lower() == 'system':
                str1=str1.encode(sys.getfilesystemencoding())
            elif str_encode.lower() == 'utf-8':
                str1 = str1.encode('utf-8')
            elif str_encode.lower() == 'gbk':
                str1 = str1.encode('gbk')
            else:
                str1 = str1.encode(str_encode)
        except Exception as e:
            print '[err]unicode_to_str:encode %s to %s failed' % (str1,str_encode)
            print e
    else:
        print '%s is not unicode ' % (str1)
    return str1

#get mel-------------------------------
def getMel():
    all_mel = {}
    default_globals = pm.PyNode("defaultRenderGlobals")
    renderer = str(GetCurrentRenderer())
    all_mel['renderer'] = renderer
    if renderer == "redshift":
        render_node = pm.PyNode("redshiftOptions")
        render_node.preRenderMel.set(l=0)
        render_node.postRenderMel.set(l=0)
        render_node.preRenderLayerMel.set(l=0)
        render_node.postRenderLayerMel.set(l=0)
        render_node.preRenderFrameMel.set(l=0)
        render_node.postRenderFrameMel.set(l=0)      
        all_mel['preRenderMel'] = unicode_to_str(render_node.preRenderMel.get())
        all_mel['postRenderMel'] = unicode_to_str(render_node.postRenderMel.get())
        all_mel['preRenderLayerMel'] = unicode_to_str(render_node.preRenderLayerMel.get())
        all_mel['postRenderLayerMel'] = unicode_to_str(render_node.postRenderLayerMel.get())
        all_mel['preRenderFrameMel'] = unicode_to_str(render_node.preRenderFrameMel.get())
        all_mel['postRenderFrameMel'] = unicode_to_str(render_node.postRenderFrameMel.get())
        render_node.preRenderMel.set("")
        render_node.postRenderMel.set("")
        render_node.preRenderLayerMel.set("")
        render_node.postRenderLayerMel.set("")
        render_node.preRenderFrameMel.set("")
        render_node.postRenderFrameMel.set("")  

    else:
        render_node = pm.PyNode("defaultRenderGlobals")
        render_node.preMel.set(l=0)
        render_node.postMel.set(l=0)
        render_node.preRenderLayerMel.set(l=0)
        render_node.postRenderLayerMel.set(l=0)
        render_node.preRenderMel.set(l=0)
        render_node.postRenderMel.set(l=0)
        all_mel['preRenderMel'] = unicode_to_str(render_node.preMel.get())
        all_mel['postRenderMel'] = unicode_to_str(render_node.postMel.get())
        all_mel['preRenderLayerMel'] = unicode_to_str(render_node.preRenderLayerMel.get())
        all_mel['postRenderLayerMel'] = unicode_to_str(render_node.postRenderLayerMel.get())
        all_mel['preRenderFrameMel'] = unicode_to_str(render_node.preRenderMel.get())
        all_mel['postRenderFrameMel'] = unicode_to_str(render_node.postRenderMel.get())
        render_node.preMel.set("")
        render_node.postMel.set("")
        render_node.preRenderLayerMel.set("")
        render_node.postRenderLayerMel.set("")
        render_node.preRenderMel.set("")
        render_node.postRenderMel.set("")
        if renderer == "vray":
            vraySettings = pm.PyNode("vraySettings")
            all_mel['preKeyframeMel'] = unicode_to_str(vraySettings.preKeyframeMel.get())
            all_mel['rtImageReadyMel'] = unicode_to_str(vraySettings.rtImageReadyMel.get())
            vraySettings.preKeyframeMel.set("")
            vraySettings.rtImageReadyMel.set("")

    return all_mel


#conduct mel --------------------------
def ConductMel():
    print '++++++++++++++++++pre_layer_mel +++++++++++++++++++++++++++++'
    # if "pgYetiMaya" in plugins and "vrayformaya" in plugins:
        # cmds.loadPlugin( "vrayformaya")
        # cmds.loadPlugin( "pgYetiVRayMaya")   
    render_node=pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()
    yeti_load=cmds.pluginInfo("pgYetiMaya", query=True, loaded=True )
    print "the yeti load is %s " % yeti_load
    yeti_vray_load=cmds.pluginInfo("pgYetiVRayMaya", query=True, loaded=True )
    print "the yeti_vray_load load is %s " % yeti_vray_load
    shave_load=cmds.pluginInfo("shaveNode", query=True, loaded=True )
    print "the shave_load load is %s " % shave_load

    all_mel_dict = getMel()
    print "Mel dict is : %s" % all_mel_dict
    sys.stdout.flush()
    preRenderMel = all_mel_dict['preRenderMel']
    if preRenderMel:
        # print "preRenderMel is : %s" % preRenderMel    
        try:
            pass
            # mel.eval(preRenderMel)
        except Exception as e:
            print '[err]Conduct preRenderMel failed'
            print e
    
    if render_name=="vray":

        print "++++++++++++++++ the renderer is vray+++++++++++++++++++++"
        if yeti_load and  yeti_vray_load and shave_load==False:
            mel.eval('pgYetiVRayPreRender;')
        if shave_load and yeti_load==False :
            mel.eval('shaveVrayPreRender;')
        if yeti_load and  yeti_vray_load and shave_load:
            mel.eval('shaveVrayPreRender;pgYetiVRayPreRender;')
            
    elif render_name=="mentalRay":
        print "++++++++++++++++ the renderer is mentalRay++++++++++++++++++"
        if shave_load:            
            render_node.preRenderMel.set("shave_MRFrameStart;")
            render_node.postRenderMel.set("shave_MRFrameEnd;")
            #mel.eval('shave_MRFrameStart')           


            
resetup()
rd_path()
if user_id not in [1813119]:  
    ConductMel()

    
 
    
    
########################### custom   start   here ########################################  

            
            

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

if user_id not in [1813119]:        
    if rendersetting:
        if 'renderableLayer' in rendersetting :
            if "," in rendersetting['renderableLayer']:
                set_layer_render(rendersetting['renderableLayer'])



            
if user_id in [1850226,1852174]:
    print start
    if start:
        cmds.currentTime(int(start),edit=True)
        print "update frame"
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")       
    
if user_id in [1860293]:
    
    #change_path_mapping("AlembicNode", "abc_File",mapping)
    print "the mode++++++"
    print cmds.evaluationManager( query=True ,mode =1 )
    print "the mode++++++"
    cmds.refresh()
    
    
    
if user_id in [1865216]:
    for i in pm.ls(type="aiOptions"):
        # i.abortOnError.set(1)
        # print "set defaultArnoldRenderOptions.abortOnError 1"
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(40960)
    change_path_mapping("AlembicNode", "abc_File",mapping)
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    
    
if user_id in [1807271]:
    change_path_mapping("ffxDyna","output_path",mapping)
    change_path_mapping("ffxDyna","wavelet_output_path",mapping)
    change_path_mapping("ffxDyna","postprocess_output_path",mapping)

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
    maya_proj_path = cmds.workspace(q=True, fullName=True)
    source_path = "%s/sourceimages" % (maya_proj_path)
    rep_path =""
    search=""
    dicts={}
    if search:
        dicts=file_dicts(search)
    for attr_dict in attr_list:
        for node_type in attr_dict:
            attr_name = attr_dict[node_type]
            change_path(node_type, attr_name, mapping, rep_path,dicts)
    replace_path("pgYetiMaya", "cacheFileName","//192.168.80.223/MayaFiles/TYBL/SC01/sh06/xiecm/TYBL_SC01_sh06","X:")                       
    replace_path("pgYetiMaya", "cacheFileName","E:/work/TYBL/Project","X:")
    change_path_mapping("pgYetiMaya", "cacheFileName",mapping)    
    if "pgYetiMaya" not in plugins or "vrayformaya" not in plugins:
        render_node.postMel.set("")
    set_yeti_imageSearchPath(mapping)
    del_node('SGFC_sc05_sh01_ly_yong:SGFC_ch010001SwimsuitGirl_l_msAnim:Facial_PanelShape')
    del_node('SGFC_sc08_sh01_0810:_1:che:SGFC_sc08_sh01_JingCha_037:SGFC_ch008001Policeman1_h_msAnim:Facial_PanelShape')
    del_node('SGFC_sc08_sh01_0810:_1:che:SGFC_sc08_sh01_JingCha_038:SGFC_ch008001Policeman1_h_msAnim:Facial_PanelShape')
    del_node("SGFC_ch008001Policeman1_h_msAnim:Facial_PanelShape")
    del_node("ch:Facial_Panel_MD_19432Shape")
    del_node("ch:Facial_Panel_MD_19431Shape")
    del_node("aiAreaLightShape1309")
    del_node("Facial_PanelShape")
    del_node("ch:Facial_Panel_MD_19433")
    del_node("Policeman16:Facial_PanelShape")
    del_node("Policeman17:Facial_PanelShape")
    del_node("Policeman16:Facial_PanelShape")
    del_node("Policeman16:Facial_PanelShape")
    del_node("Policeman16:Facial_PanelShape")
    del_node("Policeman16:Facial_PanelShape")
    del_node("Policeman16:Facial_PanelShape")
    del_node("ch:Facial_Panel_MD_19433Shape")
    del_node("SGFC_sc08_sh01_0810:_1:che:SGFC_sc08_sh01_JingCha_040:SGFC_ch008001Policeman1_h_msAnim:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:che:SGFC_sc08_sh01_JingCha_039:SGFC_ch008001Policeman1_h_msAnim:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:ch012001Policeman:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:ch012001Policeman3:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:jc1:ch012001Policeman6:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:jc1:ch012001Policeman7:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:jc3:ch012001Policeman9:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:jincha:SGFC_sc028_sh01_an_DBjuese:ch008001Policeman1:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:jc3:ch012001Policeman9:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:jc3:ch012001Policeman9:Facial_PanelShape")
    del_node("SGFC_sc08_sh01_0810:_1:dongbujuese_002:jc3:ch012001Policeman9:Facial_PanelShape")
    del_node("SGFC_sc05_sh01_ly_yong5:SGFC_ch010001SwimsuitGirl_l_msAnim:Facial_PanelShape")
    
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
            cams = rendersetting['renderableCamera']
            del_cam(cams)
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
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(25600)
        i.absoluteTexturePaths.set(0)
        i.absoluteProceduralPaths.set(0)
        
        print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
        #setAttr "defaultArnoldRenderOptions.absoluteProceduralPaths" 0;
        #i.procedural_searchpath.set(r"N:\cg_custom_setup\network\arnold\htoa-1.11.1_r1692_houdini-15.0.393_windows\arnold\procedurals")
        
        i.shader_searchpath.set(source_path)
        i.texture_searchpath.set(source_path)
        #setAttr -type "string" defaultArnoldRenderOptions.procedural_searchpath ;
if user_id in [119768]:
    for i in pm.ls(type="aiOptions"):
        # print "defaultArnoldRenderOptions.abortOnError 0"
        #i.abortOnError.set()
        i.log_verbosity.set(2)
if user_id in [1840038,1861572,1867734]:
    for i in pm.ls(type="aiOptions"):
        # if i.hasAttr("abortOnError"):
            # print "defaultArnoldRenderOptions.abortOnError 0"
            # i.abortOnError.set(0)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(40960)
    for i in pm.ls(type="pgYetiMaya"):
        if i.hasAttr("aiLoadAtInit"):
            print "%s .aiLoadAtInit 1" % (i)
            i.aiLoadAtInit.set(1)        
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad) 
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")


if user_id in [963250,1816742]:
    maya_proj_path = cmds.workspace(q=True, fullName=True)
    source_path = "%s/sourceimages" % (maya_proj_path)
    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(40960)
        # i.absoluteTexturePaths.set(0)
        # i.absoluteProceduralPaths.set(0)
        # print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
        # i.procedural_searchpath.set()
        if i.hasAttr("shader_searchpath"):
            i.shader_searchpath.set(r"B:\clientFiles\963250\htoa-2.0.0_r240c4dd_houdini-16.0.557\htoa-2.0.0_r240c4dd_houdini-16.0.557\arnold\plugins")
            print 'setAttr "defaultArnoldRenderOptions.shader_searchpath:B:\clientFiles\963250\htoa-2.0.0_r240c4dd_houdini-16.0.557\htoa-2.0.0_r240c4dd_houdini-16.0.557\arnold\plugins'
        if i.hasAttr("plugin_searchpath"):
            i.plugin_searchpath.set(r"B:\clientFiles\963250\htoa-2.0.0_r240c4dd_houdini-16.0.557\htoa-2.0.0_r240c4dd_houdini-16.0.557\arnold\plugins;B:\clientFiles\963250\htoa-2.0.0_r240c4dd_houdini-16.0.557\htoa-2.0.0_r240c4dd_houdini-16.0.557\arnold\drivers")
            print 'setAttr "defaultArnoldRenderOptions.plugin_searchpath:B:\clientFiles\963250\htoa-2.0.0_r240c4dd_houdini-16.0.557\htoa-2.0.0_r240c4dd_houdini-16.0.557\arnold\plugins;B:\clientFiles\963250\htoa-2.0.0_r240c4dd_houdini-16.0.557\htoa-2.0.0_r240c4dd_houdini-16.0.557\arnold\drivers '
        i.texture_searchpath.set(source_path)
        #setAttr -type "string" defaultArnoldRenderOptions.procedural_searchpath ;
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")

    
if user_id in [1861648]:
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
    
if user_id in [1861025,1858235]:
    for i in pm.ls(type="aiOptions"):
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(10240)
            print "textureMaxMemoryMB.set(10240)"
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    
if user_id in [1812345]:
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(10240)
            print "textureMaxMemoryMB.set(10240)"
if user_id in [1866782]:
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(10240)
            print "textureMaxMemoryMB.set(10240)"
            
if user_id in [1803147]:
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(10240)
            print "textureMaxMemoryMB.set(10240)"            
          
            
 
    
if user_id in [1861989]:
    if start:
        cmds.currentTime(int(start),edit=True)
    for i in pm.ls(type="aiOptions"):
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
            print "textureMaxMemoryMB.set(20480)"



if user_id in [1863971]:
    for i in pm.ls(type="aiOptions"):
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
            print "textureMaxMemoryMB.set(20480)"

    
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
if user_id in [1858637]:
    user_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    print user_path
    # rd_path()  
    # rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    # if "<RenderLayer>" not in  rd_path:        
        # rd_path += "/<RenderLayer>"
        # print rd_path
        # pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(rd_path)
    mel.eval('cycleCheck -e off')


# if user_id in [964590]:
    # user_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    # print user_path
    # rd_path()  
    
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
if user_id in [1845209]:
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
    mel.eval('$g_mrBatchRenderCmdOption_MemLimit = 64')
    mel.eval('$g_mrBatchRenderCmdOption_NumThreadOn = 32')
if user_id in [1852550]:
    for i in pm.ls(type="pgYetiMaya"):
        print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(0)
        print "abortOnError off"
        
        
if user_id in [963452]:
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(0)
        print "abortOnError off"
        
# if user_id in [1821228]:
    # for i in pm.ls(type="pgYetiMaya"):
        # print "%s .aiLoadAtInit 1" % (i)
        # i.aiLoadAtInit.set(1)
if user_id in [1844577,1857698,1853469,1867132,1821228]:
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
            i.srdml.set(0)
            print "set vray srdml 0"            
        if i.hasAttr("sys_message_level"):
            i.sys_message_level.set(3)
            print "set vray's log level as 3"
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

if user_id in [1861628]:
    print "replace path "
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
        # i.log_verbosity.set(0)
        # if i.hasAttr("autotx"):
            # i.autotx.set(False)
        # i.absoluteTexturePaths.set(0)
        # i.absoluteProceduralPaths.set(0)
        source_path="%s/sourceimages" % (maya_proj_paht)
        i.shader_searchpath.set(source_path)
        i.texture_searchpath.set(source_path)
    for a in pm.ls(type="mesh"):
        if a.hasAttr("deferStandinLoad"):
            cmds.setAttr((a+".deferStandinLoad"),False)
            b = cmds.getAttr(a+".deferStandinLoad")
            print a,b
        
        
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
if user_id in [1860909]:
    set_yeti_imageSearchPath(mapping)
    for i in pm.ls(type="pgYetiMaya"):
        #print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
if user_id in [1815272,1861877]:
    # for i in pm.ls(type="aiOptions"):
        # i.abortOnError.set(0)
        # print 'abortOnError-off'
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        print 'abortOnError-off'
if user_id in [1837976,1862577]:
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        print 'abortOnError-off'
if user_id in [1861648]:

    # for i in pm.ls(type="aiOptions"):
        # i.abortOnError.set(0)
        # print 'abortOnError-off'
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        print 'abortOnError-off'
# if user_id in [1840132]:
    # rd_path()
    #pre_layer_mel()
    # for i in pm.ls(type="aiOptions"):
        # i.abortOnError.set(0)
        # print 'abortOnError-off'
    # for i in pm.ls(type="aiOptions"):
        # i.abortOnError.set(0)
        # print 'abortOnError-off'
        
        
if user_id in [1016752]:
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            # org_srdml = cmds.getAttr(i+".srdml")
            # print "scens originalvray srdml set to %s " %S org_srdml
            i.srdml.set(0)
            print "set vray srdml 0"
    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            org_arnold_texturecache = cmds.getAttr(i+".textureMaxMemoryMB")
            print "org arnold texturecache to %s MB " % org_arnold_texturecache
            i.textureMaxMemoryMB.set(20480)
            print "set arnold texturecache to 20480 MB"
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad) 

if user_id in [1844854]:
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        print "abort On Error turn off"



    
if user_id in [1821226]:
    del_node('CH_GTQScale0o032_seq000:Face_cameraShape')
    for i in pm.ls(type="pgYetiMaya"):
        #print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            org_arnold_texturecache = cmds.getAttr(i+".textureMaxMemoryMB")
            print "org arnold texturecache to %s MB " % org_arnold_texturecache
            i.textureMaxMemoryMB.set(40960)
            print "set arnold texturecache to 40960 MB"
            
if user_id in [1866675]:
    for i in pm.ls(type="aiOptions"):
        i.abortOnError.set(0)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(0)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            org_arnold_texturecache = cmds.getAttr(i+".textureMaxMemoryMB")
            print "org arnold texturecache to %s MB " % org_arnold_texturecache
            i.textureMaxMemoryMB.set(40960)
            print "set arnold texturecache to 40960 MB"
            
if user_id in [1849653]:

    for i in pm.ls(type="pgYetiMaya"):
        #print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(1)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            org_arnold_texturecache = cmds.getAttr(i+".textureMaxMemoryMB")
            print "org arnold texturecache to %s MB " % org_arnold_texturecache
            i.textureMaxMemoryMB.set(40960)
            print "set arnold texturecache to 40960 MB"            


if user_id in [1861346]:
    for i in pm.ls(type="pgYetiMaya"):
        #print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("threads_autodetect"):
            i.threads_autodetect.set(1)
        if i.hasAttr("threads"):
            i.threads.set(32)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            org_arnold_texturecache = cmds.getAttr(i+".textureMaxMemoryMB")
            print "org arnold texturecache to %s MB " % org_arnold_texturecache
            i.textureMaxMemoryMB.set(40960)
            print "set arnold texturecache to 40960 MB"               
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
            
if user_id in [1848903,1863429]:
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
if user_id in [1862416]:
    mel.eval("optionVar -iv \"evaluationMode\" 1;")
    print "set evaluationMode to dg"
    for i in pm.ls(type="aiOptions"):
        #i.use_existing_tiled_textures.set(0)
        i.motion_blur_enable.set(0)
        i.log_verbosity.set(1)
if user_id in [1813119]:
    #render_node.preRenderLayerMel.set("")
    #render_node.postRenderLayerMel.set("")
    #print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(2)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
            print "set arnold textureMaxMemoryMB 20480 "
if user_id in [1859072,1859047]:
    print "set vray srdml "
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
            
if user_id in [962276]:
    if rendersetting:
        for i in pm.ls(type="VRaySettingsNode"):
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(rendersetting['width'])
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(rendersetting['height'])
        for i in pm.ls(type="resolution"):
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(int(rendersetting['width']))
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(int(rendersetting['height']))  
                
if user_id in [1861569]:
    for i in pm.ls(type="pgYetiMaya"):
        #print "%s .aiLoadAtInit 1" % (i)
        i.aiLoadAtInit.set(1)
    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
        
if user_id in [1840132]:
    if render_name == "arnold":
        for i in pm.ls(type="aiOptions"):
            i.abortOnError.set(0)
            print 'abortOnError-off'
            if i.hasAttr("log_verbosity"):
                i.log_verbosity.set(1)
                # i.abortOnError.set(0)
                print "set arnold log level to 1"
            if i.hasAttr("textureMaxMemoryMB"):
                i.textureMaxMemoryMB.set(40960)
                print "set arnold textureMaxMemory to 40960MB"
    else:
        print "currentRenderer is : %s" %render_name
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ") 
    

            
if user_id in [1863854]:
    for i in pm.ls(type="aiOptions"):
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
            print "textureMaxMemoryMB.set(20480)"
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ") 
    
if user_id in [1841452]:
    current_renderer=pm.PyNode("defaultRenderGlobals").currentRenderer.get()
    print "currentRenderer is %s" % (current_renderer)
    output_prefix = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    print "your output_prefix is %s " % (output_prefix)
    # for i in pm.ls(type="aiOptions"):
        # print "defaultArnoldRenderOptions.abortOnError 0"
        # i.abortOnError.set(1)
        # i.log_verbosity.set(1)
        # if i.hasAttr("autotx"):
            # i.autotx.set(False)
        # if i.hasAttr("textureMaxMemoryMB"):
            # i.textureMaxMemoryMB.set(40960)
        # i.absoluteTexturePaths.set(0)
        # i.absoluteProceduralPaths.set(0)
        # print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")


if user_id in [1855708,900045,962276,1855110,1833038,1834849,1857988,1826800,1860992,1163411,1862577,1830380,1822281,1852326,1868563,1849290]:
    current_renderer=pm.PyNode("defaultRenderGlobals").currentRenderer.get()
    print "currentRenderer is %s" % (current_renderer)
    output_prefix = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    print "Defaults output_prefix is %s" % (output_prefix)

    for i in pm.ls(type="aiOptions"):
        # print "defaultArnoldRenderOptions.abortOnError 0"
        # i.abortOnError.set(1)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
        # i.absoluteTexturePaths.set(0)
        # i.absoluteProceduralPaths.set(0)
        # print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            # org_srdml = cmds.getAttr(i+".srdml")
            # print "scens originalvray srdml set to %s " %S org_srdml
            i.srdml.set(0)
            print "set vray srdml 0"
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
if user_id in [1862390]:
    for i in pm.ls(type="aiOptions"):
        # print "defaultArnoldRenderOptions.abortOnError 0"
        # i.abortOnError.set(1)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
            print "set arnold textureMaxMemoryMB 20480 "
        # i.absoluteTexturePaths.set(0)
        # i.absoluteProceduralPaths.set(0)
        # print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(20480)
            print "set vray srdml 20480"
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    
if user_id in [1860934]:
    current_renderer=pm.PyNode("defaultRenderGlobals").currentRenderer.get()
    print "currentRenderer is %s" % (current_renderer)
    output_prefix = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    if output_prefix=="":
        print "output_prefix is Defaults"
        sceneName = os.path.splitext(os.path.basename(pm.system.sceneName()))[0].strip()
        pm.PyNode("defaultRenderGlobals").imageFilePrefix.set(sceneName)
        Newoutput_prefix=pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
        print "New output_prefix is %s" % (Newoutput_prefix)
    if start:
        cmds.currentTime(int(start),edit=True)
        startFrame=start
        endFrame=start
        pm.PyNode("defaultRenderGlobals").startFrame.set(startFrame)
        pm.PyNode("defaultRenderGlobals").endFrame.set(startFrame)
        print "current render frame is %s" % (startFrame)
        
# if user_id in [1163411]:
    # current_render = pm.PyNode("defaultRenderGlobals").currentRenderer.get()
    # print current_render
    # if current_render == "mentalRay":
        # for i in pm.ls(type="mentalrayGlobals"):
            # if i.hasAttr("exportVerbosity"):
                # i.exportVerbosity.set(5)
            # if i.hasAttr("renderThreads"):
                # i.renderThreads.set(32)
if user_id in [1865164,1870188]:
    if rendersetting:
        for i in pm.ls(type="VRaySettingsNode"):
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(rendersetting['width'])
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(rendersetting['height'])
        for i in pm.ls(type="resolution"):
            if 'width' in rendersetting and i.hasAttr("width") :
                i.width.set(int(rendersetting['width']))
            if 'height' in rendersetting and i.hasAttr("height") :
                i.height.set(int(rendersetting['height']))  
    for i in pm.ls(type="aiOptions"):
        # print "defaultArnoldRenderOptions.abortOnError 0"
        # i.abortOnError.set(1)
        if i.hasAttr("log_verbosity"):
            i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        if i.hasAttr("textureMaxMemoryMB"):
            i.textureMaxMemoryMB.set(20480)
            print "set arnold textureMaxMemoryMB 20480 "
        # i.absoluteTexturePaths.set(0)
        # i.absoluteProceduralPaths.set(0)
        # print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(0)
            print "set vray srdml 0"
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    

if user_id in [1826435]:
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(36000)
        if i.hasAttr("sys_distributed_rendering_on"):
            i.sys_distributed_rendering_on.set(False)
        if i.hasAttr("globopt_gi_dontRenderImage"):
            i.globopt_gi_dontRenderImage.set(False)
            
if user_id in [963480]:
    for i in pm.ls(type="VRaySettingsNode"):
        if i.hasAttr("srdml"):
            i.srdml.set(48000)
        if i.hasAttr("sys_distributed_rendering_on"):
            i.sys_distributed_rendering_on.set(False)
        if i.hasAttr("globopt_gi_dontRenderImage"):
            i.globopt_gi_dontRenderImage.set(False)         
            
if user_id in [1831496]:
    for i in pm.ls(type="aiOptions"):
        print "defaultArnoldRenderOptions.abortOnError 0"
        i.abortOnError.set(0)
        i.log_verbosity.set(1)
        if i.hasAttr("autotx"):
            i.autotx.set(False)
        i.absoluteTexturePaths.set(0)
        i.absoluteProceduralPaths.set(0)
        print 'setAttr "defaultArnoldRenderOptions.absoluteTexturePaths" 0;'
        #setAttr "defaultArnoldRenderOptions.absoluteProceduralPaths" 0;
        i.procedural_searchpath.set(r"N:\cg_custom_setup\network\arnold\htoa-1.11.1_r1692_houdini-15.0.393_windows\arnold\procedurals")
        i.shader_searchpath.set(r"N:\cg_custom_setup\network\arnold\htoa-1.11.1_r1692_houdini-15.0.393_windows\arnold\plugins")
        #setAttr -type "string" defaultArnoldRenderOptions.procedural_searchpath ;
        #setAttr -type "string" defaultArnoldRenderOptions.shader_searchpath "B:\\custom_config\\1831496\\htoa-1.11.1_r1692_houdini-15.0.393\\arnold\\plugins";
        i.renderType.set(0)            
            
if user_id in [1870536]:
    print start
    print "9999999999999999999"
    if start:
        cmds.currentTime(int(start-1),edit=True)
    mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
         

print "**********************************************the prerender end******************************************************"