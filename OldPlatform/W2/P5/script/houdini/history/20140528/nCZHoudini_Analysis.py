import hou, sys, os, string
_cid_from_cmd = sys.argv[1]
_tid_from_cmd = sys.argv[2]
_inf_from_cmd = sys.argv[3]
def nCZReadRenderInfo(_cid, _tid, _inf):

	_flag = 1
	_i = 0
	_opt = '-V -I -s'
	_idf_path = '/out'
	_infoLine = '_NC_ROP|_NC_SF|_NC_EF|_NC_BF_|_NC_OPTIONS\n'
	
	if _cid == '163494':
		_idf_path = '/obj/Render'
	if _cid == '15450':
		_idf_path = '/obj/ropnet1'

	if _flag:
		print('Searching ROPs in ' + _idf_path)
		for obj in hou.node(_idf_path).allSubChildren():
			node_fullName = _idf_path + '/' + obj.name()
			node_type = str(hou.nodeType(node_fullName))
			if node_type == '<hou.NodeType for Driver ifd>':
				if _i > 0: _infoLine += '\n'
				_infoLine += obj.name()
				_infoLine += '|' + str(obj.evalParm('f1'))
				_infoLine += '|' + str(obj.evalParm('f2'))
				_infoLine += '|' + str(obj.evalParm('f3'))
				_infoLine += '|' + _opt
				_i += 1
	else:
		_infoLine = '0::Invalid uid, analysis failed!'

	# open for w
	_inf_handle = file(_inf, 'w')
	_inf_handle.write(_infoLine)
	_inf_handle.close()

nCZReadRenderInfo(_cid_from_cmd, _tid_from_cmd, _inf_from_cmd)
