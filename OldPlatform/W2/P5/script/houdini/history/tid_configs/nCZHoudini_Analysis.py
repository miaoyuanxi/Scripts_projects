import hou, sys, os, string
_cid_from_cmd = sys.argv[1]
_tid_from_cmd = sys.argv[2]
_inf_from_cmd = sys.argv[3]
def nCZReadRenderInfo(_cid, _tid, _inf):
	_flag = 0
	_i = 0
	_infoLine = '_NC_ROP|_NC_SF|_NC_EF|_NC_BF_|_NC_OPTIONS\n'
	if _cid == '63045':
		_flag = 1
	if _cid == '53':
		_flag = 1
	if _cid == '18660':
		_flag = 1
	if _cid == '161917':
		_flag = 1
	if _cid == '161888':
		_flag = 1	
	if _flag:
		for obj in hou.node("/out").allSubChildren():			
			if _i > 0: _infoLine += '\n'
			_infoLine += obj.name()
			_infoLine += '|' + str(obj.evalParm('f1'))
			_infoLine += '|' + str(obj.evalParm('f2'))
			_infoLine += '|' + str(obj.evalParm('f3'))
			_infoLine += '|' + '-V'
			_i += 1			
	else:
		_infoLine = '0::Invalid uid, analysis failed!'
	
	# open for w
	_inf_handle = file(_inf, 'w')
	_inf_handle.write(_infoLine)
	_inf_handle.close()

nCZReadRenderInfo(_cid_from_cmd, _tid_from_cmd, _inf_from_cmd)