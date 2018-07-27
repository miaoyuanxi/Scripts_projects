
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


struct STRead(
	
	
	function getRealflowPath oTxtFile= ( 
		local rfmesh=for rr in objects where classof rr == MeshLoader collect rr

	  
		format "---realflow_mesh_path---\n" to:oTxtFile 
		
		for r in 1 to rfmesh.count where rfmesh[r]!=undefined do
		(
			print rfmesh[r].path
			print rfmesh[r].name
			print rfmesh[r].prefix 
			 
			--showproperties  rfmesh[r]
			format "rfmesh=%|%|%\n" rfmesh[r].name rfmesh[r].path rfmesh[r].prefix to:oTxtFile
			
		)
		
		format "\n" to:oTxtFile 

	),

	function getCamera oTxtFile= (  
	  format "---Cameras---\n" to:oTxtFile 
	  for i=1 to Cameras.count do 
	  ( 
	  cam=Cameras[i].name
	  format "%\n" cam to:oTxtFile 
	  ) 
	  format "\n" to:oTxtFile 
	),

	function getImageSample oTxtFile=(
		local imageSamplerType = renderers.current.imageSampler_type as string
		local filterOn = renderers.current.filter_on as string
		local filterKernel =renderers.current.filter_kernel  as string
		local filterSize = renderers.current.filter_size as string
		local fixSubdivs = renderers.current.fixedRate_subdivs as string
		local dminRate = renderers.current.twoLevel_baseSubdivs as string
		local dmaxRate = renderers.current.twoLevel_fineSubdivs as string
		local aminRate = renderers.current.adaptiveSubdivision_minRate as string
		local amaxRate = renderers.current.adaptiveSubdivision_maxRate as string
		
		
		format "---Vray Images Sample---\n" to:oTxtFile 	
		format "imageSamplerType=%\n" imageSamplerType to:oTxtfile 
		format "filterOn=%\n" filterOn to:oTxtfile 
		format "filterKernel=%\n" filterKernel to:oTxtfile 
		format "filterSize=%\n" filterSize to:oTxtfile 
		format "fixSubdivs=%\n" fixSubdivs to:oTxtfile 
		format "dminRate=%\n" dminRate to:oTxtfile 
		format "dmaxRate=%\n" dmaxRate to:oTxtfile 
		format "aminRate=%\n" aminRate to:oTxtfile 
		format "amaxRate=%\n" amaxRate to:oTxtfile 
		
	),

	function getElem oTxtFile=(
		re = maxOps.GetCurRenderElementMgr() 
		theManager = maxOps.GetRenderElementMgr #Production
		
		format "---------renderElement-----\n" to:oTxtfile
		eact = re.GetElementsActive()
		
		format "ElementsActive=%\n" eact to:oTxtfile
		for n = 0 to (theManager.numrenderelements()- 1) do
		
		(
		
			el = re.getrenderelement n
			local ename = el.elementname
			local eactive = el.enabled 

			format "ename=%._|_.%\n" ename eactive to:oTxtfile

		)

	),


	 fn getVrinfo oTxtFile= ( 
	 
		 local myrender = renderers.current
		local irrPath=myrender.adv_irradmap_loadFileName as string 
		local lchPath=myrender.lightcache_loadFileName as string 
		local mode1=myrender.adv_irradmap_mode as string 
		local mode2=myrender.lightcache_mode as string 
		local gion=myrender.gi_on as string 
		local pgiengine=myrender.gi_primary_type 
		local sgiengine=myrender.gi_secondary_type as string 
		local giprimulti=myrender.gi_primary_multiplier as string 
		local gisecmulti=myrender.gi_secondary_multiplier as string 
		
		
		local subdivs=""
			if hasProperty myrender "dmcgi_subdivs" then (
				subdivs=myrender.dmcgi_subdivs as string
			)
			if hasProperty myrender "qmcgi_subdivs" then (
				subdivs=myrender.qmcgi_subdivs as string
			)
			local secbounce=""
			if hasProperty myrender "dmcgi_depth" then (
				secbounce=myrender.dmcgi_depth as string
			)
			if hasProperty myrender "qmcgi_depth" then (
				secbounce=myrender.qmcgi_depth as string
			)


		local lightsub = myrender.lightcache_subdivs as string
		
		
			local enableFrameBuffer = myrender.output_on
			local renderToRwFile = myrender.output_saveRawFile
			local rawImgName = myrender.output_rawFileName
			local splitBuffer = myrender.output_splitgbuffer
			local splitFileName = myrender.output_splitfilename
	  
		format "---Photon path---\n" to:oTxtFile 
		local photonPath="IrrPath="+irrPath+"\nLchPath="+lchPath+"\n" 
		format "%" photonPath to:oTxtFile 
		format "IrrMode=%\nLchMode=%\n" mode1 mode2 to:oTxtFile 
		format "gion=%\n" gion to:oTxtfile 
		format "pgiengine=%\n" pgiengine to:oTxtfile 
		format "sgiengine=%\n" sgiengine to:oTxtfile 
		format "giprimulti=%\n" giprimulti to:oTxtfile 
		format "gisecmulti=%\n" gisecmulti to:oTxtfile 
		format "subdivs=%\n" subdivs to:oTxtfile 
		format "secbounce=%\n" secbounce to:oTxtfile 
		format "lightsub=%\n" lightsub to:oTxtfile
		
		format "enableFrameBuffer=%\n" enableFrameBuffer to:oTxtfile
		format "renderToRwFile=%\n" renderToRwFile to:oTxtfile
		format "rawImgName=%\n" rawImgName  to:oTxtfile
		format "splitBuffer=%\n" splitBuffer to:oTxtfile
		format "splitFileName=%\n" splitFileName to:oTxtfile
		format "\n" to:oTxtFile 
	  ),



	  
	  fn getSubStr str st ed= ( 
		if st<1 or ed>str.count then 
		( 
			return false 
		) 
		local temp="" 
		for i=st to ed do 
		( 
			temp=temp+str[i] 
		) 
		return temp 
	  ),
	  
	  
	------------gettexture----------------- 
	fn getTxtfromAsset = (
		local ar = #()
		local tmpAr = #()
		atsops.Refresh()
		atsops.getfiles &tmpAr
		
		for a in tmpAr do (
			if a!=undefined and  ATSOps.IsInputFile a then (
				append ar a
			)			
		)
		ar	
	),

	Fn EnumFileFn FileName TarArray = (
		Append TarArray FileName
	),
	Fn FileExist FileName = (
		if (Getfiles FileName).Count > 0 then true else false
	),
	
	Fn ArrayConvertToUnique FnpArray = (
		local OutArray = #()
		for Fa in FnpArray do
		(
			if Fa !=undefined then (
				local fname = (filenameFromPath ((Fa as StringStream) as String))
				local fo = (FindItem OutArray fname)		
				if fo ==0 do Append OutArray fname
			)
		)
		OutArray
	),
	

	fn getTexture txtFile = (
		
		format "---------Texture--------- \n"  to:txtFile
		RebderBitmapA = #()	
		EnumerateFiles EnumFileFn RebderBitmapA 
		
		local assetArr = getTxtfromAsset()
		join RebderBitmapA assetArr

		RebderBitmapA = ArrayConvertToUnique RebderBitmapA
		
		for Fi in RebderBitmapA do
		(
			
			if Fi != maxfilename then (
				format  "find=%\n"  Fi  to:txtFile
			)
		)
	),


	fn getFilesRecursive root pattern = ( 
		dir_array = GetDirectories (root+"*") 
		for d in dir_array do 
		join dir_array (GetDirectories (d+"*")) 
		my_files = #() 
		join my_files (getFiles (root + pattern)) 
		for f in dir_array do 
		join my_files (getFiles (f + pattern))
		my_files  
	), 
	  
	fn getFinalRenderInfo oTxtFile= (
		local enable = renderers.current.giEnable as string 
		local showPrepass = renderers.current.giShowPrepass as string 
		  local showSamples = renderers.current.giShowSamples as string 
		  local sampleColor1 = renderers.current.giSampleColor1 as string 
		  local sampleColor2 = renderers.current.giSampleColor2 as string 	
		  local solutionMode = renderers.current.giSolutionMode as string 	  
		  local solutionReuse = renderers.current.giSolutionReuse as string 
		local solutionLock = renderers.current.giSolutionLock as string 
		  local prepassOnly = renderers.current.giPrepassOnly as string 
		  local solutionAnimationMode = renderers.current.giSolutionAnimationMode as string 
		  local updateSolution = renderers.current.giUpdateSolution as string 	  
		  local solutionInterpolationFrames = renderers.current.giSolutionInterpolationFrames as string 
		  local solutionMultipleFiles = renderers.current.giSolutionMultipleFiles as string 
		  local solutionAnimationPass = renderers.current.giSolutionAnimationPass as string 	  
		  local useSolutionFile = renderers.current.giUseSolutionFile as string 
		  local solutionFile = renderers.current.giSolutionFile as string 
		  format "---FinalRender info---\n" to:oTxtFile 
		  format "finalrender.enable=%\n" enable to:oTxtfile
		  format "finalrender.showPrepass=%\n"  showPrepass to:oTxtfile
		  format "finalrender.showSamples=%\n" showSamples to:oTxtfile
		  format "finalrender.sampleColor1=%\n" sampleColor1 to:oTxtfile
		  format "finalrender.sampleColor2=%\n" sampleColor2 to:oTxtfile
		  format "finalrender.solutionMode=%\n" solutionMode to:oTxtfile
		  format "finalrender.solutionReuse=%\n" solutionReuse to:oTxtfile
		  format "finalrender.solutionLock=%\n" solutionLock to:oTxtfile
		  format "finalrender.prepassOnly=%\n" prepassOnly to:oTxtfile
		  format "finalrender.solutionAnimationMode=%\n" solutionAnimationMode to:oTxtfile
		  format "finalrender.updateSolution=%\n" updateSolution to:oTxtfile
		  format "finalrender.solutionInterpolationFrames=%\n" solutionInterpolationFrames to:oTxtfile
		  format "finalrender.solutionMultipleFiles=%\n" solutionMultipleFiles to:oTxtfile
		  format "finalrender.solutionAnimationPass=%\n" solutionAnimationPass to:oTxtfile
		  format "finalrender.useSolutionFile=%\n" useSolutionFile to:oTxtfile
		  format "finalrender.solutionFile=%\n" solutionFile to:oTxtfile
		
		  format "\n" to:oTxtFile 
	  ),


	function getmaxv = (
		local maxv = (maxVersion())[1]/1000
		maxv
	),

	function getGamma oTxtFile= (
		local maxv = getmaxv()
		local gammaMode = "gamma0"
		
		if maxv >9 then (
		 gammaMode = IDisplayGamma.colorCorrectionMode as string 	
		)
		
		
		format "\n---other info---\n"  to:oTxtFile
		format "gammaMode=%\n" gammaMode to:oTxtFile
		format "fileInGamma=%\n" fileInGamma to:oTxtFile
		format "fileOutGamma=%\n" fileOutGamma to:oTxtFile
	),

	fn read taskid pMaxFile  pTxtFile =(
		
		local debugTxt = "C:/log/analysis/"+taskid+"_debug.txt" 
		
		local objUtil = STUtil()		
		objUtil.debugLog=debugTxt
		objUtil.count=1
		objUtil.oolog "开始分析MAX文件-----------------"

		try(
			setVRaySilentMode() 
		)catch()
		try( 
		maxFile=pMaxFile   
		useFileUnits=true 
		quiet=true 
		maxPath=getFileNamePath maxFile 
		
		t1=timeStamp()
		objUtil.oolog  "---------开始加载MAX文件----" 
		loadMaxFile maxFile useFileUnits:true quiet:true 
		t2=timeStamp()
		t=t2-t1
		objUtil.oolog "----------加载MAX文件完毕------------"
		
		 


		
		allMapFiles=#() 
		oTxtFile=createFile  pTxtFile
		


		myrender=(classof renderers.current) as string 
		 format "myrender=%\n" myrender to:oTxtfile 
		
		propsName=fileProperties.getPropertyValue #contents 1  
		for i= 1 to fileProperties.getNumProperties #contents do
		(
			ppName=fileProperties.getPropertyName  #contents i
			print ppName
			if ppName == "Headers" then
			(
				propsName=fileProperties.getPropertyValue #contents i 
				break
			)
		)
		t3=timeStamp()
		t=t3-t2
		objUtil.oolog "----------获取MAX文件属性------------"
		if propsName==undefined then
		(
			continue 
		)

		for i=1 to propsName.count do  
		(  

		  if i==4 then 
		 ( 	
				t1 = timeStamp()
			objUtil.oolog "-----------获取贴图信息开始-----------"
				getTexture oTxtFile 
				t2 = timeStamp()
				t=t2-t1
				objUtil.oolog "-----------获取贴图信息完毕-----------"
				continue 
		  ) 
		  if i==5 then 
		 ( 
			t1 = timeStamp()
			objUtil.oolog "-----------获取相机信息开始-----------"
				getCamera oTxtFile 
				
				t2 = timeStamp()
				t=t2-t1
				objUtil.oolog "-----------获取相机信息完毕-----------"
			continue 
		 )
		  
		  if i==6 then 
		 ( 
			continue 
		 ) 
		  
		  local trace 
		  curProp=propsName[i] 
		  
		  t1 = timeStamp()
		  objUtil.oolog "-----------获取其它信息开始-----"
		  
		  curItems=fileProperties.getItems curProp 
		  trace="---"+curProp+"---\n" 
		  for j=1 to curItems.count do 
		  ( 
			trace=trace+curItems[j]+"\n" 
		  ) 
		  trace=trace+"\n" 
		  format "%" trace to:oTxtFile
		  
		  t2 = timeStamp()
		  t=t2-t1
			objUtil.oolog "-----------获取其它信息完毕----"
				
		  if i==8 then
		  (
			  
					t1 = timeStamp()
					objUtil.oolog "-----------获取高级信息开始-----------"
					
						if rendColorCheck then
							format ("rendColorCheck=1\n")  to:oTxtFile
						else			
							format ("rendColorCheck=0\n")  to:oTxtFile
						
						if rendAtmosphere then
							format ("rendAtmosphere=1\n")  to:oTxtFile
						else			
							format ("rendAtmosphere=0\n")  to:oTxtFile
						
						if rendSuperBlack then
							format ("rendSuperBlack=1\n")  to:oTxtFile
						else			
							format ("rendSuperBlack=0\n")  to:oTxtFile
						
						if rendHidden then
							format ("rendHidden=1\n")  to:oTxtFile
						else			
							format ("rendHidden=0\n")  to:oTxtFile
						
						if rendForce2Side then
							format ("rendForce2Side=1\n")  to:oTxtFile
						else			
							format ("rendForce2Side=0\n")  to:oTxtFile
						
						if renderEffects then
							format ("renderEffects=1\n")  to:oTxtFile
						else			
							format ("renderEffects=0\n")  to:oTxtFile
						
						if renderDisplacements then
							format ("renderDisplacements=1\n")  to:oTxtFile
						else			
							format ("renderDisplacements=0\n")  to:oTxtFile
						
						if rendFieldRender then
							format ("rendFieldRender=1\n")  to:oTxtFile
						else			
							format ("rendFieldRender=0\n")  to:oTxtFile
							
						t2 = timeStamp()
						t=t2-t1
						objUtil.oolog "-----------获取高级信息完毕-----------"
		  ) 
		)  
		  sVR=(classof renderers.current) as string 
		  isVR=(getSubStr sVR 1 5)=="V_Ray" 
		  if isVR then 
		  ( 
					t1 = timeStamp()
					objUtil.oolog "-----------获取VRAY信息开始-----------"
						
						getVrinfo oTxtFile 
						getImageSample oTxtFile 
						
						t2 = timeStamp()
						t=t2-t1
						objUtil.oolog "-----------获取VRAY信息完毕-----------"
		  ) 
		  isFR = (getSubStr sVR 1 11)=="finalRender" 
		  if isFR then
		  (
		  
					t1 = timeStamp()
					objUtil.oolog "-----------获取FINAL RENDER信息开始-----------"
					
					getFinalRenderInfo oTxtFile
					
					t2 = timeStamp()
						t=t2-t1
						objUtil.oolog "-----------获取FINAL RENDER信息完毕-----------"
		  )
		  
		t1 = timeStamp()
		objUtil.oolog "-----------获取通道信息开始-----------"
		getElem oTxtFile 	
		t2 = timeStamp()
		t=t2-t1
		objUtil.oolog "-----------获取通道信息完毕-----------"
		
		objUtil.oolog "-----------获取Realflow信息开始-----------"
		getRealflowPath oTxtFile
		
		t3 = timeStamp()
		t=t3-t2
		objUtil.oolog "-----------获取Realflow信息完毕-----------"

		getGamma oTxtFile

		DOSCommand ("echo  renderbusreadokloo") 
		objUtil.oolog "-----------分析完毕-----------"
		close oTxtFile 
		
		
		local maxv = getmaxv()	
		if maxv >9 then (
			DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string)) 
		)
		
		resetMaxFile  #noPrompt 
		quitMax #noPrompt  
	  
	   )catch ( 
			
			objUtil.oolog  ( getCurrentException() as string ) 
			
			if oTxtFile!=undefined then (
				close oTxtFile 
			)
			
			
			local maxv = getmaxv()	
			if maxv >9 then (
			 DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string)) 
			)
			resetMaxFile  #noPrompt 
			quitMax #noPrompt
			
	  
		) 
		
		
	)

)



