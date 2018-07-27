import hou, sys, os
_cid_from_cmd = sys.argv[1]
_rd_from_cmd = sys.argv[2]
_ext_from_cmd = sys.argv[3]
_rop_from_cmd = sys.argv[4]

def nCZSetOutputOverride(_cid, _path, _ext, _rop):
	if _cid == '15450':
		for obj in hou.node("/obj/ropnet1").allSubChildren():
			_ropName = obj.name()			
			if _ropName == _rop:
				_var_ext = ''
				if _ext != '':
					_var_ext = _ext
				else:
					_var_str = obj.evalParm('vm_picture')
					if _var_str != 'ip':
						_var_arr = _var_str.split('.')
						_var_ext = _var_arr[len(_var_arr)-1]
					else:
						_var_ext = 'exr'
				outPutName = _path + '$HIPNAME' + '.' + _ropName + '.$F4.' + _var_ext
				# set directory
				obj.parm('vm_picture').set(outPutName)
				thisNewPicture = obj.evalParm('vm_picture')
				print ('\r --> Redirect to: ' + thisNewPicture)
				print "Default output name config applied!"

	if _cid == '163494':
		for obj in hou.node("/obj/Render").allSubChildren():
			_ropName = obj.name()			
			if _ropName == _rop:
				_var_ext = ''
				if _ext != '':
					_var_ext = _ext
				else:
					_var_str = obj.evalParm('vm_picture')
					if _var_str != 'ip':
						_var_arr = _var_str.split('.')
						_var_ext = _var_arr[len(_var_arr)-1]
					else:
						_var_ext = 'exr'
				outPutName = _path + '$HIPNAME' + '.' + _ropName + '.$F4.' + _var_ext
				# set directory
				obj.parm('vm_picture').set(outPutName)
				thisNewPicture = obj.evalParm('vm_picture')
				print ('\r --> Redirect to: ' + thisNewPicture)
				print "Default output name config applied!"

	else:
		for obj in hou.node("/out").allSubChildren():
			_ropName = obj.name()			
			if _ropName == _rop:
				_var_ext = ''
				outPutName = _path + '$HIPNAME' + '.' + _ropName + '.$F4.' + _ext
				if _ext != '':
					_var_ext = _ext
				else:
					_var_str = obj.evalParm('vm_picture')
					if _var_str != 'ip':
						_var_str = _var_str.replace('\\','/')
						_var_arr = _var_str.split('/')[-1]
						outPutName = _path + _var_arr
				# set directory
				obj.parm('vm_picture').set(outPutName)
				thisNewPicture = obj.evalParm('vm_picture')
				print ('\r --> Redirect to: ' + thisNewPicture)
				print "Default output name config applied!"

nCZSetOutputOverride(_cid_from_cmd, _rd_from_cmd, _ext_from_cmd, _rop_from_cmd)