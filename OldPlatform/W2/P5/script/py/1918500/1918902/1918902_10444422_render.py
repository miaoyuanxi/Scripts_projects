#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='1918500'
G_USERID='1918902'
G_TASKID='10444422'
G_POOL=r'\\10.60.100.101\p5'
G_CONFIG=r'\\10.60.100.101\p5\config\1918500\1918902\10444422\render.json'
G_PLUGINS=r'\\10.60.100.101\p5\config\1918500\1918902\10444422\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.60.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.60.100.101\p5\script\py\py\1918902'
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
##name=1918902_10444422_render.py
##requirements=|OS-Windows|RAM-64
##category=BJ
##level=50
##custom=1918902
##nodelimit=500
##nodeblacklimit=3
##constraints=|10_60_200_101
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0265' '265' '265' '1' '' '' '1' '1'
##'frame0266' '266' '266' '1' '' '' '1' '1'
##'frame0267' '267' '267' '1' '' '' '1' '1'
##'frame0268' '268' '268' '1' '' '' '1' '1'
##'frame0269' '269' '269' '1' '' '' '1' '1'
##'frame0270' '270' '270' '1' '' '' '1' '1'
##'frame0271' '271' '271' '1' '' '' '1' '1'
##'frame0272' '272' '272' '1' '' '' '1' '1'
##'frame0273' '273' '273' '1' '' '' '1' '1'
##'frame0274' '274' '274' '1' '' '' '1' '1'
##'frame0275' '275' '275' '1' '' '' '1' '1'
##'frame0276' '276' '276' '1' '' '' '1' '1'
##'frame0277' '277' '277' '1' '' '' '1' '1'
##'frame0278' '278' '278' '1' '' '' '1' '1'
##'frame0279' '279' '279' '1' '' '' '1' '1'
##'frame0280' '280' '280' '1' '' '' '1' '1'
##'frame0281' '281' '281' '1' '' '' '1' '1'
##'frame0282' '282' '282' '1' '' '' '1' '1'
##'frame0283' '283' '283' '1' '' '' '1' '1'
##'frame0284' '284' '284' '1' '' '' '1' '1'
##'frame0285' '285' '285' '1' '' '' '1' '1'
##'frame0286' '286' '286' '1' '' '' '1' '1'
##'frame0287' '287' '287' '1' '' '' '1' '1'
##'frame0288' '288' '288' '1' '' '' '1' '1'
##'frame0289' '289' '289' '1' '' '' '1' '1'
##'frame0290' '290' '290' '1' '' '' '1' '1'
##'frame0291' '291' '291' '1' '' '' '1' '1'
##'frame0292' '292' '292' '1' '' '' '1' '1'
##'frame0293' '293' '293' '1' '' '' '1' '1'
##'frame0294' '294' '294' '1' '' '' '1' '1'
##'frame0295' '295' '295' '1' '' '' '1' '1'
##'frame0296' '296' '296' '1' '' '' '1' '1'
##'frame0297' '297' '297' '1' '' '' '1' '1'
##'frame0298' '298' '298' '1' '' '' '1' '1'
##'frame0299' '299' '299' '1' '' '' '1' '1'
##'frame0300' '300' '300' '1' '' '' '1' '1'
##'frame0385' '385' '385' '1' '' '' '1' '1'
##'frame0386' '386' '386' '1' '' '' '1' '1'
##'frame0387' '387' '387' '1' '' '' '1' '1'
##'frame0388' '388' '388' '1' '' '' '1' '1'
##'frame0389' '389' '389' '1' '' '' '1' '1'
##'frame0390' '390' '390' '1' '' '' '1' '1'
##'frame0391' '391' '391' '1' '' '' '1' '1'
##'frame0392' '392' '392' '1' '' '' '1' '1'
##'frame0393' '393' '393' '1' '' '' '1' '1'
##'frame0394' '394' '394' '1' '' '' '1' '1'
##'frame0395' '395' '395' '1' '' '' '1' '1'
##'frame0396' '396' '396' '1' '' '' '1' '1'
##'frame0397' '397' '397' '1' '' '' '1' '1'
##'frame0398' '398' '398' '1' '' '' '1' '1'
##'frame0399' '399' '399' '1' '' '' '1' '1'
##'frame0400' '400' '400' '1' '' '' '1' '1'
##'frame0401' '401' '401' '1' '' '' '1' '1'
##'frame0402' '402' '402' '1' '' '' '1' '1'
##'frame0403' '403' '403' '1' '' '' '1' '1'
##'frame0404' '404' '404' '1' '' '' '1' '1'
##'frame0405' '405' '405' '1' '' '' '1' '1'
##'frame0406' '406' '406' '1' '' '' '1' '1'
##'frame0407' '407' '407' '1' '' '' '1' '1'
##'frame0408' '408' '408' '1' '' '' '1' '1'
##'frame0409' '409' '409' '1' '' '' '1' '1'
##'frame0410' '410' '410' '1' '' '' '1' '1'
##'frame0411' '411' '411' '1' '' '' '1' '1'
##'frame0412' '412' '412' '1' '' '' '1' '1'
##'frame0413' '413' '413' '1' '' '' '1' '1'
##'frame0414' '414' '414' '1' '' '' '1' '1'
##'frame0415' '415' '415' '1' '' '' '1' '1'
##'frame0416' '416' '416' '1' '' '' '1' '1'
##'frame0417' '417' '417' '1' '' '' '1' '1'
##'frame0418' '418' '418' '1' '' '' '1' '1'
##'frame0419' '419' '419' '1' '' '' '1' '1'
##ENDJOBS

##END
