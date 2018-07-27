#encoding:utf-8
G_CG_NAME='Houdini'
G_USERID_PARENT='963000'
G_USERID='963447'
G_TASKID='16069206'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\963000\963447\16069206\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\963000\963447\16069206\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\963447'
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
    RenderAction.main(**paramDict)


##BEGIN
##description=This is a test script
##name=963447_16069206_render.py
##category=BJ
##level=79
##custom=963447
##nodelimit=500
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'Redshift_ROP50001' '1' '1' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50002' '2' '2' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50003' '3' '3' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50004' '4' '4' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50005' '5' '5' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50006' '6' '6' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50007' '7' '7' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50008' '8' '8' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50009' '9' '9' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50010' '10' '10' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50011' '11' '11' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50012' '12' '12' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50013' '13' '13' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50014' '14' '14' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50015' '15' '15' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50016' '16' '16' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50017' '17' '17' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50018' '18' '18' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50019' '19' '19' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50020' '20' '20' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50021' '21' '21' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50022' '22' '22' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50023' '23' '23' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50024' '24' '24' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50025' '25' '25' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50026' '26' '26' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50027' '27' '27' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50028' '28' '28' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50029' '29' '29' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50030' '30' '30' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50031' '31' '31' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50032' '32' '32' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50033' '33' '33' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50034' '34' '34' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50035' '35' '35' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50036' '36' '36' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50037' '37' '37' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50038' '38' '38' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50039' '39' '39' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50040' '40' '40' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50041' '41' '41' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50042' '42' '42' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50043' '43' '43' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50044' '44' '44' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50045' '45' '45' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50046' '46' '46' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50047' '47' '47' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50048' '48' '48' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50049' '49' '49' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50050' '50' '50' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50051' '51' '51' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50052' '52' '52' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50053' '53' '53' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50054' '54' '54' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50055' '55' '55' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50056' '56' '56' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50057' '57' '57' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50058' '58' '58' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50059' '59' '59' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50060' '60' '60' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50061' '61' '61' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50062' '62' '62' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50063' '63' '63' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50064' '64' '64' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50065' '65' '65' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50066' '66' '66' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50067' '67' '67' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50068' '68' '68' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50069' '69' '69' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50070' '70' '70' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50071' '71' '71' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50072' '72' '72' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50073' '73' '73' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50074' '74' '74' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50075' '75' '75' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50076' '76' '76' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50077' '77' '77' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50078' '78' '78' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50079' '79' '79' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50080' '80' '80' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50081' '81' '81' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50082' '82' '82' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50083' '83' '83' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50084' '84' '84' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50085' '85' '85' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50086' '86' '86' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50087' '87' '87' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50088' '88' '88' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50089' '89' '89' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50090' '90' '90' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50091' '91' '91' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50092' '92' '92' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50093' '93' '93' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50094' '94' '94' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50095' '95' '95' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50096' '96' '96' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50097' '97' '97' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50098' '98' '98' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50099' '99' '99' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50100' '100' '100' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50101' '101' '101' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50102' '102' '102' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50103' '103' '103' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50104' '104' '104' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50105' '105' '105' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50106' '106' '106' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50107' '107' '107' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50108' '108' '108' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50109' '109' '109' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50110' '110' '110' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50111' '111' '111' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50112' '112' '112' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50113' '113' '113' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50114' '114' '114' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50115' '115' '115' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50116' '116' '116' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50117' '117' '117' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50118' '118' '118' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50119' '119' '119' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50120' '120' '120' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50121' '121' '121' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50122' '122' '122' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50123' '123' '123' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50124' '124' '124' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50125' '125' '125' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50126' '126' '126' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50127' '127' '127' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50128' '128' '128' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50129' '129' '129' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50130' '130' '130' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50131' '131' '131' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50132' '132' '132' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50133' '133' '133' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50134' '134' '134' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50135' '135' '135' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50136' '136' '136' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50137' '137' '137' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50138' '138' '138' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50139' '139' '139' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50140' '140' '140' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50141' '141' '141' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50142' '142' '142' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50143' '143' '143' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50144' '144' '144' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50145' '145' '145' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50146' '146' '146' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50147' '147' '147' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50148' '148' '148' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50149' '149' '149' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50150' '150' '150' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50151' '151' '151' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50152' '152' '152' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50153' '153' '153' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50154' '154' '154' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50155' '155' '155' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50156' '156' '156' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50157' '157' '157' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50158' '158' '158' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50159' '159' '159' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP50160' '160' '160' '1' '/out/Redshift_ROP5' '-1' '1' '1'
##'Redshift_ROP60001' '1' '1' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60002' '2' '2' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60003' '3' '3' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60004' '4' '4' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60005' '5' '5' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60006' '6' '6' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60007' '7' '7' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60008' '8' '8' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60009' '9' '9' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60010' '10' '10' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60011' '11' '11' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60012' '12' '12' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60013' '13' '13' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60014' '14' '14' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60015' '15' '15' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60016' '16' '16' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60017' '17' '17' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60018' '18' '18' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60019' '19' '19' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60020' '20' '20' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60021' '21' '21' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60022' '22' '22' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60023' '23' '23' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60024' '24' '24' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60025' '25' '25' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60026' '26' '26' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60027' '27' '27' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60028' '28' '28' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60029' '29' '29' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60030' '30' '30' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60031' '31' '31' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60032' '32' '32' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60033' '33' '33' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60034' '34' '34' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60035' '35' '35' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60036' '36' '36' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60037' '37' '37' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60038' '38' '38' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60039' '39' '39' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60040' '40' '40' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60041' '41' '41' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60042' '42' '42' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60043' '43' '43' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60044' '44' '44' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60045' '45' '45' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60046' '46' '46' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60047' '47' '47' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60048' '48' '48' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60049' '49' '49' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60050' '50' '50' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60051' '51' '51' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60052' '52' '52' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60053' '53' '53' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60054' '54' '54' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60055' '55' '55' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60056' '56' '56' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60057' '57' '57' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60058' '58' '58' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60059' '59' '59' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60060' '60' '60' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60061' '61' '61' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60062' '62' '62' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60063' '63' '63' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60064' '64' '64' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60065' '65' '65' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60066' '66' '66' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60067' '67' '67' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60068' '68' '68' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60069' '69' '69' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60070' '70' '70' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60071' '71' '71' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60072' '72' '72' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60073' '73' '73' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60074' '74' '74' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60075' '75' '75' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60076' '76' '76' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60077' '77' '77' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60078' '78' '78' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60079' '79' '79' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60080' '80' '80' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60081' '81' '81' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60082' '82' '82' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60083' '83' '83' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60084' '84' '84' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60085' '85' '85' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60086' '86' '86' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60087' '87' '87' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60088' '88' '88' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60089' '89' '89' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60090' '90' '90' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60091' '91' '91' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60092' '92' '92' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60093' '93' '93' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60094' '94' '94' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60095' '95' '95' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60096' '96' '96' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60097' '97' '97' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60098' '98' '98' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60099' '99' '99' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60100' '100' '100' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60101' '101' '101' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60102' '102' '102' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60103' '103' '103' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60104' '104' '104' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60105' '105' '105' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60106' '106' '106' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60107' '107' '107' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60108' '108' '108' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60109' '109' '109' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60110' '110' '110' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60111' '111' '111' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60112' '112' '112' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60113' '113' '113' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60114' '114' '114' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60115' '115' '115' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60116' '116' '116' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60117' '117' '117' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60118' '118' '118' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60119' '119' '119' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60120' '120' '120' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60121' '121' '121' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60122' '122' '122' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60123' '123' '123' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60124' '124' '124' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60125' '125' '125' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60126' '126' '126' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60127' '127' '127' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60128' '128' '128' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60129' '129' '129' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60130' '130' '130' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60131' '131' '131' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60132' '132' '132' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60133' '133' '133' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60134' '134' '134' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60135' '135' '135' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60136' '136' '136' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60137' '137' '137' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60138' '138' '138' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60139' '139' '139' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60140' '140' '140' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60141' '141' '141' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60142' '142' '142' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60143' '143' '143' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60144' '144' '144' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60145' '145' '145' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60146' '146' '146' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60147' '147' '147' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60148' '148' '148' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60149' '149' '149' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60150' '150' '150' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60151' '151' '151' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60152' '152' '152' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60153' '153' '153' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60154' '154' '154' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60155' '155' '155' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60156' '156' '156' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60157' '157' '157' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60158' '158' '158' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60159' '159' '159' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##'Redshift_ROP60160' '160' '160' '1' '/out/Redshift_ROP6' '-1' '1' '1'
##ENDJOBS

##END
