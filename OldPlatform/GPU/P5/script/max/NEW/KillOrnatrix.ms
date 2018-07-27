


fn myKill myMaxFile=(
	useFileUnits=true 
	quiet=true 
	try(setVRaySilentMode() )catch()
	
	local ll = loadMaxFile myMaxFile useFileUnits:true quiet:true
	sleep3
	if ll then (
		try(
			rendSaveFile=false
			sleep3
			
			render outputwidth:100 outputheight:100 frame:(0 as time)
			sleep 3
			local myMaxPath= pathConfig.removePathLeaf myMaxFile
			local ext = getFilenameType myMaxFile
			local bname = getFileNameFile myMaxFile
			local myFinalMax = pathConfig.appendPath myMaxPath (bname+"_fox"+ext)
			rendSaveFile=true
			sleep 3
			saveMaxFile myFinalMax
		)catch()	
	)	
)

clearlistener()
myKill "\\10.50.1.3\d\inputdata\max\0\53\ljw\animax\990454\990454.max"