#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='119500'
G_USERID='119614'
G_TASKID='553'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\119500\119614\8002296\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\119500\119614\8002296\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.70.242.102\p5\script\py\py\common'
userRenderPy=r'\\10.70.242.102\p5\script\py\py\119614'
G_RENDEROS=r''

import os,sys,shutil


print 'copyBasePy...start'
nodePyDir=r'c:\script\py'
if G_RENDEROS=='Linux':
	nodePyDir=r'/root/rayvision/script/py'
	baseRenderPy = baseRenderPy.replace("\\","/")
	userRenderPy = userRenderPy.replace("\\","/")
if not os.path.exists(nodePyDir):
	os.makedirs(nodePyDir)
def copyPyFolder(pyFolder):
	if os.path.exists(pyFolder):
		for root, dirs, files in os.walk(pyFolder):
			print 'copyBasePy...'
			for i in xrange (0, files.__len__()):
				sf = os.path.join(root, files[i])
				shutil.copy(sf,nodePyDir)
copyPyFolder(baseRenderPy)
copyPyFolder(userRenderPy)
print 'copyBasePy...end'
#-----------------------------------------------------
sys.path.append(nodePyDir)
import AnalyseAction


if(__name__=="__main__"):
	paramDict = {'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_RENDEROS':G_RENDEROS,'G_CONFIG':G_CONFIG,'G_PLUGINS':G_PLUGINS}
	AnalyseAction.main(**paramDict)


##BEGIN
##description=This is a helper script
##name=119614_553_analyse.py
##nodelimit=100
##level=81
##custom=119614

##JOBS G_JOB_ID 

##'helperJob'	

##ENDJOBS

##END
