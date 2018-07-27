/**

----------------渲染脚本 
finalrender



--------------服务器
VRAY切换版本


---------bug-----------
负数帧，帧序列
max9的gamma还没找到好方法匹配渲染
max2013 遇到unlock 会被中断，稍后要记得一定要改进分发神器




-------------------分割渲染------------------

渲染命令
render renderType: #region  region:#(100,0,200,100) to:b--前两个是左上角的X,Y 后两个是右下角的X,Y

合并命令
b1 = openBitMap "D:\savva.single.0005.exr"
b2 = openBitMap "D:\savva.single.0007.exr"
b3=bitmap 1024 768
pasteBitmap b1 b3 [0,0] [50,50] --前两个是源的左上角X,Y 后两个是目标的左上角X,Y

display b3

-----------kg------------
kg 代表主任务 
subKg 代表光子任务

kg=0 max普通任务
kg=1 max拆分任务
kg/subkg=2 渲染叠加光子
kg/subkg=3 渲染序列光子
kg/subkg=4 快速渲染叠加光子（不能是单帧）

*/



format "render---------------\n"


fn fillSerial sourceStr= (
	if sourceStr==undefined then return sourceStr
	local str =sourceStr as string
	while str.count<4 do (
		str = "0" + str
	)
	
	str
	
)


fn getRWFileName file= (
	local ext = getFilenameType file
	local bname = getFileNameFile file
	local result = bname + ext
	result
)

fn RB_MontiorDialog =
(


	local WindowHandle = DialogMonitorOPS.GetWindowHandle()

	local dialogName = UIAccessor.GetWindowText WindowHandle
--DOSCommand ("echo dialogName... " +dialogName+">>c:/dialogName.txt") 
if  dialogName!=undefined and dialogName!="" and dialogName=="About Hot4MAX" then (

	format "Dialog Name: %\n" (UIAccessor.GetWindowText WindowHandle)
	 
	
	local hwnd_children = uiAccessor.getChildWindows WindowHandle
	for i = 1 to hwnd_children.count do (
		format "% = \"%\"\n" i (uiAccessor.getWindowText hwnd_children[i])
	)

	--UIAccessor.PressDefaultButton()
	
	--UIAccessor.CloseDialog WindowHandle
	UIAccessor.pressButtonByName WindowHandle "OK"
	--UIAccessor.SendMessageID WindowHandle #IDOK
)



if  dialogName!=undefined and dialogName!="" and dialogName=="Proxy System" then (

	format "Dialog Name: %\n" (UIAccessor.GetWindowText WindowHandle)
	 
	
	local hwnd_children = uiAccessor.getChildWindows WindowHandle
	for i = 1 to hwnd_children.count do (
		format "% = \"%\"\n" i (uiAccessor.getWindowText hwnd_children[i])
	)

	--UIAccessor.PressDefaultButton()
	
	--UIAccessor.CloseDialog WindowHandle
	UIAccessor.pressButtonByName WindowHandle "&No"
	--UIAccessor.SendMessageID WindowHandle #IDOK
)
  true
)

struct STConst (
	userId, taskId, mframe, frameSerial,maxFile,sonId,kg,
	
	renderWork = "c:/work/render/",
	taskPath,
	texPath,
	outPath,
	logPath,
	cachePath,
	photonPath,
	jobName,
	framesperjob,
	maxUserPath=#(),
	maxXrefPath=#(),
	MAX_OUT_NAME,
	MAX_GAMMA,
	MAX_INGAMMA,
	MAX_OUTGAMMA

)


	



