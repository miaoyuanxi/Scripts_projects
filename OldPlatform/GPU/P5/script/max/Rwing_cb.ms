print "callbacks....no"
RW_userPath = "c:/enfwork/RENDER_INFO/render.txt"

struct RWInfo(maxName,myrender,outPath,taskId,customerId,mapArr=#())

function RWLog logStr rwInfo=(
		local taskId = ""
		if rwInfo !=undefined and rwInfo.taskId!=undefined then (
			 taskId = rwInfo.taskId+"/"
		)
		
		local logPath = "c:/log/"+taskId+"maxFilePostOpen.log"

		local logFile = openFile logPath mode:"a+"
		if logFile==undefined then (
			logFile = createFile logPath
		)
		
		format "[%]  %\n" localTime logStr to:logFile
		close logFile		
)



function RW_readTxt=(
	local userFile = openFile RW_userPath
	local renderInfo = RWInfo()
	
	if userFile!=undefined then (
		while not eof userFile do(
			local lineInfo = readLine userFile
			if lineInfo==undefined or lineInfo=="" do continue
			
			if (findString  lineInfo "rw_execute.")==1 do (--额外执行
				local execStr = substring lineInfo 12 lineInfo.count
				try (
					execute execStr
				)catch(
					print (getCurrentException() as string)
				)				
			)
			
			if (findString  lineInfo "maxName=")==1 do (
				local maxName_ = substring lineInfo 9 lineInfo.count
				renderInfo.maxName= maxName_
			)
			
			if (findString  lineInfo "render=")==1 do (
				local myrender = substring lineInfo 8 lineInfo.count
				renderInfo.myrender=myrender
			)
			
			if (findString  lineInfo "outPath=")==1 do (
				local outPath = substring lineInfo 9 lineInfo.count
				renderInfo.outPath=outPath
			)
			if (findString  lineInfo "taskId=")==1 do (
				local taskId = substring lineInfo 8 lineInfo.count
				renderInfo.taskId=taskId
			)
			if (findString  lineInfo "customerId=")==1 do (
				local customerId = substring lineInfo 12 lineInfo.count
				renderInfo.customerId=customerId
			)
			if(findString lineInfo "map="==1) do (
				local mapPath = substring lineInfo 5 lineInfo.count
				append renderInfo.mapArr mapPath
			)
			
		)
	
		close userFile
	)else(
		renderInfo=undefined
	)
	renderInfo
)


function RW_vrfb rwInfo = (
	local myrender = renderers.current
	local outPath = rwInfo.outPath
	local rawFile = myrender.output_rawFileName 
	local splitFile = myrender.output_splitfilename 
	
	
	if rawFile!=undefined and rawFile!="" then (
		myrender.output_rawFileName = (outPath +"VFB.vrimg")
	)
	
	if splitFile!=undefined and splitFile!="" then (
		
		local sname = getFilenameFile splitFile
		local stype = getFilenameType splitFile
				
		if sname == undefined or  sname==""  then (
			sname = "VFBs"
		)
		if  stype ==undefined  or stype=="" then (
			stype = ".tga"
		)
		local splitFileName = sname + stype
		myrender.output_splitfilename = (outPath +splitFileName)
	)
)


function RW_vrMap rwInfo = (
	local outPath = rwInfo.outPath	
	local mapArr = rwInfo.mapArr
	
	local myrender = renderers.current
	
	local irrLoadFile = myrender.adv_irradmap_loadFileName
	local irrSaveFile =myrender.adv_irradmap_autoSaveFileName
	
	local ligLoadFile = myrender.lightcache_loadFileName
	local ligSaveFile = myrender.lightcache_autoSaveFileName
	local irrmapMode = myrender.adv_irradmap_mode
	
	
	 RWLog  irrLoadFile rwInfo
	 RWLog irrSaveFile rwInfo
	 RWLog  ligLoadFile rwInfo
	 RWLog ligSaveFile rwInfo
	 RWLog irrmapMode rwInfo
	RWLog "-----------before-------------" rwInfo
	if irrLoadFile!=undefined and irrLoadFile!="" do (
		
		local loadIrrFileName = filenameFromPath  irrLoadFile
		local loadIrrFileBaseName = getFilenameFile  loadIrrFileName
		local loadIrrFileType = getFilenameType loadIrrFileName
		
		if mapArr!=undefined do (
			if irrmapMode!=undefined and irrmapMode==7 then (--序列光子
				local mypartten = loadIrrFileBaseName+"*."+loadIrrFileType
				for mapPath in mapArr do (
					if (matchPattern mapPath pattern:mypartten==true) do (
						myrender.adv_irradmap_loadFileName=myMapPath	
						break			
					)
				)
			)else(
				for mapPath in mapArr do (
					if (matchPattern mapPath pattern:loadIrrFileName==true) do (
						myrender.adv_irradmap_loadFileName=myMapPath	
						break
					)
				
				)			
			)
					
		)		
	)
	
	
	if irrSaveFile!=undefined and irrSaveFile!="" do (
			local saveIrrFileName = filenameFromPath  irrSaveFile
			myrender.adv_irradmap_autoSaveFileName=(outPath+saveIrrFileName)			
			
	)
	
	
	
	if ligSaveFile!=undefined and ligSaveFile!="" do (
			local saveLigFileName = filenameFromPath ligSaveFile
			myrender.lightcache_autoSaveFileName=(outPath+saveLigFileName)
	)
	
	
	if ligLoadFile!=undefined and ligLoadFile!="" do (
		
		local loadLigFileName = filenameFromPath  ligLoadFile
		if mapArr!=undefined do (
			for mapPath in mapArr do (
				if (matchPattern mapPath pattern:loadLigFileName==true) do (
					myrender.lightcache_loadFileName=myMapPath	
					break
				)			
			)		
		)
	)

	 irrLoadFile = myrender.adv_irradmap_loadFileName
	 irrSaveFile =myrender.adv_irradmap_autoSaveFileName
	
	 ligLoadFile = myrender.lightcache_loadFileName
	 ligSaveFile = myrender.lightcache_autoSaveFileName
	 irrmapMode = myrender.adv_irradmap_mode
	 
	 RWLog irrLoadFile rwInfo
	 RWLog irrSaveFile rwInfo
	 RWLog  ligLoadFile rwInfo
	 RWLog ligSaveFile rwInfo
	 RWLog irrmapMode rwInfo

)

function RW_setVr  rwInfo=  (
	local myrender = renderers.current as string
	
	local mat1 = matchPattern myrender pattern:"*v_ray*"
	local mat2 = matchPattern myrender pattern:"*vray*" 
	local mat3 = matchPattern myrender pattern:"*v-ray*"

	if mat1==true or mat2==true or mat3==true then(
	 	RW_vrMap rwInfo
	 	RW_vrfb rwInfo
	)
)

function RW_elem rwInfo=
	(
	print "render element..."
	re = maxOps.GetCurRenderElementMgr() 
	theManager = maxOps.GetRenderElementMgr #Production
	
	RWLog "---------renderElement-----" rwInfo 
	eact = re.GetElementsActive()
	
	RWLog  eact rwInfo
	for n = 0 to (theManager.numrenderelements()- 1) do
	
	(
	
		el = re.getrenderelement n
		local ename = el.elementname
		local eactive = el.enabled 

		format "ename=%._|_.%\n" ename eactive  
		local opath = rwInfo.outPath
		re.SetRenderElementFilename n (opath+ename+".tga" )

	)

)


function RW_call = (
gc()
	local rwInfo = RW_readTxt()
	
	if rwInfo!=undefined  and rwInfo.maxName!=undefined then (
		
		
		local mymaxFile = maxFilePath+maxFileName
		local myname =  "mymaxFile:"+ mymaxFile
		local rwname = "rwmaxfile:" + rwInfo.maxName
		RWLog myname rwInfo
		RWLog rwname rwInfo
		
		if mymaxFile==rwInfo.maxName then (
			rendTimeType=2	
			renderSceneDialog.update()
			renderSceneDialog.commit()
			RW_setVr rwInfo	
			RW_elem rwInfo
		)
	)
gc()
)

try(

	callbacks.removeScripts #filePostOpen id:#RW_postfile	
	callbacks.addScript #filePostOpen "RW_call()" id:#RW_postfile
	
	
	
	

)catch(

print (getCurrentException() as string)

)


