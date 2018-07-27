fn test = (
	
	--for ss in sceneMaterials do (
		--format "sceneMaterials...%\n" ss
		
	--)
	--showproperties sceneMaterials
	
	format "\n--------------------\n"
	--show sceneMaterials
	
	
	format "\n--------------------\n"
	--showproperties sceneMaterials[1]
	
	format "\n--------------------\n"
	
	
	for sceneM in sceneMaterials do (
		
		if hasProperty sceneM "maps" then (
			for m in sceneM.maps do (
				if m!=undefined and (classof m)==Bitmaptexture then (
		
					format "m.....%...%\n" (classof m)  m.fileName 
					--showproperties m
				)
				
				
				if m!=undefined and (classof m)==VRayMap then (
					--showproperties m
					format "refract_filterMap.....%...%\n" (classof m)  m.refract_filterMap 
					format "reflect_filterMap.....%...%\n" (classof m)  m.reflect_filterMap 
					format "environmentMap.....%...%\n" (classof m)  m.environmentMap 
					
					--showproperties m
				)
				
				--VRayMap
			)
		)
		

		
		
	)
	
)

clearlistener()
test()