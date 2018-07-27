#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1917000'
G_USERID='1917342'
G_TASKID='16158863'
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
##name=1917342_16158863_render.py
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
##'frame0231' '231' '231' '1' '' '' '0' '1'
##'frame0232' '232' '232' '1' '' '' '0' '1'
##'frame0233' '233' '233' '1' '' '' '0' '1'
##'frame0234' '234' '234' '1' '' '' '0' '1'
##'frame0235' '235' '235' '1' '' '' '0' '1'
##'frame0236' '236' '236' '1' '' '' '0' '1'
##'frame0237' '237' '237' '1' '' '' '0' '1'
##'frame0238' '238' '238' '1' '' '' '0' '1'
##'frame0239' '239' '239' '1' '' '' '0' '1'
##'frame0240' '240' '240' '1' '' '' '0' '1'
##'frame0241' '241' '241' '1' '' '' '0' '1'
##'frame0242' '242' '242' '1' '' '' '0' '1'
##'frame0243' '243' '243' '1' '' '' '0' '1'
##'frame0244' '244' '244' '1' '' '' '0' '1'
##'frame0245' '245' '245' '1' '' '' '0' '1'
##'frame0246' '246' '246' '1' '' '' '0' '1'
##'frame0247' '247' '247' '1' '' '' '0' '1'
##'frame0248' '248' '248' '1' '' '' '0' '1'
##'frame0249' '249' '249' '1' '' '' '0' '1'
##'frame0250' '250' '250' '1' '' '' '0' '1'
##'frame0251' '251' '251' '1' '' '' '0' '1'
##'frame0252' '252' '252' '1' '' '' '0' '1'
##'frame0253' '253' '253' '1' '' '' '0' '1'
##'frame0254' '254' '254' '1' '' '' '0' '1'
##'frame0255' '255' '255' '1' '' '' '0' '1'
##'frame0256' '256' '256' '1' '' '' '0' '1'
##'frame0257' '257' '257' '1' '' '' '0' '1'
##'frame0258' '258' '258' '1' '' '' '0' '1'
##'frame0259' '259' '259' '1' '' '' '0' '1'
##'frame0260' '260' '260' '1' '' '' '0' '1'
##'frame0261' '261' '261' '1' '' '' '0' '1'
##'frame0262' '262' '262' '1' '' '' '0' '1'
##'frame0263' '263' '263' '1' '' '' '0' '1'
##'frame0264' '264' '264' '1' '' '' '0' '1'
##'frame0265' '265' '265' '1' '' '' '0' '1'
##'frame0266' '266' '266' '1' '' '' '0' '1'
##'frame0267' '267' '267' '1' '' '' '0' '1'
##'frame0268' '268' '268' '1' '' '' '0' '1'
##'frame0269' '269' '269' '1' '' '' '0' '1'
##'frame0270' '270' '270' '1' '' '' '0' '1'
##ENDJOBS

##END
