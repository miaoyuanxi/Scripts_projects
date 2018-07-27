#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='963000'
G_USERID='963394'
G_TASKID='6615'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\963000\963394\8017664\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\963000\963394\8017664\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.70.242.102\p5\script\py\py\common'
userRenderPy=r'\\10.70.242.102\p5\script\py\py\963394'
G_RENDEROS=r''
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
                

cgList=['Nuke','Preprocess','MaxClient','Merge']
if G_CG_NAME in cgList:
#if os.path.exists(scriptCg):
    if G_CG_NAME == 'Preprocess' or G_CG_NAME == 'MaxClient' or G_CG_NAME == 'Merge':
        G_CG_NAME_PATH = 'Max'
    else:
        G_CG_NAME_PATH = G_CG_NAME
    script2=G_POOL+'\\script2'
    scriptBase=script2+'\\Base'
    scriptCg=script2+'\\'+G_CG_NAME_PATH
    scriptNodeBase=nodePyDir+'\\Base'
    scriptNodeCg=nodePyDir+'\\'+G_CG_NAME_PATH
    print script2
    print scriptBase
    print scriptCg

    userRenderPy=script2+'\\user\\'+G_USERID
    shutil.rmtree(nodePyDir)
    copyFolder(scriptBase,scriptNodeBase)
    copyFolder(scriptCg,scriptNodeCg)
    copyFolder(userRenderPy,nodePyDir)
    sys.path.append(scriptNodeBase)
else:
    copyPyFolder(baseRenderPy)
    copyPyFolder(userRenderPy)
    
print 'copyBasePy...end'
#-----------------------------------------------------
sys.path.append(nodePyDir)

import AnalyseAction


if(__name__=="__main__"):
    paramDict = {'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_NODE_PY':nodePyDir,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_RENDEROS':G_RENDEROS,'G_CONFIG':G_CONFIG,'G_PLUGINS':G_PLUGINS}
    AnalyseAction.main(**paramDict)


##BEGIN
##description=This is a helper script
##name=963394_6615_analyse.py
##nodelimit=100
##properties=|BJ
##level=81
##custom=963394

##JOBS G_JOB_ID 

##'helperJob'	

##ENDJOBS

##END
