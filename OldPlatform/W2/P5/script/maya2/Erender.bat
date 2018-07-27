@echo off
set mel=//10.50.100.1/p/script/maya2/render_18445_maya2.mel


echo RenderBegin
	echo OptionsBegin______
		set _bat_cid=%~1
		echo _bat_cid = %_bat_cid%

		set _bat_tid=%~2
		echo _bat_tid = %_bat_tid%

		set _bat_sf=%~3
		echo _bat_sf = %_bat_sf%

		set _bat_ef=%~4
		echo _bat_ef = %_bat_ef%

		set _bat_bf=%~5
		echo _bat_bf = %_bat_bf%

		set _bat_cgv=%~6
		echo _bat_cgv = %_bat_cgv%

		set _bat_pro=%~7
		set _bat_pro=%_bat_pro:\=/%
		echo _bat_pro = %_bat_pro%

		set _bat_file=%~8
		set _bat_file=%_bat_file:\=/%
		echo _bat_file = %_bat_file%

		set _bat_rd=%~9
		set _bat_rd=%_bat_rd:\=/%
		echo _bat_rd = %_bat_rd%
	
	echo OptionsEnd______

if "%_bat_cid%"=="18445" goto render_18445


:render_18445
	echo ---
	echo DOD4 Configure Applied @ 18445 - TEMP
	echo ---

	net use * /delete /y
	net use L: \\10.50.100.6\hq\18000\18445 /persistent:yes
	

	rmdir /s/q "C:\users\enfuzion\Documents\maya\2012-x64\prefs"

	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\18000\18445\support\env\ssd\Maya.env" "C:\users\enfuzion\Documents\maya\2012-x64\"
	echo xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\18000\18445\support\env\prefs" "C:\users\enfuzion\Documents\maya\2012-x64\prefs\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\18000\18445\support\env\mtoa.mod" "C:\users\enfuzion\Documents\maya\2012-x64\modules\"

	set renderROOT=C:/Program Files/Autodesk/Maya2012

	"%renderROOT%/bin/render.exe" -preRender "source \"%mel%\";render_18445_maya2(\"%_bat_pro%\",\"%_bat_rd%\")" -mr:art -mr:aml -proj "%_bat_pro%" -rd %_bat_rd% -s %_bat_sf% -e %_bat_ef% -b %_bat_bf%  "%_bat_file%"  
	
	net use * /delete /y
	goto end

:end
echo "Rendering Completed!"