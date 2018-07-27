#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import os,sys,re
import time
print "+++++++++++++++++++++++++++++++++the prerender strat++++++++++++++++++++++++++++++++++++++++++++++++"
premel_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print "the prerender strat time :: %s \n" % premel_start_time
## Edit by shen 2018.1.19
try:
    from pymel import versions
    print("The Maya version with update: %s"%str(versions.current()))
    RenderNode = pm.PyNode("defaultRenderGlobals")
    Renderer_name = RenderNode.currentRenderer.get()
    print("Current renderner: %s"%Renderer_name)
    print("Current Outpu setting: %s"%RenderNode.attr("imageFilePrefix").get())
    print("Current Outpu format: %s"%RenderNode.attr("imageFormat").get())
    if Renderer_name == "arnold":
        print("Arnold base settings for threads and tex Memory: full thread/40960")
        aiop = pm.PyNode("defaultArnoldRenderOptions")
        if not aiop.attr("threads_autodetect").get():
            aiop.attr("threads_autodetect").set(True)
        if int(aiop.attr("textureMaxMemoryMB").get()) < 40960:
            aiop.attr("textureMaxMemoryMB").set(40960)
    renderable_cam = []
    for i in pm.ls(type="camera"):
        if i.renderable.get():renderable_cam.append(i)
    if not len(renderable_cam):
        print("PL set an camera to render scene.")
        sys.exit(001)
    print(".")
except:
    pass

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
        if i.hasAttr("threads_autodetect"):
            threads_autodetect = i.threads_autodetect.get()
            print "Scene threads_autodetect is : %s" % str(threads_autodetect)
            if threads_autodetect == 0:
                if i.hasAttr("threads"):
                    threads = i.threads.get()                        
                    print  "Scene threads is : %s" % str(threads)
        if i.hasAttr("motion_blur_enable"):
            motion_blur_enable = i.motion_blur_enable.get()
            print "Scene motion_blur_enable is : %s" % str(motion_blur_enable)
            if motion_blur_enable == 1:
                if i.hasAttr("ignoreMotionBlur"):
                    ignoreMotionBlur = i.ignoreMotionBlur.get()                    
                    print  "Scene ignoreMotionBlur is : %s" % str(ignoreMotionBlur)
    print "get you scene attritubes end >>>>>>>>>>>"
    for i in pm.ls(type="pgYetiMaya"):
        if i.hasAttr("aiLoadAtInit"):
            i.aiLoadAtInit.set(1)
            # print "%s .aiLoadAtInit 1" % (i)
            
    # for i in pm.ls(type="VRaySettingsNode"):
        # if i.hasAttr("srdml"):
            # i.srdml.set(0)
            # print "set vray srdml 0"            
                    
    for i in pm.ls(type="aiStandIn"):
        if i.hasAttr("deferStandinLoad"):
            i.deferStandinLoad.set(0)
            print "set %s to 0" % (i.deferStandinLoad)
            
    # mel.eval("putenv(\"MAYA_DISABLE_BATCH_RUNUP\",\"1\"); global proc dynRunupForBatchRender() {}; ")
    sys.stdout.flush()
    #------set Frame/Animation ext: name.#.ext---
    #mel.eval("setMayaSoftwareFrameExt(3,0);")

def rd_path():
    
    rd_path = pm.PyNode("defaultRenderGlobals").imageFilePrefix.get()
    mel.eval('setAttr -l false "defaultRenderGlobals.imageFilePrefix";')
    render_node=pm.PyNode("defaultRenderGlobals")
    render_name = render_node.currentRenderer.get()
    if render_name == "vray":
        rd_path = pm.PyNode("vraySettings").fnprx.get()
    print rd_path
    if rd_path is not None:
        if not isinstance(rd_path,str):
            rd_path = str(rd_path)
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
    # print "Mel dict is : %s" % all_mel_dict
    sys.stdout.flush()
    preRenderMel = all_mel_dict['preRenderMel']
    # if preRenderMel:
        # # print "preRenderMel is : %s" % preRenderMel    
        # try:
            # pass
            # # mel.eval(preRenderMel)
        # except Exception as e:
            # print '[err]Conduct preRenderMel failed'
            # print e
    
    if render_name=="vray":

        print "++++++++++++++++ the renderer is vray+++++++++++++++++++++"
        if yeti_load and shave_load==False:
            mel.eval('pgYetiVRayPreRender;')
        if shave_load and yeti_load==False :
            mel.eval('shaveVrayPreRender;')
        if yeti_load and shave_load:
            mel.eval('shaveVrayPreRender;pgYetiVRayPreRender;')
            
    elif render_name=="mentalRay":
        print "++++++++++++++++ the renderer is mentalRay++++++++++++++++++"
        if shave_load:            
            render_node.preRenderMel.set("shave_MRFrameStart;")
            render_node.postRenderMel.set("shave_MRFrameEnd;")
            #mel.eval('shave_MRFrameStart')           


            
resetup()
rd_path()
ConductMel()

if user_id in [1844854]:
    print "Set rendering thread start>>>"
    for i in pm.ls(type="aiOptions"):
        if i.hasAttr("threads_autodetect"):
            auto_thread=i.threads_autodetect.get()
            print "auto_thread is %s" % (auto_thread)
            i.threads_autodetect.set(0)
            print "Set auto_thread to false "
            if i.hasAttr("threads"):
                i.threads.set(32)
                thread=i.threads.get()
                print "Current rendering thread is %s" % (thread)
    print "Set rendering thread end >>>"
            

premel_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print "the prerender end time :: %s \n" % premel_end_time
print "**********************************************the prerender end******************************************************"