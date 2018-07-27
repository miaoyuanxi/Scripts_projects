#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1917000'
G_USERID='1917342'
G_TASKID='16158905'
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
##name=1917342_16158905_render.py
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
##'frame0361' '361' '361' '1' '' '' '0' '1'
##'frame0362' '362' '362' '1' '' '' '0' '1'
##'frame0363' '363' '363' '1' '' '' '0' '1'
##'frame0364' '364' '364' '1' '' '' '0' '1'
##'frame0365' '365' '365' '1' '' '' '0' '1'
##'frame0366' '366' '366' '1' '' '' '0' '1'
##'frame0367' '367' '367' '1' '' '' '0' '1'
##'frame0368' '368' '368' '1' '' '' '0' '1'
##'frame0369' '369' '369' '1' '' '' '0' '1'
##'frame0370' '370' '370' '1' '' '' '0' '1'
##'frame0371' '371' '371' '1' '' '' '0' '1'
##'frame0372' '372' '372' '1' '' '' '0' '1'
##'frame0373' '373' '373' '1' '' '' '0' '1'
##'frame0374' '374' '374' '1' '' '' '0' '1'
##'frame0375' '375' '375' '1' '' '' '0' '1'
##'frame0376' '376' '376' '1' '' '' '0' '1'
##'frame0377' '377' '377' '1' '' '' '0' '1'
##'frame0378' '378' '378' '1' '' '' '0' '1'
##'frame0379' '379' '379' '1' '' '' '0' '1'
##'frame0380' '380' '380' '1' '' '' '0' '1'
##'frame0381' '381' '381' '1' '' '' '0' '1'
##'frame0382' '382' '382' '1' '' '' '0' '1'
##'frame0383' '383' '383' '1' '' '' '0' '1'
##'frame0384' '384' '384' '1' '' '' '0' '1'
##'frame0385' '385' '385' '1' '' '' '0' '1'
##'frame0386' '386' '386' '1' '' '' '0' '1'
##'frame0387' '387' '387' '1' '' '' '0' '1'
##'frame0388' '388' '388' '1' '' '' '0' '1'
##'frame0389' '389' '389' '1' '' '' '0' '1'
##'frame0390' '390' '390' '1' '' '' '0' '1'
##'frame0391' '391' '391' '1' '' '' '0' '1'
##'frame0392' '392' '392' '1' '' '' '0' '1'
##'frame0393' '393' '393' '1' '' '' '0' '1'
##'frame0394' '394' '394' '1' '' '' '0' '1'
##'frame0395' '395' '395' '1' '' '' '0' '1'
##'frame0396' '396' '396' '1' '' '' '0' '1'
##'frame0397' '397' '397' '1' '' '' '0' '1'
##'frame0398' '398' '398' '1' '' '' '0' '1'
##'frame0399' '399' '399' '1' '' '' '0' '1'
##'frame0400' '400' '400' '1' '' '' '0' '1'
##'frame0401' '401' '401' '1' '' '' '0' '1'
##'frame0402' '402' '402' '1' '' '' '0' '1'
##'frame0403' '403' '403' '1' '' '' '0' '1'
##'frame0404' '404' '404' '1' '' '' '0' '1'
##'frame0405' '405' '405' '1' '' '' '0' '1'
##'frame0406' '406' '406' '1' '' '' '0' '1'
##'frame0407' '407' '407' '1' '' '' '0' '1'
##'frame0408' '408' '408' '1' '' '' '0' '1'
##'frame0409' '409' '409' '1' '' '' '0' '1'
##'frame0410' '410' '410' '1' '' '' '0' '1'
##'frame0411' '411' '411' '1' '' '' '0' '1'
##'frame0412' '412' '412' '1' '' '' '0' '1'
##'frame0413' '413' '413' '1' '' '' '0' '1'
##'frame0414' '414' '414' '1' '' '' '0' '1'
##'frame0415' '415' '415' '1' '' '' '0' '1'
##'frame0416' '416' '416' '1' '' '' '0' '1'
##'frame0417' '417' '417' '1' '' '' '0' '1'
##'frame0418' '418' '418' '1' '' '' '0' '1'
##'frame0419' '419' '419' '1' '' '' '0' '1'
##ENDJOBS

##END
