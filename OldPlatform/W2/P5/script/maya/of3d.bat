 @ECHO off
netstat -an |find "EST"

SET userId=%~1
SET taskId=%~2
SET render=%~3
SET txt=%~4
SET startframe=%~5
SET endframe=%~6
SET byframe=%~7
SET proj=%~8
SET mb=%~9


shift 
SET _bat_opt=%~9
SET RD=c:/work/render/%taskId%/output/

ECHO task info:
	ECHO	userId:		%userId%
	ECHO	taskId:		%taskId%
	ECHO	render:		%render%
	ECHO	txt:	%txt%
	ECHO	startframe:	%startframe%
	ECHO	endframe:	%endframe%
	ECHO	byframe:	%byframe%
	ECHO	proj:	%proj%
	ECHO	mb:	%mb%
	ECHO	_bat_opt:	%_bat_opt%


if "%userId%"=="53" goto render_53
goto end

	
:render_53
	ECHO Configure Applied @ 53
	ECHO Redshift3d render
	
	SET USER_PATH=C:\Program Files\NVIDIA Corporation\NVSMI
	SET _CUDA_DEVICE_SELECTED=0123
	SET _IPADDRES_LOCAL=10.50.2.12
	FOR /f "tokens=1-2 delims=:" %%a in ('ipconfig^|find "IPv4"') do set ip=%%b
	SET _IPADDRES_LOCAL=%ip:~1%
	SET _CUDA_DEVICE_SELECTED=%_bat_opt%
	
	SET _V_RS=2.0.03
	SET _V_MTOA=1.2.2.0
	SET _V_MAYA=2016
	SET _VN_REDSHIFT=REDSHIFT-%_V_RS%
	
	ECHO.
	ECHO SOURCING SERVER SETUP ...
	SET _PLUGINS_FIXED_DIR=TD\PLUGINS\MAYA
	SET _RUN_WINRAR_ROOT=C:\PROGRAM FILES\WINRAR
	SET MAYAROOT=C:\Program Files\Autodesk\Maya%_V_MAYA%
	SET PATH=%PATH%;%_RUN_WINRAR_ROOT%
	
	SET _RESOURCE_SERVER_ROOT=\\10.50.242.1
	SET _RESOURCE_LOCAL_ROOT=D:
	SET /A NUM=%RANDOM% %%2
	IF "%NUM%"=="0" SET _RESOURCE_SERVER_ROOT=\\10.50.242.6
	ECHO SOURCING FROM %_RESOURCE_SERVER_ROOT%
	
	SET _REDSHIFT_RUN_DIR=%_RESOURCE_SERVER_ROOT%\%_PLUGINS_FIXED_DIR%\REDSHIFT\%_VN_REDSHIFT%

	SET _RV_LOAD_ONLINE_ROOT=\\10.50.1.22\td\plugins
	SET _USER_CONFIG_ROOT=%_RV_LOAD_ONLINE_ROOT%\users\964309
	
	SET _PLG_SHAVE=%_USER_CONFIG_ROOT%\SHAVE-9.0v36-MAYA2016
	SET _PLG_OF3D_OPIUMPIPE=%_USER_CONFIG_ROOT%\opiumPipe\0.51
	SET _PLG_HOTOCEANDEFORMER=%_USER_CONFIG_ROOT%\hotOceanDeformer_2016
	SET _PLG_QUALOTH=%_USER_CONFIG_ROOT%\qualoth-4.2.1
	
	SET _PLG_MTOA=%_USER_CONFIG_ROOT%\mtoa\2016\1.2.2.0
	SET _PLG_ALSHADERS=%_USER_CONFIG_ROOT%\alShaders-win-1.0.0rc10-ai4.2.2.0
	SET _PLG_OF3D_ALSHADERS=%_USER_CONFIG_ROOT%\alshader_of3d\2015
	SET _PLG_JF_WATERSHADE=%_USER_CONFIG_ROOT%\jf_waterShade

	SET _USER_MAYA_PLUG_IN_PATH=%_PLG_SHAVE%\shave\plug-ins;%_PLG_OF3D_OPIUMPIPE%\plugins;%_PLG_HOTOCEANDEFORMER%\deformer;%_PLG_MTOA%\plug-ins;%_PLG_QUALOTH%\plug-ins;
	SET _USER_MAYA_SCRIPT_PATH=%_PLG_SHAVE%\shave\scripts;%_USER_CONFIG_ROOT%\scripts\mel;%_PLG_HOTOCEANDEFORMER%\scripts;%_PLG_QUALOTH%\scripts;
	SET _USER_MAYA_MODULE_PATH=%_PLG_MTOA%;%_PLG_MTOA%\bin;%_PLG_SHAVE%\shave\samples;
	
	SET _USER_ARNOLD_SHADERS=%_PLG_HOTOCEANDEFORMER%\mtoa\1.0.0;%_PLG_MTOA%\shaders;%_PLG_JF_WATERSHADE%;%_PLG_ALSHADERS%\bin;%_PLG_OF3D_ALSHADERS%
	SET _USER_MTOA_TEMPLATES_PATH=%_PLG_OF3D_ALSHADERS%\ae;%_PLG_ALSHADERS%\ae;%_PLG_JF_WATERSHADE%\ae

	ECHO.
	SET REDSHIFT_LICENSEPATH=%_RV_LOAD_ONLINE_ROOT%\maya\redshift\license\redshift-core.lic
	SET REDSHIFT_PREFSPATH=%_RV_LOAD_ONLINE_ROOT%\maya\redshift\prefs\%_IPADDRES_LOCAL%\%_CUDA_DEVICE_SELECTED%\preferences.xml
	SET REDSHIFT_LOCALDATAPATH=C:\Users\%username%\AppData\Local\_RV_RS
	SET REDSHIFT_COREDATAPATH=%_REDSHIFT_RUN_DIR%
	SET REDSHIFT_COMMON_ROOT=%REDSHIFT_COREDATAPATH%\Plugins\Maya\Common
	SET REDSHIFT_PLUG_IN_PATH=%REDSHIFT_COREDATAPATH%\Plugins\Maya\%_V_MAYA%\nt-x86-64
	SET REDSHIFT_SCRIPT_PATH=%REDSHIFT_COMMON_ROOT%\scripts
	SET REDSHIFT_XBMLANGPATH=%REDSHIFT_COMMON_ROOT%\icons
	SET REDSHIFT_RENDER_DESC_PATH=%REDSHIFT_COMMON_ROOT%\rendereRDesc
	
	SET MAYA_PLUG_IN_PATH=%REDSHIFT_PLUG_IN_PATH%;%_USER_MAYA_PLUG_IN_PATH%
	SET MAYA_SCRIPT_PATH=%REDSHIFT_SCRIPT_PATH%;%_USER_MAYA_SCRIPT_PATH%
	SET MAYA_MODULE_PATH=%_USER_MAYA_MODULE_PATH%;%_USER_MAYA_PLUG_IN_PATH%
	
	SET MAYA_RENDER_DESC_PATH=%REDSHIFT_RENDER_DESC_PATH%;%_USER_MAYA_MODULE_PATH%
	
	SET ARNOLD_PLUGIN_PATH=%_PLG_MTOA%\procedurals;%_USER_ARNOLD_SHADERS%;%_USER_MAYA_MODULE_PATH%
	SET MTOA_TEMPLATES_PATH=%_USER_MTOA_TEMPLATES_PATH%
	
	SET PYTHONPATH=%REDSHIFT_SCRIPT_PATH%
	SET XBMLANGPATH=%REDSHIFT_XBMLANGPATH%
	SET LOCALAPPDATA=%REDSHIFT_LOCALDATAPATH%\%_CUDA_DEVICE_SELECTED%\%taskId%
	SET MAYA_ROOT=C:\Program Files\Autodesk\Maya%_V_MAYA%\bin
	SET PATH=%PATH%;%REDSHIFT_PLUG_IN_PATH%;%MAYA_MODULE_PATH%;%_PLG_OF3D_OPIUMPIPE%\bin;%_PLG_SHAVE%\shave\samples;

	net use S: \\10.50.242.6\d\inputdata\964000\964309\jueji1\maya\S /persistent:yes
	net use K: \\10.50.242.6\d\inputdata\964000\964309\jueji1\maya\K /persistent:yes
	net use Y: \\10.50.242.6\d\inputdata\964000\964309\jueji1\maya\Y /persistent:yes
	net use V: \\10.50.242.6\d\inputdata\964000\964309\jueji1\maya\V /persistent:yes

	ECHO.
	ECHO INSTALLING SHAVE ...
	xcopy /V /Q /Y /E "%_PLG_SHAVE%\maya" "%MAYAROOT%\"
	XCOPY /V /Q /Y /E "%_PLG_SHAVE%\mentalrayForMaya2016" "C:\Program Files\Autodesk\"
	XCOPY /V /Q /Y "%_PLG_SHAVE%\rlm\shave.lic" "C:\rlm\"
	
	ECHO.
	"%MAYA_ROOT%\render.exe" -s %startframe% -e %endframe% -b %byframe% -preRender "_RV_RSConfig;" -proj "%proj%" -rd %RD% -r redshift -logLevel 2 "%mb%"
	ECHO "%MAYA_ROOT%\render.exe" -s %startframe% -e %endframe% -b %byframe% -rl %txt% -preRender "_RV_RSConfig;" -proj "%proj%" -rd %RD% -r redshift -logLevel 2 "%mb%"
	
	ECHO Clean up ...
	RD /s /q %LOCALAPPDATA%
	goto end

:end
ECHO "Rendering Completed!"