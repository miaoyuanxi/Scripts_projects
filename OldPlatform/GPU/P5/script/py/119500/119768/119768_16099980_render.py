#encoding:utf-8
G_CG_NAME='Maya'
G_USERID_PARENT='119500'
G_USERID='119768'
G_TASKID='16099980'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\119500\119768\16099980\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\119500\119768\16099980\plugins.json'
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
##name=119768_16099980_render.py
##requirements=|ladaojeifang1
##properties=|ladaojeifang1
##level=79
##custom=119768
##nodelimit=5
##nodeblacklimit=3
##priority=20
##autorestartlimit=4
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0001_0050' '1' '50' '1' '' '' '1' '1'
##'frame0051_0100' '51' '100' '1' '' '' '1' '1'
##'frame0101_0150' '101' '150' '1' '' '' '1' '1'
##'frame0151_0200' '151' '200' '1' '' '' '1' '1'
##'frame0201_0250' '201' '250' '1' '' '' '1' '1'
##'frame0251_0300' '251' '300' '1' '' '' '1' '1'
##'frame0301_0350' '301' '350' '1' '' '' '1' '1'
##'frame0351_0400' '351' '400' '1' '' '' '1' '1'
##'frame0401_0450' '401' '450' '1' '' '' '1' '1'
##'frame0451_0500' '451' '500' '1' '' '' '1' '1'
##'frame0501_0550' '501' '550' '1' '' '' '1' '1'
##'frame0551_0600' '551' '600' '1' '' '' '1' '1'
##'frame0601_0650' '601' '650' '1' '' '' '1' '1'
##'frame0651_0700' '651' '700' '1' '' '' '1' '1'
##'frame0701_0750' '701' '750' '1' '' '' '1' '1'
##'frame0751_0800' '751' '800' '1' '' '' '1' '1'
##'frame0801_0850' '801' '850' '1' '' '' '1' '1'
##'frame0851_0900' '851' '900' '1' '' '' '1' '1'
##'frame0901_0950' '901' '950' '1' '' '' '1' '1'
##'frame0951_1000' '951' '1000' '1' '' '' '1' '1'
##'frame1001_1050' '1001' '1050' '1' '' '' '1' '1'
##'frame1051_1100' '1051' '1100' '1' '' '' '1' '1'
##'frame1101_1150' '1101' '1150' '1' '' '' '1' '1'
##'frame1151_1200' '1151' '1200' '1' '' '' '1' '1'
##'frame1201_1250' '1201' '1250' '1' '' '' '1' '1'
##'frame1251_1300' '1251' '1300' '1' '' '' '1' '1'
##'frame1301_1350' '1301' '1350' '1' '' '' '1' '1'
##'frame1351_1400' '1351' '1400' '1' '' '' '1' '1'
##'frame1401_1450' '1401' '1450' '1' '' '' '1' '1'
##'frame1451_1500' '1451' '1500' '1' '' '' '1' '1'
##'frame1501_1550' '1501' '1550' '1' '' '' '1' '1'
##'frame1551_1600' '1551' '1600' '1' '' '' '1' '1'
##'frame1601_1650' '1601' '1650' '1' '' '' '1' '1'
##'frame1651_1700' '1651' '1700' '1' '' '' '1' '1'
##'frame1701_1750' '1701' '1750' '1' '' '' '1' '1'
##'frame1751_1800' '1751' '1800' '1' '' '' '1' '1'
##'frame1801_1850' '1801' '1850' '1' '' '' '1' '1'
##'frame1851_1900' '1851' '1900' '1' '' '' '1' '1'
##'frame1901_1950' '1901' '1950' '1' '' '' '1' '1'
##'frame1951_2000' '1951' '2000' '1' '' '' '1' '1'
##'frame2001_2050' '2001' '2050' '1' '' '' '1' '1'
##'frame2051_2100' '2051' '2100' '1' '' '' '1' '1'
##'frame2101_2150' '2101' '2150' '1' '' '' '1' '1'
##'frame2151_2200' '2151' '2200' '1' '' '' '1' '1'
##'frame2201_2250' '2201' '2250' '1' '' '' '1' '1'
##'frame2251_2300' '2251' '2300' '1' '' '' '1' '1'
##'frame2301_2350' '2301' '2350' '1' '' '' '1' '1'
##'frame2351_2400' '2351' '2400' '1' '' '' '1' '1'
##'frame2401_2450' '2401' '2450' '1' '' '' '1' '1'
##'frame2451_2500' '2451' '2500' '1' '' '' '1' '1'
##'frame2501_2550' '2501' '2550' '1' '' '' '1' '1'
##'frame2551_2600' '2551' '2600' '1' '' '' '1' '1'
##'frame2601_2650' '2601' '2650' '1' '' '' '1' '1'
##'frame2651_2700' '2651' '2700' '1' '' '' '1' '1'
##'frame2701_2750' '2701' '2750' '1' '' '' '1' '1'
##'frame2751_2800' '2751' '2800' '1' '' '' '1' '1'
##'frame2801_2850' '2801' '2850' '1' '' '' '1' '1'
##'frame2851_2900' '2851' '2900' '1' '' '' '1' '1'
##'frame2901_2950' '2901' '2950' '1' '' '' '1' '1'
##'frame2951_3000' '2951' '3000' '1' '' '' '1' '1'
##'frame3001_3050' '3001' '3050' '1' '' '' '1' '1'
##'frame3051_3100' '3051' '3100' '1' '' '' '1' '1'
##'frame3101_3150' '3101' '3150' '1' '' '' '1' '1'
##'frame3151_3200' '3151' '3200' '1' '' '' '1' '1'
##'frame3201_3250' '3201' '3250' '1' '' '' '1' '1'
##'frame3251_3300' '3251' '3300' '1' '' '' '1' '1'
##'frame3301_3350' '3301' '3350' '1' '' '' '1' '1'
##'frame3351_3400' '3351' '3400' '1' '' '' '1' '1'
##'frame3401_3450' '3401' '3450' '1' '' '' '1' '1'
##'frame3451_3500' '3451' '3500' '1' '' '' '1' '1'
##'frame3501_3550' '3501' '3550' '1' '' '' '1' '1'
##'frame3551_3600' '3551' '3600' '1' '' '' '1' '1'
##'frame3601_3650' '3601' '3650' '1' '' '' '1' '1'
##'frame3651_3700' '3651' '3700' '1' '' '' '1' '1'
##'frame3701_3750' '3701' '3750' '1' '' '' '1' '1'
##'frame3751_3800' '3751' '3800' '1' '' '' '1' '1'
##'frame3801_3850' '3801' '3850' '1' '' '' '1' '1'
##'frame3851_3900' '3851' '3900' '1' '' '' '1' '1'
##'frame3901_3950' '3901' '3950' '1' '' '' '1' '1'
##'frame3951_4000' '3951' '4000' '1' '' '' '1' '1'
##'frame4001_4050' '4001' '4050' '1' '' '' '1' '1'
##'frame4051_4100' '4051' '4100' '1' '' '' '1' '1'
##'frame4101_4150' '4101' '4150' '1' '' '' '1' '1'
##'frame4151_4200' '4151' '4200' '1' '' '' '1' '1'
##'frame4201_4250' '4201' '4250' '1' '' '' '1' '1'
##'frame4251_4300' '4251' '4300' '1' '' '' '1' '1'
##'frame4301_4350' '4301' '4350' '1' '' '' '1' '1'
##'frame4351_4400' '4351' '4400' '1' '' '' '1' '1'
##'frame4401_4450' '4401' '4450' '1' '' '' '1' '1'
##'frame4451_4500' '4451' '4500' '1' '' '' '1' '1'
##'frame4501_4550' '4501' '4550' '1' '' '' '1' '1'
##'frame4551_4600' '4551' '4600' '1' '' '' '1' '1'
##'frame4601_4650' '4601' '4650' '1' '' '' '1' '1'
##'frame4651_4700' '4651' '4700' '1' '' '' '1' '1'
##'frame4701_4750' '4701' '4750' '1' '' '' '1' '1'
##'frame4751_4800' '4751' '4800' '1' '' '' '1' '1'
##'frame4801_4850' '4801' '4850' '1' '' '' '1' '1'
##'frame4851_4900' '4851' '4900' '1' '' '' '1' '1'
##'frame4901_4950' '4901' '4950' '1' '' '' '1' '1'
##'frame4951_5000' '4951' '5000' '1' '' '' '1' '1'
##ENDJOBS

##END
