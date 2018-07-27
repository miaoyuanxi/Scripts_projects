@echo off
set userId=%~1
set taskId=%~2
set render=%~3
set txt=%~4
set startframe=%~5
set endframe=%~6
set byframe=%~7
set proj=%~8
set mb=%~9

shift
set tile_index=%~9

shift
set tiles=%~9

if not defined tile_index set tile_index=0
if not defined tiles set tiles=1

echo task info:
	echo	userId:		%userId%
	echo	taskId:		%taskId%
	echo	render:		%render%
	echo	txt:	%txt%
	echo	startframe:	%startframe%
	echo	endframe:	%endframe%
	echo	byframe:	%byframe%
	echo	proj:	%proj%
	echo	mb:	%mb%
	echo	tile_index:	%tile_index%
	echo	tiles:	%tiles%

echo %mb%
dir /ad %mb% && goto arnold
if  %mb:~-4%==.hip goto houdini

:cgrender_with_multi_storages
	echo "Start py27 to render using cgrender_with_multi_storages."
	echo "c:\python27\python.exe" "\\10.70.242.102\o5\py\model\cgrender_with_multi_storages.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1008 --sp %proj% --tile_index %tile_index% --tiles %tiles%
	"c:\python27\python.exe" "\\10.70.242.102\o5\py\model\cgrender_with_multi_storages.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1008 --sp %proj% --tile_index %tile_index% --tiles %tiles%
goto end

:houdini
	echo "start Erender.bat to render houdini."
	set output=c:/work/render/%taskId%/output/
	IF NOT EXIST "%output%" MD "%output%"
	for /f %%i in ('c:\python27\python.exe \\10.70.242.102\o5\py\model\get_houdini_rop.py %taskId%') do set rop=%%i
	echo \\10.50.1.3\p\script\houdini\_NC_w5_Houdini_Erender.bat 0 0 %startframe% %endframe% %byframe% "cgv" "proj" %mb% %output% %rop% "-V -I -s"
	\\10.50.1.3\p\script\houdini\_NC_w5_Houdini_Erender.bat 0 0 %startframe% %endframe% %byframe% "cgv" "proj" %mb% %output% %rop% "-V -I -s"
goto end

:cgrender
	echo "Start py27 to render using cgrender."
	echo "c:\python27\python.exe" "\\10.70.242.102\o5\py\model\cgrender.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1008
	"c:\python27\python.exe" "\\10.70.242.102\o5\py\model\cgrender.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1008
goto end

:cgrender_test
	echo "Start py27 to render using cgrender_test."
	echo "c:\python27\python.exe" "\\10.70.242.102\o5\py\model\cgrender_test.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1008
	"c:\python27\python.exe" "\\10.70.242.102\o5\py\model\cgrender_test.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1008
goto end

:arnold
	echo "Start py27 to render arnold."
	echo "c:\python27\python.exe" "\\10.70.242.102\o5\py\model\arnold_render.py" %taskId% %startframe% %endframe% %byframe%
	"c:\python27\python.exe" "\\10.70.242.102\o5\py\model\arnold_render.py" %taskId% %startframe% %endframe% %byframe%
goto end2

:end2
	echo "Rendering Completed!"
	wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
	wmic process where name="rlm.exe" delete
	exit /b 0

:end
	echo exitcode: %errorlevel%
	wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
	wmic process where name="rlm.exe" delete
	if not %errorlevel%==0 goto fail
	::if not %userId%==963480 goto ok
	goto ok
:vray_gi
	echo vray_gi
	echo xcopy /y /f  "\\10.50.1.22\td\custom_config\119768\vray_gi\vray_gi_temp_____.png" "C:\work\render\%taskId%\output\"
	xcopy /y /f  "\\10.50.1.22\td\custom_config\119768\vray_gi\vray_gi_temp_____.png" "C:\work\render\%taskId%\output\"

:ok
	echo "Rendering Completed!"
	wmic process where name="rlm.exe" delete
	wmic process where name="JGS_mtoa_licserver.exe" delete
	::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
	\\10.50.1.22\td_new\td\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
	\\10.50.1.22\td_new\td\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
	REM rd C:\users\enfuzion\Documents\maya\2016.5 /s /q
	exit /b 0


:fail
	if %userId%==963480 (if %errorlevel%==1 goto ok)
	if %userId%==1811662 (if %errorlevel%==1 goto ok)
	echo "Rendering Failed!"
	wmic process where name="rlm.exe" delete
	wmic process where name="JGS_mtoa_licserver.exe" delete
	::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
	\\10.50.1.22\td_new\td\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
	\\10.50.1.22\td_new\td\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
	REM rd C:\users\enfuzion\Documents\maya\2016.5 /s /q
	exit /b 1
