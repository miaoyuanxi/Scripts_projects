#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1917000'
G_USERID='1917342'
G_TASKID='16158884'
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
##name=1917342_16158884_render.py
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
##'frame0151' '151' '151' '1' '' '' '0' '1'
##'frame0152' '152' '152' '1' '' '' '0' '1'
##'frame0153' '153' '153' '1' '' '' '0' '1'
##'frame0154' '154' '154' '1' '' '' '0' '1'
##'frame0155' '155' '155' '1' '' '' '0' '1'
##'frame0156' '156' '156' '1' '' '' '0' '1'
##'frame0157' '157' '157' '1' '' '' '0' '1'
##'frame0158' '158' '158' '1' '' '' '0' '1'
##'frame0159' '159' '159' '1' '' '' '0' '1'
##'frame0160' '160' '160' '1' '' '' '0' '1'
##'frame0161' '161' '161' '1' '' '' '0' '1'
##'frame0162' '162' '162' '1' '' '' '0' '1'
##'frame0163' '163' '163' '1' '' '' '0' '1'
##'frame0164' '164' '164' '1' '' '' '0' '1'
##'frame0165' '165' '165' '1' '' '' '0' '1'
##'frame0166' '166' '166' '1' '' '' '0' '1'
##'frame0167' '167' '167' '1' '' '' '0' '1'
##'frame0168' '168' '168' '1' '' '' '0' '1'
##'frame0169' '169' '169' '1' '' '' '0' '1'
##'frame0170' '170' '170' '1' '' '' '0' '1'
##'frame0171' '171' '171' '1' '' '' '0' '1'
##'frame0172' '172' '172' '1' '' '' '0' '1'
##'frame0173' '173' '173' '1' '' '' '0' '1'
##'frame0174' '174' '174' '1' '' '' '0' '1'
##'frame0175' '175' '175' '1' '' '' '0' '1'
##'frame0176' '176' '176' '1' '' '' '0' '1'
##'frame0177' '177' '177' '1' '' '' '0' '1'
##'frame0178' '178' '178' '1' '' '' '0' '1'
##'frame0179' '179' '179' '1' '' '' '0' '1'
##'frame0180' '180' '180' '1' '' '' '0' '1'
##'frame0181' '181' '181' '1' '' '' '0' '1'
##'frame0182' '182' '182' '1' '' '' '0' '1'
##'frame0183' '183' '183' '1' '' '' '0' '1'
##'frame0184' '184' '184' '1' '' '' '0' '1'
##'frame0185' '185' '185' '1' '' '' '0' '1'
##'frame0186' '186' '186' '1' '' '' '0' '1'
##'frame0187' '187' '187' '1' '' '' '0' '1'
##'frame0188' '188' '188' '1' '' '' '0' '1'
##'frame0189' '189' '189' '1' '' '' '0' '1'
##'frame0190' '190' '190' '1' '' '' '0' '1'
##ENDJOBS

##END
