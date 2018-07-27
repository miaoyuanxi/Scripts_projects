import hou, sys, os
_cid_from_cmd = sys.argv[1]
_rd_from_cmd = sys.argv[2]
_ext_from_cmd = sys.argv[3]


def nCZSetOutputOverride(cid, path, ext):
	if cid == '15315':
		for obj in hou.node("/out").allSubChildren():
			outNodeName = obj.name()
			print ('\r\n Out Node Name: ' + outNodeName)
			outPicture = obj.evalParm('vm_picture')
			nukeName = outPicture[outPicture.rindex('/')+1:]
			nukeName = nukeName[0:nukeName.index('.')]
			outPutName = nukeName + '.' + outNodeName + '.$F4.' + ext
			# set directory
			obj.parm('vm_picture').set(path + outPutName)
			thisNewPicture = obj.evalParm('vm_picture')
			print ('\r --> Redirect to: ' + thisNewPicture)
			print '\r\n'

	if cid == '63045':
		for obj in hou.node("/out").allSubChildren():
			outNodeName = obj.name()
			print ('\r\n Out Node Name: ' + outNodeName)
			outPicture = obj.evalParm('vm_picture')
			nukeName = outPicture[outPicture.rindex('/')+1:]
			nukeName = nukeName[0:nukeName.index('.')]
			outPutName = nukeName + '.' + outNodeName + '.$F4.' + ext
			# set directory
			obj.parm('vm_picture').set(path + outPutName)
			thisNewPicture = obj.evalParm('vm_picture')
			print ('\r --> Redirect to: ' + thisNewPicture)
			print '\r\n'

	elif cid == '53':
		for obj in hou.node("/out").allSubChildren():
			outNodeName = obj.name()
			print ('\r\n Out Node Name: ' + outNodeName)
			outPicture = obj.evalParm('vm_picture')
			nukeName = outPicture[outPicture.rindex('/')+1:]
			nukeName = nukeName[0:nukeName.index('.')]
			outPutName = nukeName + '.' + outNodeName + '.$F4.' + ext
			# set directory
			obj.parm('vm_picture').set(path + outPutName)
			thisNewPicture = obj.evalParm('vm_picture')
			print ('\r --> Redirect to: ' + thisNewPicture)
			print '\r\n'			
	else:
		print "ID does NOT exists!"

nCZSetOutputOverride(_cid_from_cmd, _rd_from_cmd, _ext_from_cmd)