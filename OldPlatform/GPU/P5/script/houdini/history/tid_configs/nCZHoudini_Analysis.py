import hou, sys, os
_cid_from_cmd = sys.argv[1]
_tid_from_cmd = sys.argv[2]
_inf_from_cmd = sys.argv[3]

def nCZReadRenderInfo(_cid, _tid, _inf):
	# open for w
	_inf_handle = file(_inf, 'w')

	if _cid == '63045':
		str = '1';
		for obj in hou.node("/out").allSubChildren():
			str += '::' + obj.name()
			str += '::' + obj.evalParm('f1')
			str += '::' + obj.evalParm('f2')
			str += '::' + obj.evalParm('f3')
			str += '::' + obj.evalParm('res_overridex')
			str += '::' + obj.evalParm('res_overridey')
			str += '::' + ' -V'
			str += '\r\n'
			_inf_handle.write(str)	
	else:
		_inf_handle.write('Unknow uid provided, analysis failed!')

nCZReadRenderInfo(_cid_from_cmd, _tid_from_cmd, _inf_from_cmd)