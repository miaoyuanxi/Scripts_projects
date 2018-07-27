#encoding:utf-8
G_CG_NAME='Maya'
G_USERID_PARENT='961000'
G_USERID='961408'
G_TASKID='3637'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\961000\961408\8009369\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\961000\961408\8009369\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.70.242.102\p5\script\py\py\common'
userRenderPy=r'\\10.70.242.102\p5\script\py\py\961408'
G_RENDEROS=r'Windows'

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
##name=961408_3637_analyse.py
##nodelimit=100
##properties=|SH
##level=81
##custom=961408

##JOBS G_JOB_ID 

##'helperJob'	

##ENDJOBS

##END
