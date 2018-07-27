fn OOlog key val = (
	local logPath = "c:/stitch.txt"
	local logFile = openFile logPath mode:"a+"
	try(
		if logFile==undefined then (
			logFile = createFile logPath
		)
		key = (key as string)
		val = (val as string)
		format "[%]  %  %\n" localTime key val
		
		format "[%]  %  %\n" localTime key val to:logFile
		
		close logFile 
	)catch(
			close logFile
	)
)


fn OOgetFileName file= (
	local ext = getFilenameType file
	local bname = getFileNameFile file
	local result = bname + ext
	result
)

fn getBigFilename fileName= (
	local ffArr = filterString fileName "_"
	local bigName = ""
	if ffArr.count>5 then (
		
		for i=1 to  ffArr.count do (					
			if i>5 then (						
				append bigName ffArr[i]
			)
		)		
	)
	bigName
)

fn sortFiles workPath = (--multi array
	local match = workPath+"block*"
	OOlog "match " match
	local fileArr = getfiles match
	local allFileArr =#()
	if fileArr!=undefined and fileArr.count>0 then (	
		local allFileArr = #()
		for f in fileArr  do (
			
			local fullName = OOgetFileName f 
			local bigName = getBigFilename fullName			
			local fullnameFindHome = false			
			
				
			for  fArr  in allFileArr do (
				if fArr.count>0 then (
					local tempName = fArr[1]
					local tempBigName = getBigFilename tempName
					if bigName ==tempBigName then (
						append fArr fullName
						fullnameFindHome = true
					)
					
				)
			)
			if allFileArr.count==0 or fullnameFindHome==false then (
				local tempArr = #()
				append tempArr fullname
				append allFileArr tempArr
				
			)
			
			
		)
		
		
	)
	

	
	allFileArr
	
	
)

fn mergePic  frame width height   workPath=(
	
	
	local fileArr = sortFiles workPath
	for fArr in fileArr do (
		try(
			if fArr !=undefined and fArr.count>0 then (
				format "farr1......%\n" fArr[1]
				local tempBitmap = openBitMap (workPath+fArr[1])
				local tempGamma = tempBitmap.gamma
				
				local tempBigFileName = getBigFilename fArr[1]			
				
				local resultBitmap = bitmap width height filename:(workPath+tempBigFileName)
				
				for f in fArr do (
					local tBitmap = openBitMap (workPath+f)
					
					local arr = filterString f "_"
					if arr.count>5 then (
						local left = arr[2] as float
						local top = arr[3] as float
						pasteBitmap   tBitmap resultBitmap   [0,0] [left,top] --type:#composite
						resultBitmap.gamma=tempGamma
						display resultBitmap
						save resultBitmap frame:frame quiet:true --gamma:3.2
					)
					
				)
			)
		)catch(
			OOlog "exeception...." (getCurrentException() as string)
		)
		
	)
	
)

fn stitch frame width height   workPath= (
	try(
		OOlog "Start" " merge"
		mergePic frame width height   workPath
		DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string))  
	)catch(
		OOlog "final .exeception...." (getCurrentException() as string)
		DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string))  
	)
)



--stitch 8  640 480 "D:/3dsmax/test/ab/"



/*

stitch 3 1440 810   "D:/renderbus/mergepic/53/900116/"
fn tt = (
	stitch 5 3200 2400 2.2 "ffgg.jpg" "C:/renderwork/900130/comp/"
)
*/
--stitch 7 3200 2400 2.2 "ffgg.jpg" "C:/renderwork/900130/comp/"


--block3_80_120_200_350_ffgg_0007.jpg


/*
帧数
宽高
gamma
文件名
工作目录
*/

/*
第几块
KG
区域四参数
文件名



*/

