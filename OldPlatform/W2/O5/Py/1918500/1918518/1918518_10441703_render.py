#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1918500'
G_USERID='1918518'
G_TASKID='10441703'
G_POOL=r'\\10.60.100.101\p5'
G_CONFIG=r''
G_PLUGINS=r''
G_RENDEROS=r''
baseRenderPy=r'\\10.60.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.60.100.101\p5\script\py\py\1918518'
G_VRAY_LICENSE='2'
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
##name=1918518_10441703_render.py
##requirements=|OS-Windows|RAM-64
##category=HW
##level=80
##custom=1918518
##nodelimit=1
##nodeblacklimit=3
##constraints=10_60_200_102
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0100' '100' '100' '1' '' '' '0' '1'
##'frame0101' '101' '101' '1' '' '' '0' '1'
##'frame0102' '102' '102' '1' '' '' '0' '1'
##'frame0103' '103' '103' '1' '' '' '0' '1'
##'frame0104' '104' '104' '1' '' '' '0' '1'
##'frame0105' '105' '105' '1' '' '' '0' '1'
##'frame0106' '106' '106' '1' '' '' '0' '1'
##'frame0107' '107' '107' '1' '' '' '0' '1'
##'frame0108' '108' '108' '1' '' '' '0' '1'
##'frame0109' '109' '109' '1' '' '' '0' '1'
##'frame0110' '110' '110' '1' '' '' '0' '1'
##'frame0111' '111' '111' '1' '' '' '0' '1'
##'frame0112' '112' '112' '1' '' '' '0' '1'
##'frame0113' '113' '113' '1' '' '' '0' '1'
##'frame0114' '114' '114' '1' '' '' '0' '1'
##'frame0115' '115' '115' '1' '' '' '0' '1'
##'frame0116' '116' '116' '1' '' '' '0' '1'
##'frame0117' '117' '117' '1' '' '' '0' '1'
##'frame0118' '118' '118' '1' '' '' '0' '1'
##'frame0119' '119' '119' '1' '' '' '0' '1'
##'frame0120' '120' '120' '1' '' '' '0' '1'
##'frame0121' '121' '121' '1' '' '' '0' '1'
##'frame0122' '122' '122' '1' '' '' '0' '1'
##'frame0123' '123' '123' '1' '' '' '0' '1'
##'frame0124' '124' '124' '1' '' '' '0' '1'
##'frame0125' '125' '125' '1' '' '' '0' '1'
##'frame0126' '126' '126' '1' '' '' '0' '1'
##'frame0127' '127' '127' '1' '' '' '0' '1'
##'frame0128' '128' '128' '1' '' '' '0' '1'
##'frame0129' '129' '129' '1' '' '' '0' '1'
##'frame0130' '130' '130' '1' '' '' '0' '1'
##'frame0131' '131' '131' '1' '' '' '0' '1'
##'frame0132' '132' '132' '1' '' '' '0' '1'
##'frame0133' '133' '133' '1' '' '' '0' '1'
##'frame0134' '134' '134' '1' '' '' '0' '1'
##'frame0135' '135' '135' '1' '' '' '0' '1'
##'frame0136' '136' '136' '1' '' '' '0' '1'
##'frame0137' '137' '137' '1' '' '' '0' '1'
##'frame0138' '138' '138' '1' '' '' '0' '1'
##'frame0139' '139' '139' '1' '' '' '0' '1'
##'frame0140' '140' '140' '1' '' '' '0' '1'
##ENDJOBS

##END
