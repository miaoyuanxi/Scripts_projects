
fn delAllUserPath = (
	
	local cc =mapPaths.count()
	format "cc...%\n" cc
	for i in cc to 1 by -1 do (
		mapPaths.delete i
	)
	
	
)

fn getAllUserPath=(
	
	local userPathArr = #()
	for i=1 to mapPaths.count() do (
		local myPath = mapPaths.get i
		append userPathArr myPath
	)
	userPathArr
)

fn addUserPath userPathArr = (
	
	for i=1 to userPathArr.count do (
		mapPaths.add userPathArr[i]
		
	)
	
	
)



fn userPath = (
	
	
	format "\nbefore render config user path----------------------%-------------------------\n" localtime
	local pathArr = getAllUserPath()
	local userPathArr=#("c:\\work\\render\\121\\")
	addUserPath userPathArr
	
	format "\nafter render config user path----------------------%-------------------------\n" localtime
	delAllUserPath()
	addUserPath pathArr
	
)
format "\n----------------------%-------------------------\n" localtime
clearlistener()
userPath()
--taskPathArr=#("c:\\work\\render\\1233322\\")
--cfgUserPath taskPathArr
