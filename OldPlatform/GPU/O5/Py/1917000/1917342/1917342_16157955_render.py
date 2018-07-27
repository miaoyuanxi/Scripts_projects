#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1917000'
G_USERID='1917342'
G_TASKID='16157955'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r''
G_PLUGINS=r''
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\1917342'
G_VRAY_LICENSE='1'
#script_param_mark#
import os,sys,shutil


print 'copyBasePy...start'
nodePyDir=r'c:\script\py'
if G_RENDEROS=='Linux':
    nodePyDir=r'/root/rayvision/script/py'
if not os.path.exists(nodePyDir):
    os.makedirs(nodePyDir)
    
    

def copyPyFolder(pyFolder):
    if os.path.exists(pyFolder):
        for root, dirs, files in os.walk(pyFolder):
            print 'copyBasePy...'
            for i in xrange (0, files.__len__()):
                sf = os.path.join(root, files[i])
                shutil.copy(sf,nodePyDir)
                
def copyFolder(source,target):
    if not os.path.exists(target):
        os.makedirs(target)
    if os.path.exists(source):
        for root, dirs, files in os.walk(source):
            print 'copyBasePy...'
            for dirname in  dirs:
                tdir=os.path.join(root,dirname)
                if not os.path.exists(tdir):
                    os.makedirs(tdir)
            for i in xrange (0, files.__len__()):
                sf = os.path.join(root, files[i])
                folder=target+root[len(source):len(root)]+"/"
                if not os.path.exists(folder):
                    os.makedirs(folder)
                shutil.copy(sf,folder)
                

cgList=['Nuke','Preprocess','Max','MaxClient','Merge','Blender','C4D','Lightwave','Clarisse','SketchUp','Vue','Vray','OctaneRender','Softimage','Mrstand','Maya','MayaPre','MayaClient','Houdini','Katana','Keyshot']#preprocess,maxclient
if G_CG_NAME in cgList:
#if os.path.exists(scriptCg):
    if G_CG_NAME == 'Preprocess' or G_CG_NAME == 'MaxClient' or G_CG_NAME == 'Merge':
        G_CG_NAME_PATH = 'Max'
    elif G_CG_NAME == 'MayaPre' or G_CG_NAME == 'MayaClient':
        G_CG_NAME_PATH = 'Maya'
    else:
        G_CG_NAME_PATH = G_CG_NAME
    script2=G_POOL+'/script2'
    scriptBase=script2+'/Base'
    scriptCg=script2+'/'+G_CG_NAME_PATH
    scriptUtil=script2+'/Util'
    scriptNodeBase=nodePyDir+'/Base'
    scriptNodeCg=nodePyDir+'/'+G_CG_NAME_PATH
    scriptNodeUtil=nodePyDir+'/Util'
    print script2
    print scriptBase
    print scriptCg
    print scriptUtil

    userRenderPy=script2+'/user/'+G_USERID
    try:
        shutil.rmtree(nodePyDir)
    except:
        pass
    copyFolder(scriptBase,scriptNodeBase)
    copyFolder(scriptCg,scriptNodeCg)
    copyFolder(scriptUtil,scriptNodeUtil)
    copyFolder(userRenderPy,nodePyDir)
    sys.path.append(scriptNodeBase)
else:
    copyPyFolder(baseRenderPy)
    copyPyFolder(userRenderPy)

print 'copyBasePy...end'

sys.path.append(nodePyDir)

import RenderAction


if(__name__=="__main__"):
    paramDict = {'G_JOB_ID':G_JOB_ID,'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_NODE_PY':nodePyDir,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION,'G_CONFIG':G_CONFIG,'G_PLUGINS':G_PLUGINS,'G_RENDEROS':G_RENDEROS,'G_CG_TILE':G_CG_TILE,'G_CG_TILECOUNT':G_CG_TILECOUNT}
    try:
        paramDict['G_SCHEDULER_CLUSTER_ID']=G_SCHEDULER_CLUSTER_ID
    except:
        pass
        
    try:
        paramDict['G_SCHEDULER_CLUSTER_NODES']=G_SCHEDULER_CLUSTER_NODES
    except:
        pass
        
    try:
        paramDict['G_HOUDINI_TYPE']=G_HOUDINI_TYPE
    except:
        pass
        
    try:
        paramDict['G_VRAY_LICENSE']=G_VRAY_LICENSE
    except:
        pass
    RenderAction.main(**paramDict)


