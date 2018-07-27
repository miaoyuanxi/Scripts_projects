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
set json=%~9

shift
set plugins_json=%~9

echo task info:
	echo	userId:		%userId%
	echo	taskId:		%taskId%
	echo	render:		%render%
	echo	txt:		%txt%
	echo	startframe:	%startframe%
	echo	endframe:	%endframe%
	echo	byframe:	%byframe%
	echo	proj:		%proj%
	echo	mb:			%mb%
	echo	json:		%json%
	echo	plugins_json:		%plugins_json%
if %taskId:~0,2%==10 (set py_path=\\10.60.100.105\stg_data\input\o5\py\model&&set pt=1000&&set b_path=\\10.60.100.151\td)
if %taskId:~0,1%==9 (set py_path=\\10.60.100.101\o5\py\model&&set pt=1002&&set b_path=\\10.60.100.151\td)
if %taskId:~0,1%==5 (set py_path=\\10.50.5.29\o5\py\model&&set pt=1005&&set b_path=\\10.50.1.22\td_new\td)
if %taskId:~0,1%==8 (set py_path=\\10.70.242.102\o5\py\model&&set pt=1008&&set b_path=\\10.70.242.50\td)
if %taskId:~0,2%==19 (set py_path=\\10.80.100.101\o5\py\model&&set pt=1009&&set b_path=\\10.80.243.50\td)
if %taskId:~0,2%==16 (set py_path=\\10.90.100.101\o5\py\model&&set pt=1016&&set b_path=\\10.90.96.51\td1)

echo py_path ::%py_path%
echo pt  :: %pt%
echo b_path :: %b_path%
set output=c:/work/render/%taskId%/output/

REM if "%userId%"=="1868564" goto render_1868564
if "%userId%"=="119768" goto render_119768
if "%userId%"=="1868563" goto render_1868563
REM :render_1868564
    REM SET _APP_NAME=Maya
    REM SET _APP_VERS=2018
    REM SET REDSHIFT_LICENSE=5059@127.0.0.1
    REM goto _RS_RENDER
 
REM :_RS_RENDER
    REM REM SET USER_MAYA_SCRIPT_PATH=B:\scripts\Maya\redshift_cmd\scripts
    REM wmic process where name="rlm_redshift.exe" delete
    REM start D:\redshift_rlm_server_win64\rlm_redshift.exe

    REM set REDSHIFT_LICENSEPATH = D:/redshift_rlm_server_win64/redshift-core2.lic
    REM set PATH=%PATH%;D:\PLUGINS\MAYA\REDSHIFT\2560\bin;C:\Program Files\Autodesk\Maya2018\bin
    REM SET _CUDA_DEVICE_SELECTED=01

    REM SET _PLUGINS_LOCAL_PATH=D:\PLUGINS\MAYA\REDSHIFT

    REM set REDSHIFT_LOCALDATAPATH=D:/temp/REDSHIFT/CACHE

    REM set _PLUGINS_LOCAL_RUN_PATH=D:\PLUGINS\MAYA\REDSHIFT\2560


    REM SET REDSHIFT_COREDATAPATH=%_PLUGINS_LOCAL_RUN_PATH%

    REM SET REDSHIFT_PREFSPATH=B:\plugins\maya\redshift\PREFS\1080\preferences.xml


    REM SET REDSHIFT_COMMON_ROOT=%REDSHIFT_COREDATAPATH%\Plugins\%_APP_NAME%\Common
    REM SET REDSHIFT_PLUG_IN_PATH=%REDSHIFT_COREDATAPATH%\Plugins\%_APP_NAME%\%_APP_VERS%\nt-x86-64
    REM ECHO REDSHIFT_PLUG_IN_PATH=%REDSHIFT_PLUG_IN_PATH%

    REM SET REDSHIFT_SCRIPT_PATH=%REDSHIFT_COMMON_ROOT%\scripts
    REM SET REDSHIFT_XBMLANGPATH=%REDSHIFT_COMMON_ROOT%\icons
    REM SET REDSHIFT_RENDER_DESC_PATH=%REDSHIFT_COMMON_ROOT%\rendereRDesc
    REM SET MAYA_SCRIPT_PATH=%REDSHIFT_SCRIPT_PATH%
    REM SET MAYA_PLUG_IN_PATH=%REDSHIFT_PLUG_IN_PATH%
    REM SET MAYA_RENDER_DESC_PATH=%REDSHIFT_RENDER_DESC_PATH%;
    REM SET PYTHONPATH=%REDSHIFT_SCRIPT_PATH%
    REM SET XBMLANGPATH=%REDSHIFT_XBMLANGPATH%

    REM ECHO REDSHIFT_PREFSPATH=%REDSHIFT_PREFSPATH%

    REM SET LOCALAPPDATA=%REDSHIFT_LOCALDATAPATH%\%_CUDA_DEVICE_SELECTED%
    REM SET MAYAROOT=C:\Program Files\Autodesk\%_APP_NAME%%_APP_VERS%
    REM SET PATH=%PATH%;%REDSHIFT_PLUG_IN_PATH%;%MAYAROOT%\bin

    REM set PATH=%PATH%;D:\PLUGINS\MAYA\REDSHIFT\2560\bin;C:\Program Files\Autodesk\Maya2018\bin
    REM set REDSHIFT_PREFSPATH=B:\plugins\maya\redshift\PREFS\1080\preferences.xml

    REM set REDSHIFT_COREDATAPATH=D:\PLUGINS\MAYA\REDSHIFT\2560

    REM set REDSHIFT_LOCALDATAPATH=D:/temp/REDSHIFT/CACHE
    REM set REDSHIFT_COMMON_ROOT=D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\Common
    REM set REDSHIFT_PLUG_IN_PATH=D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\2018\nt-x86-64
    REM set REDSHIFT_SCRIPT_PATH=D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\Common\scripts
    REM set REDSHIFT_XBMLANGPATH=D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\Common\icons
    REM set REDSHIFT_RENDER_DESC_PATH=D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\Common\rendererDesc


    REM set REDSHIFT_MAYAEXTENSIONSPATH=%REDSHIFT_MAYAEXTENSIONSPATH%;D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\2018\nt-x86-64\extensions
    REM set MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%;D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\Common\scripts
    REM set MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%;D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\2018\nt-x86-64
    REM set MAYA_RENDER_DESC_PATH=%MAYA_RENDER_DESC_PATH%;D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\Common\rendererDesc
    REM set PYTHONPATH=%PYTHONPATH%;D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\Common\scripts

    REM set XBMLANGPATH=D:\PLUGINS\MAYA\REDSHIFT\2560\Plugins\Maya\Common\icons
    REM set LOCALAPPDATA=D:/temp/REDSHIFT/CACHE
    REM goto REDSHIFT_render

