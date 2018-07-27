#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='963000'
G_USERID='963394'
G_TASKID='8038968'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\963000\963394\8038968\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\963000\963394\8038968\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.70.242.102\p5\script\py\py\common'
userRenderPy=r'\\10.70.242.102\p5\script\py\py\963394'
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
                

cgList=['Nuke','Preprocess','Max','MaxClient','Merge','Blender','C4D','Lightwave','Clarisse','SketchUp','Vue','Vray','OctaneRender','Softimage','Mrstand','Maya','MayaPre','MayaClient','Houdini','Katana']#preprocess,maxclient
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
    shutil.rmtree(nodePyDir)
    copyFolder(scriptBase,scriptNodeBase)
    copyFolder(scriptCg,scriptNodeCg)
    copyFolder(userRenderPy,nodePyDir)
    copyFolder(scriptUtil,scriptNodeUtil)
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
##name=963394_8038968_render.py
##properties=|BJ
##level=79
##custom=963394
##nodelimit=99
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0000' '0' '0' '1' '' '' '1' '1'
##'frame0001' '1' '1' '1' '' '' '1' '1'
##'frame0002' '2' '2' '1' '' '' '1' '1'
##'frame0003' '3' '3' '1' '' '' '1' '1'
##'frame0004' '4' '4' '1' '' '' '1' '1'
##'frame0005' '5' '5' '1' '' '' '1' '1'
##'frame0006' '6' '6' '1' '' '' '1' '1'
##'frame0007' '7' '7' '1' '' '' '1' '1'
##'frame0008' '8' '8' '1' '' '' '1' '1'
##'frame0009' '9' '9' '1' '' '' '1' '1'
##'frame0010' '10' '10' '1' '' '' '1' '1'
##'frame0011' '11' '11' '1' '' '' '1' '1'
##'frame0012' '12' '12' '1' '' '' '1' '1'
##'frame0013' '13' '13' '1' '' '' '1' '1'
##'frame0014' '14' '14' '1' '' '' '1' '1'
##'frame0015' '15' '15' '1' '' '' '1' '1'
##'frame0016' '16' '16' '1' '' '' '1' '1'
##'frame0017' '17' '17' '1' '' '' '1' '1'
##'frame0018' '18' '18' '1' '' '' '1' '1'
##'frame0019' '19' '19' '1' '' '' '1' '1'
##'frame0020' '20' '20' '1' '' '' '1' '1'
##'frame0021' '21' '21' '1' '' '' '1' '1'
##'frame0022' '22' '22' '1' '' '' '1' '1'
##'frame0023' '23' '23' '1' '' '' '1' '1'
##'frame0024' '24' '24' '1' '' '' '1' '1'
##'frame0025' '25' '25' '1' '' '' '1' '1'
##'frame0026' '26' '26' '1' '' '' '1' '1'
##'frame0027' '27' '27' '1' '' '' '1' '1'
##'frame0028' '28' '28' '1' '' '' '1' '1'
##'frame0029' '29' '29' '1' '' '' '1' '1'
##'frame0030' '30' '30' '1' '' '' '1' '1'
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
##ENDJOBS

##END