struct STMentalRayEdit (
	objUtil,
		
	function emptysc=(
		local RDwasOpen = renderSceneDialog.isOpen()
		if renderSceneDialog.isOpen() then renderSceneDialog.close()
		preRendScript = ""
		usePreRendScript = false
		if RDwasOpen then renderSceneDialog.open()
	),

	function emsc=(
		local RDwasOpen = renderSceneDialog.isOpen()
		if renderSceneDialog.isOpen() then renderSceneDialog.close()
		rendFileNumberBase =0
		postRendScript = ""
		usePostRendScript = false
		if RDwasOpen then renderSceneDialog.open()
	),


	function setcam =(  
		cnt=0
	  for i=1 to Cameras.count do 
	  ( 
		local prefix="0" 
		local isCam=(classof Cameras[i])==Targetcamera or \ 
		(classof Cameras[i])==FreeCamera or \
		  (classof Cameras[i])==VRayPhysicalCamera or \ 
		   (classof Cameras[i])==VRayDomeCamera 
		if cnt>9 then 
		( 
			prefix="" 
		) 
		if isCam then 
		( 
			Cameras[i].name="Cam"+prefix+(cnt as string)
			cnt=cnt+1 
		) 
	  ) 
	  
	),

	fn getFilesRecursive root pattern =
	   ( 
		dir_array = GetDirectories (root+"*") 
		for d in dir_array do 
		join dir_array (GetDirectories (d+"*")) 
		my_files = #() 
		join my_files (getFiles (root + pattern)) 
		for f in dir_array do 
		join my_files (getFiles (f + pattern))
		my_files  
	), 
	  
	fn clePhoto = (
		renderers.current.UseFinalGatherFile=false
		renderers.current.PhotonMapUseFile=false
		renderers.current.PhotonMapFilename=""
		renderers.current.FinalGatherFilename="" 
	),

	fn setCommonInfo = (
		rendTimeType=2	
	
	),
  -----------set render elements------------------

	fn rdElement elemlist outpath = (		
	
	
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
				re.SetRenderElementFilename n (outpath + myel + elext )
				
			)	
			
		)

	
	),
	
	fn elemDisable = (
		re = maxOps.GetCurRenderElementMgr() 
		re.SetElementsActive(false)
	),


	
	fn cleElem =(
		re = maxOps.GetCurRenderElementMgr() 
		re.removeallrenderelements() 
	)
	

)


