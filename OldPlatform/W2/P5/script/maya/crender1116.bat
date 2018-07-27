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

:cgrender
	echo "Start py27 to cgrender"
	echo "c:\python27\python.exe" "\\10.50.5.29\o5\py\model\cgrender.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1005
	"c:\python27\python.exe" "\\10.50.5.29\o5\py\model\cgrender.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt 1005
goto end

:arnold
	echo "Start py27 to render arnold"
	echo "c:\python27\python.exe" "\\10.50.5.29\o5\py\model\arnold_render.py" %taskId% %startframe% %endframe% %byframe%
	"c:\python27\python.exe" "\\10.50.5.29\o5\py\model\arnold_render.py" %taskId% %startframe% %endframe% %byframe%
goto end2

:end2
		echo "Rendering Completed!"
		exit /b 0

:end
    echo exitcode: %errorlevel%
    if not %errorlevel%==0 goto fail
    echo "Rendering Completed!"
    exit /b 0

:fail
    echo "Rendering Failed!"
    exit /b 1
