#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='1917500'
G_USERID='1917991'
G_TASKID='16158694'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\1917500\1917991\16158694\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\1917500\1917991\16158694\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\1917991'
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
##name=1917991_16158694_render.py
##requirements=|OS-Windows
##category=SH
##level=50
##custom=1917991
##nodelimit=5
##nodeblacklimit=3
##constraints=|10_90_100_101
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
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
##'frame0420' '420' '420' '1' '' '' '1' '1'
##'frame0421' '421' '421' '1' '' '' '1' '1'
##'frame0422' '422' '422' '1' '' '' '1' '1'
##'frame0423' '423' '423' '1' '' '' '1' '1'
##'frame0424' '424' '424' '1' '' '' '1' '1'
##'frame0425' '425' '425' '1' '' '' '1' '1'
##'frame0426' '426' '426' '1' '' '' '1' '1'
##'frame0427' '427' '427' '1' '' '' '1' '1'
##'frame0428' '428' '428' '1' '' '' '1' '1'
##'frame0429' '429' '429' '1' '' '' '1' '1'
##'frame0430' '430' '430' '1' '' '' '1' '1'
##'frame0431' '431' '431' '1' '' '' '1' '1'
##'frame0432' '432' '432' '1' '' '' '1' '1'
##'frame0433' '433' '433' '1' '' '' '1' '1'
##'frame0434' '434' '434' '1' '' '' '1' '1'
##'frame0435' '435' '435' '1' '' '' '1' '1'
##'frame0436' '436' '436' '1' '' '' '1' '1'
##'frame0437' '437' '437' '1' '' '' '1' '1'
##'frame0438' '438' '438' '1' '' '' '1' '1'
##'frame0439' '439' '439' '1' '' '' '1' '1'
##'frame0440' '440' '440' '1' '' '' '1' '1'
##'frame0441' '441' '441' '1' '' '' '1' '1'
##'frame0442' '442' '442' '1' '' '' '1' '1'
##'frame0443' '443' '443' '1' '' '' '1' '1'
##'frame0444' '444' '444' '1' '' '' '1' '1'
##'frame0445' '445' '445' '1' '' '' '1' '1'
##'frame0446' '446' '446' '1' '' '' '1' '1'
##'frame0447' '447' '447' '1' '' '' '1' '1'
##'frame0448' '448' '448' '1' '' '' '1' '1'
##'frame0449' '449' '449' '1' '' '' '1' '1'
##'frame0450' '450' '450' '1' '' '' '1' '1'
##'frame0451' '451' '451' '1' '' '' '1' '1'
##'frame0452' '452' '452' '1' '' '' '1' '1'
##'frame0453' '453' '453' '1' '' '' '1' '1'
##'frame0454' '454' '454' '1' '' '' '1' '1'
##'frame0455' '455' '455' '1' '' '' '1' '1'
##'frame0456' '456' '456' '1' '' '' '1' '1'
##'frame0457' '457' '457' '1' '' '' '1' '1'
##'frame0458' '458' '458' '1' '' '' '1' '1'
##'frame0459' '459' '459' '1' '' '' '1' '1'
##'frame0460' '460' '460' '1' '' '' '1' '1'
##'frame0461' '461' '461' '1' '' '' '1' '1'
##'frame0462' '462' '462' '1' '' '' '1' '1'
##'frame0463' '463' '463' '1' '' '' '1' '1'
##'frame0464' '464' '464' '1' '' '' '1' '1'
##'frame0465' '465' '465' '1' '' '' '1' '1'
##'frame0466' '466' '466' '1' '' '' '1' '1'
##'frame0467' '467' '467' '1' '' '' '1' '1'
##'frame0468' '468' '468' '1' '' '' '1' '1'
##'frame0469' '469' '469' '1' '' '' '1' '1'
##'frame0470' '470' '470' '1' '' '' '1' '1'
##'frame0471' '471' '471' '1' '' '' '1' '1'
##'frame0472' '472' '472' '1' '' '' '1' '1'
##'frame0473' '473' '473' '1' '' '' '1' '1'
##'frame0474' '474' '474' '1' '' '' '1' '1'
##'frame0475' '475' '475' '1' '' '' '1' '1'
##'frame0476' '476' '476' '1' '' '' '1' '1'
##'frame0477' '477' '477' '1' '' '' '1' '1'
##'frame0478' '478' '478' '1' '' '' '1' '1'
##'frame0479' '479' '479' '1' '' '' '1' '1'
##'frame0480' '480' '480' '1' '' '' '1' '1'
##'frame0481' '481' '481' '1' '' '' '1' '1'
##'frame0482' '482' '482' '1' '' '' '1' '1'
##'frame0483' '483' '483' '1' '' '' '1' '1'
##'frame0484' '484' '484' '1' '' '' '1' '1'
##'frame0485' '485' '485' '1' '' '' '1' '1'
##'frame0486' '486' '486' '1' '' '' '1' '1'
##'frame0487' '487' '487' '1' '' '' '1' '1'
##'frame0488' '488' '488' '1' '' '' '1' '1'
##'frame0489' '489' '489' '1' '' '' '1' '1'
##'frame0490' '490' '490' '1' '' '' '1' '1'
##'frame0491' '491' '491' '1' '' '' '1' '1'
##'frame0492' '492' '492' '1' '' '' '1' '1'
##'frame0493' '493' '493' '1' '' '' '1' '1'
##'frame0494' '494' '494' '1' '' '' '1' '1'
##'frame0495' '495' '495' '1' '' '' '1' '1'
##'frame0496' '496' '496' '1' '' '' '1' '1'
##'frame0497' '497' '497' '1' '' '' '1' '1'
##'frame0498' '498' '498' '1' '' '' '1' '1'
##'frame0499' '499' '499' '1' '' '' '1' '1'
##'frame0500' '500' '500' '1' '' '' '1' '1'
##ENDJOBS

##END