struct STEdit (
	
	objUtil,
	
	function emptysc=(
	--local RDwasOpen = renderSceneDialog.isOpen()
	--if renderSceneDialog.isOpen() then renderSceneDialog.close()
	--preRendScript = ""
	--usePreRendScript = false
	--if RDwasOpen then renderSceneDialog.open()


	),

	function emsc=(
		local RDwasOpen = renderSceneDialog.isOpen()
		if renderSceneDialog.isOpen() then renderSceneDialog.close()
		postRendScript = ""
		--globalVars.set #rendFileNumberBase 0
		rendFileNumberBase =0
		usePostRendScript = false
		if RDwasOpen then renderSceneDialog.open()

	),



	function setcam =(  
		cnt=0
		for i=1 to Cameras.count do( 
			try(
				local prefix="0" 
				local isCam=(classof Cameras[i])==Targetcamera or \ 
				(classof Cameras[i])==FreeCamera or \
				  (classof Cameras[i])==VRayPhysicalCamera or \ 
				   (classof Cameras[i])==VRayDomeCamera or \
				(classof Cameras[i])==XIdMary or (classof Cameras[i]) ==stereocam
				if cnt>9 then 
				( 
					prefix="" 
				) 
				if isCam then 
				( 
					Cameras[i].name="Cam"+prefix+(cnt as string)
					cnt=cnt+1 
				) 
			)catch(
				objUtil.oolog (getCurrentException() as string)
			)
		) 
		  
	),


	fn getFilesRecursive root pattern =( 
		dir_array = GetDirectories (root+"*") 
		for d in dir_array do 
		join dir_array (GetDirectories (d+"*")) 
		my_files = #() 
		join my_files (getFiles (root + pattern)) 
		for f in dir_array do 
		join my_files (getFiles (f + pattern))
		my_files  
	),
  
  
  -----------set render elements------------------
	fn rdElement elemlist outpath = (		
	
	
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
				re.SetRenderElementFilename n (outpath + myel + elext )
				
			)	
			
		)

	
	),
	
	fn elemDisable = (
		re = maxOps.GetCurRenderElementMgr() 
		re.SetElementsActive(false)
	),
	
	fn cleElem =(
		re = maxOps.GetCurRenderElementMgr() 
		re.removeallrenderelements() 
	),
	
	fn setCommonInfo = (
		rendTimeType=2	
		rendUseActiveView=true
	
	),
	
	fn setVrayInfo outPath outName = (
		
		local myrender=renderers.current
		
		----------------dynamic memory limit ---------------

		try(
			local mmInfo=sysinfo.getSystemMemoryInfo()
			local mem = ((mmInfo[2]/1024/1024)*0.9)			
			myrender.system_raycaster_memLimit=mem
		)catch()




		myrender.options_dontRenderImage=false
		
		-------------VFB------------
		local enableFrameBuffer = myrender.output_on
		
		if(enableFrameBuffer==true) then (
			local renderToRwFile = myrender.output_saveRawFile
			local rawImgName = myrender.output_rawFileName
			local splitBuffer = myrender.output_splitgbuffer
			
			if(renderToRwFile==true ) then (
				myrender.output_rawFileName = outPath+outName +"VFB.vrimg"
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
				myrender.output_splitfilename=outPath+outName + bufferExt
				
			)
			
			
		
		)
		

		
	)
	
)


