import hou, sys, os
for obj in hou.node("/out").allSubChildren():
	outNodeName = obj.name()
	outPicture = obj.parm('vm_picture')
	outPutRoot = 'c:/enfwork/' + sys.argv[1]
	if not os.path.exists(outPutRoot):
		os.makedirs(outPutRoot)
	outPicture.set(outPutRoot +'/' + '$HIPNAME' + '.' + outNodeName + '.$F4.exr')
	obj.evalParm('vm_picture')