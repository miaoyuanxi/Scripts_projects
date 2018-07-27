#encoding:utf-8
G_CG_NAME='C4D'
G_USERID_PARENT='963500'
G_USERID='963682'
G_TASKID='8004239'
G_POOL=r'\\10.70.242.102\p5'
G_CONFIG=r'\\10.70.242.102\p5\config\963500\963682\8004239\render.json'
G_PLUGINS=r'\\10.70.242.102\p5\config\963500\963682\8004239\plugins.json'
G_RENDEROS=r''
baseRenderPy=r'\\10.70.242.102\p5\script\py\py\common'
userRenderPy=r'\\10.70.242.102\p5\script\py\py\963682'

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
##name=963682_8004239_render.py
##properties=|CD
##level=79
##custom=963682
##nodelimit=99
##nodeblacklimit=3
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION G_CG_TILE G_CG_TILECOUNT
##'frame0116' '116' '116' '1' '' '' '1' '1'
##'frame0117' '117' '117' '1' '' '' '1' '1'
##'frame0118' '118' '118' '1' '' '' '1' '1'
##'frame0119' '119' '119' '1' '' '' '1' '1'
##'frame0120' '120' '120' '1' '' '' '1' '1'
##'frame0121' '121' '121' '1' '' '' '1' '1'
##'frame0122' '122' '122' '1' '' '' '1' '1'
##'frame0123' '123' '123' '1' '' '' '1' '1'
##'frame0124' '124' '124' '1' '' '' '1' '1'
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
##'frame0171' '171' '171' '1' '' '' '1' '1'
##'frame0172' '172' '172' '1' '' '' '1' '1'
##'frame0173' '173' '173' '1' '' '' '1' '1'
##'frame0174' '174' '174' '1' '' '' '1' '1'
##'frame0175' '175' '175' '1' '' '' '1' '1'
##'frame0176' '176' '176' '1' '' '' '1' '1'
##'frame0177' '177' '177' '1' '' '' '1' '1'
##'frame0178' '178' '178' '1' '' '' '1' '1'
##'frame0179' '179' '179' '1' '' '' '1' '1'
##'frame0180' '180' '180' '1' '' '' '1' '1'
##'frame0181' '181' '181' '1' '' '' '1' '1'
##'frame0182' '182' '182' '1' '' '' '1' '1'
##'frame0183' '183' '183' '1' '' '' '1' '1'
##'frame0184' '184' '184' '1' '' '' '1' '1'
##'frame0185' '185' '185' '1' '' '' '1' '1'
##'frame0186' '186' '186' '1' '' '' '1' '1'
##'frame0187' '187' '187' '1' '' '' '1' '1'
##'frame0188' '188' '188' '1' '' '' '1' '1'
##'frame0189' '189' '189' '1' '' '' '1' '1'
##'frame0190' '190' '190' '1' '' '' '1' '1'
##'frame0191' '191' '191' '1' '' '' '1' '1'
##'frame0192' '192' '192' '1' '' '' '1' '1'
##'frame0193' '193' '193' '1' '' '' '1' '1'
##'frame0194' '194' '194' '1' '' '' '1' '1'
##'frame0195' '195' '195' '1' '' '' '1' '1'
##'frame0196' '196' '196' '1' '' '' '1' '1'
##'frame0197' '197' '197' '1' '' '' '1' '1'
##'frame0198' '198' '198' '1' '' '' '1' '1'
##'frame0199' '199' '199' '1' '' '' '1' '1'
##'frame0200' '200' '200' '1' '' '' '1' '1'
##'frame0201' '201' '201' '1' '' '' '1' '1'
##'frame0202' '202' '202' '1' '' '' '1' '1'
##'frame0203' '203' '203' '1' '' '' '1' '1'
##'frame0204' '204' '204' '1' '' '' '1' '1'
##'frame0205' '205' '205' '1' '' '' '1' '1'
##'frame0206' '206' '206' '1' '' '' '1' '1'
##'frame0207' '207' '207' '1' '' '' '1' '1'
##'frame0208' '208' '208' '1' '' '' '1' '1'
##'frame0209' '209' '209' '1' '' '' '1' '1'
##'frame0210' '210' '210' '1' '' '' '1' '1'
##'frame0211' '211' '211' '1' '' '' '1' '1'
##'frame0212' '212' '212' '1' '' '' '1' '1'
##'frame0213' '213' '213' '1' '' '' '1' '1'
##'frame0214' '214' '214' '1' '' '' '1' '1'
##'frame0215' '215' '215' '1' '' '' '1' '1'
##'frame0216' '216' '216' '1' '' '' '1' '1'
##'frame0217' '217' '217' '1' '' '' '1' '1'
##'frame0218' '218' '218' '1' '' '' '1' '1'
##'frame0219' '219' '219' '1' '' '' '1' '1'
##'frame0220' '220' '220' '1' '' '' '1' '1'
##'frame0221' '221' '221' '1' '' '' '1' '1'
##'frame0222' '222' '222' '1' '' '' '1' '1'
##'frame0223' '223' '223' '1' '' '' '1' '1'
##'frame0224' '224' '224' '1' '' '' '1' '1'
##'frame0225' '225' '225' '1' '' '' '1' '1'
##'frame0226' '226' '226' '1' '' '' '1' '1'
##'frame0227' '227' '227' '1' '' '' '1' '1'
##'frame0228' '228' '228' '1' '' '' '1' '1'
##'frame0229' '229' '229' '1' '' '' '1' '1'
##'frame0230' '230' '230' '1' '' '' '1' '1'
##'frame0231' '231' '231' '1' '' '' '1' '1'
##'frame0232' '232' '232' '1' '' '' '1' '1'
##'frame0233' '233' '233' '1' '' '' '1' '1'
##'frame0234' '234' '234' '1' '' '' '1' '1'
##'frame0235' '235' '235' '1' '' '' '1' '1'
##'frame0236' '236' '236' '1' '' '' '1' '1'
##'frame0237' '237' '237' '1' '' '' '1' '1'
##'frame0238' '238' '238' '1' '' '' '1' '1'
##'frame0239' '239' '239' '1' '' '' '1' '1'
##'frame0240' '240' '240' '1' '' '' '1' '1'
##'frame0241' '241' '241' '1' '' '' '1' '1'
##'frame0242' '242' '242' '1' '' '' '1' '1'
##'frame0243' '243' '243' '1' '' '' '1' '1'
##'frame0244' '244' '244' '1' '' '' '1' '1'
##'frame0245' '245' '245' '1' '' '' '1' '1'
##'frame0246' '246' '246' '1' '' '' '1' '1'
##'frame0247' '247' '247' '1' '' '' '1' '1'
##'frame0248' '248' '248' '1' '' '' '1' '1'
##'frame0249' '249' '249' '1' '' '' '1' '1'
##'frame0250' '250' '250' '1' '' '' '1' '1'
##ENDJOBS

##END
