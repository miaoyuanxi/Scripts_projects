#encoding:utf-8
G_CG_NAME='Houdini'
G_USERID_PARENT='1917500'
G_USERID='1917527'
G_TASKID='16157717'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\1917500\1917527\16157717\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\1917500\1917527\16157717\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\1917527'
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
##name=1917527_16157717_render.py
##requirements=|OS-Windows
##category=BJ
##level=79
##custom=1917527
##nodelimit=99
##nodeblacklimit=3
##constraints=|10_90_100_102
##priority=20
##autorestartlimit=4
##jobdurationlimit=2592000
##durationlimitdisable=false
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'render1_250[1]' '1' '250' '1' '/obj/cloud_setup/cloud_base_VOL/render' '0' '' ''
##'render1_250[1]' '1' '250' '1' '/obj/cloud_setup/cloud_base_GEO/render' '0' '' ''
##'render1_250[1]' '1' '250' '1' '/obj/cloud_setup/cloud_base_detail_VOL/render' '0' '' ''
##'RND0001' '1' '1' '1' '/out/RND' '-1' '1' '1'
##'RND0002' '2' '2' '1' '/out/RND' '-1' '1' '1'
##'RND0003' '3' '3' '1' '/out/RND' '-1' '1' '1'
##'RND0004' '4' '4' '1' '/out/RND' '-1' '1' '1'
##'RND0005' '5' '5' '1' '/out/RND' '-1' '1' '1'
##'RND0006' '6' '6' '1' '/out/RND' '-1' '1' '1'
##'RND0007' '7' '7' '1' '/out/RND' '-1' '1' '1'
##'RND0008' '8' '8' '1' '/out/RND' '-1' '1' '1'
##'RND0009' '9' '9' '1' '/out/RND' '-1' '1' '1'
##'RND0010' '10' '10' '1' '/out/RND' '-1' '1' '1'
##'RND0011' '11' '11' '1' '/out/RND' '-1' '1' '1'
##'RND0012' '12' '12' '1' '/out/RND' '-1' '1' '1'
##'RND0013' '13' '13' '1' '/out/RND' '-1' '1' '1'
##'RND0014' '14' '14' '1' '/out/RND' '-1' '1' '1'
##'RND0015' '15' '15' '1' '/out/RND' '-1' '1' '1'
##'RND0016' '16' '16' '1' '/out/RND' '-1' '1' '1'
##'RND0017' '17' '17' '1' '/out/RND' '-1' '1' '1'
##'RND0018' '18' '18' '1' '/out/RND' '-1' '1' '1'
##'RND0019' '19' '19' '1' '/out/RND' '-1' '1' '1'
##'RND0020' '20' '20' '1' '/out/RND' '-1' '1' '1'
##'RND0021' '21' '21' '1' '/out/RND' '-1' '1' '1'
##'RND0022' '22' '22' '1' '/out/RND' '-1' '1' '1'
##'RND0023' '23' '23' '1' '/out/RND' '-1' '1' '1'
##'RND0024' '24' '24' '1' '/out/RND' '-1' '1' '1'
##'RND0025' '25' '25' '1' '/out/RND' '-1' '1' '1'
##'RND0026' '26' '26' '1' '/out/RND' '-1' '1' '1'
##'RND0027' '27' '27' '1' '/out/RND' '-1' '1' '1'
##'RND0028' '28' '28' '1' '/out/RND' '-1' '1' '1'
##'RND0029' '29' '29' '1' '/out/RND' '-1' '1' '1'
##'RND0030' '30' '30' '1' '/out/RND' '-1' '1' '1'
##'RND0031' '31' '31' '1' '/out/RND' '-1' '1' '1'
##'RND0032' '32' '32' '1' '/out/RND' '-1' '1' '1'
##'RND0033' '33' '33' '1' '/out/RND' '-1' '1' '1'
##'RND0034' '34' '34' '1' '/out/RND' '-1' '1' '1'
##'RND0035' '35' '35' '1' '/out/RND' '-1' '1' '1'
##'RND0036' '36' '36' '1' '/out/RND' '-1' '1' '1'
##'RND0037' '37' '37' '1' '/out/RND' '-1' '1' '1'
##'RND0038' '38' '38' '1' '/out/RND' '-1' '1' '1'
##'RND0039' '39' '39' '1' '/out/RND' '-1' '1' '1'
##'RND0040' '40' '40' '1' '/out/RND' '-1' '1' '1'
##'RND0041' '41' '41' '1' '/out/RND' '-1' '1' '1'
##'RND0042' '42' '42' '1' '/out/RND' '-1' '1' '1'
##'RND0043' '43' '43' '1' '/out/RND' '-1' '1' '1'
##'RND0044' '44' '44' '1' '/out/RND' '-1' '1' '1'
##'RND0045' '45' '45' '1' '/out/RND' '-1' '1' '1'
##'RND0046' '46' '46' '1' '/out/RND' '-1' '1' '1'
##'RND0047' '47' '47' '1' '/out/RND' '-1' '1' '1'
##'RND0048' '48' '48' '1' '/out/RND' '-1' '1' '1'
##'RND0049' '49' '49' '1' '/out/RND' '-1' '1' '1'
##'RND0050' '50' '50' '1' '/out/RND' '-1' '1' '1'
##'RND0051' '51' '51' '1' '/out/RND' '-1' '1' '1'
##'RND0052' '52' '52' '1' '/out/RND' '-1' '1' '1'
##'RND0053' '53' '53' '1' '/out/RND' '-1' '1' '1'
##'RND0054' '54' '54' '1' '/out/RND' '-1' '1' '1'
##'RND0055' '55' '55' '1' '/out/RND' '-1' '1' '1'
##'RND0056' '56' '56' '1' '/out/RND' '-1' '1' '1'
##'RND0057' '57' '57' '1' '/out/RND' '-1' '1' '1'
##'RND0058' '58' '58' '1' '/out/RND' '-1' '1' '1'
##'RND0059' '59' '59' '1' '/out/RND' '-1' '1' '1'
##'RND0060' '60' '60' '1' '/out/RND' '-1' '1' '1'
##'RND0061' '61' '61' '1' '/out/RND' '-1' '1' '1'
##'RND0062' '62' '62' '1' '/out/RND' '-1' '1' '1'
##'RND0063' '63' '63' '1' '/out/RND' '-1' '1' '1'
##'RND0064' '64' '64' '1' '/out/RND' '-1' '1' '1'
##'RND0065' '65' '65' '1' '/out/RND' '-1' '1' '1'
##'RND0066' '66' '66' '1' '/out/RND' '-1' '1' '1'
##'RND0067' '67' '67' '1' '/out/RND' '-1' '1' '1'
##'RND0068' '68' '68' '1' '/out/RND' '-1' '1' '1'
##'RND0069' '69' '69' '1' '/out/RND' '-1' '1' '1'
##'RND0070' '70' '70' '1' '/out/RND' '-1' '1' '1'
##'RND0071' '71' '71' '1' '/out/RND' '-1' '1' '1'
##'RND0072' '72' '72' '1' '/out/RND' '-1' '1' '1'
##'RND0073' '73' '73' '1' '/out/RND' '-1' '1' '1'
##'RND0074' '74' '74' '1' '/out/RND' '-1' '1' '1'
##'RND0075' '75' '75' '1' '/out/RND' '-1' '1' '1'
##'RND0076' '76' '76' '1' '/out/RND' '-1' '1' '1'
##'RND0077' '77' '77' '1' '/out/RND' '-1' '1' '1'
##'RND0078' '78' '78' '1' '/out/RND' '-1' '1' '1'
##'RND0079' '79' '79' '1' '/out/RND' '-1' '1' '1'
##'RND0080' '80' '80' '1' '/out/RND' '-1' '1' '1'
##'RND0081' '81' '81' '1' '/out/RND' '-1' '1' '1'
##'RND0082' '82' '82' '1' '/out/RND' '-1' '1' '1'
##'RND0083' '83' '83' '1' '/out/RND' '-1' '1' '1'
##'RND0084' '84' '84' '1' '/out/RND' '-1' '1' '1'
##'RND0085' '85' '85' '1' '/out/RND' '-1' '1' '1'
##'RND0086' '86' '86' '1' '/out/RND' '-1' '1' '1'
##'RND0087' '87' '87' '1' '/out/RND' '-1' '1' '1'
##'RND0088' '88' '88' '1' '/out/RND' '-1' '1' '1'
##'RND0089' '89' '89' '1' '/out/RND' '-1' '1' '1'
##'RND0090' '90' '90' '1' '/out/RND' '-1' '1' '1'
##'RND0091' '91' '91' '1' '/out/RND' '-1' '1' '1'
##'RND0092' '92' '92' '1' '/out/RND' '-1' '1' '1'
##'RND0093' '93' '93' '1' '/out/RND' '-1' '1' '1'
##'RND0094' '94' '94' '1' '/out/RND' '-1' '1' '1'
##'RND0095' '95' '95' '1' '/out/RND' '-1' '1' '1'
##'RND0096' '96' '96' '1' '/out/RND' '-1' '1' '1'
##'RND0097' '97' '97' '1' '/out/RND' '-1' '1' '1'
##'RND0098' '98' '98' '1' '/out/RND' '-1' '1' '1'
##'RND0099' '99' '99' '1' '/out/RND' '-1' '1' '1'
##'RND0100' '100' '100' '1' '/out/RND' '-1' '1' '1'
##ENDJOBS

##END
