#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='963000'
G_USERID='963394'
G_TASKID='16124719'
G_POOL=r'\\10.90.100.101\p5'
G_CONFIG=r'\\10.90.100.101\p5\config\963000\963394\16124719\render.json'
G_PLUGINS=r'\\10.90.100.101\p5\config\963000\963394\16124719\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.90.100.101\p5\script\py\py\common'
userRenderPy=r'\\10.90.100.101\p5\script\py\py\963394'
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
##name=963394_16124719_render.py
##requirements=|OS-Windows
##category=BJ
##level=79
##custom=963394
##nodelimit=5
##nodeblacklimit=3
##constraints=|10_90_100_101
##priority=20
##autorestartlimit=4
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0125' '125' '125' '1' '' '' '1' '1'
##'frame0126' '126' '126' '1' '' '' '1' '1'
##'frame0127' '127' '127' '1' '' '' '1' '1'
##'frame0128' '128' '128' '1' '' '' '1' '1'
##'frame0129' '129' '129' '1' '' '' '1' '1'
##'frame0130' '130' '130' '1' '' '' '1' '1'
##'frame0131' '131' '131' '1' '' '' '1' '1'
##'frame0132' '132' '132' '1' '' '' '1' '1'
##'frame0133' '133' '133' '1' '' '' '1' '1'
##'frame0134' '134' '134' '1' '' '' '1' '1'
##'frame0135' '135' '135' '1' '' '' '1' '1'
##'frame0136' '136' '136' '1' '' '' '1' '1'
##'frame0137' '137' '137' '1' '' '' '1' '1'
##'frame0138' '138' '138' '1' '' '' '1' '1'
##'frame0139' '139' '139' '1' '' '' '1' '1'
##'frame0140' '140' '140' '1' '' '' '1' '1'
##'frame0141' '141' '141' '1' '' '' '1' '1'
##'frame0142' '142' '142' '1' '' '' '1' '1'
##'frame0143' '143' '143' '1' '' '' '1' '1'
##'frame0144' '144' '144' '1' '' '' '1' '1'
##'frame0145' '145' '145' '1' '' '' '1' '1'
##'frame0146' '146' '146' '1' '' '' '1' '1'
##'frame0147' '147' '147' '1' '' '' '1' '1'
##'frame0148' '148' '148' '1' '' '' '1' '1'
##'frame0149' '149' '149' '1' '' '' '1' '1'
##'frame0150' '150' '150' '1' '' '' '1' '1'
##'frame0151' '151' '151' '1' '' '' '1' '1'
##'frame0152' '152' '152' '1' '' '' '1' '1'
##'frame0153' '153' '153' '1' '' '' '1' '1'
##'frame0154' '154' '154' '1' '' '' '1' '1'
##'frame0155' '155' '155' '1' '' '' '1' '1'
##'frame0156' '156' '156' '1' '' '' '1' '1'
##'frame0157' '157' '157' '1' '' '' '1' '1'
##'frame0158' '158' '158' '1' '' '' '1' '1'
##'frame0159' '159' '159' '1' '' '' '1' '1'
##'frame0160' '160' '160' '1' '' '' '1' '1'
##'frame0161' '161' '161' '1' '' '' '1' '1'
##'frame0162' '162' '162' '1' '' '' '1' '1'
##'frame0163' '163' '163' '1' '' '' '1' '1'
##'frame0164' '164' '164' '1' '' '' '1' '1'
##'frame0165' '165' '165' '1' '' '' '1' '1'
##'frame0166' '166' '166' '1' '' '' '1' '1'
##'frame0167' '167' '167' '1' '' '' '1' '1'
##'frame0168' '168' '168' '1' '' '' '1' '1'
##'frame0169' '169' '169' '1' '' '' '1' '1'
##'frame0170' '170' '170' '1' '' '' '1' '1'
##ENDJOBS

##END
