
import os,sys,shutil


print 'copyBasePy...start'
nodePyDir=r'c:\script\py'
inputIp='10.60.100.7'
#ip = 'www.storage.com'#getIpByNode()
if G_RENDEROS=='Linux':
	nodePyDir=r'/root/rayvision/script/py'
if not os.path.exists(nodePyDir):
	os.makedirs(nodePyDir)
def copyPyFolder(pyFolder):
	
	#pyFolder = pyFolder.replace(inputIp,ip)
	if os.path.exists(pyFolder):
		for root, dirs, files in os.walk(pyFolder):
			print 'copyBasePy...'
			for i in xrange (0, files.__len__()):
				sf = os.path.join(root, files[i])
				shutil.copy(sf,nodePyDir)
def getIpByNode():
	nodeList=["GA","GB","GC","GD"]
	#nodeCount = len(nodeList)*240
	#ipNodeCount=nodeCount/10
	ipList=["10.60.100.3","10.60.100.4","10.60.100.5","10.60.100.6","10.60.100.7","10.60.100.8","10.60.100.9","10.60.100.10","10.60.100.11","10.60.100.12"]
	node=sys.argv[5]
	for nodeFs in nodeList:
		if nodeFs in node:
			nodeNum = int(node.replace(nodeFs,""))
			if nodeNum>240:
				return ipList[9]
			index = nodeNum/24
			if nodeNum%24==0:
				index = index-1
			return ipList[index] 
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
##name=render.py
##requirements=
##properties=
##level=50
##custom=NONO
##nodelimit=
##nodeblacklimit=3
##constraint=
##JOBS G_JOB_ID G_CG_START_FRAME G_CG_END_FRAME G_CG_BY_FRAME G_CG_LAYER_NAME G_CG_OPTION  ##ENDJOBS

##END