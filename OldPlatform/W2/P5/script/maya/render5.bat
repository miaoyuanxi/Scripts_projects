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

shift
set tile_index=%~9

shift
set tiles=%~9

echo task info:
	echo	userId:		%userId%
	echo	taskId:		%taskId%
	echo	render:		%render%
	echo	txt:	    %txt%
	echo	startframe:	%startframe%
	echo	endframe:	%endframe%
	echo	byframe:	%byframe%
	echo	proj:	    %proj%
	echo	mb:	        %mb%
	echo    json:       %json%
	echo    plugins_json:       %plugins_json%
    echo 	tile_index:	%tile_index%
    echo 	tiles:	%tiles%
if %taskId:~0,2%==10 (set py_path=\\10.60.100.104\stg_data\input\o5\py\model&&set pt=1000&&set b_path=\\10.60.100.151\td)
if %taskId:~0,1%==9 (set py_path=\\10.60.100.101\o5\py\model&&set pt=1002&&set b_path=\\10.60.100.151\td)
if %taskId:~0,2%==10 (set py_path=\\10.60.100.101\o5\py\model&&set pt=1002&&set b_path=\\10.60.100.151\td)
if %taskId:~0,1%==5 (set py_path=\\10.50.5.29\o5\py\model&&set pt=1005&&set b_path=\\10.50.1.22\td_new\td)
if %taskId:~0,1%==8 (set py_path=\\10.70.242.102\o5\py\model&&set pt=1008&&set b_path=\\10.70.242.50\td)
if %taskId:~0,2%==19 (set py_path=\\10.60.100.105\stg_data\input\o5\py\model&&set pt=1009&&set b_path=\\10.70.242.50\td)

echo py_path ::%py_path%
echo pt  :: %pt%
echo b_path :: %b_path%
set output=c:/work/render/%taskId%/output/

set MAYA_OPENCL_IGNORE_DRIVER_VERSION=1
echo MAYA_OPENCL_IGNORE_DRIVER_VERSION :: %MAYA_OPENCL_IGNORE_DRIVER_VERSION%
set MAYA_VP2_DEVICE_OVERRIDE=VirtualDeviceDx11
echo MAYA_VP2_DEVICE_OVERRIDE :: %MAYA_VP2_DEVICE_OVERRIDE%
set MAYA_ENABLE_LEGACY_HYPERSHADE=1
echo MAYA_ENABLE_LEGACY_HYPERSHADE :: %MAYA_ENABLE_LEGACY_HYPERSHADE%

:default
    xcopy /y /f "%py_path%\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
    xcopy /y /f "%py_path%\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
    
    echo "Start py27 to render using cgrender."   
    set process_path=%py_path%\process
    set user_path="%py_path%\User\%userId%\main\cgrender.py"
    echo user_path :: %user_path%
    if exist %user_path% (set process_path=%py_path%\User\%userId%\main)
    echo process_path ::%process_path%
    echo "Using cgrender.py to render"

	echo "c:\python27\python.exe" "%process_path%\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --sp %proj% --tile_index %tile_index% --tiles %tiles% --pt %pt%
	"c:\python27\python.exe" "%process_path%\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --sp %proj%  --tile_index %tile_index% --tiles %tiles%  --pt %pt%
goto end



:end
    echo exitcode: %errorlevel%
    if not %errorlevel%==0 if %userId%==1854599 goto ok
    if not %errorlevel%==0 goto fail
    echo Render progress end.
    taskkill /F /IM "rlm.exe"  /T 
    wmic process where name="rlm.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
    wmic process where name="maya.exe" delete
	::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
	%b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\rlm_shave\rlm_shave.exe" /cls
	%b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm_Golaem.exe" /cls
	REM rd C:\users\enfuzion\Documents\maya\2016.5 /s /q
    echo Render progress end.
    if "%userId%"=="1865352" goto end_1865352
    echo "end rlm"
    echo "Exit Success"
    exit /b 0
:end_1865352
    echo convert to 1080 start
    "\\10.60.100.101\o5\py\model\1865352.py" "c:/work/render/%taskId%/output/720" "c:/work/render/%taskId%/output/1080"
    echo convert to 1080 end
    echo "end rlm"
    echo "Exit Success"
    exit /b 0
:fail
    echo Render progress failed.
    taskkill /F /IM "rlm.exe"  /T 
    wmic process where name="rlm.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
    wmic process where name="maya.exe" delete
    ::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
	%b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
	%b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm_Golaem.exe" /cls
	REM rd C:\users\enfuzion\Documents\maya\2016.5 /s /q
    echo Render progress failed.
    echo "end rlm"
    echo "Exit Fail"
    exit /b 1
:ok
    echo "the is  ok "
    echo "exit rlm "
    ::for /f "tokens=2 " %a in ('tasklist  /fi "imagename eq rlm.exe" /nh') do taskkill /f /pid  %a
    taskkill /F /IM "rlm.exe"  /T 
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
    wmic process where name="maya.exe" delete
    wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm_Golaem.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    echo "end rlm"
    echo "Exit Success"
    exit /b 0
