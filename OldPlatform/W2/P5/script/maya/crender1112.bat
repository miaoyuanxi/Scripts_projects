@echo off
set global_config=//10.50.1.229/renderscene/chenzhong
set _NC_clients_config_ini=%global_config%/_NC_clients_configs/_NC_clients_config_ini.bat
echo current_config = %global_config%

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
set renderer=%~9
set mel=c:/script/maya/maya_preRender5.mel
set rd=c:/work/render/%taskId%/output/


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
	echo	renderer:	%renderer%

echo %mb%
dir /ad %mb% && goto arnold

::if "%userId%"=="119663" goto gdc_render
::if "%userId%"=="119875" goto silas_render
::if "%userId%"=="120151" goto ants_render
::if "%userId%"=="120268" goto lianlinfx_render

::if "%userId%"=="119365" goto gdc_render

::if "%userId%"=="962796" goto default
::if "%userId%"=="962539" goto default

:cgrender
	echo "Start py27 to cgrender"
	echo "c:\python27\python.exe" "\\10.50.5.29\o5\py\model\cgrender.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1005
	"c:\python27\python.exe" "\\10.50.5.29\o5\py\model\cgrender.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1005
goto end

:default
	echo "Start py27 to render maya"
	echo "c:\python27\python.exe" "\\10.50.5.29\o5\py\model\maya.py" %taskId% %startframe% %endframe% %byframe%
	"c:\python27\python.exe" "\\10.50.5.29\o5\py\model\maya.py" %taskId% %startframe% %endframe% %byframe%
goto end

:arnold
	echo "Start py27 to render arnold"
	echo "c:\python27\python.exe" "\\10.50.5.29\o5\py\model\arnold_render.py" %taskId% %startframe% %endframe% %byframe%
	"c:\python27\python.exe" "\\10.50.5.29\o5\py\model\arnold_render.py" %taskId% %startframe% %endframe% %byframe%
goto end

:gdc_render
	echo "Using gdc specific render"
	set test=//10.50.24.10/d/inputdata5/119000/119386/gdc/file-cluster/GDC/Projects
	set idmt_projects=//10.50.24.10/d/inputdata5/119000/119386/gdc/file-cluster/GDC/Projects
	:: set idmt_projects=//10.50.1.6/d/inputdata8/maya/18000/18445/file-cluster/GDC/Projects
	set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;//10.50.8.16/p/script/_NC_Settings/_NC_maya_scripts/_18445/plugins/2012
	set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;//10.50.19.150/p5/script/maya/gdc_usersetup

	"%render%" -s %startframe% -e %endframe% -b %byframe%  -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"
goto end

:silas_render
	echo "Using silas specific render"
	set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;//10.50.19.150/p5/script/maya/usersetup/render/silas
	"%render%" -s %startframe% -e %endframe% -b %byframe%  -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"
goto end

:ants_render
	echo "Using ants specific render"
	net use x: \\10.50.24.10\d\inputdata5\120000\120151\x
	net use y: \\10.50.24.10\d\inputdata5\120000\120151\y

	xcopy /y /v /e "\\10.50.8.16\td\zhaoxiaofei\10_229\300048\script" "C:\users\enfuzion\Documents\maya\2013-x64\scripts\"
	xcopy /y /v /e "\\10.50.8.16\td\zhaoxiaofei\10_229\300048\arnold" "C:\users\enfuzion\Documents\maya\2013-x64\"
	xcopy /y /f "\\10.50.8.16\td\zhaoxiaofei\10_229\300048\1.0.0.2\ai.dll" "C:\solidangle\mtoadeploy\2013_1.0.0.2\bin\"

	"%render%" -s %startframe% -e %endframe% -b %byframe%  -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"
	net use * /delete /y

goto end

:lianlinfx_render
	echo "Using lianlinfx specific render"
	net use o: \\10.50.24.10\d\inputdata5\120000\120268\o
	net use z: \\10.50.24.10\d\inputdata5\120000\120268\z
	set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;//10.50.19.150/p5/script/maya/usersetup/render/lianlinfx

	xcopy /y /v /e "\\10.50.19.150\p5\script\maya\usersetup\render\lianlinfx\maya.env" "C:\users\enfuzion\Documents\maya\2014-x64\"
	xcopy /y /v /e "\\10.50.19.150\p5\script\maya\usersetup\render\lianlinfx\mtoa.mod" "C:\users\enfuzion\Documents\maya\2014-x64\modules\"

	"%render%" -s %startframe% -e %endframe% -b %byframe%  -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"
	net use * /delete /y

	del /q "C:\users\enfuzion\Documents\maya\2014-x64\"
	del /q "C:\users\enfuzion\Documents\maya\2014-x64\modules\"

goto end

:ktcartoon_render
	echo "Using ktcartoon specific render"
	set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;//10.50.19.150/p5/script/maya/usersetup/render/ktcartoon

	echo "%render%" -s %startframe% -e %endframe% -b %byframe%  -proj "//10.50.24.10/d/inputdata5/120000/120299/LFX" -rd %rd% -mr:art -mr:aml "%mb%"
	"%render%" -s %startframe% -e %endframe% -b %byframe%  -proj "//10.50.24.10/d/inputdata5/120000/120299/LFX" -rd %rd% -mr:art -mr:aml "%mb%"
	net use * /delete /y

goto end

:end
echo "Rendering Completed!"
