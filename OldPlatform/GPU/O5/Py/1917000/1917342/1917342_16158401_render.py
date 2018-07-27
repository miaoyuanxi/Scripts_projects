#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1917000'
G_USERID='1917342'
G_TASKID='16158401'
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
##name=1917342_16158401_render.py
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
##'frame0690' '690' '690' '1' '' '' '0' '1'
##'frame0691' '691' '691' '1' '' '' '0' '1'
##'frame0692' '692' '692' '1' '' '' '0' '1'
##'frame0693' '693' '693' '1' '' '' '0' '1'
##'frame0694' '694' '694' '1' '' '' '0' '1'
##'frame0695' '695' '695' '1' '' '' '0' '1'
##'frame0696' '696' '696' '1' '' '' '0' '1'
##'frame0697' '697' '697' '1' '' '' '0' '1'
##'frame0698' '698' '698' '1' '' '' '0' '1'
##'frame0699' '699' '699' '1' '' '' '0' '1'
##'frame0700' '700' '700' '1' '' '' '0' '1'
##'frame0701' '701' '701' '1' '' '' '0' '1'
##'frame0702' '702' '702' '1' '' '' '0' '1'
##'frame0703' '703' '703' '1' '' '' '0' '1'
##'frame0704' '704' '704' '1' '' '' '0' '1'
##'frame0705' '705' '705' '1' '' '' '0' '1'
##'frame0706' '706' '706' '1' '' '' '0' '1'
##'frame0707' '707' '707' '1' '' '' '0' '1'
##'frame0708' '708' '708' '1' '' '' '0' '1'
##'frame0709' '709' '709' '1' '' '' '0' '1'
##'frame0710' '710' '710' '1' '' '' '0' '1'
##'frame0711' '711' '711' '1' '' '' '0' '1'
##'frame0712' '712' '712' '1' '' '' '0' '1'
##'frame0713' '713' '713' '1' '' '' '0' '1'
##'frame0714' '714' '714' '1' '' '' '0' '1'
##'frame0715' '715' '715' '1' '' '' '0' '1'
##'frame0716' '716' '716' '1' '' '' '0' '1'
##'frame0717' '717' '717' '1' '' '' '0' '1'
##'frame0718' '718' '718' '1' '' '' '0' '1'
##'frame0719' '719' '719' '1' '' '' '0' '1'
##'frame0720' '720' '720' '1' '' '' '0' '1'
##'frame0721' '721' '721' '1' '' '' '0' '1'
##'frame0722' '722' '722' '1' '' '' '0' '1'
##'frame0723' '723' '723' '1' '' '' '0' '1'
##'frame0724' '724' '724' '1' '' '' '0' '1'
##'frame0725' '725' '725' '1' '' '' '0' '1'
##'frame0726' '726' '726' '1' '' '' '0' '1'
##'frame0727' '727' '727' '1' '' '' '0' '1'
##'frame0728' '728' '728' '1' '' '' '0' '1'
##'frame0729' '729' '729' '1' '' '' '0' '1'
##'frame0730' '730' '730' '1' '' '' '0' '1'
##'frame0731' '731' '731' '1' '' '' '0' '1'
##'frame0732' '732' '732' '1' '' '' '0' '1'
##'frame0733' '733' '733' '1' '' '' '0' '1'
##'frame0734' '734' '734' '1' '' '' '0' '1'
##'frame0735' '735' '735' '1' '' '' '0' '1'
##'frame0736' '736' '736' '1' '' '' '0' '1'
##'frame0737' '737' '737' '1' '' '' '0' '1'
##'frame0738' '738' '738' '1' '' '' '0' '1'
##'frame0739' '739' '739' '1' '' '' '0' '1'
##'frame0740' '740' '740' '1' '' '' '0' '1'
##ENDJOBS

##END
