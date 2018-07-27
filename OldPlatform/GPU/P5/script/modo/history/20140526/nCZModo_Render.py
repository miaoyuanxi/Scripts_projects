#!/usr/bin/python
import lx,sys,os,string
lx.eval('log.toConsole true')
lx.out("Loading libs...")

# arguments ini
args = lx.arg().split('|')
lx.out("Initializing parmeters...")

# arguments display
_bat_cid = args[0]
_bat_tid = args[1]
_bat_sf = args[2]
_bat_ef = args[3]
_bat_bf = args[4]
_bat_cgv = str(args[5])
_bat_pro = str(args[6])
_bat_file = str(args[7])
_bat_rd = str(args[8])
_bat_ch = str(args[9])
_bat_rop = str(args[10])
_bat_opt = str(args[11])

"""
lx.out("0_bat_cid = " + _bat_cid)
lx.out("1_bat_tid = " + _bat_tid)
lx.out("2_bat_sf = " + _bat_sf)
lx.out("3_bat_ef = " + _bat_ef)
lx.out("4_bat_bf = " + _bat_bf)
lx.out("5_bat_cgv = " + _bat_cgv)
lx.out("6_bat_pro = " + _bat_pro)
lx.out("7_bat_file = " + _bat_file)
lx.out("8_bat_rd = " + _bat_rd)
lx.out("9_bat_ch = " + _bat_ch)
lx.out("10_bat_rop = " + _bat_rop)
lx.out("11_bat_opt = " + _bat_opt)
"""

# open modo scene
lx.eval('scene.open {0}'.format(_bat_file))
lx.out("Scene loaded.")
lx.eval('pref.value render.threads auto')
lx.out("Auto threads.")

# output channels
with open(_bat_ch) as f:
	for line in f:
		_flag = -1
		_str = line.split('=')[-1]
		chs = _str.split('|')
		_flag = chs[1].find('1') + 1
		# item count
		n = lx.eval1("query sceneservice item.N ?")
		# item loops
		for i in range(n):
			itemType = lx.eval("query sceneservice item.type ? %s" % i)
			if(itemType == "renderOutput"):
				# item Name
				_ch_name = lx.eval("query sceneservice item.name ? %s" % i)
				if(_ch_name == chs[0]):
					# item select
					itemID = lx.eval("query sceneservice item.id ? %s" % i)
					lx.command("select.item",item=itemID)
					if _flag:
						lx.eval("item.channel textureLayer$enable true")
					else:
						lx.eval("item.channel textureLayer$enable false")

outputName =  _bat_file.split('/')[-1]
outputName =  outputName.split('"')[0]
outputName = '"' + _bat_rd + '/' + outputName + '."'
outputFormat = "openexr32"
_bat_opt = "{*}"

# select the render item in order to change its attributes
lx.eval('select.item Render')
# sf
lx.eval('item.channel first {0}'.format(_bat_sf))
# ef
lx.eval('item.channel last {0}'.format(_bat_ef))
# bf
lx.eval('item.channel step {0}'.format(_bat_bf))
# render the animation
lx.eval('render.animation {0} {1}'.format(outputName, _bat_opt))
# quit
lx.eval("app.quit")