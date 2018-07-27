#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='1918500'
G_USERID='1918770'
G_TASKID='10442902'
G_POOL=r'\\10.60.100.101\p5'
G_CONFIG=r'\\10.60.100.101\p5\config\1918500\1918770\10442902\render.json'
G_PLUGINS=r'\\10.60.100.101\p5\config\1918500\1918770\10442902\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.60.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.60.100.101\p5\script\py\py\1918770'
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
##name=1918770_10442902_render.py
##requirements=|OS-Windows|RAM-64
##category=BJ
##level=50
##custom=1918770
##nodelimit=500
##nodeblacklimit=3
##constraints=|10_60_200_103
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0031' '31' '31' '1' '' '' '1' '1'
##'frame0032' '32' '32' '1' '' '' '1' '1'
##'frame0033' '33' '33' '1' '' '' '1' '1'
##'frame0034' '34' '34' '1' '' '' '1' '1'
##'frame0035' '35' '35' '1' '' '' '1' '1'
##'frame0036' '36' '36' '1' '' '' '1' '1'
##'frame0037' '37' '37' '1' '' '' '1' '1'
##'frame0038' '38' '38' '1' '' '' '1' '1'
##'frame0039' '39' '39' '1' '' '' '1' '1'
##'frame0040' '40' '40' '1' '' '' '1' '1'
##'frame0041' '41' '41' '1' '' '' '1' '1'
##'frame0042' '42' '42' '1' '' '' '1' '1'
##'frame0043' '43' '43' '1' '' '' '1' '1'
##'frame0044' '44' '44' '1' '' '' '1' '1'
##'frame0045' '45' '45' '1' '' '' '1' '1'
##'frame0046' '46' '46' '1' '' '' '1' '1'
##'frame0047' '47' '47' '1' '' '' '1' '1'
##'frame0048' '48' '48' '1' '' '' '1' '1'
##'frame0049' '49' '49' '1' '' '' '1' '1'
##'frame0050' '50' '50' '1' '' '' '1' '1'
##'frame0051' '51' '51' '1' '' '' '1' '1'
##'frame0052' '52' '52' '1' '' '' '1' '1'
##'frame0053' '53' '53' '1' '' '' '1' '1'
##'frame0054' '54' '54' '1' '' '' '1' '1'
##'frame0055' '55' '55' '1' '' '' '1' '1'
##'frame0056' '56' '56' '1' '' '' '1' '1'
##'frame0057' '57' '57' '1' '' '' '1' '1'
##'frame0058' '58' '58' '1' '' '' '1' '1'
##'frame0059' '59' '59' '1' '' '' '1' '1'
##'frame0060' '60' '60' '1' '' '' '1' '1'
##'frame0061' '61' '61' '1' '' '' '1' '1'
##'frame0062' '62' '62' '1' '' '' '1' '1'
##'frame0063' '63' '63' '1' '' '' '1' '1'
##'frame0064' '64' '64' '1' '' '' '1' '1'
##'frame0065' '65' '65' '1' '' '' '1' '1'
##'frame0066' '66' '66' '1' '' '' '1' '1'
##'frame0067' '67' '67' '1' '' '' '1' '1'
##'frame0068' '68' '68' '1' '' '' '1' '1'
##'frame0069' '69' '69' '1' '' '' '1' '1'
##'frame0070' '70' '70' '1' '' '' '1' '1'
##'frame0071' '71' '71' '1' '' '' '1' '1'
##'frame0072' '72' '72' '1' '' '' '1' '1'
##'frame0073' '73' '73' '1' '' '' '1' '1'
##'frame0074' '74' '74' '1' '' '' '1' '1'
##'frame0075' '75' '75' '1' '' '' '1' '1'
##'frame0175' '175' '175' '1' '' '' '1' '1'
##'frame0176' '176' '176' '1' '' '' '1' '1'
##'frame0177' '177' '177' '1' '' '' '1' '1'
##'frame0178' '178' '178' '1' '' '' '1' '1'
##'frame0179' '179' '179' '1' '' '' '1' '1'
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
