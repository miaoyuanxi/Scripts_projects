#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='1917500'
G_USERID='1917556'
G_TASKID='16160344'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\1917500\1917556\16160344\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\1917500\1917556\16160344\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\1917556'
G_VRAY_LICENSE='1'
G_HOUDINI_TYPE=''
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
##name=1917556_16160344_render.py
##requirements=|OS-Windows
##category=BJ
##level=79
##custom=1917556
##nodelimit=99
##nodeblacklimit=3
##constraints=|10_90_100_102
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0080' '80' '80' '1' '' '' '1' '1'
##'frame0081' '81' '81' '1' '' '' '1' '1'
##'frame0082' '82' '82' '1' '' '' '1' '1'
##'frame0083' '83' '83' '1' '' '' '1' '1'
##'frame0084' '84' '84' '1' '' '' '1' '1'
##'frame0085' '85' '85' '1' '' '' '1' '1'
##'frame0086' '86' '86' '1' '' '' '1' '1'
##'frame0087' '87' '87' '1' '' '' '1' '1'
##'frame0088' '88' '88' '1' '' '' '1' '1'
##'frame0089' '89' '89' '1' '' '' '1' '1'
##'frame0090' '90' '90' '1' '' '' '1' '1'
##'frame0091' '91' '91' '1' '' '' '1' '1'
##'frame0092' '92' '92' '1' '' '' '1' '1'
##'frame0093' '93' '93' '1' '' '' '1' '1'
##'frame0094' '94' '94' '1' '' '' '1' '1'
##'frame0095' '95' '95' '1' '' '' '1' '1'
##'frame0096' '96' '96' '1' '' '' '1' '1'
##'frame0097' '97' '97' '1' '' '' '1' '1'
##'frame0098' '98' '98' '1' '' '' '1' '1'
##'frame0099' '99' '99' '1' '' '' '1' '1'
##'frame0100' '100' '100' '1' '' '' '1' '1'
##'frame0101' '101' '101' '1' '' '' '1' '1'
##'frame0102' '102' '102' '1' '' '' '1' '1'
##'frame0103' '103' '103' '1' '' '' '1' '1'
##'frame0104' '104' '104' '1' '' '' '1' '1'
##'frame0105' '105' '105' '1' '' '' '1' '1'
##'frame0106' '106' '106' '1' '' '' '1' '1'
##'frame0107' '107' '107' '1' '' '' '1' '1'
##'frame0108' '108' '108' '1' '' '' '1' '1'
##'frame0109' '109' '109' '1' '' '' '1' '1'
##'frame0110' '110' '110' '1' '' '' '1' '1'
##'frame0111' '111' '111' '1' '' '' '1' '1'
##'frame0112' '112' '112' '1' '' '' '1' '1'
##'frame0113' '113' '113' '1' '' '' '1' '1'
##'frame0114' '114' '114' '1' '' '' '1' '1'
##'frame0115' '115' '115' '1' '' '' '1' '1'
##'frame0116' '116' '116' '1' '' '' '1' '1'
##'frame0117' '117' '117' '1' '' '' '1' '1'
##'frame0118' '118' '118' '1' '' '' '1' '1'
##'frame0119' '119' '119' '1' '' '' '1' '1'
##'frame0120' '120' '120' '1' '' '' '1' '1'
##ENDJOBS

##END
