sub preRender_XSI(projPath, txtPath, renderFrame)
	
	set fs =createobject("scripting.filesystemobject")
	'test if the folder exists
	if (Not fs.folderexists(projPath)) then 
		Quit
	End if

	'set project
	'Application.ActiveProject2 = Application.CreateProject( projPath )

	Dim realPath
	realPath = txtPath & "_render.txt"
'	realPath = txtPath 

	if (fs.fileexists(realPath)) then
		
		set f=fs.opentextfile(realPath,1, true)
		do while f.atendofstream<>true 
			Dim nextLine
			Dim buf,num
			nextLine = f.readline 
			
			'1.set texture for those missed
			if (nextLine = "separator----texture.A.f") then
				nextLine = f.readline 
				
				buf = Split(nextLine, "::") 
				'logmessage "    nextline " & nextLine
				num = UBound(buf)
				do while num = 2 
					if (buf(2) =1) then
						'SetValue ("Sources." & buf(0) & ".FileName"), buf(1)
						set oObject = Dictionary.GetObject( buf(0), false )
						oObject.Source.Parameters("FileName").Value = buf(1)
					end if
					nextLine = f.readline 
					buf = Split(nextLine, "::") 
					num = UBound(buf)
				loop 
			end if

			'2.set FileCacheSource for those missed
			if (nextLine = "separator----FileCacheSource.B.f") then
				nextLine = f.readline 
				
				buf = Split(nextLine, "::") 
				num = UBound(buf)
				do while num = 2 
					if (buf(2) =1) then
						'SetValue (buf(0) & ".FileName"), buf(1)
						set oObject = Dictionary.GetObject( buf(0), false )
						oObject.Path.Value = buf(1)
					end if
					nextLine = f.readline 
					buf = Split(nextLine, "::") 
					num = UBound(buf)
				loop 
			end if

			'3.set render settings
			if (nextLine = "separator----RenderSettings.B") then
				'disable all render channels first
				set oPasses = FindObjects( null , "{BFDAF164-5DD8-4422-9F1E-35527CDC2A02}" ) ' render pass
				For each item in oPasses
					Set channels = item.Framebuffers
					For Each och In channels
						'setValue (och & ".Enabled"), 0
						och.Enabled.value = 0
					Next
				Next
				
				do while Trim(nextLine) <> "" 
					pos = Instr(nextLine,"Render Pass")
					if (pos <> 0)	then
						buf = Split(nextLine, "::") 
						
						For each item in oPasses
							Set channels = item.Framebuffers
							For Each och In channels
								if (och = buf(1)) then
									'setValue (och & ".Enabled"), 1
									och.Enabled.value = 1
								End If
							Next
						Next
					End if
					nextLine = f.readline 
					buf = Split(nextLine, "::") 
				loop 
			end if
		loop 
		f.close

		'get the rendered image name
		Dim renderedImg 
		renderedImg = txtPath & "_image.txt"
		Set fn = fs.opentextfile(renderedImg,2, true)
		
		set oremainedPasses = FindObjects( null , "{BFDAF164-5DD8-4422-9F1E-35527CDC2A02}" ) ' render pass
		for Each item in oremainedPasses
			Set channels = item.Framebuffers
			For Each och In channels
				dim rState
				rState = och.Enabled.value
				If rState = "True" Then
					Dim currentName, namebuf
					currentName = och.GetResolvedPath("")
					namebuf = Split(currentName, "\") 
					'SetValue (och & ".Filename"), namebuf(UBound(namebuf))
					och.Parameters("FileName").Value = namebuf(UBound(namebuf))
					
					currentName = och.GetResolvedPath(renderFrame)
					fn.writeline (och & "::" & currentName )
				End if	
			next
		Next
		fn.close

	end if

end Sub

