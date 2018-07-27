fn test=(
	
	for c in cameras do (
		
		format ".....%\n" c
	)
	--render()
	
	format "camera....%\n" (getActiveCamera())
	format "getcamera....%\n" (viewport.getCamera())	
	 format " viewport.getType()...............%\n" (viewport.getType())
		 
	
		
	format "viewport.activeViewport....%\n" (viewport.activeViewport)
	

format "rendUseActiveView....%\n" (rendUseActiveView)	

		 
		 format "rendViewIndex....%\n" (rendViewIndex)	
		 
	
		-- viewport.ResetAllViews()
		 
		 
			
	format "\n------------------------------\n"
	(
		local renderView
		if (rendUseActiveView) then ( 
			renderView = viewport.activeViewport 
		)else ( 
			renderView = rendViewIndex 
		)
		format "k......%.....%\n" renderView (viewport.getCamera index:renderView)

	)
		
)

clearlistener()
test()


/*

#view_top -- Top
#view_bottom -- Bottom
#view_right -- Right
#view_left -- Left
#view_front -- Front
#view_back -- Back
#view_persp_user -- Perspective
#view_iso_user -- User
#view_camera -- Camera
#view_spot -- Light
#view_shape -- Shape
#view_grid -- Grid

*/