REM :REDSHIFT_render
    REM echo "C:/Program Files/Autodesk/maya2018/bin/render.exe" -s 1 -e 10000 -b 1 -proj "" -rd "c:/work/render/44444444/output/11111/" -preRender "_RV_RSConfig;" -r redshift -logLevel 2 -gpu {0,1} "N:/TD_test_gpu/maya2018_rs2560.ma" 

    REM "C:/Program Files/Autodesk/maya2018/bin/render.exe" -s 1 -e 10000 -b 1 -proj "" -rd "c:/work/render/44444444/output/11111/" -preRender "_RV_RSConfig;" -r redshift -logLevel 2 -gpu {0,1} "N:/TD_test_gpu/maya2018_rs2560.ma" 


    REM ECHO Clean up ...
    REM ::RD /s /q %REDSHIFT_LOCALDATAPATH%
    REM RD /s /q %_PLUGINS_LOCAL_PATH%
    REM goto end



:default
    set MAYA_DISABLE_CIP=1
    set MAYA_DISABLE_CLIC_IPM=1
    set MAYA_DISABLE_CER=1
    
	xcopy /y /f "%py_path%\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
	xcopy /y /f "%py_path%\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
    xcopy /y /f "%py_path%\maya2016\prefs\userPrefs.mel" "C:\users\enfuzion\Documents\maya\2016\prefs\"
	echo "Using cgrender.py to render"
	echo "c:\python27\python.exe" "%py_path%\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
	"c:\python27\python.exe" "%py_path%\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
goto end

:render_119768
    set MAYA_DISABLE_CIP=1
    set MAYA_DISABLE_CLIC_IPM=1
    set MAYA_DISABLE_CER=1
    
	xcopy /y /f "%py_path%\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
	xcopy /y /f "%py_path%\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
    xcopy /y /f "%py_path%\maya2016\prefs\userPrefs.mel" "C:\users\enfuzion\Documents\maya\2016\prefs\"
	echo "Using cgrender.py to render"
	echo "c:\python27\python.exe" "%py_path%\cgrender_119768.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
	"c:\python27\python.exe" "%py_path%\cgrender_119768.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
goto end


:render_1868563
    set MAYA_DISABLE_CIP=1
    set MAYA_DISABLE_CLIC_IPM=1
    set MAYA_DISABLE_CER=1
    
	xcopy /y /f "%py_path%\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
	xcopy /y /f "%py_path%\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
    xcopy /y /f "%py_path%\maya2016\prefs\userPrefs.mel" "C:\users\enfuzion\Documents\maya\2016\prefs\"
	echo "Using cgrender.py to render"
	echo "c:\python27\python.exe" "%py_path%\cgrender_1868563.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
	"c:\python27\python.exe" "%py_path%\cgrender_1868563.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
goto end


:end    
    echo exitcode: %errorlevel%
    if "%userId%"=="1820586" (set %errorlevel%==0)
    if not %errorlevel%==0 goto fail
    echo Render progress end.
    echo "exit rlm "
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
    
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\RLMServer\rlm_shave.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\redshift_rlm_server_win64\rlm_redshift.exe" /cls
    exit /b 0

:fail
    echo Render progress failed.
    echo "exit rlm "
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\RLMServer\rlm_shave.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\redshift_rlm_server_win64\rlm_redshift.exe" /cls
    exit /b 1


