#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='963500'
G_USERID='963842'
G_TASKID='8015052'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\963500\963842\8015052\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\963500\963842\8015052\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.70.242.102\p5\script\py\py\common'
userRenderPy=r'\\10.70.242.102\p5\script\py\py\963842'
#script_param_mark#

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
	paramDict = {'G_JOB_ID':G_JOB_ID,'G_USERID':G_USERID,'G_USERID_PARENT':G_USERID_PARENT,'G_TASKID':G_TASKID,'G_CG_NAME':G_CG_NAME,'G_SYS_ARGVS':sys.argv,'G_POOL':G_POOL,'G_CG_START_FRAME':G_CG_START_FRAME,'G_CG_END_FRAME':G_CG_END_FRAME,'G_CG_BY_FRAME':G_CG_BY_FRAME,'G_CG_LAYER_NAME':G_CG_LAYER_NAME,'G_CG_OPTION':G_CG_OPTION,'G_CONFIG':G_CONFIG,'G_PLUGINS':G_PLUGINS,'G_RENDEROS':G_RENDEROS,'G_CG_TILE':G_CG_TILE,'G_CG_TILECOUNT':G_CG_TILECOUNT}
	RenderAction.main(**paramDict)


##BEGIN
##description=This is a test script
##name=963842_8015052_render.py
##properties=|BJ
##level=50
##custom=963842
##nodelimit=99
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
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
##'frame0051' '51' '51' '1' '' '' '1' '1'
##'frame0052' '52' '52' '1' '' '' '1' '1'
##'frame0053' '53' '53' '1' '' '' '1' '1'
##'frame0054' '54' '54' '1' '' '' '1' '1'
##'frame0055' '55' '55' '1' '' '' '1' '1'
##'frame0056' '56' '56' '1' '' '' '1' '1'
##'frame0057' '57' '57' '1' '' '' '1' '1'
##'frame0058' '58' '58' '1' '' '' '1' '1'
##'frame0059' '59' '59' '1' '' '' '1' '1'
##'frame0060' '60' '60' '1' '' '' '1' '1'
##'frame0061' '61' '61' '1' '' '' '1' '1'
##ENDJOBS

##END
