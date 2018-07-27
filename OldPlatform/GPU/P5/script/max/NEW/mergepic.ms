

struct STUtil(
	debugLog,
	count=1,
	
	fn oolog  val = (
		
		local msgtype = "msg"+(count as string)
		local msg = "["+(localTime as string)+"]"+ (val as string)
		format "% %\n" msgtype  msg	
		if (maxversion())[1] >= 15000 then(
			SetINISetting debugLog "debug" msgtype msg forceUTF16:false
		)else(
			SetINISetting debugLog "debug" msgtype msg
		)
		
		count=count+1
		
	)
	
)


struct STMergePic(
		
	fn RBgetFileName file= (
		local ext = getFilenameType file
		local bname = getFileNameFile file
		local result = bname + ext
		result
	),


	fn sortFiles workPath = (--multi array
		
		local match = workPath+"*"
		format "match....%\n" match
		local blockDirArr = getDirectories match
		local allFileArr =#()
		format "blockDirArr...\n"
		if blockDirArr!=undefined and blockDirArr.count>0 then (	
			local allFileArr = #()
			for blockDir in blockDirArr do(
				local blockPicArr = getFiles (blockDir+"*")
				for blockPic in blockPicArr  do (
					local nowFileName = RBgetFileName blockPic 
					local fullnameFindHome = false
					
					for  fArr  in allFileArr do (
						if fArr.count>0 and  fullnameFindHome==false then (
							local tempFile = fArr[1]
							local tempName = RBgetFileName tempFile
							if nowFileName==tempName then (
								append fArr blockPic
								fullnameFindHome = true
							)
							
						)
					)
					if allFileArr.count==0 or fullnameFindHome==false then (
						local tempArr = #()
						append tempArr blockPic
						append allFileArr tempArr	
					)
					
				)
				
			)
			
		)	
		allFileArr
	),

	fn RBpasteBitmap mframe resultBitmap picFile picGamma blockArr= (

		
		local parentPath = pathconfig.removePathLeaf picFile
		local blockName = pathconfig.stripPathToLeaf parentPath
		local blockIndex = replace blockName 1 5 ""
		local blockIndexInt = blockIndex as integer

		local blockInfoStr = blockArr[blockIndexInt]
		
		local blockInfoArr = filterString blockInfoStr "_"
		local leftTopX =blockInfoArr[2] as Float
		local leftTopY =blockInfoArr[3] as Float
		
		format "% __x....%....y....%\n" blockInfoArr leftTopX leftTopY
		
		local tBitmap = openBitMap picFile
		pasteBitmap   tBitmap resultBitmap   [0,0] [leftTopX,leftTopY] --type:#composite
		resultBitmap.gamma=picGamma
		display resultBitmap
		save resultBitmap frame:mframe quiet:true --gamma:3.2


	),
	
	fn getBlockArr workPath = (
		selfCfg=workPath+"cfg/self.cfg"
		local txt = selfCfg
		if doesFileExist txt then (
			local blockinfo = GetINISetting txt "common" "blockinfo"
			local blockArr = filterString blockinfo "|"
		)
	),

	fn mergePic  mframe width height   workPath=(
		format "width...%\....height...%\n" width height
		local blockSize = 5
		local widthPerBlock=width/blockSize
		local heightPerBlock=height/blockSize
		
		local resultArr = sortFiles (workPath+"temp/")
		
		resultpath = workPath+"result/"
		if not doesfileExist resultpath then (
			makeDir resultpath
		)
		local blockArr = getBlockArr workPath
		format "blockarr...%\n" blockArr
		for picArr in resultArr do (
			try(
				if picArr!=undefined and picArr.count>0 then (
					format "picArr......%\n" picArr[1]
					local tempBitmap = openBitMap (picArr[1])
					local picGamma = tempBitmap.gamma				
					local tempBigFileName = RBgetFileName picArr[1]
					local resultBitmap = bitmap width height filename:(workPath+"result/"+tempBigFileName)
					
					for pfile in picArr do (
						RBpasteBitmap mframe resultBitmap pfile picGamma blockArr
					)
				)
			)catch(
				format  "exeception....%\n" (getCurrentException() as string)
			)
			
		)
		
	),

	fn stitch taskId mframe width height workPath= (
		
		local debugTxt = "C:/log/analyse/"+(taskId as string)+"_debug.txt" 
		
		local objUtil = STUtil()		
		objUtil.debugLog=debugTxt
		objUtil.count=1
		objUtil.oolog "Start  merge-----------------"
		
		try(
			mergePic mframe width height workPath
			DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string))  
		)catch(
			format "final .exeception....%\n" (getCurrentException() as string)
			DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string))  
		)
	)

)
clearlistener()

fn RBmerge taskId mframe width height workPath=(
	mergePic = STMergePic()
	mergePic.stitch taskId mframe width height workPath
)

--RBmerge "79279" 5  1280 720 "C:/work/analyse/79279/"
--
