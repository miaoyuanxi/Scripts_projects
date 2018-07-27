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
kg 代表主任务 从0-99
subKg 代表光子任务 从100-200

kg=0 max普通任务
kg=1 max拆分任务
kg=2 

kg=7 maya

kg=9
kg=11 C4D
kg=12 blender
kg=15 快渲
kg=16 houdini
subkg=100 渲染叠加光子
subkg=101 拆分渲染叠加光子（不能是单帧）
subkg=102 渲染序列光子

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

struct STRealflow (
	nodeName,
	cachePath
)

struct STConst (
	userId, taskId, mframe, frameSerial,maxFile,sonId,kg,
	gamma,
	inGamma,
	outGamma,
	renderWork = "c:/work/render/",
	taskPath,
	texPath,
	outPath,
	logPath,
	cachePath,
	photonPath,
	outName,
	fromWhere,
	elementStr,
	imageWidth,
	imageHeight,
	camera,
	selfCfg,
	jobName,
	realflowArray
)


	



struct RBRender (
	
	stCon ,
	logArr=#(),
	
	
	fn init u t s f kg j m=(
		stCon=STConst()
		stCon.userId = u
		stCon.taskId = t
		stCon.sonId=s
		stCon.mframe = f
		stCon.kg = kg
		stCon.jobName=j
		stCon.maxFile= m
		
		
		stCon.taskPath = stCon.renderWork+t+"/"
		stCon.selfCfg=stCon.taskPath+"cfg/self.cfg"
		stCon.outPath=stCon.taskPath+"output/"
		if kg=="1" then (
			stCon.outPath=stCon.taskPath+"output/"
		)
		
		
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
		
		local txt = stCon.selfCfg
		if doesFileExist txt then (
			local gamma = GetINISetting txt "rendersettings" "gamma"
			local inGamma = GetINISetting txt "rendersettings" "ingamma"
			local outGamma = GetINISetting txt "rendersettings" "outgamma"
			local cachePath = GetINISetting txt "attached" "cachePath"
			local photonPath = GetINISetting txt "attached" "photonPath"
			local outName = GetINISetting txt "rendersettings" "outputname"
			local fromWhere = GetINISetting txt "common" "fromwhere"
			local imageWidth = GetINISetting txt "rendersettings" "width"
			local imageHeight = GetINISetting txt "rendersettings" "height"
			local camera = GetINISetting txt "rendersettings" "camera"
			
			stCon.gamma =gamma
			stCon.inGamma=inGamma
			stCon.outGamma=outGamma
			stCon.cachePath=cachePath
			stCon.photonPath=photonPath
			stCon.fromWhere=fromWhere
			stCon.imageWidth=imageWidth
			stCon.imageHeight=imageHeight
			stCon.camera=camera
			stCon.outName=outName
			
			
			if fromWhere=="web" then (
				stCon.elementStr=GetINISetting txt "rendersettings" "elementstr"
			)
		)
		

	),
	
	fn nnlog key val = (
		local logPath = stCon.logPath+stCon.jobName+"_debug.txt"
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

	
	fn commonFN = (--common
		
		
		
			if (maxversion())[1] > 9000 then(
				if stCon.gamma!=undefined and stCon.gamma=="on" then (
					IDisplayGamma.colorCorrectionMode == #gamma	
					fileInGamma=stCon.inGamma as float
					fileOutGamma=stCon.outGamma as float
				)else(
					IDisplayGamma.colorCorrectionMode == #none
				)
			)else(
				if stCon.gamma!=undefined and stCon.gamma=="on" then (
					setIniSetting iniFile "Gamma" "DisplayCorrectionMode" "0"
					fileInGamma=stCon.inGamma as float
					fileOutGamma=stCon.outGamma as float
				)else(
					setIniSetting iniFile "Gamma" "DisplayCorrectionMode" "2"
				)
			)
		
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
		local ll = loadMaxFile stCon.maxFile useFileUnits:true quiet:true missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1  missingDLLsAction:#(#logmsg) missingDLLsList:&logarr2
		
		join logArr logarr1
		join logArr logarr2
		
		
		ll
	),
	
	
	fn textureFN = (
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
	
	fn elementWebFN = (
		if stCon.elementStr==undefined or stCon.elementStr=="" then (
			nnlog "elem is undefined" ""
			re = maxOps.GetCurRenderElementMgr() 
			re.SetElementsActive(false)
		)else(
			nnlog "elem is " stCon.elementStr
			
			elemList=filterString stCon.elementStr "|"
			
			local outpath=stCon.outPath
			if stCon.kg=="1" then (--render split pic
				local frameArr = filterString stCon.mframe "_"--frame_left_top_right_bottom_block_width_height			
				local OOpath = stCon.outPath + "block"+frameArr[6]+"/"
				outpath=OOpath
			)
			
			re = maxOps.GetCurRenderElementMgr() 
			re.SetElementsActive(true)
			for i=1 to (elemlist.count) do (
				n=i-1
				myel = elemlist[i]
				
				el = re.getrenderelement n			
				
				if myel=="" or myel==null  then(
					el.enabled = false		
				)else(
					el.enabled = true
					
					elext = ".tga"
					elname = re.GetRenderElementFilename n	
					if(elname!=null and elname!=undefined and elname!="") then (					
							elext = getFilenameType elname					
							
					)
					if(elext==null or elext=="" or elext==undefined) then (
						elext=".tga"
					)
					re.SetRenderElementFilename n (outpath + myel+"_"+stCon.frameSerial + elext )
					
				)	
				
			)
		)
	),

	fn elementClientFN =(
		
		print "render element..."
		re = maxOps.GetCurRenderElementMgr() 
		theManager = maxOps.GetRenderElementMgr #Production
		
		nnlog   "----------------start render elem------------- "  ""
		eact = re.GetElementsActive()		
		
		local outpath=stCon.outPath
		if stCon.kg=="1" then (--render split pic
			local frameArr = filterString stCon.mframe "_"--frame_left_top_right_bottom_block_width_height			
			local OOpath = stCon.outPath + "block"+frameArr[6]+"/"
			outpath=OOpath
		)
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
			re.SetRenderElementFilename n (outpath + resultName )
			
		)
		nnlog   "--------------render elem completed-------------- " ""
	),
	
	fn elementFN =(
		if stCon.fromWhere=="web" then (
			elementWebFN()
		)else(
			elementClientFN()
		)
		
	),
	
	
	fn vrayWebFN=(
		nnlog   "------------vrayWebFN vray set start----------------- " ""
		
		
		local txt = stCon.selfCfg
		local gion = GetINISetting txt "vray" "gion"
		local irrmode = GetINISetting txt "vray" "irrmode"
		local lchmode = GetINISetting txt "vray" "lchmode"
		local photonfromfile = GetINISetting txt "vray" "photonfromfile"
		local cachefromfile = GetINISetting txt "vray" "cachefromfile"
		local pgiengine = GetINISetting txt "vray" "pgiengine"
		local sgiengine = GetINISetting txt "vray" "sgiengine"
		local subdivs = GetINISetting txt "vray" "subdivs"
		local secbounce = GetINISetting txt "vray" "secbounce"
		local giprimulti = GetINISetting txt "vray" "giprimulti"
		local gisecmulti = GetINISetting txt "vray" "gisecmulti"
		local imagewidth = GetINISetting txt "vray" "imagewidth"
		local imageheight = GetINISetting txt "vray" "imageheight"
		local pixelratio = GetINISetting txt "vray" "pixelratio"
		local photonanimationprepassfile = GetINISetting txt "vray" "photonanimationprepassfile"
		local photonanimationrederingfile = GetINISetting txt "vray" "photonanimationrederingfile"
		local photonincfile = GetINISetting txt "vray" "photonincfile"
		local cacheflytfile = GetINISetting txt "vray" "cacheflytfile"
		local photonincnetfile = GetINISetting txt "vray" "photonincnetfile"
		local lightsub = GetINISetting txt "vray" "lightsub"
		local imagesamplertype = GetINISetting txt "vray" "imagesamplertype"
		local filteron = GetINISetting txt "vray" "filteron"
		local filterkernel = GetINISetting txt "vray" "filterkernel"
		local filtersize = GetINISetting txt "vray" "filtersize"
		local fixsubdiv = GetINISetting txt "vray" "fixsubdiv"
		local dmcminrate = GetINISetting txt "vray" "dmcminrate"
		local dmcmaxrate = GetINISetting txt "vray" "dmcmaxrate"
		local subminrate = GetINISetting txt "vray" "subminrate"
		local submaxrate = GetINISetting txt "vray" "submaxrate"
		local enableframebuffer = GetINISetting txt "vray" "enableframebuffer"
		local rendertorwfile = GetINISetting txt "vray" "rendertorwfile"
		local rawimgname = GetINISetting txt "vray" "rawimgname"
		local splitbuffer = GetINISetting txt "vray" "splitbuffer"
		local splitfilename = GetINISetting txt "vray" "splitfilename"
		
		
		local myrender=renderers.current
		-------------VFB------------
		nnlog   "vfb set" ""
		local enableFrameBuffer = myrender.output_on
		
		
		local outBaseName=getFileNameFile stCon.outName
		if(enableFrameBuffer==true) then (
			local renderToRwFile = myrender.output_saveRawFile
			local rawImgName = myrender.output_rawFileName
			local splitBuffer = myrender.output_splitgbuffer
			
			if(renderToRwFile==true ) then (
				myrender.output_rawFileName = stCon.outPath+outBaseName +"VFB.vrimg"
				--if ( rawImgName==undefined or rawImgName=="" ) then (		)
				
			)
			
			if(splitBuffer==true) then (
				
				local splitFileName = myrender.output_splitfilename
				
				local bufferExt = ".tga"
				if( splitFileName!=undefined and splitFileName!="") then (					
						bufferExt = getFilenameType splitFileName					
						
				)
				if(bufferExt==undefined or  bufferExt=="" ) then (
					bufferExt=".tga"
				)				
				myrender.output_splitfilename=stCon.outPath+outBaseName + bufferExt
				
			)		
		)
		
		
		----------vray set-----------------
		nnlog   "vray gi set" ""
		
		if gion=="true" then(			
			nnlog   "vray_gi on.." ""
			myrender.gi_on=true
			myrender.adv_irradmap_autoSave=false
			myrender.adv_irradmap_dontDelete=false
			myrender.lightcache_autoSave=false
			myrender.lightcache_dontDelete=false
			if giprimulti!=undefined and  giprimulti!="" and giprimulti!="null" then (
				myrender.gi_primary_multiplier=(giprimulti as Float)
			)
			if pgiengine=="0" then (--0:Irradiance map
				myrender.gi_primary_type=0
				if irrmode=="0" then (-- 0:singl frame
					myrender.adv_irradmap_mode=0
				) else if irrmode=="2" then (-- 2: from file
					myrender.adv_irradmap_mode=2 
					if photonfromfile!=undefined and photonfromfile!="" and photonfromfile!="null" then (
						local photonfromfileBase = getFileNameFile photonfromfile
						local photonfromfileExt = getFilenameType photonfromfile
						myrender.adv_irradmap_loadFileName = pathConfig.appendPath  stCon.taskPath (photonfromfileBase+photonfromfileExt)
					
					)
				) else if irrmode=="4" then (-- 4: Incremental add to current map
					myrender.adv_irradmap_mode=4
					myrender.gi_irradmap_showCalcPhase=on
					myrender.adv_irradmap_autoSaveFileName=pathConfig.appendPath  stCon.outPath (photonincfile+".vrmap")
					myrender.options_dontRenderImage=true 
					myrender.adv_irradmap_switchToSavedMap=true
					myrender.adv_irradmap_dontDelete=true
					myrender.adv_irradmap_autoSave=true
				) else if irrmode=="5" then (-- 5: Bucket mode
					myrender.adv_irradmap_mode=5
				) else if irrmode=="6" then (-- 6:  Animation(prepass)渲染序列帧
					myrender.adv_irradmap_mode=6 
					myrender.gi_irradmap_showCalcPhase=on
					--myrender.adv_irradmap_autoSaveFileName=pathConfig.appendPath  stCon.outPath (photonanimationprepassfile+"_"+stCon.frameSerial+".vrmap")
					myrender.adv_irradmap_autoSaveFileName=pathConfig.appendPath  stCon.outPath (photonanimationprepassfile+"_.vrmap")
					myrender.options_dontRenderImage=true
					myrender.adv_irradmap_switchToSavedMap=true
					myrender.adv_irradmap_dontDelete=true
					myrender.adv_irradmap_autoSave=true
				) else if irrmode=="7" then (-- 7: Animation(rendering)调用序列帧
					local photonanimationrederingfileBase = getFileNameFile photonanimationrederingfile
					local photonanimationrederingfileExt = getFilenameType photonanimationrederingfile
					myrender.adv_irradmap_mode=7
					myrender.adv_irradmap_loadFileName=pathConfig.appendPath  stCon.taskPath (photonanimationrederingfileBase+photonanimationrederingfileExt)
				) else if irrmode=="44" then (-- 44: 前台是渲染叠加光子，实际是Animation(prepass)渲染序列帧
					myrender.adv_irradmap_mode=4
					myrender.gi_irradmap_showCalcPhase=on
					myrender.adv_irradmap_autoSaveFileName=pathConfig.appendPath  stCon.outPath (photonincnetfile+"_"+stCon.frameSerial+".vrmap")
					myrender.options_dontRenderImage=true
					myrender.adv_irradmap_switchToSavedMap=true
					myrender.adv_irradmap_dontDelete=true
					myrender.adv_irradmap_autoSave=true
				)else if irrmode=="46" then (-- 46: 前台是渲染叠加光子，实际是Animation(prepass)渲染序列帧
					myrender.adv_irradmap_mode=6
					myrender.gi_irradmap_showCalcPhase=on
					myrender.adv_irradmap_autoSaveFileName=pathConfig.appendPath  stCon.outPath (photonincnetfile+"_"+stCon.frameSerial+".vrmap")
					myrender.options_dontRenderImage=true
					myrender.adv_irradmap_switchToSavedMap=true
					myrender.adv_irradmap_dontDelete=true
					myrender.adv_irradmap_autoSave=true
				)
			) else if pgiengine=="2" then (-- 2:Brute force
				myrender.gi_primary_type=2 
				if hasProperty myrender "dmcgi_subdivs" then (
					myrender.dmcgi_subdivs=(subdivs as Integer)
				)
				
				if hasProperty myrender "qmcgi_subdivs" then (
					myrender.qmcgi_subdivs=(subdivs  as Integer)
				)
			) else if pgiengine=="3" then (-- 3:Light cache
				myrender.gi_primary_type=3
				myrender.lightcache_numPasses=24 
				if lightsub!=undefined and lightsub!="" and lightsub!=null then (
					myrender.lightcache_subdivs=(lightsub  as Integer)
				)
				
				if lchmode=="0" then (--0:singl frame
					myrender.lightcache_mode=0
				) else if lchmode=="1" then (--1:渲染叠加光缓存
					myrender.lightcache_mode=1
					myrender.options_dontRenderImage=true
					myrender.lightcache_dontDelete=true
					myrender.lightcache_autoSave=true
					myrender.lightcache_switchToSavedMap=true
					myrender.lightcache_autoSaveFileName=pathConfig.appendPath  stCon.outPath (cacheflytfile+".vrlmap")
				) else if lchmode=="2" then (--2: from file
					cachefromfileBase = getFileNameFile cachefromfile
					cachefromfileType = getFilenameType cachefromfile
					myrender.lightcache_mode=2
					myrender.lightcache_loadFileName=pathConfig.appendPath  stCon.taskPath (cachefromfileBase+cachefromfileType)
				)
			
			)
			
			
			----------Secondary bounces------------
			if gisecmulti!=undefined and gisecmulti!="" and gisecmulti!="null" then (
				myrender.gi_secondary_multiplier=(gisecmulti as Float)
			)
			if sgiengine=="0" then (--0:none
				myrender.gi_secondary_type=0
			) else if sgiengine=="2" then (--2:Brute force
				myrender.gi_secondary_type=2
				if pgiengine!="2" then (
					if hasProperty myrender "dmcgi_subdivs" then (
						myrender.dmcgi_subdivs=(subdivs as Integer)
					)
					
					if hasProperty myrender "qmcgi_subdivs" then (
						myrender.qmcgi_subdivs=(subdivs   as Integer)
					)
				)
				
				if hasProperty myrender "dmcgi_depth" then (
					myrender.dmcgi_depth=(secbounce   as Integer)
				)
				
				if hasProperty myrender "qmcgi_depth" then (
					myrender.qmcgi_depth=(secbounce   as Integer)
				)
			) else if sgiengine=="3" then (--3:Light cache
				myrender.gi_secondary_type=3
				myrender.lightcache_numPasses=24
				
				if lightsub!=undefined and lightsub!="" and lightsub!="null" then (
					myrender.lightcache_subdivs=(lightsub   as Integer)
				)
				
				if pgiengine !="3" then (
					if pgiengine=="0" and irrmode=="44" then (
						myrender.lightcache_mode=0
					)else if pgiengine=="0" and irrmode=="46" then (
						myrender.lightcache_mode=0
					)else(
						if lchmode=="0" then (--0:singl frame
							myrender.lightcache_mode=0 
						) else if  lchmode=="1" then (
							local cacheflytfileBase = getFileNameFile cacheflytfile
							
							myrender.lightcache_mode=1
							myrender.options_dontRenderImage=true
							myrender.lightcache_dontDelete=true
							myrender.lightcache_autoSave=true
							myrender.lightcache_switchToSavedMap=true 
							myrender.lightcache_autoSaveFileName=pathConfig.appendPath  stCon.outPath (cacheflytfileBase+".vrlmap")
						)else if  lchmode=="2" then (
							myrender.lightcache_mode=2 
							if cachefromfile!=undefined and cachefromfile!="" and cachefromfile!="null" then (
								local cachefromfileBase = getFileNameFile cachefromfile
								local cachefromfileType = getFilenameType cachefromfile								
								myrender.lightcache_loadFileName=pathConfig.appendPath  stCon.taskPath  (cachefromfileBase+cachefromfileType)
							)
						)
					)
				
				)
			)
			
		)else (
			myrender.gi_on=false
		)
		nnlog   "vray  other set" ""
		
		if imagesamplertype!=undefined and imagesamplertype!="" and imagesamplertype!="null" then (
			myrender.imageSampler_type=(imagesamplertype as Integer)
		)
		if fixsubdiv!=undefined and fixsubdiv!="" and fixsubdiv!="null" then (
			myrender.fixedRate_subdivs=(fixsubdiv as Integer)
		)
		if dmcminrate!=undefined and dmcminrate!="" and dmcminrate!="null" then (
			myrender.twoLevel_baseSubdivs=(dmcminrate as Integer)
		)
		if dmcmaxrate!=undefined and dmcmaxrate!="" and dmcmaxrate!="null" then (
			myrender.twoLevel_fineSubdivs=(dmcmaxrate as Integer)
		)
		if subminrate!=undefined and subminrate!="" and subminrate!="null" then (
			myrender.adaptiveSubdivision_minRate=(subminrate as Float)
		)
		if submaxrate!=undefined and submaxrate!="" and submaxrate!="null" then (
			myrender.adaptiveSubdivision_maxRate=(submaxrate as Float)
		)
		if filtern=="true" then (
			myrender.filter_on=true
			if filterkernel!=undefined and filterkernel!="" and filterkernel!="null" then (
				filterkernel="renderers.current.filterkernel="+filterkernel+"()"
				execute filterkernel
			)
		) else (
			myrender.filter_on=false
		)
		
		
		
		if filtersize!=undefined and filtersize!="" and filtersize!="null" then (
			myrender.filter_size=(filtersize as Float)
		)
		
		nnlog   "---vray set end---" ""
	),
	
	fn vrayClientFN = (
		
		nnlog   "------------vrayClientFN.start vray----------------- " ""
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
			
			if stCon.sonId==stCon.taskId then (--子任务（渲光子）
				local irrSaveFile =rend.adv_irradmap_autoSaveFileName		
				local ligSaveFile = rend.lightcache_autoSaveFileName		
				local irrMode = rend.adv_irradmap_mode
				
				if irrMode == 4 or irrMode==6 then (
					if irrSaveFile!=undefined and irrSaveFile!="" do (
						local saveIrrFileName = getRWFileName  irrSaveFile
						rend.adv_irradmap_autoSaveFileName=(stCon.outPath+saveIrrFileName)
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
	
	
	fn vrayFN = (
	
		if stCon.fromWhere=="web" then (
			vrayWebFN()
		) else (
			vrayClientFN()
		)
		
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
	
	
		
	fn realflowFN = (
		
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
	
	
	
	fn renderFN = (
		nnlog   "-------------start render---------------- " ""
		
		
		
		local outName = rendOutputFilename
		if stCon.fromWhere=="web" then (
			outName = stCon.outName 
		)
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
		
		local cam = getActiveCamera()		
		if (maxVersion())[1] >= 11000 then(
			if rendUseActiveView == false and rendViewIndex != undefined then( -- viewport locked
				cam = viewport.getCamera index:rendViewIndex
			)
		)
		
		
		local logarr1 = #()
		local logarr2 = #()
		local logarr3 = #()
		
		
		if stCon.kg=="1" then (--render split pic
			local frameArr = filterString stCon.mframe "_"--frame_left_top_right_bottom_block_width_height
			
			local OOpath = stCon.outPath + "block"+frameArr[6]+"/"
			if not doesfileexist oopath then (
				makeDir  OOpath
			)
			local myoutpath = (OOpath+bname+ext)
			nnlog   "start split render ..."  myoutpath 
			
			local elemArr=#()
			nnlog   "stCon.fromWhere ..."  stCon.fromWhere 
			if stCon.fromWhere=="web" then (
				nnlog "Render ... split....From web" ""
				for c in cameras do (
					if (classof c)!=Targetobject and c.name==stCon.camera then (
						render outputwidth:(stCon.imageWidth as Integer) outputheight:(stCon.imageHeight as Integer) camera:c frame:(frameArr[1] as time) renderType:#regionCrop   region:#(frameArr[2] as number,frameArr[3] as number,frameArr[4] as number,frameArr[5] as number) outputfile:myoutpath quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 --"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
					)
				)
			)else(
				nnlog "Render ... split....From client" ""
				local imgBitmap = render camera:cam frame:(frameArr[1] as time) renderType:#regionCrop   region:#(frameArr[2] as number,frameArr[3] as number,frameArr[4] as number,frameArr[5] as number)  quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 --"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
				imgBitmap.filename=myoutpath--outputfile:myoutpath
				save imgBitmap 
				convertExr imgBitmap
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
			
		)else if stCon.kg=="2"  or stCon.kg=="100" then (-- render inc photon
			local frameArr = filterString stCon.mframe "_"
			local start = frameArr[1]
			local end = frameArr[2]
			
			local nth = "1"
			if frameArr.count==3 then (
				nth = frameArr[3]
			)
			
			nnlog  ("start:"+start+" end:" + end + " nth:" + nth) ""
			if stCon.fromWhere=="web" then (
				nnlog "Render ... common....From web" ""
				for c in cameras do (
					if (classof c)!=Targetobject and c.name==stCon.camera then (
						render outputwidth:(stCon.imageWidth as Integer) outputheight:(stCon.imageHeight as Integer) camera:c fromframe:(start as time)  toframe:(end as time) nthframe:(nth as time) outputfile:outPath2 quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 --"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
					)
				)
			)else(
				nnlog "Render ... common....From client" ""
				if cam==undefined then (
					render  fromframe:(start as time)  toframe:(end as time) nthframe:(nth as time) quiet:true outputfile:outPath2  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3--"E:/inputData/53/TEST/tex/scene/TT_2011.max"
				)else(
					render  camera:cam fromframe:(start as time)  toframe:(end as time) nthframe:(nth as time) quiet:true outputfile:outPath2  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3--"E:/inputData/53/TEST/tex/scene/TT_2011.max"
				)
			)
			
			
		)else(
			nnlog "Render ... common...." ""
			local frameArr = filterString stCon.mframe "_"--frame_left_top_right_bottom_block_width_height
			
			--local OOpath = stCon.outPath 			
			--local myoutpath = (OOpath+bname+"_"+ext)
			--nnlog   "start  render ..."  myoutpath 
			
			--render frame:(frameArr[1] as time) renderType:#regionCrop   region:#(frameArr[2] as number,frameArr[3] as number,frameArr[4] as number,frameArr[5] as number) outputfile:myoutpath quiet:true   missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3--"E:/inputData/53/TEST/tex/scene/TT_2011.max"	
			local elemArr=#()
			
			if stCon.fromWhere=="web" then (
				nnlog "Render ... common....From web" ""
				for c in cameras do (
					if (classof c)!=Targetobject and c.name==stCon.camera then (
						if stCon.outGamma==undefined then (
							render outputwidth:(stCon.imageWidth as Integer) outputheight:(stCon.imageHeight as Integer) camera:c frame:(frameArr[1] as time) outputfile:outPath2 quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3
						)else(
							local mybm=render outputwidth:(stCon.imageWidth as Integer) outputheight:(stCon.imageHeight as Integer) camera:c frame:(frameArr[1] as time) outputfile:outPath2 quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3
							mybm.filename=outPath2
							mybm.gamma=(stCon.outGamma as Float)
							save mybm
							close mybm							
						)						
					)
				)
			)else(
				nnlog "Render ... common....From client" ""
				if cam==undefined then (
					if stCon.outGamma==undefined then (
						render  frame:(frameArr[1] as time) outputfile:outPath2 quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 
					)else(
						local mybm=render  frame:(frameArr[1] as time) quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 
						mybm.filename=outPath2
						mybm.gamma=(stCon.outGamma as Float)
						save mybm
						close mybm
					)
					--local mybm=render  frame:(frameArr[1] as time) outputfile:outPath2 quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3
					
				)else(
					if stCon.outGamma==undefined then (
						render  camera:cam frame:(frameArr[1] as time) outputfile:outPath2 quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 --"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
					)else(
						local mybm=render  camera:cam frame:(frameArr[1] as time)  quiet:true renderElements:true renderElementBitmaps:&elemArr  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3 --"E:/inputData/53/TEST/tex/scene/TT_2011.max"			
						mybm.filename=outPath2
						mybm.gamma=(stCon.outGamma as Float)
						save mybm
						close mybm
					)
					
				)
			)
			
			--imgBitmap.filename=myoutpath--outputfile:myoutpath
			--save imgBitmap frame:(stCon.mframe as integer) 
			--convertExr imgBitmap
			if elemArr != undefined then (
				for elem in elemArr do (					
					save elem				
					convertExr elem
				)
			)
			--render frame:(stCon.mframe as time)   quiet:true outputfile:outPath2  missingExtFilesAction:#(#logmsg)  missingExtFilesList:&logarr1 missingUVWAction:#(#logmsg) missingUVWList:&logarr2 unsupportedRenderEffectAction:#(#logmsg)  unsupportedRenderEffectList:&logarr3--"E:/inputData/53/TEST/tex/scene/TT_2011.max"
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
		nnlog "jobName" stCon.jobName
		
		commonFN()
		local ll = loadMaxFN()
		if ll then (
			try(
				nnlog   "----------------load max file successed------------- " ""
				textureFN()
				elementFN()
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
				realflowFN()
				renderSceneDialog.update()
				renderSceneDialog.commit()
				renderFN()
				
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

fn rwRender userId taskId sonId mframe kg jobName maxFile = (
	
	--local st = STConst()
	--st.init userId taskId sonId frame maxFile
	local r = RBRender()
	r.init  userId taskId sonId mframe kg jobName maxFile 
	--r.stCon = st
	--r.init userId taskId frame maxFile
	r.myRender()
)


--script
--rwRender "53" "100041" "0" "7_80_120_200_350_3_150_150" "1" "C:/renderwork/100041/region2012_elem.max" --split render image



--cmd
--"C:\Program Files\Autodesk\3ds Max 2011\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/render.ms\";rwRender \"53\" \"100053\" \"0\" \"5\" \"C:/renderwork/100053/submit_vr.max\" "


--enf
--C:\RbNodeService\TryOnce.exe "C:\Program Files\Autodesk\3ds Max 2011\3dsmax.exe" -silent  -mxs "filein \\\"c:/script/max/render.ms\\\";rwRender \\\"53\\\" \\\"100053\\\" \\\"5\\\" \\\"C:/renderwork/100053/submit_vr.max\\\""
