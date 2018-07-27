'.A ---- customer cannot assign folder
'.B ---- customer can assign folder
'.d ---- the item is a folder
'.f ---- the item is a file

sub checkNet(projPath, xsiFile, txtPath)
	'set project
	Application.ActiveProject2 = Application.CreateProject( projPath )

	OpenScene xsiFile, false

	'output info txt according to different type
	set fs =createobject("scripting.filesystemobject")
	set f=fs.opentextfile(txtPath,2, true)

	'1.check textures
	f.writeline ("separator----texture.A.f")
	set oReturn = FindObjects( null , "{22C3E8F8-CCEA-11D2-B35B-00105A1E70DE}" ) ' CLSID_3DImageClip
	'set oReturn = Application.FindObjects2( siImageClipID  ) -- it's the same as above
	for each item in oReturn
		oClipSource = item.Source.Name
		oFile = item.GetFileName()
		If oClipSource <> "noIcon_pic" Then
			if (fs.fileexists(oFile)) then
				f.writeline (item & "::" & oFile & "::1")
			else
				f.writeline (item & "::" & oFile & "::0")
			end if
		End if
	next
	
	'2.check cache
	f.writeline ("separator----FileCacheSource.B.f")
	set oReturn = FindObjects( null , "{C3911D76-93F9-4e06-802C-0FA9AFC09CE8}" ) ' CLSID_3DFileCacheSource
	for each item in oReturn
		dim FCacheSource
		FCacheSource = item.Path.value
		if (fs.fileexists(FCacheSource)) then
			f.writeline (item & "::" & FCacheSource & "::1")
		else
			f.writeline (item & "::" & FCacheSource & "::0")
		end if
	Next
	
	'3.check render settings
	'render pass
	f.writeline ("separator----RenderSettings.B")
	set oReturn = FindObjects( null , "{BFDAF164-5DD8-4422-9F1E-35527CDC2A02}" ) ' render pass
	'set oReturn = Application.FindObjects2( siPassID   )
	for each item in oReturn
		Set channels = item.Framebuffers
		For Each och In channels
			dim rState
			rState = och.Enabled.value
			If rState = "True" then
				f.writeline ("Render Pass::" & och & "::1" )
			Else
				f.writeline ("Render Pass::" & och & "::0" )
			End if
		next
	next
	'start and end frame
	set oScene = ActiveProject.ActiveScene
	set oSceneProp = oScene.PassContainer.Properties( "Scene Render Options" )
	f.writeline ("Start::" &  oSceneProp.FrameStart.value)
	f.writeline ("End::" & oSceneProp.FrameEnd.value)

	f.writeblanklines 1
	f.close

end Sub