struct STName(
	--update:2011-01-15
--修正VRayDirt问题
--修正Unwarp UVW 背景贴图BUG
--修正Multiscatter问题
--已经修正相同路径比较的问题
--已经修正光域网bug

	objUtil,

	fn fl_convertNumStr T N =(	--T,数字位数; N ,要转换的数字
		Nstr=N as string ;resultStr=""
		ncnt=Nstr.count
		if T>ncnt then 
		(	resultStr=""
			for i in 1 to (T-ncnt) do resultStr+="0"
			resultStr+=Nstr
		)
		else if T==ncnt then resultStr=Nstr
		else
		(	resultStr=Nstr
		)
		resultStr="GaoBin"+resultStr
		resultStr
	),

	

	fn fl_renameFilesOnly newPath Num:6 =(	--更新路径,newPath为新路径,Num为序列数字的位数，默认为6
		
		--与Vray相关的路径
		--更改VRayMesh路径
		objUtil.oolog "开始更新中文名"
		
		objUtil.oolog    "更新VRay代理----"
		vmeshNum=1
		vrmesh=for a in geometry where classof a == VrayProxy collect a
		for a in vrmesh where a != undefined and a.filename!=undefined do
		(
			oldPtemp=a.filename
			oldP=newPath+"\\"+filenameFromPath oldPtemp
			newP=newPath+"\\VrayMesh"+fl_convertNumStr Num vmeshNum + getFilenameType oldP
			if copyFile oldP newP then
			(
				meshname="VrayMesh"+fl_convertNumStr Num vmeshNum + getFilenameType oldPtemp
				a.filename=getFilenamePath oldPtemp + ""+meshname
				InstanceMgr.GetInstances a &vv
				for vr in vv do if (idx=finditem vrmesh vr) != 0 then vrmesh[idx]=undefined
				--for vr in vrmesh where vr!=undefined and getFilenameFile vr.filename==getFilenameFile oldPtemp do 
				for vr in vrmesh where vr!=undefined and vr.filename!=undefined  and filenameFromPath vr.filename==filenameFromPath oldPtemp do 
				(	--同名不同路径
				--	print vr
					temp01=vr.filename
					vr.filename=getFilenamePath temp01+""+meshname
					InstanceMgr.GetInstances vr &vv
					for vr1 in vv do if (idx=finditem vrmesh vr1) != 0 then vrmesh[idx]=undefined
				)
				
				vmeshNum+=1
			)else (
				objUtil.oolog   ("error重名出错："+oldPtemp)
			)
		)
		objUtil.oolog    "VRay代理更新完毕！"
	--	format "%  %\n" localtime "VRay代理更新完毕！"
		--更新光域网
		objUtil.oolog   "更新光域网:"
	--	format "%  %\n" localtime "正在更新光域网..."
		iesNum=1
		iesFiles=for l in lights where matchPattern (classof l as string) pattern:"*_*" and \
		hasProperty l "webFile"and l.webfile!=undefined collect l
		iesPath=for i=1 to iesFiles.count collect iesFiles[i].webFile--IES路径
		iesNewPath=#()--更新后的路径，后来还要用于VRayIES
	--	format "%\n%\n" iesFiles iesPath
		if iesFiles.count!=0 then
		(
			iesNewPath[iesPath.count]=undefined
			for ii in 1 to iesFiles.count where iesFiles[ii] != undefined do (
			oldPtemp=iesFiles[ii].webFile
			
			oldP=newPath+"\\"+filenameFromPath oldPtemp
			newP=newPath+"\\IES"+fl_convertNumStr Num iesNum + getFilenameType oldP
			newP01=getFilenamePath oldPtemp+"\\IES"+fl_convertNumStr Num iesNum + getFilenameType oldPtemp
			sameIes=#()--重复路径
			for i in 1 to iesPath.count do 
				if iesPath[i]==oldPtemp then append sameIes i
			if sameIes.count==1 then (
				if copyFile oldP newP then
				(
					tempValue=iesFiles[ii].intensity
					iesFiles[ii].webFile=newP01
					iesFiles[ii].intensity=tempValue
					iesNewPath[ii]=newP
					
					iesNum+=1
				)else(
					objUtil.oolog ("error重名出错："+oldP)
				)
			)--end if
			else if sameIes.count>1 then	(
				if copyFile oldP newP then
				(
					for s in sameIes do
					(	tempValue=iesFiles[s].intensity
						iesFiles[s].webFile=newP01
						iesFiles[s].intensity=tempValue
						iesNewPath[s]=newP
						iesFiles[s]=undefined
					)
					
					iesNum+=1
				)else (
					objUtil.oolog  ("error重名出错："+oldPtemp)
				)
			)
			else ()
			)--end for
		)
		objUtil.oolog    "光域网更新完毕！"
	--	format "%  %\n" localtime "光域网更新完毕！"
		--更新VRayIES
		objUtil.oolog   "更新VRayIES:"
	--	format "%  %\n" localtime "正在更新VRayIES..."
		vriesNum=1
		vries=for a in lights where classof a == VRayIES and a.ies_file!=undefined and a.ies_file!="" collect a
		viesFiles=for f in 1 to vries.count where vries[f]!=undefined and vries[f].ies_file!=undefined collect vries[f].ies_file
		for a in vries where a != undefined do
		(
			tempValue=a.power
			--是否有VRayIES和IES共用光域网文件的情况
			idx=finditem iesPath a.ies_file--找一下是否和IES相同
			if idx!=0 and iesNewPath[idx]!=undefined then	--如果有相同的，则调用以前路径
			(
				a.ies_file=iesNewPath[idx]
				a.power=tempValue
			)
			else (--如果不相同，就更新自己的路径
			oldPtemp=a.ies_file
			oldP=newPath+"\\"+filenameFromPath oldPtemp
			newP=newPath+"\\VrayIES"+fl_convertNumStr Num vriesNum + getFilenameType oldP
			newP01=getFilenamePath oldPtemp+"\\VrayIES"+fl_convertNumStr Num vriesNum + getFilenameType oldPtemp	
			sameIes=#()--重复路径
			for v1 in 1 to viesFiles.count do
				if viesFiles[v1] == oldPtemp then append sameIes v1
			if sameIes.count == 1 then (
				if copyFile oldP newP then
				(
					a.ies_file=newP01
					a.power=tempValue
					
					vriesNum+=1
				)else (
					objUtil.oolog    ("error重名出错："+oldPtemp)   
				)
			)--end if
			else if sameIes.count > 1 then (
				if copyFile oldP newP then
				(
					for b in sameIes do
					(	tempb=vries[b].power
						vries[b].ies_file=newP01
						vries[b].power=tempb
						vries[b]=undefined
					)
					
					vriesNum+=1
				)
				else (
					objUtil.oolog    ("error重名出错："+oldPtemp)   
					
				)
				)--end else if
			else ()
			)--end else
		)--end for
		objUtil.oolog  "VRayIES更新完毕！" 
	--	format "%  %\n" localtime "VRayIES更新完毕！"
			--更新VRayHDRI
		objUtil.oolog  "更新VRayHDRI:"
	--	format "%  %\n" localtime "正在更新VRayHDRI..."
		mapNum=1
		allMaps=try getClassInstances VRayHDRI catch undefined
		if allMaps!=undefined then (
		oldFiles=for f in 1 to allmaps.count collect allmaps[f].HDRIMapName--老路径
		for m in 1 to allMaps.count where allMaps[m]!=undefined  and allMaps[m].HDRIMapName !=undefined  do
		(
			oldPtemp=allMaps[m].HDRIMapName
			oldP=newPath+"\\"+filenameFromPath oldPtemp
			newP=newPath+"\\VrayHDRI"+fl_convertNumStr Num mapNum + getFilenameType oldP
			newP01=getFilenamePath oldPtemp+"\\VrayHDRI"+fl_convertNumStr Num mapNum + getFilenameType oldPtemp
			idxall=#()--收集路径相同的VRayHDRI
			for j in 1 to allMaps.count do
			(	--if oldFiles[j]==oldPtemp then append idxall j
				if oldFiles[j]!=undefined and ( (filenameFromPath oldFiles[j]) as name) == ((filenameFromPath oldPtemp) as name) then append idxall j
			)
			if idxall.count==1 then (-- 如果路径唯一,就直接更新
				if copyFile oldP newP then
				(
					allMaps[m].HDRIMapName=newP01
					
					mapNum+=1
				)else (					
					objUtil.oolog    ("error重名出错："+oldP)  
				)
			)
			else if idxall.count>1 then--路径重复的,更新一个,其他的按这个更新
			(
				if copyFile oldP newP then
				(
					for k in idxall do 
					(	allMaps[k].HDRIMapName=newP01
						allMaps[k]=undefined
					)
					
					mapNum+=1
				)else (					
					objUtil.oolog    ("error重名出错："+oldPtemp)  
				)
			)
			else ()
		)--end for
		)--end if
		objUtil.oolog   "VRayHDRI更新完毕！"  
	--	format "%  %\n" localtime "VRayHDRI更新完毕！"
		--更新材质和环境贴图
		objUtil.oolog "更新材质和环境贴图:" 
		objUtil.oolog "正在更新材质和环境贴图..."
		--去掉Unwrap UVW背景贴图 2011.01.07
		for i in geometry where i.modifiers.count>1 do
		(	for j in i.modifiers where classof j == Unwrap_UVW do
			(	j.texMapList.count=1
				j.texMapIDList.count=1
				j.texMapList[1] = Checker ()
				j.texMapIDList[1] = -1
			)
		)
		mapNum=1
		allMaps=getClassInstances bitmapTexture
		--2011.01.15 添加VRayDirt
		if classof VRayDirt == textureMap then
		(
			VDmaps=getClassInstances VRayDirt
			if VDmaps.count!=0 then
			(
				for i in VDmaps do
				(
					map1=i.texmap_radius
					if classof map1 == bitmapTexture then 
						if finditem allMaps map1==0 then append allMaps map1
					map2=i.texmap_occluded_color
					if classof map2 == bitmapTexture then 
						if finditem allMaps map2==0 then append allMaps map2
					map3=i.texmap_unoccluded_color
					if classof map3 == bitmapTexture then 
						if finditem allMaps map3==0 then append allMaps map3
					
				)
			)
		)
		--添加更新MultiScatter
		mulsct=for i in geometry where classof i == MultiScatter collect i
		if mulsct.count!=0 then
		(
			for m in mulsct do
			(
				for b in m.Scatter_Object_Mask where b!=undefined and classof b != Vertex_Color and \
					finditem allMaps b==0 do append allMaps b

				if m.Density_Map!=undefined and classof m.Density_Map != Vertex_Color and finditem allMaps m.Density_Map==0 do --2011.01.07
					append allMaps m.Density_Map

				if m.Color_Texture1!=undefined and classof m.Color_Texture1 != Vertex_Color and finditem allMaps m.Color_Texture1==0 do 
					append allMaps m.Color_Texture1

				if m.Scale_Map!=undefined and classof m.Scale_Map != Vertex_Color and finditem allMaps m.Scale_Map==0 do 
					append allMaps m.Scale_Map

				if m.Rotation_Map!=undefined and classof m.Rotation_Map != Vertex_Color and finditem allMaps m.Rotation_Map==0 do 
					append allMaps m.Rotation_Map

				if m.AniShift_Map!=undefined and classof m.AniShift_Map != Vertex_Color and finditem allMaps m.AniShift_Map==0 do 
					append allMaps m.AniShift_Map
			)
		)
		oldFiles=for f in 1 to allmaps.count where (hasProperty allmaps[f]   "filename") collect allmaps[f].filename--老路径
		iflFiles=#()
	--	s=newscript()--Debug !!!!!!!!!!!!!!!!!!
		for m in 1 to allMaps.count where allMaps[m]!=undefined and (hasProperty allmaps[m]   "filename") and allMaps[m].filename!=undefined do
		(
			oldPtemp=allMaps[m].filename
			oldP=newPath+"\\"+filenameFromPath oldPtemp
			newFilename="Map"+fl_convertNumStr Num mapNum + getFilenameType oldP
			newP=newPath+"\\"+newFilename
			newP01=getFilenamePath oldPtemp+newFilename
			idxall=#()--收集路径相同的bitmaptexture
			for j in 1 to allMaps.count do
			( 
				if oldFiles[j]!=undefined and ( (filenameFromPath oldFiles[j]) as name) == ((filenameFromPath oldPtemp) as name) then append idxall j
			)
		/*	--Debug
			fff=#()
			for j in 1 to allMaps.count do
			(	if oldFiles[j]==oldPtemp then append fff oldPtemp
			)
			format "%\n" fff to:s
		*/	
			if idxall.count==1 then (-- 如果路径唯一,就直接更新
				if copyFile oldP newP then
				(	
					allMaps[m].filename=""
					allMaps[m].filename = newP01
			--		format "YES:%\nYES:%\n" newP01 allMaps[m].filename to:s	--Debug
					
					if getFilenameType oldPtemp==".ifl" then append iflFiles newFilename--收集IFL文件
					allMaps[m]=undefined
					)
				else (
			--		format "NO:%\n%\n" oldP newP to:s --Debug					
					objUtil.oolog    ("error重名出错："+oldP)  
				)
				mapNum+=1
			)
			else if idxall.count>1 then--路径重复的,更新一个,其他的按这个更新
			(
				if copyFile oldP newP then
				(	
					if getFilenameType oldPtemp==".ifl" then append iflFiles newFilename--收集IFL文件
					for k in idxall do 
					(	allMaps[k].filename=""
						allMaps[k].filename=newP01
				--		format "YES:%\nYES:%\n" newP01 allMaps[k].filename to:s --Debug
						allMaps[k]=undefined
					)
					
				)
				else (
				--	format "NO:%\n%\n" oldP newP to:s  --Debug					
					objUtil.oolog    ("error重名出错："+oldPtemp) 
					)
				mapNum+=1
			)
			else ( )
	/**/	)	--end for
	--	format "iflFiles:%\n" iflFiles
		--更新IFL路径
		if iflFiles.count!=0 then 
		(
			for i in 1 to iflFiles.count-1 do 
				for j in i+1 to iflFiles.count do
					if iflFiles[i]==iflFiles[j] then iflFiles[j]=undefined
			iflFiles01=for k in iflFiles where k!=undefined collect k
			for i in 1 to iflFiles01.count do
			(
				fname=newPath+"\\"+iflFiles01[i]
				openf=openFile fname
				files=#()
				while not eof openf do append files (readLine openf)--收集序列帧
				close openf
				newfname=createfile fname
				for j in 1 to files.count do
				(
					oldF=newPath+"\\"+getFilenameFile  files[j]+getFilenameType files[j]
					newName="MapList"+i as string+"_"+fl_convertNumStr Num j + getFilenameType oldF
					newF=newPath+"\\"+newName
					if renamefile oldF newF then (						
						objUtil.oolog  (files[j] +"-->>"+newName)
					)
			--		format "%\n%\n" files[j] oldF 
				)
				close newfname
		--		format "i=%-%\n" i files
			)
		)
		objUtil.oolog  "材质和环境贴图更新完毕！"
	--	format "%  %\n" localtime "材质和环境贴图更新完毕！"

		--更新动作缓存
		fn detectPC obj = (	--检测动作缓存
			idx=0;mods=obj.modifiers
			for i in 1 to mods.count where classof mods[i]==Point_Cache do idx=i
			idx
		)
		objUtil.oolog   "更新动作缓存:"
		pcNum=1
		pcObjs=for oo in objects where validModifier oo Point_Cache and oo.modifiers[detectPC oo]!=undefined collect oo
		pcFiles=for f in 1 to pcObjs.count collect pcObjs[f].modifiers[detectPC pcObjs[f]].filename
		for oo in pcObjs where oo!=undefined and (id=detectPC oo)!=0 do 
		(	
	--		format "id:%  oo:%\n" id oo
			oldPtemp=oo.modifiers[id].filename
			if oldPtemp!=undefined then (
			oldP=newPath+"\\"+filenameFromPath oldPtemp
			newP=newPath+"\\PointCache"+fl_convertNumStr Num pcNum + getFilenameType oldP

			--add by zq
			oldP_mc=(getFilenamePath oldP)+ (getFilenameFile oldP)+".mc"
			newP_mc=(getFilenamePath newP)+ (getFilenameFile newP)+".mc"
			--add end

			newP01=getFilenamePath oldPtemp+"\\PointCache"+fl_convertNumStr Num pcNum + getFilenameType oldPtemp
			pcIdx=#()
			for i in 1 to pcFiles.count where pcFiles[i]==oldPtemp do append pcIdx i 
			if pcIdx.count==1 then (
				--先改路径,再改名
				p_start=oo.modifiers[id].playbackStart
				p_end=oo.modifiers[id].playbackEnd
				oo.modifiers[id].filename = newP01
				oo.modifiers[id].playbackStart=p_start
				oo.modifiers[id].playbackEnd=p_end

				if copyFile oldP newP then
				(
					

					--add by zq
					copyFile oldP_mc newP_mc
					
					--add end

					pcNum+=1
				)
				else (--改不了名,路径要改回去
					p_start=oo.modifiers[id].playbackStart
					p_end=oo.modifiers[id].playbackEnd
					oo.modifiers[id].filename = oldPtemp
					oo.modifiers[id].playbackStart=p_start
					oo.modifiers[id].playbackEnd=p_end				
					objUtil.oolog    ("error重名出错："+oldPtemp) 
					)
				)--end if pcIdx.count==1
			else if pcIdx.count>1 then--先改路径,再改名
			(	for pp in pcIdx do (
					idtemp=detectPC pcObjs[pp]
					p_start=pcObjs[pp].modifiers[idtemp].playbackStart
					p_end=pcObjs[pp].modifiers[idtemp].playbackEnd
					pcObjs[pp].modifiers[idtemp].filename = newP01
					pcObjs[pp].modifiers[idtemp].playbackStart=p_start
					pcObjs[pp].modifiers[idtemp].playbackEnd=p_end
				)
				if copyFile oldP newP then
				(
					

					--add by zq
					copyFile oldP_mc newP_mc
					
					--add end

					pcNum+=1
				)else (--改不了名,路径要改回去
					for pp in pcIdx do (
						idtemp=detectPC pcObjs[pp]
						p_start=pcObjs[pp].modifiers[idtemp].playbackStart
						p_end=pcObjs[pp].modifiers[idtemp].playbackEnd
						pcObjs[pp].modifiers[idtemp].filename = oldPtemp
						pcObjs[pp].modifiers[idtemp].playbackStart=p_start
						pcObjs[pp].modifiers[idtemp].playbackEnd=p_end
					)
					
					objUtil.oolog    ("error重名出错："+oldPtemp) 
				)
				
			)else ()--end if pcIdx.count>1 
				
				)--end if oldP!=undefined 
		)
		objUtil.oolog   "动作缓存更新完毕！"

		objUtil.oolog "所有路径更新完毕"
		--关闭文本
		
		objUtil.oolog   "所有路径更新完毕" 
	)

	
)


