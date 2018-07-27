#!/usr/bin/python
import lx,sys,os,string
lx.eval('log.toConsole true')

# arguments ini
args = lx.arg().split('|')

# arguments display
_bat_cid = args[0]
_bat_tid = args[1]
_bat_cgv = str(args[2])
_bat_file = str(args[3])
_bat_info = str(args[4])
"""
lx.out("0_bat_cid = " + _bat_cid)
lx.out("1_bat_tid = " + _bat_tid)
lx.out("2_bat_cgv = " + _bat_cgv)
lx.out("3_bat_file = " + _bat_file)
lx.out("4_bat_info = " + _bat_info)
"""
# open modo scene
lx.eval('scene.open {0}'.format(_bat_file))
lx.out("Scene loaded.")

_flag = 1
_i = 0
if _flag:	
	# render settings
	lx.eval('select.item Render')
	_sf = str(lx.eval('item.channel first ?'))
	_ef = str(lx.eval('item.channel last ?'))
	_bf = str(lx.eval('item.channel step ?'))
	_infoLine = 'Render' + '=' + _sf + '|' + _ef + '|' + _bf + '|' + '1'
	_i += 1
	# item count
	n = lx.eval1("query sceneservice item.N ?")
	# item loops
	for i in range(n):
		itemType = lx.eval("query sceneservice item.type ? %s" % i)
		if(itemType == "renderOutput"):
			# item Name
			_ch_name = lx.eval("query sceneservice item.name ? %s" % i)
			# item select
			itemID = lx.eval("query sceneservice item.id ? %s" % i)
			lx.command("select.item",item=itemID)
			_ch_bool = str(lx.eval("item.channel textureLayer$enable ?"))
			# info line
			if _i > 0: _infoLine += '\n'
			_infoLine += 'ch=' + _ch_name
			_infoLine += '|' + _ch_bool
			_i += 1
else:
	_infoLine = '0::Invalid uid, analysis failed!'

_inf_handle = file(_bat_info, 'w')
_inf_handle.write(_infoLine)
_inf_handle.close()

# quit
lx.eval("app.quit")