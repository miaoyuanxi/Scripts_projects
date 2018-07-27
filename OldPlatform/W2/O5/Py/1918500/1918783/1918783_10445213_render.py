#encoding:utf-8
G_CG_NAME='MayaClient'
G_USERID_PARENT='1918500'
G_USERID='1918783'
G_TASKID='10445213'
G_POOL=r'\\10.60.100.101\p5'
G_CONFIG=r''
G_PLUGINS=r''
G_RENDEROS=r''
baseRenderPy=r'\\10.60.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.60.100.101\p5\script\py\py\1918783'
G_VRAY_LICENSE='2'
#script_param_mark#
import os,sys,shutil,time
G_SCRIPT_START_TIME = str(int(time.time()))

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
    paramDict = {'G_JOB_ID':G_JOB_ID,'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_NODE_PY':nodePyDir,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION,'G_CONFIG':G_CONFIG,'G_PLUGINS':G_PLUGINS,'G_RENDEROS':G_RENDEROS,'G_CG_TILE':G_CG_TILE,'G_CG_TILECOUNT':G_CG_TILECOUNT,'G_SCRIPT_START_TIME':G_SCRIPT_START_TIME}
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
##name=1918783_10445213_render.py
##requirements=|OS-Windows|RAM-64
##level=79
##custom=1918783
##nodelimit=10
##nodeblacklimit=3
##constraints=10_60_100_103
##frequencytime=60
##frequencycount=100
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0001' '1' '1' '1' '' '' '0' '1'
##'frame0002' '2' '2' '1' '' '' '0' '1'
##'frame0003' '3' '3' '1' '' '' '0' '1'
##'frame0004' '4' '4' '1' '' '' '0' '1'
##'frame0005' '5' '5' '1' '' '' '0' '1'
##'frame0006' '6' '6' '1' '' '' '0' '1'
##'frame0007' '7' '7' '1' '' '' '0' '1'
##'frame0008' '8' '8' '1' '' '' '0' '1'
##'frame0009' '9' '9' '1' '' '' '0' '1'
##'frame0010' '10' '10' '1' '' '' '0' '1'
##'frame0011' '11' '11' '1' '' '' '0' '1'
##'frame0012' '12' '12' '1' '' '' '0' '1'
##'frame0013' '13' '13' '1' '' '' '0' '1'
##'frame0014' '14' '14' '1' '' '' '0' '1'
##'frame0015' '15' '15' '1' '' '' '0' '1'
##'frame0016' '16' '16' '1' '' '' '0' '1'
##'frame0017' '17' '17' '1' '' '' '0' '1'
##'frame0018' '18' '18' '1' '' '' '0' '1'
##'frame0019' '19' '19' '1' '' '' '0' '1'
##'frame0020' '20' '20' '1' '' '' '0' '1'
##'frame0021' '21' '21' '1' '' '' '0' '1'
##'frame0022' '22' '22' '1' '' '' '0' '1'
##'frame0023' '23' '23' '1' '' '' '0' '1'
##'frame0024' '24' '24' '1' '' '' '0' '1'
##'frame0025' '25' '25' '1' '' '' '0' '1'
##'frame0026' '26' '26' '1' '' '' '0' '1'
##'frame0027' '27' '27' '1' '' '' '0' '1'
##'frame0028' '28' '28' '1' '' '' '0' '1'
##'frame0029' '29' '29' '1' '' '' '0' '1'
##'frame0030' '30' '30' '1' '' '' '0' '1'
##'frame0031' '31' '31' '1' '' '' '0' '1'
##'frame0032' '32' '32' '1' '' '' '0' '1'
##'frame0033' '33' '33' '1' '' '' '0' '1'
##'frame0034' '34' '34' '1' '' '' '0' '1'
##'frame0035' '35' '35' '1' '' '' '0' '1'
##'frame0036' '36' '36' '1' '' '' '0' '1'
##'frame0037' '37' '37' '1' '' '' '0' '1'
##'frame0038' '38' '38' '1' '' '' '0' '1'
##'frame0039' '39' '39' '1' '' '' '0' '1'
##'frame0040' '40' '40' '1' '' '' '0' '1'
##'frame0041' '41' '41' '1' '' '' '0' '1'
##'frame0042' '42' '42' '1' '' '' '0' '1'
##'frame0043' '43' '43' '1' '' '' '0' '1'
##'frame0044' '44' '44' '1' '' '' '0' '1'
##'frame0045' '45' '45' '1' '' '' '0' '1'
##'frame0046' '46' '46' '1' '' '' '0' '1'
##'frame0047' '47' '47' '1' '' '' '0' '1'
##'frame0048' '48' '48' '1' '' '' '0' '1'
##'frame0049' '49' '49' '1' '' '' '0' '1'
##'frame0050' '50' '50' '1' '' '' '0' '1'
##'frame0051' '51' '51' '1' '' '' '0' '1'
##'frame0052' '52' '52' '1' '' '' '0' '1'
##'frame0053' '53' '53' '1' '' '' '0' '1'
##'frame0054' '54' '54' '1' '' '' '0' '1'
##'frame0055' '55' '55' '1' '' '' '0' '1'
##'frame0056' '56' '56' '1' '' '' '0' '1'
##'frame0057' '57' '57' '1' '' '' '0' '1'
##'frame0058' '58' '58' '1' '' '' '0' '1'
##'frame0059' '59' '59' '1' '' '' '0' '1'
##'frame0060' '60' '60' '1' '' '' '0' '1'
##'frame0061' '61' '61' '1' '' '' '0' '1'
##'frame0062' '62' '62' '1' '' '' '0' '1'
##'frame0063' '63' '63' '1' '' '' '0' '1'
##'frame0064' '64' '64' '1' '' '' '0' '1'
##'frame0065' '65' '65' '1' '' '' '0' '1'
##'frame0066' '66' '66' '1' '' '' '0' '1'
##'frame0067' '67' '67' '1' '' '' '0' '1'
##'frame0068' '68' '68' '1' '' '' '0' '1'
##'frame0069' '69' '69' '1' '' '' '0' '1'
##'frame0070' '70' '70' '1' '' '' '0' '1'
##'frame0071' '71' '71' '1' '' '' '0' '1'
##'frame0072' '72' '72' '1' '' '' '0' '1'
##'frame0073' '73' '73' '1' '' '' '0' '1'
##'frame0074' '74' '74' '1' '' '' '0' '1'
##'frame0075' '75' '75' '1' '' '' '0' '1'
##'frame0076' '76' '76' '1' '' '' '0' '1'
##'frame0077' '77' '77' '1' '' '' '0' '1'
##'frame0078' '78' '78' '1' '' '' '0' '1'
##'frame0079' '79' '79' '1' '' '' '0' '1'
##'frame0080' '80' '80' '1' '' '' '0' '1'
##'frame0081' '81' '81' '1' '' '' '0' '1'
##'frame0082' '82' '82' '1' '' '' '0' '1'
##'frame0083' '83' '83' '1' '' '' '0' '1'
##'frame0084' '84' '84' '1' '' '' '0' '1'
##'frame0085' '85' '85' '1' '' '' '0' '1'
##'frame0086' '86' '86' '1' '' '' '0' '1'
##'frame0087' '87' '87' '1' '' '' '0' '1'
##'frame0088' '88' '88' '1' '' '' '0' '1'
##'frame0089' '89' '89' '1' '' '' '0' '1'
##'frame0090' '90' '90' '1' '' '' '0' '1'
##'frame0091' '91' '91' '1' '' '' '0' '1'
##'frame0092' '92' '92' '1' '' '' '0' '1'
##'frame0093' '93' '93' '1' '' '' '0' '1'
##'frame0094' '94' '94' '1' '' '' '0' '1'
##'frame0095' '95' '95' '1' '' '' '0' '1'
##'frame0096' '96' '96' '1' '' '' '0' '1'
##'frame0097' '97' '97' '1' '' '' '0' '1'
##'frame0098' '98' '98' '1' '' '' '0' '1'
##'frame0099' '99' '99' '1' '' '' '0' '1'
##'frame0100' '100' '100' '1' '' '' '0' '1'
##ENDJOBS

##END
