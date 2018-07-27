@echo off


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

		shift
		set _bat_rop=%~9
		echo _bat_rop=%_bat_rop%

		shift
		set _bat_opt=%~9
		echo _bat_opt=%_bat_opt%
		set _bat_opt=%_bat_opt: =@%
	
	echo OptionsEnd______


shift 
set renderer=%~9
set mel=c:/script/maya/maya_preRender.mel
set rd=c:/enfwork/%taskId%/output/


echo task info:
	echo	userId:		%_bat_cid=%
	echo	taskId:		%_bat_tid%
	echo	startframe:	%_bat_sf%
	echo	endframe:	%_bat_ef%
	echo	byframe:	%_bat_bf%
	echo	proj:		%_bat_pro%
	echo	mayafile:	%_bat_file%
	echo	rd:		%_bat_rd%


if "%_bat_cid%"=="18445" goto render_18445

if "%render%"=="C:/Program Files/Autodesk/Maya8.5/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2008/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2009/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2010/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2011/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2012/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2013/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2013.5/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2014/bin/Render.exe" goto render2


:render1
	"%render%" -s %startframe% -e %endframe% -b %byframe% -r mr -art -aml -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% "%mb%"  
	goto end

:render2
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
	goto end

:render3
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -r maxwell "%mb%"  
	goto end


:render_18445
	echo ---
	echo DOD4 Configure Applied @ 18445 - TEMP
	echo ---

	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\18000\18445\support\env\ssd\Maya.env" "C:\users\enfuzion\Documents\maya\2012-x64\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\18000\18445\support\env\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2012-x64\prefs\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\18000\18445\support\env\mtoa.mod" "C:\users\enfuzion\Documents\maya\2012-x64\modules\"

	set render=="C:/Program Files/Autodesk/Maya2012/bin/Render.exe"

	"%render%" -s %_bat_sf% -e %_bat_ef% -b %_bat_bf% -preRender "source \"%mel%\";maya_preRender(\"%_bat_pro%\",\"%txt%\",\"%_bat_sf%\");" -proj "%_bat_pro%" -rd %rd% -mr:art -mr:aml "%_bat_file%"  
	goto end

:end
echo "Rendering Completed!"