##BEGIN
##description=This is a test script
##name=1917342_16157955_render.py
##requirements=|OS-Windows
##category=SH
##level=79
##custom=1917342
##nodelimit=20
##nodeblacklimit=3
##constraints=10_90_100_101
##priority=20
##autorestartlimit=4
##jobdurationlimit=3600
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0300' '300' '300' '1' '' '' '0' '1'
##'frame0301' '301' '301' '1' '' '' '0' '1'
##'frame0302' '302' '302' '1' '' '' '0' '1'
##'frame0303' '303' '303' '1' '' '' '0' '1'
##'frame0304' '304' '304' '1' '' '' '0' '1'
##'frame0305' '305' '305' '1' '' '' '0' '1'
##'frame0306' '306' '306' '1' '' '' '0' '1'
##'frame0307' '307' '307' '1' '' '' '0' '1'
##'frame0308' '308' '308' '1' '' '' '0' '1'
##'frame0309' '309' '309' '1' '' '' '0' '1'
##'frame0310' '310' '310' '1' '' '' '0' '1'
##'frame0311' '311' '311' '1' '' '' '0' '1'
##'frame0312' '312' '312' '1' '' '' '0' '1'
##'frame0313' '313' '313' '1' '' '' '0' '1'
##'frame0314' '314' '314' '1' '' '' '0' '1'
##'frame0315' '315' '315' '1' '' '' '0' '1'
##'frame0316' '316' '316' '1' '' '' '0' '1'
##'frame0317' '317' '317' '1' '' '' '0' '1'
##'frame0318' '318' '318' '1' '' '' '0' '1'
##'frame0319' '319' '319' '1' '' '' '0' '1'
##'frame0320' '320' '320' '1' '' '' '0' '1'
##'frame0321' '321' '321' '1' '' '' '0' '1'
##'frame0322' '322' '322' '1' '' '' '0' '1'
##'frame0323' '323' '323' '1' '' '' '0' '1'
##'frame0324' '324' '324' '1' '' '' '0' '1'
##'frame0325' '325' '325' '1' '' '' '0' '1'
##'frame0326' '326' '326' '1' '' '' '0' '1'
##'frame0327' '327' '327' '1' '' '' '0' '1'
##'frame0328' '328' '328' '1' '' '' '0' '1'
##'frame0329' '329' '329' '1' '' '' '0' '1'
##'frame0330' '330' '330' '1' '' '' '0' '1'
##'frame0331' '331' '331' '1' '' '' '0' '1'
##'frame0332' '332' '332' '1' '' '' '0' '1'
##'frame0333' '333' '333' '1' '' '' '0' '1'
##'frame0334' '334' '334' '1' '' '' '0' '1'
##'frame0335' '335' '335' '1' '' '' '0' '1'
##'frame0336' '336' '336' '1' '' '' '0' '1'
##'frame0337' '337' '337' '1' '' '' '0' '1'
##'frame0338' '338' '338' '1' '' '' '0' '1'
##'frame0339' '339' '339' '1' '' '' '0' '1'
##'frame0340' '340' '340' '1' '' '' '0' '1'
##'frame0341' '341' '341' '1' '' '' '0' '1'
##'frame0342' '342' '342' '1' '' '' '0' '1'
##'frame0343' '343' '343' '1' '' '' '0' '1'
##'frame0344' '344' '344' '1' '' '' '0' '1'
##'frame0345' '345' '345' '1' '' '' '0' '1'
##'frame0346' '346' '346' '1' '' '' '0' '1'
##'frame0347' '347' '347' '1' '' '' '0' '1'
##'frame0348' '348' '348' '1' '' '' '0' '1'
##'frame0349' '349' '349' '1' '' '' '0' '1'
##'frame0350' '350' '350' '1' '' '' '0' '1'
##'frame0351' '351' '351' '1' '' '' '0' '1'
##'frame0352' '352' '352' '1' '' '' '0' '1'
##'frame0353' '353' '353' '1' '' '' '0' '1'
##'frame0354' '354' '354' '1' '' '' '0' '1'
##'frame0355' '355' '355' '1' '' '' '0' '1'
##'frame0356' '356' '356' '1' '' '' '0' '1'
##'frame0357' '357' '357' '1' '' '' '0' '1'
##'frame0358' '358' '358' '1' '' '' '0' '1'
##'frame0359' '359' '359' '1' '' '' '0' '1'
##'frame0360' '360' '360' '1' '' '' '0' '1'
##ENDJOBS

##END
