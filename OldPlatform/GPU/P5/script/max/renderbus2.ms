
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
			--DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string)) 
		)
		
		--resetMaxFile  #noPrompt 
		--quitMax #noPrompt  
	  
	   )catch ( 
			
			objUtil.oolog  ( getCurrentException() as string ) 
			
			if oTxtFile!=undefined then (
				close oTxtFile 
			)
			
			
			local maxv = getmaxv()	
			if maxv >9 then (
			 --DOSCommand ("c:\\maxkill.exe " +(windows.getMAXHWND() as string)) 
			)
			--resetMaxFile  #noPrompt 
			--quitMax #noPrompt
			
	  
		) 
		
		
	)

)


fn read userId taskId cgFile cgTxt=(

objRead = STRead()
objRead.read taskId cgFile cgTxt
--objRead.read "68596" "//18.1.0.229/inputData/53/QSY/scence/BDZX/huisuo_LHP/huisuo_LHP/A001_C019_LHP.max" "C:/enfwork/analysis/68596/QSY_scence_BDZX_huisuo_LHP_huisuo_LHP_A001_C019_LHP.max_20131231172946_63029248_net.txt" 
)

