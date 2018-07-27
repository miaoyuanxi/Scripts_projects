#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1917000'
G_USERID='1917342'
G_TASKID='16157971'
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
##name=1917342_16157971_render.py
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
##'frame0420' '420' '420' '1' '' '' '0' '1'
##'frame0421' '421' '421' '1' '' '' '0' '1'
##'frame0422' '422' '422' '1' '' '' '0' '1'
##'frame0423' '423' '423' '1' '' '' '0' '1'
##'frame0424' '424' '424' '1' '' '' '0' '1'
##'frame0425' '425' '425' '1' '' '' '0' '1'
##'frame0426' '426' '426' '1' '' '' '0' '1'
##'frame0427' '427' '427' '1' '' '' '0' '1'
##'frame0428' '428' '428' '1' '' '' '0' '1'
##'frame0429' '429' '429' '1' '' '' '0' '1'
##'frame0430' '430' '430' '1' '' '' '0' '1'
##'frame0431' '431' '431' '1' '' '' '0' '1'
##'frame0432' '432' '432' '1' '' '' '0' '1'
##'frame0433' '433' '433' '1' '' '' '0' '1'
##'frame0434' '434' '434' '1' '' '' '0' '1'
##'frame0435' '435' '435' '1' '' '' '0' '1'
##'frame0436' '436' '436' '1' '' '' '0' '1'
##'frame0437' '437' '437' '1' '' '' '0' '1'
##'frame0438' '438' '438' '1' '' '' '0' '1'
##'frame0439' '439' '439' '1' '' '' '0' '1'
##'frame0440' '440' '440' '1' '' '' '0' '1'
##'frame0441' '441' '441' '1' '' '' '0' '1'
##'frame0442' '442' '442' '1' '' '' '0' '1'
##'frame0443' '443' '443' '1' '' '' '0' '1'
##'frame0444' '444' '444' '1' '' '' '0' '1'
##'frame0445' '445' '445' '1' '' '' '0' '1'
##'frame0446' '446' '446' '1' '' '' '0' '1'
##'frame0447' '447' '447' '1' '' '' '0' '1'
##'frame0448' '448' '448' '1' '' '' '0' '1'
##'frame0449' '449' '449' '1' '' '' '0' '1'
##'frame0450' '450' '450' '1' '' '' '0' '1'
##'frame0451' '451' '451' '1' '' '' '0' '1'
##'frame0452' '452' '452' '1' '' '' '0' '1'
##'frame0453' '453' '453' '1' '' '' '0' '1'
##'frame0454' '454' '454' '1' '' '' '0' '1'
##'frame0455' '455' '455' '1' '' '' '0' '1'
##'frame0456' '456' '456' '1' '' '' '0' '1'
##'frame0457' '457' '457' '1' '' '' '0' '1'
##'frame0458' '458' '458' '1' '' '' '0' '1'
##'frame0459' '459' '459' '1' '' '' '0' '1'
##'frame0460' '460' '460' '1' '' '' '0' '1'
##'frame0461' '461' '461' '1' '' '' '0' '1'
##'frame0462' '462' '462' '1' '' '' '0' '1'
##'frame0463' '463' '463' '1' '' '' '0' '1'
##'frame0464' '464' '464' '1' '' '' '0' '1'
##'frame0465' '465' '465' '1' '' '' '0' '1'
##'frame0466' '466' '466' '1' '' '' '0' '1'
##'frame0467' '467' '467' '1' '' '' '0' '1'
##'frame0468' '468' '468' '1' '' '' '0' '1'
##'frame0469' '469' '469' '1' '' '' '0' '1'
##'frame0470' '470' '470' '1' '' '' '0' '1'
##'frame0471' '471' '471' '1' '' '' '0' '1'
##'frame0472' '472' '472' '1' '' '' '0' '1'
##'frame0473' '473' '473' '1' '' '' '0' '1'
##'frame0474' '474' '474' '1' '' '' '0' '1'
##'frame0475' '475' '475' '1' '' '' '0' '1'
##'frame0476' '476' '476' '1' '' '' '0' '1'
##'frame0477' '477' '477' '1' '' '' '0' '1'
##'frame0478' '478' '478' '1' '' '' '0' '1'
##'frame0479' '479' '479' '1' '' '' '0' '1'
##'frame0480' '480' '480' '1' '' '' '0' '1'
##'frame0481' '481' '481' '1' '' '' '0' '1'
##'frame0482' '482' '482' '1' '' '' '0' '1'
##'frame0483' '483' '483' '1' '' '' '0' '1'
##'frame0484' '484' '484' '1' '' '' '0' '1'
##'frame0485' '485' '485' '1' '' '' '0' '1'
##'frame0486' '486' '486' '1' '' '' '0' '1'
##'frame0487' '487' '487' '1' '' '' '0' '1'
##'frame0488' '488' '488' '1' '' '' '0' '1'
##'frame0489' '489' '489' '1' '' '' '0' '1'
##'frame0490' '490' '490' '1' '' '' '0' '1'
##'frame0491' '491' '491' '1' '' '' '0' '1'
##'frame0492' '492' '492' '1' '' '' '0' '1'
##'frame0493' '493' '493' '1' '' '' '0' '1'
##'frame0494' '494' '494' '1' '' '' '0' '1'
##'frame0495' '495' '495' '1' '' '' '0' '1'
##'frame0496' '496' '496' '1' '' '' '0' '1'
##'frame0497' '497' '497' '1' '' '' '0' '1'
##'frame0498' '498' '498' '1' '' '' '0' '1'
##'frame0499' '499' '499' '1' '' '' '0' '1'
##'frame0500' '500' '500' '1' '' '' '0' '1'
##'frame0501' '501' '501' '1' '' '' '0' '1'
##'frame0502' '502' '502' '1' '' '' '0' '1'
##'frame0503' '503' '503' '1' '' '' '0' '1'
##'frame0504' '504' '504' '1' '' '' '0' '1'
##'frame0505' '505' '505' '1' '' '' '0' '1'
##'frame0506' '506' '506' '1' '' '' '0' '1'
##'frame0507' '507' '507' '1' '' '' '0' '1'
##'frame0508' '508' '508' '1' '' '' '0' '1'
##'frame0509' '509' '509' '1' '' '' '0' '1'
##'frame0510' '510' '510' '1' '' '' '0' '1'
##'frame0511' '511' '511' '1' '' '' '0' '1'
##'frame0512' '512' '512' '1' '' '' '0' '1'
##'frame0513' '513' '513' '1' '' '' '0' '1'
##'frame0514' '514' '514' '1' '' '' '0' '1'
##'frame0515' '515' '515' '1' '' '' '0' '1'
##'frame0516' '516' '516' '1' '' '' '0' '1'
##'frame0517' '517' '517' '1' '' '' '0' '1'
##'frame0518' '518' '518' '1' '' '' '0' '1'
##'frame0519' '519' '519' '1' '' '' '0' '1'
##'frame0520' '520' '520' '1' '' '' '0' '1'
##'frame0521' '521' '521' '1' '' '' '0' '1'
##'frame0522' '522' '522' '1' '' '' '0' '1'
##'frame0523' '523' '523' '1' '' '' '0' '1'
##'frame0524' '524' '524' '1' '' '' '0' '1'
##'frame0525' '525' '525' '1' '' '' '0' '1'
##'frame0526' '526' '526' '1' '' '' '0' '1'
##'frame0527' '527' '527' '1' '' '' '0' '1'
##'frame0528' '528' '528' '1' '' '' '0' '1'
##'frame0529' '529' '529' '1' '' '' '0' '1'
##'frame0530' '530' '530' '1' '' '' '0' '1'
##'frame0531' '531' '531' '1' '' '' '0' '1'
##'frame0532' '532' '532' '1' '' '' '0' '1'
##'frame0533' '533' '533' '1' '' '' '0' '1'
##'frame0534' '534' '534' '1' '' '' '0' '1'
##'frame0535' '535' '535' '1' '' '' '0' '1'
##'frame0536' '536' '536' '1' '' '' '0' '1'
##'frame0537' '537' '537' '1' '' '' '0' '1'
##'frame0538' '538' '538' '1' '' '' '0' '1'
##'frame0539' '539' '539' '1' '' '' '0' '1'
##'frame0540' '540' '540' '1' '' '' '0' '1'
##'frame0541' '541' '541' '1' '' '' '0' '1'
##'frame0542' '542' '542' '1' '' '' '0' '1'
##'frame0543' '543' '543' '1' '' '' '0' '1'
##'frame0544' '544' '544' '1' '' '' '0' '1'
##'frame0545' '545' '545' '1' '' '' '0' '1'
##'frame0546' '546' '546' '1' '' '' '0' '1'
##'frame0547' '547' '547' '1' '' '' '0' '1'
##'frame0548' '548' '548' '1' '' '' '0' '1'
##'frame0549' '549' '549' '1' '' '' '0' '1'
##'frame0550' '550' '550' '1' '' '' '0' '1'
##'frame0551' '551' '551' '1' '' '' '0' '1'
##'frame0552' '552' '552' '1' '' '' '0' '1'
##'frame0553' '553' '553' '1' '' '' '0' '1'
##'frame0554' '554' '554' '1' '' '' '0' '1'
##'frame0555' '555' '555' '1' '' '' '0' '1'
##'frame0556' '556' '556' '1' '' '' '0' '1'
##'frame0557' '557' '557' '1' '' '' '0' '1'
##'frame0558' '558' '558' '1' '' '' '0' '1'
##'frame0559' '559' '559' '1' '' '' '0' '1'
##'frame0560' '560' '560' '1' '' '' '0' '1'
##'frame0561' '561' '561' '1' '' '' '0' '1'
##'frame0562' '562' '562' '1' '' '' '0' '1'
##'frame0563' '563' '563' '1' '' '' '0' '1'
##'frame0564' '564' '564' '1' '' '' '0' '1'
##'frame0565' '565' '565' '1' '' '' '0' '1'
##'frame0566' '566' '566' '1' '' '' '0' '1'
##'frame0567' '567' '567' '1' '' '' '0' '1'
##'frame0568' '568' '568' '1' '' '' '0' '1'
##'frame0569' '569' '569' '1' '' '' '0' '1'
##'frame0570' '570' '570' '1' '' '' '0' '1'
##'frame0571' '571' '571' '1' '' '' '0' '1'
##'frame0572' '572' '572' '1' '' '' '0' '1'
##'frame0573' '573' '573' '1' '' '' '0' '1'
##'frame0574' '574' '574' '1' '' '' '0' '1'
##'frame0575' '575' '575' '1' '' '' '0' '1'
##'frame0576' '576' '576' '1' '' '' '0' '1'
##'frame0577' '577' '577' '1' '' '' '0' '1'
##'frame0578' '578' '578' '1' '' '' '0' '1'
##'frame0579' '579' '579' '1' '' '' '0' '1'
##'frame0580' '580' '580' '1' '' '' '0' '1'
##'frame0581' '581' '581' '1' '' '' '0' '1'
##'frame0582' '582' '582' '1' '' '' '0' '1'
##'frame0583' '583' '583' '1' '' '' '0' '1'
##'frame0584' '584' '584' '1' '' '' '0' '1'
##'frame0585' '585' '585' '1' '' '' '0' '1'
##'frame0586' '586' '586' '1' '' '' '0' '1'
##'frame0587' '587' '587' '1' '' '' '0' '1'
##'frame0588' '588' '588' '1' '' '' '0' '1'
##'frame0589' '589' '589' '1' '' '' '0' '1'
##'frame0590' '590' '590' '1' '' '' '0' '1'
##'frame0591' '591' '591' '1' '' '' '0' '1'
##'frame0592' '592' '592' '1' '' '' '0' '1'
##'frame0593' '593' '593' '1' '' '' '0' '1'
##'frame0594' '594' '594' '1' '' '' '0' '1'
##'frame0595' '595' '595' '1' '' '' '0' '1'
##'frame0596' '596' '596' '1' '' '' '0' '1'
##'frame0597' '597' '597' '1' '' '' '0' '1'
##'frame0598' '598' '598' '1' '' '' '0' '1'
##'frame0599' '599' '599' '1' '' '' '0' '1'
##'frame0600' '600' '600' '1' '' '' '0' '1'
##'frame0601' '601' '601' '1' '' '' '0' '1'
##'frame0602' '602' '602' '1' '' '' '0' '1'
##'frame0603' '603' '603' '1' '' '' '0' '1'
##'frame0604' '604' '604' '1' '' '' '0' '1'
##'frame0605' '605' '605' '1' '' '' '0' '1'
##'frame0606' '606' '606' '1' '' '' '0' '1'
##'frame0607' '607' '607' '1' '' '' '0' '1'
##'frame0608' '608' '608' '1' '' '' '0' '1'
##'frame0609' '609' '609' '1' '' '' '0' '1'
##'frame0610' '610' '610' '1' '' '' '0' '1'
##ENDJOBS

##END
