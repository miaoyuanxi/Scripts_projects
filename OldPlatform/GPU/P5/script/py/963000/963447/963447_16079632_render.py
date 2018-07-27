#encoding:utf-8
G_CG_NAME='Houdini'
G_USERID_PARENT='963000'
G_USERID='963447'
G_TASKID='16079632'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\963000\963447\16079632\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\963000\963447\16079632\plugins.json'
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
##name=963447_16079632_render.py
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
##ENDJOBS

##END
