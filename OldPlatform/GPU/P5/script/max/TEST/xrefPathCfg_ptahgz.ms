
	fn delAllXrefPath = (
		
		local cc =xrefPaths.count()
		for i in cc to 1 by -1 do (
			try(
				xrefPaths.delete i
			)catch()
		)
		
	)

	fn getAllXrefPath=(
		
		local xrefPathArr = #()
		for i=1 to xrefPaths.count() do (
			local myPath = xrefPaths.get i
			append xrefPathArr myPath
		)
		xrefPathArr
	)

	fn addXrefPath xrefPathArr = (
		
		for i=1 to xrefPathArr.count do (
			local mpath = xrefPathArr[i]
			if mpath!=undefined then (
				xrefPaths.add mpath
			)
			
		)
		
		
	)
	
	
	
	fn myXref = (
		local pathArr = getAllXrefPath()
		--stCon.maxUserPath=pathArr
		local xrefPathArr=#("c:/enfwork/ptahgz")--#(stCon.taskPath,stCon.cachePath)
		addXrefPath xrefPathArr
		
		
		
		
		--------------------------------------
		/*
		try(
			delAllUserPath()
			addUserPath stCon.maxUserPath
		)catch()
		*/
	)
	
	myXref()