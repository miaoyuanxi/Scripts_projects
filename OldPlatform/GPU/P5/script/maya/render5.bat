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
REM if "%userId%"=="1868563" goto render_1868563


:default
    set MAYA_DISABLE_CIP=1
    set MAYA_DISABLE_CLIC_IPM=1
    set MAYA_DISABLE_CER=1
    
	xcopy /y /f "%py_path%\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
	xcopy /y /f "%py_path%\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
    xcopy /y /f "%py_path%\maya2016\prefs\userPrefs.mel" "C:\users\enfuzion\Documents\maya\2016\prefs\"

    echo "Start py27 to render using cgrender."    

    set process_path=%py_path%\process
    
    set user_path="%py_path%\User\%userId%\main\cgrender.py"
    echo user_path :: %user_path%
    if exist %user_path% (set process_path=%py_path%\User\%userId%\main)
    echo process_path ::%process_path%
    echo "Using cgrender.py to render"
    

	echo "c:\python27\python.exe" "%process_path%\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
	"c:\python27\python.exe" "%process_path%\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
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
    wmic process where name="maya.exe" delete
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\RLMServer\rlm_shave.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\redshift_rlm_server_win64\rlm_redshift.exe" /cls
    echo "Exit Success"
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
    wmic process where name="maya.exe" delete
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\RLMServer\rlm_shave.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\redshift_rlm_server_win64\rlm_redshift.exe" /cls
    echo "Exit Fail"
    exit /b 1