struct RBRender (
	
	stCon ,
	logArr=#(),
	
	
	fn init u t s f kg j m =(
		stCon=STConst()
		stCon.userId = u
		stCon.taskId = t
		stCon.sonId=s
		stCon.mframe = f
		stCon.kg = kg
		stCon.jobName=j
		stCon.maxFile= m
		
		stCon.taskPath = stCon.renderWork+t+"/"
		stCon.outPath=stCon.taskPath+"output/"
		
		if kg=="15" then (
			stCon.texPath = pathConfig.removePathLeaf stCon.maxFile			
		)else(
			stCon.texPath=stCon.taskPath
		)
		
		stCon.logPath="c:/log/render/"+t+"/"
		
		
			
		if kg=="1" then (--frame_left_top_right_bottom_block_width_height			
			local frameArr = filterString stCon.mframe "_"
			stCon.frameSerial =fillSerial frameArr[1]
		)else(
			stCon.frameSerial  = fillSerial f
		)
		
		
		local txt = stCon.taskPath+"/cfg/self.cfg"
		if doesFileExist txt then (
			local gamma = GetINISetting txt "rendersettings" "gamma"
			local inGamma = GetINISetting txt "rendersettings" "inGamma"
			local outGamma = GetINISetting txt "rendersettings" "outGamma"
			local cachePath = GetINISetting txt "path" "cache"
			local photonPath = GetINISetting txt "path" "photon"
			
			stCon.MAX_GAMMA =gamma
			stCon.MAX_INGAMMA=inGamma
			stCon.MAX_OUTGAMMA=outGamma
			stCon.cachePath=cachePath+"\\"+stCon.taskId+"\\"
			stCon.photonPath=photonPath
		)
		
		
		

	),
	
	fn nnlog mkey val = (
		--local logPath = stCon.logPath+"render_"+stCon.mframe+".txt"
		local logPath = stCon.logPath+stCon.jobName+"_debug.txt"
		
		local logFile = openFile logPath mode:"a+"
		try(
			if logFile==undefined then (
				logFile = createFile logPath
			)
			key = (key as string)
			val = (val as string)
			format "[%]  %  %\n" localTime mkey val
			
			format "[%]  %  %\n" localTime mkey val to:logFile
			
			close logFile 
		)catch(
			if logFile!=undefined then (
				close logFile 
			)
		)
	),
	
	
	fn convertExr exrBitmap = (--convert exr to jpg
		
		if exrBitmap!=undefined   then (
			local exrFile =  exrBitmap.fileName			
			nnlog "exrName.." exrFile
			local ext = getFilenameType exrFile			
			if ext==".exr" then (
				if (maxversion())[1]>11000 then (		
					local exrName = getFilenameFile exrFile	
					local exrFather = pathConfig.removePathLeaf exrFile					
					local jpgDir = exrFather + "/JPG/"
					if not doesfileExist jpgDir then (
						makeDir jpgDir
					)
						
					local jpg = jpgDir+exrName+".jpg"
					local jpgBitmap = bitmap exrBitmap.width exrBitmap.height gamma:exrBitmap.gamma filename:jpg 
					pasteBitmap exrBitmap jpgBitmap  [0,0] [0,0] 					
					save jpgBitmap quiet:true
				)	
			)
		)
	),
	
	fn setMyOutputFile =(
		
		--stCon.MAX_OUT_NAME=rendOutputFilename
		local outName = rendOutputFilename
		
		local outPath2 = (stCon.outPath+"RW.tga")
		local frameSerail = ""--RENDER INC  MAP
		if (findstring stCon.mframe "_") == undefind then (
			frameSerail = fillSerial stCon.mframe
		)
		
		local ext = ""
		local bname = "RW"
		if outName ==undefined or outName=="" then(
			ext = ".tga"			
		)else (
			ext = getFilenameType outName
			bname = getFileNameFile outName			
		)
		outPath2 = (stCon.outPath+bname+frameSerail+ext)
		
		nnlog "outPath2 " outPath2 
		/*
		if myKg=="1" then (--split frame
			local OOpath = stCon.outPath + "block"+frameArr[6]+"/"
			if not doesfileexist oopath then (
				makeDir  OOpath
			)
			local myoutpath = (OOpath+bname+ext)
			nnlog   "start split render ..."  myoutpath 
			
		)
		*/
		rendSaveFile=true
		rendOutputFilename=outPath2
		stCon.MAX_OUT_NAME=outPath2
		outPath2
	),

	
	
	fn delAllUserPath = (
		
		local cc =mapPaths.count()
		for i in cc to 1 by -1 do (
			try(
				mapPaths.delete i
			)catch()
		)
		
	),

	fn getAllUserPath=(
		
		local userPathArr = #()
		for i=1 to mapPaths.count() do (
			local myPath = mapPaths.get i
			append userPathArr myPath
		)
		userPathArr
	),

	fn addUserPath userPathArr = (
		
		for i=1 to userPathArr.count do (
			local mpath = userPathArr[i]
			if mpath!=undefined then (
				mapPaths.add mpath
			)
			
		)
		
		
	),

	
	fn delAllXrefPath = (
		
		local cc =xrefPaths.count()
		for i in cc to 1 by -1 do (
			try(
				xrefPaths.delete i
			)catch()
		)
		
	),

	fn getAllXrefPath=(
		
		local xrefPathArr = #()
		for i=1 to xrefPaths.count() do (
			local myPath = xrefPaths.get i
			append xrefPathArr myPath
		)
		xrefPathArr
	),

	fn addXrefPath xrefPathArr = (
		
		for i=1 to xrefPathArr.count do (
			local mpath = xrefPathArr[i]
			if mpath!=undefined then (
				xrefPaths.add mpath
			)
			
		)
		
		
	),
	
	
	fn initMaxFN = (
		
		local pathArr = getAllUserPath()
		stCon.maxUserPath=pathArr
		local userPathArr=#(stCon.taskPath,stCon.texPath,stCon.cachePath)
		addUserPath userPathArr
		
		local xrefPathArr =getAllXrefPath()
		stCon.maxXrefPath=xrefPathArr
		local xrefPathArr=#(stCon.taskPath,stCon.texPath,stCon.cachePath)
		addUserPath xrefPathArr
		
	),
		
	fn commonFN = (--common
		
		if (maxversion())[1] > 9000 then(
			if stCon.MAX_GAMMA!=undefined and stCon.MAX_GAMMA=="on" then (
				IDisplayGamma.colorCorrectionMode == #gamma	
				fileInGamma=stCon.MAX_INGAMMA as float
				fileOutGamma=stCon.MAX_OUTGAMMA as float
			)else(
				IDisplayGamma.colorCorrectionMode == #none
			)
		)else(
			if stCon.MAX_GAMMA!=undefined and stCon.MAX_GAMMA=="on" then (
				setIniSetting iniFile "Gamma" "DisplayCorrectionMode" "0"
				fileInGamma=stCon.MAX_INGAMMA as float
				fileOutGamma=stCon.MAX_OUTGAMMA as float
			)else(
				setIniSetting iniFile "Gamma" "DisplayCorrectionMode" "2"
			)
		)
		
		setMyOutputFile()  
		
		
		
		renderSceneDialog.update()
		renderSceneDialog.commit()
		
		
		/*
			
			displayGamma = 2.2
			iniFile = getMaxIniFile()

			setIniSetting iniFile "Gamma" "CorrectColorPickerState" "1"
			setIniSetting iniFile "Gamma" "CorrectMtlEditorState" "1"
		*/
		
		
	),
	
	fn loadMaxFN = (
		

		
		useFileUnits=true 
		quiet=true 
		try(setVRaySilentMode() )catch()
		nnlog   "-----------start loading -----------" ""
		local logarr1 = #()
		local logarr2 = #()
		
		DialogMonitorOPS.unRegisterNotification id:#RB_Monitor_Dialog 
		
		DialogMonitorOPS.RegisterNotification RB_MontiorDialog id:#RB_Monitor_Dialog
		DialogMonitorOPS.Enabled = true
		
		if stCon.userId=="160699"  then (
			try (
				xrefPaths.add "\\\\10.50.1.3\\d\\inputdata\\max\\160500\\160699\\bollywood\\xrefs"
			)catch()
		)
		
		local ll = loadMaxFile stCon.maxFile useFileUnits:true quiet:true missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1  missingDLLsAction:#(#logmsg) missingDLLsList:&logarr2
		
		join logArr logarr1
		join logArr logarr2
		
		
		ll
	),
	
	
	fn tex = (
		try(
			
			nnlog   "----------------start tex------------- " ""
			
			if (maxversion())[1] >= 12000 then( -- vray environment files are not in asset tracker in max 2010
			
				local env = useEnvironmentMap	--extremely weird bug in max: if a special hdr file is in the env slot it activates the env map. nobody knows why... FUCK MAX
				local rend = renderers.production
				if classof rend == vray   then(
					
					try(
						
						if rend.environment_gi_on and rend.environment_gi_map != undefined then(	
							envGimap=rend.environment_gi_map					
							rend.environment_gi_map.name="GI" 
							setMeditMaterial 1 rend.environment_gi_map 
						)
						if rend.environment_rr_on and rend.environment_rr_map != undefined then(
							envRrmap =rend.environment_rr_map
							rend.environment_rr_map.name="GI" 
							setMeditMaterial 2 rend.environment_rr_map 
						)
						if rend.environment_refract_on and rend.environment_refract_map != undefined then(	
							envRefractmap=rend.environment_refract_map			
							rend.environment_refract_map.name="GI" 
							setMeditMaterial 3 rend.environment_refract_map 
						)
						
						
					)catch()
					
					
				)
				useEnvironmentMap = env
			)
			
			ATSOps.Visible = true
			ATSOps.Disabled = false	
			ATSOps.SetPath stCon.texPath
			ATSOps.Visible = false
			
			nnlog   "----------------tex completed------------- "  ""
		)catch(		
			nnlog   (getCurrentException() as string)	""	
			sleep 10
		)
	),

	fn elem =(
		
		print "render element..."
		re = maxOps.GetCurRenderElementMgr() 
		theManager = maxOps.GetRenderElementMgr #Production
		
		nnlog   "----------------start render elem------------- "  ""
		eact = re.GetElementsActive()		
		
		for n = 0 to (theManager.numrenderelements()- 1) do(
		
			local el = re.getrenderelement n	
				
			local elName = re.GetRenderElementFilename n
			local elType = el.elementname
			nnlog   "eleName..." elname
			
			local resultName = ""
			if elName==undefined or elName=="" then(				
				resultName = elType+"_"+stCon.frameSerial+".tga"
			)else(
				local elext = getFilenameType elname	
				local elBasename = getFilenameFile elname
				resultName = elBasename +"_"+stCon.frameSerial+ elext
			)
			
			nnlog   "resultname......" resultName
			re.SetRenderElementFilename n (stCon.outPath + resultName )
			
		)
		nnlog   "--------------render elem completed-------------- " ""
	),
	
	fn vrayFN = (
		
		nnlog   "------------start vray----------------- " ""
		local rend = renderers.current
	
		if not doesfileexist stCon.logPath then (
			makeDir stCon.logPath all:true	
		)	
		rend.system_vrayLog_file=stCon.logPath+"vr.log"
			/*
			rend.system_region_x 
			rend.system_vrayLog_level
			rend.system_numThreads
			rend.system_raycaster_memLimit
			*/
		
		
		rend.output_width = renderWidth 
		rend.output_height = renderHeight 
		
		rend.options_dontRenderImage=false
		
		local enableFrameBuffer = rend.output_on
		local renderToRwFile = rend.output_saveRawFile			
		local splitBuffer = rend.output_splitgbuffer
		if(enableFrameBuffer==true) then (--vray frame buffer
			local outputRawFile = rend.output_rawFileName
			if renderToRwFile==true and outputRawFile!=undefined and outputRawFile!=""  then (					
				local outputRawFileT = getFilenameType outputRawFile
				local outputRawFileN = getFileNameFile outputRawFile
				rend.output_rawFileName =stCon.outPath + outputRawFileN + outputRawFileT
			)
				
			local splitFileName = rend.output_splitfilename
			if splitBuffer==true and splitFileName!=undefined and splitFileName != "" then (					
				local splitFileT = getFilenameType splitFileName
				local splitFileN = getFileNameFile splitFileName					
				rend.output_splitfilename = stCon.outPath + splitFileN + splitFileT
				
			)
		)
		
		
		
		local irrLoadFile = rend.adv_irradmap_loadFileName
		local ligLoadFile = rend.lightcache_loadFileName
		if irrLoadFile!=undefined and irrLoadFile!="" then(
			local irrLoadFileName =  getRWFileName irrLoadFile
			rend.adv_irradmap_loadFileName=stCon.texPath +irrLoadFileName
		)
		
		if  ligLoadFile!=undefined and ligLoadFile!="" then(
			local ligLoadFileName =  getRWFileName ligLoadFile
			rend.lightcache_loadFileName=stCon.texPath +ligLoadFileName
		)

/*		
		IrradianceMap
			IncrementalAddToCurrentMap
			AnimationPrepass

		LightCache
			Flythrough	
*/	
		
		if stCon.sonId!=undefined  and stCon.sonId!="" and  stCon.sonId!="0" then (--组合任务，父子任务（先渲光子任务，后调用光子渲正图）
			nnlog   "father and son " ""
			if stCon.sonId==stCon.taskId then (--子任务（渲光子）
				local irrSaveFile =rend.adv_irradmap_autoSaveFileName		
				local ligSaveFile = rend.lightcache_autoSaveFileName		
				local irrMode = rend.adv_irradmap_mode
				
				if stCon.kg=="2" and  irrMode == 4 then (--渲染叠加光子
					nnlog   "渲染叠加光子 " ""
					if irrSaveFile!=undefined and irrSaveFile!="" do (--inc
						local ext = getFilenameType irrSaveFile
						local bname = getFileNameFile irrSaveFile
						rend.adv_irradmap_autoSaveFileName=(stCon.outPath+bname+ext)
						rend.options_dontRenderImage=true
						rend.gi_irradmap_showCalcPhase=true
					)
				)else if stCon.kg=="3"  and irrMode==6 then (--渲染序列光子
					nnlog   "渲染序列光子 " ""
					if irrSaveFile!=undefined and irrSaveFile!="" do (
						local ext = getFilenameType irrSaveFile
						local bname = getFileNameFile irrSaveFile
						
						rend.adv_irradmap_autoSaveFileName=(stCon.outPath+bname+ext)
						rend.options_dontRenderImage=true
						rend.gi_irradmap_showCalcPhase=true
					)
				)else if stCon.kg=="4"  and irrMode==4 then (--快速渲染叠加光子（不能是单帧）
					nnlog   "快速渲染叠加光子（不能是单帧） " ""
					if irrSaveFile!=undefined and irrSaveFile!="" do (--inc
						local ext = getFilenameType irrSaveFile
						local bname = getFileNameFile irrSaveFile
						rend.adv_irradmap_autoSaveFileName=(stCon.outPath+bname+stCon.frameSerial+ext)
						rend.options_dontRenderImage=true
						rend.gi_irradmap_showCalcPhase=true
					)
				)
				
				
				local ligMode = rend.lightcache_mode
				if ligMode==1 then (
					if ligSaveFile!=undefined and ligSaveFile!="" do (
						local saveLigFileName = getRWFileName ligSaveFile
						rend.lightcache_autoSaveFileName=(stCon.outPath+saveLigFileName)
						rend.options_dontRenderImage=true
						rend.gi_irradmap_showCalcPhase=true
					)
				)



			) else (--父任务（调用光子渲正图）
				rend.options_dontRenderImage=false
				local irrMode = rend.adv_irradmap_mode
				if irrMode == 4  then (
					local saveFile = rend.adv_irradmap_autoSaveFileName
					local saveFileName = getRWFileName saveFile
					rend.adv_irradmap_mode=2  --from file
					rend.adv_irradmap_loadFileName=stCon.texPath+saveFileName
				)else if irrMode==6 then (
					local saveFile = rend.adv_irradmap_autoSaveFileName
					local saveFileName = getRWFileName saveFile
					rend.adv_irradmap_mode=7  --animation (rendering) 
					rend.adv_irradmap_loadFileName=stCon.texPath+saveFileName
				)
				
				local ligMode=rend.lightcache_mode 
				if ligMode==1 then (
					local saveFile = rend.lightcache_autoSaveFileName
					local saveFileName = getRWFileName saveFile							
					rend.lightcache_mode=2
					rend.lightcache_loadFileName=stCon.texPath+saveFileName
				)
				
				
			)
				
			
			
		)else(--非组合任务（渲正图或者调用光子渲正图）
				
			local irrSaveFile =rend.adv_irradmap_autoSaveFileName		
			local ligSaveFile = rend.lightcache_autoSaveFileName		
			local irrMode = rend.adv_irradmap_mode
			
			if irrMode == 4 or irrMode==6 then (
				if irrSaveFile!=undefined and irrSaveFile!="" do (
					local saveIrrFileName = filenameFromPath  irrSaveFile
					rend.adv_irradmap_autoSaveFileName=(stCon.outPath+saveIrrFileName)
					
					
				)
			)
			
			
			local ligMode = rend.lightcache_mode
			if ligMode==1 then (
				if ligSaveFile!=undefined and ligSaveFile!="" do (
					local saveLigFileName = filenameFromPath ligSaveFile
					rend.lightcache_autoSaveFileName=(stCon.outPath+saveLigFileName)
					
					
				)
			)
			
					
		)
		
		/*
		if then (--渲染光子任务（拆分任务：渲染光子，调光子渲染图）
			
			
		)else(--直接上传光子渲染图片的任务
			
		)
		*/
		nnlog   "------------vray completed---------------- " ""
	),
	
	fn finalRenderFN = (
		nnlog   "----------------finalRenderFN------------- " ""
		local rend = renderers.production
	
		local giEnable = rend.giEnable
		local giSolutionMode = rend.giSolutionMode
		local giSolutionMultipleFiles = rend.giSolutionMultipleFiles
		local giUseSolutionFile = rend.giUseSolutionFile
		local giSolutionFile = rend.giSolutionFile
		if giEnable and giUseSolutionFile and giSolutionFile!=undefined and giSolutionFile!="" then (
			nnlog   "giSolutionFile------------ " ""
			if giSolutionFile.count>4  and matchPattern giSolutionFile pattern:"*.gis" then (
				local photonName = getRWFileName giSolutionFile
				local myGiSolutionFile = pathConfig.appendPath maxfilePath photonName
				rend.giSolutionFile = myGiSolutionFile
				nnlog   "giSolutionFile------------" myGiSolutionFile 
			)
		)
		nnlog   "----------------finalRenderFN.end------------- "  ""
	),
	
	fn phoenixFN = (
		try(
			local arr = getclassinstances PHXSimulator
			for a in arr do (
				--showproperties a
				
				local phoenixName = getFilenameFile a.rendinput
				a.rendinput=pathConfig.appendPath stCon.texPath phoenixName
				
			)
		)catch()
	),
	
	fn fumefxFN=(
		try(
			local arr = getclassinstances FumeFX
			for a in arr do(
				local defaultPath = a.GetPath "default"
				local waveletPath = a.GetPath "wavelet"
				local retimerPath = a.GetPath "retimer"
				
				local defaultName = getRWFileName defaultPath
				local waveletName = getRWFileName waveletPath
				local retimerName = getRWFileName retimerPath
				local defaultSysPath = pathConfig.appendPath stCon.cachePath (defaultName+".fxd")
				local waveletSysPath = pathConfig.appendPath stCon.cachePath (waveletName+".fxd")
				local retimerSysPath = pathConfig.appendPath stCon.cachePath (retimerName+".fxd")
				
				nnlog   "-------------defaultSysPath--------------- " defaultSysPath
				nnlog   "-------------waveletSysPath--------------- " waveletSysPath
				nnlog   "-------------retimerSysPath--------------- " retimerSysPath
				a.SetPath defaultSysPath #("default")
				a.SetPath waveletSysPath #("wavelet")
				a.SetPath retimerSysPath #("retimer")
			)
			
		)catch()
		
	),
	
	
		
	fn realflow = (
		
		nnlog  "--RFMeshLoader--" ""
		try(
			local rfMeshes = getClassInstances RFMeshLoader		
			for rfMesh in rfMeshes do(	

				local meshPath = rfMesh.path			
				if meshPath!=undefined and meshPath!="" then (
					rfMesh.path = stCon.cachePath
					
				)
				
			)
		)catch	()
			
			
		nnlog  "--ParticleLoader--"  ""
		try(
			local isValidVersionParticleLoader = true
			local rfParticles = getClassInstances ParticleLoader
			if rfParticles.count > 0 then(
				if not hasProperty rfParticles[1] "binPath" then(
					isValidVersionParticleLoader=false				
				)
				
				if isValidVersionParticleLoader then (
					for rfp in rfParticles do (
						rfp.binPath = stCon.cachePath
					)
				)
			)
			
		)catch()
			
			
		nnlog  "--RFSoftBody--" ""
		try(
			local isValidVersionRFSoftBody = true	
			if rfEditableMeshPaths.count>0 then (
				local rfEditableMeshPaths = getClassInstances RFSoftBody
				if not hasProperty rfEditableMeshPaths[1] "SD_Filename" then (
					isValidVersionRFSoftBody = false					
				)
				
				if isValidVersionRFSoftBody then (
							
					for rfMesh in rfEditableMeshPaths do(
						
						local rfMeshPath = rfMesh.SD_Filename
						if rfMeshPath!=undefined and rfMeshPath!="" then (
							local rfMeshName =  getRWFileName rfMeshPath
							if rfMeshName==undefined then (
								rfMeshName = ""
							)
							rfMesh.SD_Filename =stCon.taskPath + rfMeshName						
						)
					)
				)
			)
			
		)catch()
		
	),
	
	
	fn xmeshFn=(
		try(
			local cacheArr = getclassinstances XMeshLoader
			for mycache in cacheArr do (
				
				--showproperties mycache
				
				local renderSequencePath = mycache.renderSequence
				local proxySequencePath = mycache.proxySequence
				
				
				if renderSequencePath!=undefined and renderSequencePath!="" then (
					local renderSequenceName = getRWFileName renderSequencePath
					local resultPath = pathConfig.appendPath stCon.cachePath renderSequenceName
					mycache.renderSequence = resultPath
					
					nnlog   "-------------renderSequencePath--------------- " resultPath
				)
				
				if proxySequencePath!=undefined and proxySequencePath!="" then (
					local proxySequenceName = getRWFileName proxySequencePath
					mycache.proxySequence = pathConfig.appendPath stCon.cachePath proxySequenceName
					
					
				)
				
				
			)
		)catch()
		
	),
	
	
	fn getMyCamera=(
		local myCamera = getActiveCamera()
		local renderView
		try(
			if (rendUseActiveView) then ( 
				renderView = viewport.activeViewport 
			)else ( 
				renderView = rendViewIndex 
			)
			myCamera =  (viewport.getCamera index:renderView)
			
			--if myCamera==undefined then (
				--myCamera= viewport.Gettype() 
			--)
		)catch()
		
		myCamera
	),
	
	
	fn renderFramesPerJobFN  myKg= (
		nnlog   "-------------renderFramesPerJobFN---------------- " ""
		local logarr1 = #()
		local logarr2 = #()
		local logarr3 = #()
		local elemArr=#()
		
		local myOutputFile=stCon.MAX_OUT_NAME
		local frameArr = filterString stCon.mframe "_"
		local myStart = frameArr[1]
		local myEnd = frameArr[2]
		
		local myByframe = "1"
		if frameArr.count==3 then (
			myByframe = frameArr[3]
		)
		
		nnlog  ("start:"+myStart+" end:" + myEnd + " nth:" + myByframe) ""
		
		nnlog "Render ... common....From web" ""
		for c in cameras do (
			
			local cameraNameStr=trimright (trimleft c.name)
			if (classof c)!=Targetobject and cameraNameStr==stCon.myCamera then (

				render outputwidth:(stCon.imageWidth as Integer) outputheight:(stCon.imageHeight as Integer) camera:c fromframe:(myStart as time)  toframe:(myEnd as time) nthframe:(myByframe as time) outputfile:myOutputFile quiet:true progressbar:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 --"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
			)
		)
		
		
		join logArr logarr1
		join logArr logarr2
		join logArr logarr3
			
	),
	
	fn renderFrameSplitPicFn myKg= (
		
		nnlog   "-------------renderFrameSplitPicFn---------------- " ""
		local elemArr=#()
		local logarr1 = #()
		local logarr2 = #()
		local logarr3 = #()
		
		local frameArr = filterString stCon.mframe "_"--frame_left_top_right_bottom_block_width_height
		local myOutputFile=stCon.MAX_OUT_NAME
		
		nnlog "Render ... split....From web" ""
		for c in cameras do (
			
			
			local cameraNameStr=trimright (trimleft c.name)
			if (classof c)!=Targetobject and cameraNameStr==stCon.myCamera then (

				render outputwidth:(stCon.imageWidth as Integer) outputheight:(stCon.imageHeight as Integer) camera:c frame:(frameArr[1] as time) renderType:#regionCrop   region:#(frameArr[2] as number,frameArr[3] as number,frameArr[4] as number,frameArr[5] as number) outputfile:myOutputFile quiet:true progressbar:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 --"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
			)
		)
			
		if elemArr != undefined then (
				for elem in elemArr do (
					local elemName = getRWFileName elem.fileName
					local elemTemp = bitmap imgBitmap.width imgBitmap.height  fileName:(OOpath+elemName)				
					pasteBitmap elem elemTemp  [0,0] [0,0]				
					save elemTemp				
					convertExr elemTemp
				)
		)
		
		join logArr logarr1
		join logArr logarr2
		join logArr logarr3
		
	),
	
	fn renderIncPhotonFn myKg=(
		nnlog   "-------------renderIncPhotonFn---------------- " ""
		local logarr1 = #()
		local logarr2 = #()
		local logarr3 = #()
		
		local frameArr = filterString stCon.mframe "_"
		local myStart = frameArr[1]
		local myEnd = frameArr[2]
		
		local myBy = "1"
		if frameArr.count==3 then (
			myBy = frameArr[3]
		)
		local myOutputFile=stCon.MAX_OUT_NAME
		nnlog  ("start:"+myStart+" end:" + myEnd + " nth:" + myBy) ""
		
	
		render fromframe:(myStart as time)  toframe:(myEnd as time) nthframe:(myBy as time) outputfile:myOutputFile quiet:true progressbar:true  renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 --"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
		
		
				
		join logArr logarr1
		join logArr logarr2
		join logArr logarr3

		
	),
	
	fn renderCommonFn myKg=(
		nnlog   "-------------renderCommonFn---------------- " ""
		local frameArr = filterString stCon.mframe "_"--frame_left_top_right_bottom_block_width_height
		local elemArr=#()
		local myOutputFile=stCon.MAX_OUT_NAME
		nnlog "client.." myOutputFile
		

			
				
		local enableFrameBuffer = false
		local renderToRwFile = false
		local myrender=renderers.current
		local myrenderStr = classof renderers.current as string
		try(
			enableFrameBuffer = myrender.output_on
			renderToRwFile = myrender.output_saveRawFile
		)catch()
	
		local myCamera = getMyCamera()
		
		
		nnlog "Render common" myCamera
		if myCamera == undefined then (
			nnlog "camera is undefined" ""
			render  frame:(frameArr[1] as time) outputfile:myOutputFile quiet:true progressbar:true  renderElements:true renderElementBitmaps:&elemArr  
		)else(
			nnlog "camera is " myCamera
			if stCon.MAX_GAMMA!=undefined and stCon.MAX_GAMMA=="on" then (
				nnlog "MAX_GAMMA ON" ""
				--local myBitmap = bitmap 720 480 filename: myOutputFile gamma:stCon.MAX_OUTGAMMA
				if enableFrameBuffer and renderToRwFile then (
					nnlog "VFB ON" ""
					
					render frame:(frameArr[1] as time)  quiet:true progressbar:true camera:myCamera renderMultiPassEffects:true 
					
				) else(
					nnlog "VFB OFF" ""
					local myBitmap = bitmap renderWidth renderHeight filename:myOutputFile
					--render  frame:(frameArr[1] as time) outputfile:myOutputFile quiet:true progressbar:true camera:myCamera renderElements:true renderElementBitmaps:&elemArr  
					render  frame:(frameArr[1] as time) to:myBitmap quiet:true progressbar:true camera:myCamera renderElements:true renderElementBitmaps:&elemArr  
					myBitmap.gamma=(stCon.MAX_OUTGAMMA as Float)
					save myBitmap 
					close myBitmap
				)	
			)else(
				nnlog "MAX_GAMMA OFF" ""
				if enableFrameBuffer and renderToRwFile then (
					nnlog "VFB ON" ""
					render frame:(frameArr[1] as time)  quiet:true progressbar:true camera:myCamera renderMultiPassEffects:true 
					
				) else(
					nnlog "VFB OFF" ""
					render  frame:(frameArr[1] as time) outputfile:myOutputFile quiet:true progressbar:true camera:myCamera renderElements:true renderElementBitmaps:&elemArr  
					
				)
			)
		)
		
		
			/*
			
			if enableFrameBuffer and renderToRwFile then (
				nnlog "Render ... common....From client.width vfb" ""
				if myCamera==undefined then (
					nnlog "Render ... common....From client.width vfb.camera.undefined" ""
					render frame:(frameArr[1] as time)  quiet:true progressbar:true  renderMultiPassEffects:true  
				)else(
					nnlog "Render ... common....From client.width vfb.camera" ""
					render frame:(frameArr[1] as time)  quiet:true progressbar:true camera:myCamera renderMultiPassEffects:true  
				)
				
			) else(
				nnlog "Render ... common....From client.widthout vfb" ""
				if myCamera==undefined then (
					nnlog "Render ... common....From client.widthout vfb camera.undefined" ""
					render  frame:(frameArr[1] as time) outputfile:myOutputFile quiet:true progressbar:true renderElements:true renderElementBitmaps:&elemArr  
				)else(
					nnlog "Render ... common....From client.widthout vfb camera" ""
					render  frame:(frameArr[1] as time) outputfile:myOutputFile quiet:true progressbar:true camera:myCamera renderElements:true renderElementBitmaps:&elemArr  
				)
				
			)						
			
			*/
			--render filename:"somotherthing.jpg" gamma:1.0 -- an override
			
			--imgBitmap.filename=myoutpath--outputfile:myoutpath
			--save imgBitmap frame:(stCon.mframe as integer) 
			--convertExr imgBitmap
			if elemArr != undefined then (
				for elem in elemArr do (					
					save elem				
					convertExr elem
				)
			)
	),
	
	fn preRenderParam = (
		
		
	),
	
	fn r = (
		nnlog   "-------------start render---------------- " ""
		
		
		
		
		local logarr1 = #()
		local logarr2 = #()
		local logarr3 = #()
		
		
		if stCon.kg=="1" then (--render split pic
			renderFrameSplitPicFn stCon.kg
		)else if stCon.kg=="2" then (-- render inc photon
			renderIncPhotonFn stCon.kg
		)else(
			renderCommonFn stCon.kg
		)
			
		
		
		
		join logArr logarr1
		join logArr logarr2
		join logArr logarr3
		if logArr!=undefined and logArr.count>0 then (
			nnlog  "------Warning-------" ""
			for lg in  logArr do(
				nnlog  lg ""
			)
		)
		nnlog   "----------------completed render------------ " ""
		
	),

	fn myRender = (
		
		
		nnlog "userId" stCon.userId
		nnlog "taskId" stCon.taskId
		nnlog "sonId" stCon.sonId
		nnlog "mframe" stCon.mframe
		nnlog "kg" stCon.kg
		nnlog "maxFile" stCon.maxFile
		nnlog "taskPath" stCon.taskPath
		nnlog "outPath" stCon.outPath
		nnlog "texPath" stCon.texPath
		nnlog "logPath" stCon.logPath
		--nnlog "jobName" stCon.jobName
		nnlog "MAX_GAMMA" stCon.MAX_GAMMA
		nnlog "MAX_INGAMMA" stCon.MAX_INGAMMA
		nnlog "MAX_OUTGAMMA" stCon.MAX_OUTGAMMA
		nnlog "cachePath" stCon.cachePath
		nnlog "photonPath" stCon.photonPath
		
		
		initMaxFN()
		local ll = loadMaxFN()
		if ll then (
			try(
				nnlog   "----------------load max file successed------------- " ""
				commonFN()
				tex()
				elem()
				local rendStr = (classof renderers.production ) as string
				
				if (rendStr == (vray as string)) then (
					vrayFN()
				) else if (rendStr == (default_scanline_renderer as string)) then (
					
				) else if rendStr == (finalRender_stage_1 as string) then (
					finalRenderFN()
				) else if (rendStr == (MaxwellRenderer as string)) then (
					
				) else if (rendStr == (mental_ray_renderer as string)) then (
					
				) else if (rendStr == (mental_ray_iray_Renderer as string)) then (
					
				) else if (rendStr == (Quicksilver_Hardware_Renderer as string)) then (
					
				) 
				realflow()
				phoenixFN()
				fumefxFN()
				xmeshFn()
				renderSceneDialog.update()
				renderSceneDialog.commit()
				r()
				
				
				try(
					delAllUserPath()
					addUserPath stCon.maxUserPath
				)catch()
				
				try(
					delAllXrefPath()
					addXrefPath stCon.maxXrefPath
				)catch()
				
				/*
				rlog  "----------------resetMaxFile  -------------\n" 
				resetMaxFile  #noPrompt
				rlog  "----------------quitMax-------------\n" 
				quitMax #noPrompt 
				rlog  "----------------sleep-------------\n" 
				sleep 10
				*/
				nnlog   "----------------maxkil------------- " ""
				DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string))  
				nnlog   "----------------game over------------ " ""
			)catch(
				try(
					DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string))  
					nnlog   "----------------Excep.game over------------ " ""
					nnlog   (getCurrentException() as string) ""
				)catch()
				)
		)else(
			nnlog  "load max file faild... " ""
		)
		
	)

)




fn rwRender userId taskId sonId mframe kg jobName maxFile= (
	
	--local st = STConst()
	--st.init userId taskId sonId frame maxFile
	
	local r = RBRender()
	r.init  userId taskId sonId mframe kg jobName maxFile
	
	--r.stCon = st
	--r.init userId taskId frame maxFile
	r.myRender()
)





--clearlistener()
---rendercommon
--rwRender "119870" "3114" "3113" "2" "3" "frame0002" "C:/work/render/3114/3114.max"

--serial vrmap
--rwRender "100001" "3139" "3139" "2" "3" "frame0002" "C:/work/render/3139/3139.max"



--fast inc vrmap
--rwRender "100001" "3137" "3137" "2" "4" "frame0002" "C:/work/render/3137/3137.max"





-- inc vrmap
--rwRender "100001" "3143" "3143" "0_100_10" "2" "frame0002" "C:/work/render/3143/3143.max"