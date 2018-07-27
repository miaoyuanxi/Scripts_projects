#encoding:utf-8
G_CG_NAME='Maya'
G_USERID_PARENT='119500'
G_USERID='119768'
G_TASKID='16100087'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\119500\119768\16100087\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\119500\119768\16100087\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\119768'
G_VRAY_LICNESE='1'
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
    RenderAction.main(**paramDict)


##BEGIN
##description=This is a test script
##name=119768_16100087_render.py
##level=99
##custom=119768
##nodelimit=5
##nodeblacklimit=3
##priority=20
##autorestartlimit=4
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0001_0010' '1' '10' '1' '' '' '1' '1'
##'frame0011_0020' '11' '20' '1' '' '' '1' '1'
##'frame0021_0030' '21' '30' '1' '' '' '1' '1'
##'frame0031_0040' '31' '40' '1' '' '' '1' '1'
##'frame0041_0050' '41' '50' '1' '' '' '1' '1'
##'frame0051_0060' '51' '60' '1' '' '' '1' '1'
##'frame0061_0070' '61' '70' '1' '' '' '1' '1'
##'frame0071_0080' '71' '80' '1' '' '' '1' '1'
##'frame0081_0090' '81' '90' '1' '' '' '1' '1'
##'frame0091_0100' '91' '100' '1' '' '' '1' '1'
##'frame0101_0110' '101' '110' '1' '' '' '1' '1'
##'frame0111_0120' '111' '120' '1' '' '' '1' '1'
##'frame0121_0130' '121' '130' '1' '' '' '1' '1'
##'frame0131_0140' '131' '140' '1' '' '' '1' '1'
##'frame0141_0150' '141' '150' '1' '' '' '1' '1'
##'frame0151_0160' '151' '160' '1' '' '' '1' '1'
##'frame0161_0170' '161' '170' '1' '' '' '1' '1'
##'frame0171_0180' '171' '180' '1' '' '' '1' '1'
##'frame0181_0190' '181' '190' '1' '' '' '1' '1'
##'frame0191_0200' '191' '200' '1' '' '' '1' '1'
##'frame0201_0210' '201' '210' '1' '' '' '1' '1'
##'frame0211_0220' '211' '220' '1' '' '' '1' '1'
##'frame0221_0230' '221' '230' '1' '' '' '1' '1'
##'frame0231_0240' '231' '240' '1' '' '' '1' '1'
##'frame0241_0250' '241' '250' '1' '' '' '1' '1'
##'frame0251_0260' '251' '260' '1' '' '' '1' '1'
##'frame0261_0270' '261' '270' '1' '' '' '1' '1'
##'frame0271_0280' '271' '280' '1' '' '' '1' '1'
##'frame0281_0290' '281' '290' '1' '' '' '1' '1'
##'frame0291_0300' '291' '300' '1' '' '' '1' '1'
##'frame0301_0310' '301' '310' '1' '' '' '1' '1'
##'frame0311_0320' '311' '320' '1' '' '' '1' '1'
##'frame0321_0330' '321' '330' '1' '' '' '1' '1'
##'frame0331_0340' '331' '340' '1' '' '' '1' '1'
##'frame0341_0350' '341' '350' '1' '' '' '1' '1'
##'frame0351_0360' '351' '360' '1' '' '' '1' '1'
##'frame0361_0370' '361' '370' '1' '' '' '1' '1'
##'frame0371_0380' '371' '380' '1' '' '' '1' '1'
##'frame0381_0390' '381' '390' '1' '' '' '1' '1'
##'frame0391_0400' '391' '400' '1' '' '' '1' '1'
##'frame0401_0410' '401' '410' '1' '' '' '1' '1'
##'frame0411_0420' '411' '420' '1' '' '' '1' '1'
##'frame0421_0430' '421' '430' '1' '' '' '1' '1'
##'frame0431_0440' '431' '440' '1' '' '' '1' '1'
##'frame0441_0450' '441' '450' '1' '' '' '1' '1'
##'frame0451_0460' '451' '460' '1' '' '' '1' '1'
##'frame0461_0470' '461' '470' '1' '' '' '1' '1'
##'frame0471_0480' '471' '480' '1' '' '' '1' '1'
##'frame0481_0490' '481' '490' '1' '' '' '1' '1'
##'frame0491_0500' '491' '500' '1' '' '' '1' '1'
##'frame0501_0510' '501' '510' '1' '' '' '1' '1'
##'frame0511_0520' '511' '520' '1' '' '' '1' '1'
##'frame0521_0530' '521' '530' '1' '' '' '1' '1'
##'frame0531_0540' '531' '540' '1' '' '' '1' '1'
##'frame0541_0550' '541' '550' '1' '' '' '1' '1'
##'frame0551_0560' '551' '560' '1' '' '' '1' '1'
##'frame0561_0570' '561' '570' '1' '' '' '1' '1'
##'frame0571_0580' '571' '580' '1' '' '' '1' '1'
##'frame0581_0590' '581' '590' '1' '' '' '1' '1'
##'frame0591_0600' '591' '600' '1' '' '' '1' '1'
##'frame0601_0610' '601' '610' '1' '' '' '1' '1'
##'frame0611_0620' '611' '620' '1' '' '' '1' '1'
##'frame0621_0630' '621' '630' '1' '' '' '1' '1'
##'frame0631_0640' '631' '640' '1' '' '' '1' '1'
##'frame0641_0650' '641' '650' '1' '' '' '1' '1'
##'frame0651_0660' '651' '660' '1' '' '' '1' '1'
##'frame0661_0670' '661' '670' '1' '' '' '1' '1'
##'frame0671_0680' '671' '680' '1' '' '' '1' '1'
##'frame0681_0690' '681' '690' '1' '' '' '1' '1'
##'frame0691_0700' '691' '700' '1' '' '' '1' '1'
##'frame0701_0710' '701' '710' '1' '' '' '1' '1'
##'frame0711_0720' '711' '720' '1' '' '' '1' '1'
##'frame0721_0730' '721' '730' '1' '' '' '1' '1'
##'frame0731_0740' '731' '740' '1' '' '' '1' '1'
##'frame0741_0750' '741' '750' '1' '' '' '1' '1'
##'frame0751_0760' '751' '760' '1' '' '' '1' '1'
##'frame0761_0770' '761' '770' '1' '' '' '1' '1'
##'frame0771_0780' '771' '780' '1' '' '' '1' '1'
##'frame0781_0790' '781' '790' '1' '' '' '1' '1'
##'frame0791_0800' '791' '800' '1' '' '' '1' '1'
##'frame0801_0810' '801' '810' '1' '' '' '1' '1'
##'frame0811_0820' '811' '820' '1' '' '' '1' '1'
##'frame0821_0830' '821' '830' '1' '' '' '1' '1'
##'frame0831_0840' '831' '840' '1' '' '' '1' '1'
##'frame0841_0850' '841' '850' '1' '' '' '1' '1'
##'frame0851_0860' '851' '860' '1' '' '' '1' '1'
##'frame0861_0870' '861' '870' '1' '' '' '1' '1'
##'frame0871_0880' '871' '880' '1' '' '' '1' '1'
##'frame0881_0890' '881' '890' '1' '' '' '1' '1'
##'frame0891_0900' '891' '900' '1' '' '' '1' '1'
##'frame0901_0910' '901' '910' '1' '' '' '1' '1'
##'frame0911_0920' '911' '920' '1' '' '' '1' '1'
##'frame0921_0930' '921' '930' '1' '' '' '1' '1'
##'frame0931_0940' '931' '940' '1' '' '' '1' '1'
##'frame0941_0950' '941' '950' '1' '' '' '1' '1'
##'frame0951_0960' '951' '960' '1' '' '' '1' '1'
##'frame0961_0970' '961' '970' '1' '' '' '1' '1'
##'frame0971_0980' '971' '980' '1' '' '' '1' '1'
##'frame0981_0990' '981' '990' '1' '' '' '1' '1'
##'frame0991_1000' '991' '1000' '1' '' '' '1' '1'
##ENDJOBS

##END
