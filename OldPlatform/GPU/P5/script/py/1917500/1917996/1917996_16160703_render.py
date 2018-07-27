#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='1917500'
G_USERID='1917996'
G_TASKID='16160703'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\1917500\1917996\16160703\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\1917500\1917996\16160703\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\1917996'
G_VRAY_LICENSE='2'
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
##name=1917996_16160703_render.py
##requirements=|OS-Windows
##category=HW
##level=79
##custom=1917996
##nodelimit=10
##nodeblacklimit=3
##constraints=|10_90_100_102
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0180' '180' '180' '1' '' '' '1' '1'
##'frame0181' '181' '181' '1' '' '' '1' '1'
##'frame0182' '182' '182' '1' '' '' '1' '1'
##'frame0183' '183' '183' '1' '' '' '1' '1'
##'frame0184' '184' '184' '1' '' '' '1' '1'
##'frame0185' '185' '185' '1' '' '' '1' '1'
##'frame0186' '186' '186' '1' '' '' '1' '1'
##'frame0187' '187' '187' '1' '' '' '1' '1'
##'frame0188' '188' '188' '1' '' '' '1' '1'
##'frame0189' '189' '189' '1' '' '' '1' '1'
##'frame0190' '190' '190' '1' '' '' '1' '1'
##'frame0191' '191' '191' '1' '' '' '1' '1'
##'frame0192' '192' '192' '1' '' '' '1' '1'
##'frame0193' '193' '193' '1' '' '' '1' '1'
##'frame0194' '194' '194' '1' '' '' '1' '1'
##'frame0195' '195' '195' '1' '' '' '1' '1'
##'frame0196' '196' '196' '1' '' '' '1' '1'
##'frame0197' '197' '197' '1' '' '' '1' '1'
##'frame0198' '198' '198' '1' '' '' '1' '1'
##'frame0199' '199' '199' '1' '' '' '1' '1'
##'frame0200' '200' '200' '1' '' '' '1' '1'
##'frame0201' '201' '201' '1' '' '' '1' '1'
##'frame0202' '202' '202' '1' '' '' '1' '1'
##'frame0203' '203' '203' '1' '' '' '1' '1'
##'frame0204' '204' '204' '1' '' '' '1' '1'
##'frame0205' '205' '205' '1' '' '' '1' '1'
##'frame0206' '206' '206' '1' '' '' '1' '1'
##'frame0207' '207' '207' '1' '' '' '1' '1'
##'frame0208' '208' '208' '1' '' '' '1' '1'
##'frame0209' '209' '209' '1' '' '' '1' '1'
##'frame0210' '210' '210' '1' '' '' '1' '1'
##'frame0211' '211' '211' '1' '' '' '1' '1'
##'frame0212' '212' '212' '1' '' '' '1' '1'
##'frame0213' '213' '213' '1' '' '' '1' '1'
##'frame0214' '214' '214' '1' '' '' '1' '1'
##'frame0215' '215' '215' '1' '' '' '1' '1'
##'frame0216' '216' '216' '1' '' '' '1' '1'
##'frame0217' '217' '217' '1' '' '' '1' '1'
##'frame0218' '218' '218' '1' '' '' '1' '1'
##'frame0219' '219' '219' '1' '' '' '1' '1'
##'frame0220' '220' '220' '1' '' '' '1' '1'
##'frame0221' '221' '221' '1' '' '' '1' '1'
##'frame0222' '222' '222' '1' '' '' '1' '1'
##'frame0223' '223' '223' '1' '' '' '1' '1'
##'frame0224' '224' '224' '1' '' '' '1' '1'
##'frame0225' '225' '225' '1' '' '' '1' '1'
##'frame0226' '226' '226' '1' '' '' '1' '1'
##'frame0227' '227' '227' '1' '' '' '1' '1'
##'frame0228' '228' '228' '1' '' '' '1' '1'
##'frame0229' '229' '229' '1' '' '' '1' '1'
##'frame0230' '230' '230' '1' '' '' '1' '1'
##'frame0231' '231' '231' '1' '' '' '1' '1'
##'frame0232' '232' '232' '1' '' '' '1' '1'
##'frame0233' '233' '233' '1' '' '' '1' '1'
##'frame0234' '234' '234' '1' '' '' '1' '1'
##'frame0235' '235' '235' '1' '' '' '1' '1'
##'frame0236' '236' '236' '1' '' '' '1' '1'
##'frame0237' '237' '237' '1' '' '' '1' '1'
##'frame0238' '238' '238' '1' '' '' '1' '1'
##'frame0239' '239' '239' '1' '' '' '1' '1'
##'frame0240' '240' '240' '1' '' '' '1' '1'
##'frame0241' '241' '241' '1' '' '' '1' '1'
##'frame0242' '242' '242' '1' '' '' '1' '1'
##'frame0243' '243' '243' '1' '' '' '1' '1'
##'frame0244' '244' '244' '1' '' '' '1' '1'
##'frame0245' '245' '245' '1' '' '' '1' '1'
##'frame0246' '246' '246' '1' '' '' '1' '1'
##'frame0247' '247' '247' '1' '' '' '1' '1'
##'frame0248' '248' '248' '1' '' '' '1' '1'
##'frame0249' '249' '249' '1' '' '' '1' '1'
##'frame0250' '250' '250' '1' '' '' '1' '1'
##'frame0251' '251' '251' '1' '' '' '1' '1'
##'frame0252' '252' '252' '1' '' '' '1' '1'
##'frame0253' '253' '253' '1' '' '' '1' '1'
##'frame0254' '254' '254' '1' '' '' '1' '1'
##'frame0255' '255' '255' '1' '' '' '1' '1'
##'frame0256' '256' '256' '1' '' '' '1' '1'
##'frame0257' '257' '257' '1' '' '' '1' '1'
##'frame0258' '258' '258' '1' '' '' '1' '1'
##'frame0259' '259' '259' '1' '' '' '1' '1'
##'frame0260' '260' '260' '1' '' '' '1' '1'
##'frame0261' '261' '261' '1' '' '' '1' '1'
##'frame0262' '262' '262' '1' '' '' '1' '1'
##'frame0263' '263' '263' '1' '' '' '1' '1'
##ENDJOBS

##END
