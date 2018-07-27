#encoding:utf-8
G_CG_NAME='Houdini'
G_USERID_PARENT='963000'
G_USERID='963447'
G_TASKID='16064134'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\963000\963447\16064134\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\963000\963447\16064134\plugins.json'
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
##name=963447_16064134_render.py
##category=BJ
##level=79
##custom=963447
##nodelimit=500
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'Redshift_ROP30001' '1' '1' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30002' '2' '2' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30003' '3' '3' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30004' '4' '4' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30005' '5' '5' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30006' '6' '6' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30007' '7' '7' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30008' '8' '8' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30009' '9' '9' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30010' '10' '10' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30011' '11' '11' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30012' '12' '12' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30013' '13' '13' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30014' '14' '14' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30015' '15' '15' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30016' '16' '16' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30017' '17' '17' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30018' '18' '18' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30019' '19' '19' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30020' '20' '20' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30021' '21' '21' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30022' '22' '22' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30023' '23' '23' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30024' '24' '24' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30025' '25' '25' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30026' '26' '26' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30027' '27' '27' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30028' '28' '28' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30029' '29' '29' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30030' '30' '30' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30031' '31' '31' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30032' '32' '32' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30033' '33' '33' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30034' '34' '34' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30035' '35' '35' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30036' '36' '36' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30037' '37' '37' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30038' '38' '38' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30039' '39' '39' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30040' '40' '40' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30041' '41' '41' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30042' '42' '42' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30043' '43' '43' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30044' '44' '44' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30045' '45' '45' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30046' '46' '46' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30047' '47' '47' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30048' '48' '48' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30049' '49' '49' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30050' '50' '50' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30051' '51' '51' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30052' '52' '52' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30053' '53' '53' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30054' '54' '54' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30055' '55' '55' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30056' '56' '56' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30057' '57' '57' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30058' '58' '58' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30059' '59' '59' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30060' '60' '60' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30061' '61' '61' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30062' '62' '62' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30063' '63' '63' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30064' '64' '64' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30065' '65' '65' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30066' '66' '66' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30067' '67' '67' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30068' '68' '68' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30069' '69' '69' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30070' '70' '70' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30071' '71' '71' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30072' '72' '72' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30073' '73' '73' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30074' '74' '74' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30075' '75' '75' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30076' '76' '76' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30077' '77' '77' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30078' '78' '78' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30079' '79' '79' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP30080' '80' '80' '1' '/out/Redshift_ROP3' '-1' '1' '1'
##'Redshift_ROP40001' '1' '1' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40002' '2' '2' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40003' '3' '3' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40004' '4' '4' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40005' '5' '5' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40006' '6' '6' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40007' '7' '7' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40008' '8' '8' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40009' '9' '9' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40010' '10' '10' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40011' '11' '11' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40012' '12' '12' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40013' '13' '13' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40014' '14' '14' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40015' '15' '15' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40016' '16' '16' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40017' '17' '17' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40018' '18' '18' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40019' '19' '19' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40020' '20' '20' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40021' '21' '21' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40022' '22' '22' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40023' '23' '23' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40024' '24' '24' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40025' '25' '25' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40026' '26' '26' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40027' '27' '27' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40028' '28' '28' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40029' '29' '29' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40030' '30' '30' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40031' '31' '31' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40032' '32' '32' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40033' '33' '33' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40034' '34' '34' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40035' '35' '35' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40036' '36' '36' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40037' '37' '37' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40038' '38' '38' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40039' '39' '39' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40040' '40' '40' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40041' '41' '41' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40042' '42' '42' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40043' '43' '43' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40044' '44' '44' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40045' '45' '45' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40046' '46' '46' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40047' '47' '47' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40048' '48' '48' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40049' '49' '49' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40050' '50' '50' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40051' '51' '51' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40052' '52' '52' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40053' '53' '53' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40054' '54' '54' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40055' '55' '55' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40056' '56' '56' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40057' '57' '57' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40058' '58' '58' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40059' '59' '59' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40060' '60' '60' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40061' '61' '61' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40062' '62' '62' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40063' '63' '63' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40064' '64' '64' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40065' '65' '65' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40066' '66' '66' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40067' '67' '67' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40068' '68' '68' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40069' '69' '69' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40070' '70' '70' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40071' '71' '71' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40072' '72' '72' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40073' '73' '73' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40074' '74' '74' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40075' '75' '75' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40076' '76' '76' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40077' '77' '77' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40078' '78' '78' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40079' '79' '79' '1' '/out/Redshift_ROP4' '-1' '1' '1'
##'Redshift_ROP40080' '80' '80' '1' '/out/Redshift_ROP4' '-1' '1' '1'
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
##ENDJOBS

##END
