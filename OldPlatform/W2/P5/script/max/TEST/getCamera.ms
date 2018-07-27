	fn getMyCamera=(
		local myCamera = getActiveCamera()
		format "c1......%\n" myCamera
		local renderView
		try(
			if (rendUseActiveView) then ( 
				renderView = viewport.activeViewport 
			)else ( 
				renderView = rendViewIndex 
			)
			format "renderView...%\n" renderView
			
			myCamera =  (viewport.getCamera index:renderView)
			format "c2......%\n" myCamera
			if myCamera==undefined then (
				myCamera= viewport.Gettype() 
			)
			format "c3......%\n" myCamera
		)catch()
		
		myCamera
	)
	
	getMyCamera()