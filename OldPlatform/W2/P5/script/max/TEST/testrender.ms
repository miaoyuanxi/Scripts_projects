

fn test = (
	local myOutputFile = "c:/work/render/aaaabbnn.tga"
	local myBitmap = bitmap renderWidth renderHeight filename:myOutputFile-- gamma:2.2
	
	
	rendSaveFile=true
	rendOutputFilename=myoutputFile
	render outputfile:myOutputFile to:myBitmap --to:myBitmap --outputfile:myOutputFile  pixelAspect:1.0  --gamma:2.2
	
	
	
	myBitmap.gamma=2.2
	save myBitmap 
	close myBitmap
	
	/*
	local resultBitmap2 =  openbitmap myOutputFile
	resultBitmap2.filename=myOutputFile+"2.tga"
	save resultBitmap2 gamma:2.2
	close resultBitmap2
	
	*/
	--save myBitmap gamma:2.2
	--close myBitmap
	
)


clearlistener()
test()