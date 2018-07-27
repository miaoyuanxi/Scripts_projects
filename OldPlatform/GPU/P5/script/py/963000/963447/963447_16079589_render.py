#encoding:utf-8
G_CG_NAME='Houdini'
G_USERID_PARENT='963000'
G_USERID='963447'
G_TASKID='16079589'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\963000\963447\16079589\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\963000\963447\16079589\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\963447'
G_VRAY_LICNESE='1'
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
##name=963447_16079589_render.py
##category=BJ
##level=79
##custom=963447
##nodelimit=500
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'Redshift_ROP10001' '1' '1' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10002' '2' '2' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10003' '3' '3' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10004' '4' '4' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10005' '5' '5' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10006' '6' '6' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10007' '7' '7' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10008' '8' '8' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10009' '9' '9' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10010' '10' '10' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10011' '11' '11' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10012' '12' '12' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10013' '13' '13' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10014' '14' '14' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10015' '15' '15' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10016' '16' '16' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10017' '17' '17' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10018' '18' '18' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10019' '19' '19' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10020' '20' '20' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10021' '21' '21' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10022' '22' '22' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10023' '23' '23' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10024' '24' '24' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10025' '25' '25' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10026' '26' '26' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10027' '27' '27' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10028' '28' '28' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10029' '29' '29' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10030' '30' '30' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10031' '31' '31' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10032' '32' '32' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10033' '33' '33' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10034' '34' '34' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10035' '35' '35' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10036' '36' '36' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10037' '37' '37' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10038' '38' '38' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10039' '39' '39' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10040' '40' '40' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10041' '41' '41' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10042' '42' '42' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10043' '43' '43' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10044' '44' '44' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10045' '45' '45' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10046' '46' '46' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10047' '47' '47' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10048' '48' '48' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10049' '49' '49' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10050' '50' '50' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10051' '51' '51' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10052' '52' '52' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10053' '53' '53' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10054' '54' '54' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10055' '55' '55' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10056' '56' '56' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10057' '57' '57' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10058' '58' '58' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10059' '59' '59' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10060' '60' '60' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10061' '61' '61' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10062' '62' '62' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10063' '63' '63' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10064' '64' '64' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10065' '65' '65' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10066' '66' '66' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10067' '67' '67' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10068' '68' '68' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10069' '69' '69' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10070' '70' '70' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10071' '71' '71' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10072' '72' '72' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10073' '73' '73' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10074' '74' '74' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10075' '75' '75' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10076' '76' '76' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10077' '77' '77' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10078' '78' '78' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10079' '79' '79' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10080' '80' '80' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10081' '81' '81' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10082' '82' '82' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10083' '83' '83' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10084' '84' '84' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10085' '85' '85' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10086' '86' '86' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10087' '87' '87' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10088' '88' '88' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10089' '89' '89' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10090' '90' '90' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10091' '91' '91' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10092' '92' '92' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10093' '93' '93' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10094' '94' '94' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10095' '95' '95' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10096' '96' '96' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10097' '97' '97' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10098' '98' '98' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10099' '99' '99' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10100' '100' '100' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10101' '101' '101' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10102' '102' '102' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10103' '103' '103' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10104' '104' '104' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10105' '105' '105' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10106' '106' '106' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10107' '107' '107' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10108' '108' '108' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10109' '109' '109' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10110' '110' '110' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10111' '111' '111' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10112' '112' '112' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10113' '113' '113' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10114' '114' '114' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10115' '115' '115' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10116' '116' '116' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10117' '117' '117' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10118' '118' '118' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10119' '119' '119' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10120' '120' '120' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10121' '121' '121' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10122' '122' '122' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10123' '123' '123' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10124' '124' '124' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10125' '125' '125' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10126' '126' '126' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10127' '127' '127' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10128' '128' '128' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10129' '129' '129' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10130' '130' '130' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10131' '131' '131' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10132' '132' '132' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10133' '133' '133' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10134' '134' '134' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10135' '135' '135' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10136' '136' '136' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10137' '137' '137' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10138' '138' '138' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10139' '139' '139' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10140' '140' '140' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10141' '141' '141' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10142' '142' '142' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10143' '143' '143' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10144' '144' '144' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10145' '145' '145' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10146' '146' '146' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10147' '147' '147' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10148' '148' '148' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10149' '149' '149' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP10150' '150' '150' '1' '/out/Redshift_ROP1' '-1' '1' '1'
##'Redshift_ROP20001' '1' '1' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20002' '2' '2' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20003' '3' '3' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20004' '4' '4' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20005' '5' '5' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20006' '6' '6' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20007' '7' '7' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20008' '8' '8' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20009' '9' '9' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20010' '10' '10' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20011' '11' '11' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20012' '12' '12' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20013' '13' '13' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20014' '14' '14' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20015' '15' '15' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20016' '16' '16' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20017' '17' '17' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20018' '18' '18' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20019' '19' '19' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20020' '20' '20' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20021' '21' '21' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20022' '22' '22' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20023' '23' '23' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20024' '24' '24' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20025' '25' '25' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20026' '26' '26' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20027' '27' '27' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20028' '28' '28' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20029' '29' '29' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20030' '30' '30' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20031' '31' '31' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20032' '32' '32' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20033' '33' '33' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20034' '34' '34' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20035' '35' '35' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20036' '36' '36' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20037' '37' '37' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20038' '38' '38' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20039' '39' '39' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20040' '40' '40' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20041' '41' '41' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20042' '42' '42' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20043' '43' '43' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20044' '44' '44' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20045' '45' '45' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20046' '46' '46' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20047' '47' '47' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20048' '48' '48' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20049' '49' '49' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20050' '50' '50' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20051' '51' '51' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20052' '52' '52' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20053' '53' '53' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20054' '54' '54' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20055' '55' '55' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20056' '56' '56' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20057' '57' '57' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20058' '58' '58' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20059' '59' '59' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20060' '60' '60' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20061' '61' '61' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20062' '62' '62' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20063' '63' '63' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20064' '64' '64' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20065' '65' '65' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20066' '66' '66' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20067' '67' '67' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20068' '68' '68' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20069' '69' '69' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20070' '70' '70' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20071' '71' '71' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20072' '72' '72' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20073' '73' '73' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20074' '74' '74' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20075' '75' '75' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20076' '76' '76' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20077' '77' '77' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20078' '78' '78' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20079' '79' '79' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20080' '80' '80' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20081' '81' '81' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20082' '82' '82' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20083' '83' '83' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20084' '84' '84' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20085' '85' '85' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20086' '86' '86' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20087' '87' '87' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20088' '88' '88' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20089' '89' '89' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20090' '90' '90' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20091' '91' '91' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20092' '92' '92' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20093' '93' '93' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20094' '94' '94' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20095' '95' '95' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20096' '96' '96' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20097' '97' '97' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20098' '98' '98' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20099' '99' '99' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20100' '100' '100' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20101' '101' '101' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20102' '102' '102' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20103' '103' '103' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20104' '104' '104' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20105' '105' '105' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20106' '106' '106' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20107' '107' '107' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20108' '108' '108' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20109' '109' '109' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20110' '110' '110' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20111' '111' '111' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20112' '112' '112' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20113' '113' '113' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20114' '114' '114' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20115' '115' '115' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20116' '116' '116' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20117' '117' '117' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20118' '118' '118' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20119' '119' '119' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20120' '120' '120' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20121' '121' '121' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20122' '122' '122' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20123' '123' '123' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20124' '124' '124' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20125' '125' '125' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20126' '126' '126' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20127' '127' '127' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20128' '128' '128' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20129' '129' '129' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20130' '130' '130' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20131' '131' '131' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20132' '132' '132' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20133' '133' '133' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20134' '134' '134' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20135' '135' '135' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20136' '136' '136' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20137' '137' '137' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20138' '138' '138' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20139' '139' '139' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20140' '140' '140' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20141' '141' '141' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20142' '142' '142' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20143' '143' '143' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20144' '144' '144' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20145' '145' '145' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20146' '146' '146' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20147' '147' '147' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20148' '148' '148' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20149' '149' '149' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##'Redshift_ROP20150' '150' '150' '1' '/out/Redshift_ROP2' '-1' '1' '1'
##ENDJOBS

##END
