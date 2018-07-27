#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='119500'
G_USERID='119614'
G_TASKID='8002292'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\119500\119614\8002292\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\119500\119614\8002292\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.70.242.102\p5\script\py\py\common'
userRenderPy=r'\\10.70.242.102\p5\script\py\py\119614'

import os,sys,shutil
import subprocess

print 'copyBasePy...start'
nodePyDir=r'c:\script\py'
def cmd(cmdStr,myShell=False):#continueOnErr=true-->not exit ; continueOnErr=false--> exit 
	print cmdStr
	cmdp=subprocess.Popen(cmdStr,stdin = subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = myShell)
	while cmdp.poll()!=None:
		resultLine = cmdp.stdout.readline().strip()
	resultStr = cmdp.stdout.read()
	resultCode = cmdp.returncode
	return resultStr
    
if G_RENDEROS=='Linux':
	nodePyDir=r'/root/rayvision/script/py'
	baseRenderPy = baseRenderPy.replace("\\","/")
	userRenderPy = userRenderPy.replace("\\","/")
else:
	pySitePackagesPool=os.path.join(G_POOL,'script','pySitePackages').replace('/','\\')
	cScript=r'c:\script\\'
	pySitePackagesNode=cScript+'pySitePackages'
	copyPySitePackagesCmd=r'c:\fcopy\FastCopy.exe /speed=full /force_close /no_confirm_stop /force_start "'+pySitePackagesPool+'" /to="'+cScript+'"'
	cmd(copyPySitePackagesCmd)
	sys.path.append(pySitePackagesNode)
if not os.path.exists(nodePyDir):
	os.makedirs(nodePyDir)
	
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

sys.path.append(nodePyDir)
import RenderAction


if(__name__=="__main__"):	
	paramDict = {'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION,'G_CONFIG':G_CONFIG,'G_PLUGINS':G_PLUGINS,'G_RENDEROS':G_RENDEROS,'G_CG_TILE':G_CG_TILE,'G_CG_TILECOUNT':G_CG_TILECOUNT}
	RenderAction.main(**paramDict)


##BEGIN
##description=This is a test script
##name=119614_8002292_render.py
##level=79
##custom=119614
##nodelimit=99
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0000' '0' '0' '1' '' '' '1' '1'
##ENDJOBS

##END