struct STPath (
	--update:2011-01-15
--修正VRayDirt问题
--修正Multiscatter问题
--for bug filenameFromPath

	objUtil,
	fn fl_updatePaths2 newPath =(	--更新路径,newPath为新路径
			--与Vray相关的路径
			--更改VRayMesh路径
			objUtil.oolog   "开始更新路径..." 
			
			vrmesh=for a in geometry where classof a == VrayProxy collect a
			for a in vrmesh where a != undefined and a.filename!=undefined do(
				
				oldPtemp=a.filename				
				oldP=newPath+"\\"+getFilenameFile oldPtemp+getFilenameType oldPtemp
				a.filename=oldP				
				objUtil.oolog (oldPtemp +"-->>"+oldP)
				InstanceMgr.GetInstances a &vv
				for vr in vv do if (idx=finditem vrmesh vr) != 0 then vrmesh[idx]=undefined
			)
			--更新光域网
			iesFiles=for l in lights where matchPattern (classof l as string) pattern:"*_*" and \
			hasProperty l "webFile" collect l
			if iesFiles.count!=0 then(
				for ii in 1 to iesFiles.count where iesFiles[ii] != undefined and iesFiles[ii].webFile != undefined do (
				oldPtemp=iesFiles[ii].webFile
				tempValue=iesFiles[ii].intensity
				oldP=newPath+"\\"+getFilenameFile oldPtemp+getFilenameType oldPtemp
				iesFiles[ii].webFile=oldP
				iesFiles[ii].intensity=tempValue
				)--end for
			)
			--更新VRayIES
			vries=for a in lights where classof a == VRayIES and a.ies_file!="" collect a
			viesFiles=for f in 1 to vries.count collect vries[f].ies_file
			for a in vries where a != undefined do(
				oldPtemp=a.ies_file
				tempValue=a.power
				oldP=newPath+"\\"+getFilenameFile oldPtemp+getFilenameType oldPtemp
				a.ies_file=oldP
				a.power=tempValue
			)--end for
			--更新材质和环境贴图
			
			allMaps=getClassInstances bitmapTexture
			--2011.01.15 添加VRayDirt
			if classof VRayDirt == textureMap then(
				VDmaps=getClassInstances VRayDirt
				if VDmaps.count!=0 then
				(
					for i in VDmaps do
					(
						map1=i.texmap_radius
						if classof map1 == bitmapTexture then 
							if finditem allMaps map1==0 then append allMaps map1
						map2=i.texmap_occluded_color
						if classof map2 == bitmapTexture then 
							if finditem allMaps map2==0 then append allMaps map2
						map3=i.texmap_unoccluded_color
						if classof map3 == bitmapTexture then 
							if finditem allMaps map3==0 then append allMaps map3
						
					)
				)
			)

			--添加更新MultiScatter
			mulsct=for i in geometry where classof i == MultiScatter collect i
			if mulsct.count!=0 then(
				for m in mulsct do
				(
					for b in m.Scatter_Object_Mask where b!=undefined and classof b != Vertex_Color and \
						finditem allMaps b==0 do append allMaps b

					if m.Density_Map!=undefined and classof m.Density_Map != Vertex_Color and finditem allMaps m.Density_Map==0 do --2011.01.07
						append allMaps m.Density_Map

					if m.Color_Texture1!=undefined and classof m.Color_Texture1 != Vertex_Color and finditem allMaps m.Color_Texture1==0 do 
						append allMaps m.Color_Texture1

					if m.Scale_Map!=undefined and classof m.Scale_Map != Vertex_Color and finditem allMaps m.Scale_Map==0 do 
						append allMaps m.Scale_Map

					if m.Rotation_Map!=undefined and classof m.Rotation_Map != Vertex_Color and finditem allMaps m.Rotation_Map==0 do 
						append allMaps m.Rotation_Map

					if m.AniShift_Map!=undefined and classof m.AniShift_Map != Vertex_Color and finditem allMaps m.AniShift_Map==0 do 
						append allMaps m.AniShift_Map
				)
			)
			oldFiles=for f in 1 to allmaps.count where (hasProperty allmaps[f]   "filename") collect allmaps[f].filename--老路径
			for m in 1 to allMaps.count where allMaps[m]!=undefined  and (hasProperty allmaps[m]   "filename")  and allMaps[m].filename != undefined do
			(
				oldPtemp=allMaps[m].filename
				
				oldP=newPath+"\\"+getFilenameFile oldPtemp+getFilenameType oldPtemp
				try (allMaps[m].filename=oldP )
				catch(
				
					objUtil.oolog ("error设置路径失败:"+oldP)
				)
				
				
				objUtil.oolog (oldPtemp +"-->>"+oldP)

			)--end for
			
			--更新VRayHDRI
			allMaps=try getClassInstances VRayHDRI catch undefined
			if allMaps!=undefined then (
				for m in 1 to allMaps.count where allMaps[m]!=undefined do
				(
					oldPtemp=allMaps[m].HDRIMapName
					if oldPtemp !=undefined then(
						oldP=newPath+"\\"+getFilenameFile oldPtemp+getFilenameType oldPtemp
						allMaps[m].HDRIMapName=oldP
					)
				)--end for
			)--end if
		--更新动作缓存
		fn detectPC obj = (	--检测动作缓存
			idx=0;mods=obj.modifiers
			for i in 1 to mods.count where classof mods[i]==Point_Cache do idx=i
			idx
		)
		
		pcObjs=for oo in objects where validModifier oo Point_Cache and oo.modifiers[detectPC oo]!=undefined collect oo
		for oo in pcObjs where oo!=undefined and (id=detectPC oo)!=0 do 
		(	oldPtemp=oo.modifiers[id].filename
			if oldPtemp!=undefined then (
			oldP=newPath+"\\"+getFilenameFile oldPtemp+getFilenameType oldPtemp
				p_start=oo.modifiers[id].playbackStart
				p_end=oo.modifiers[id].playbackEnd
				oo.modifiers[id].filename = oldP
				oo.modifiers[id].playbackStart=p_start
				oo.modifiers[id].playbackEnd=p_end
			)
		)
		--更新realflow缓存
	--	rlmesh=for rr in objects where classof rr == MeshLoader collect rr
	--	for r in 1 to rlmesh.count where rlmesh[r]!=undefined do
	--	(
	--			rlmesh[r].path=newPath+"\\"
	--		InstanceMgr.GetInstances rlmesh[r] &rfm
	--		for rf in rfm do if (idx=finditem rlmesh rf) != 0 then rlmesh[idx]=undefined
	--	)		
		objUtil.oolog "所有路径更新完毕"
	),

	--跑2遍
	fn fl_updatePaths newPath =
	(
		try(
		t=trackviewnodes
		n=t[#Max_MotionClip_Manager]
		deleteTrackViewController t n.controller
		)catch(print "eee1")

		try(
			fl_updatePaths2 newPath
		)catch(print "error")
		try(	
			fl_updatePaths2 newPath
		)catch(print "error")

		try(
			if (findstring (renderers.current as String) "V_Ray" ) != undefined then
			renderers.current.options_dontRenderImage =false
		)catch(print "eeeee")
	),

	function setRealflowPathByName rfName rfPath=(
		
		local rfmesh=for rr in objects where classof rr == MeshLoader collect rr
		for r in 1 to rfmesh.count where rfmesh[r]!=undefined and rfmesh[r].name==rfName do
		(
			rfmesh[r].path=rfPath	
		)
		
	)
	
)

