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
	echo	txt:	    %txt%
	echo	startframe:	%startframe%
	echo	endframe:	%endframe%
	echo	byframe:	%byframe%
	echo	proj:	    %proj%
	echo	mb:	        %mb%
	echo    json:       %json%
	echo    plugins_json:       %plugins_json%
if %taskId:~0,2%==10 (set py_path=\\10.60.100.105\stg_data\input\o5\py\model&&set pt=1000&&set b_path=\\10.60.100.151\td)
if %taskId:~0,1%==9 (set py_path=\\10.60.100.101\o5\py\model&&set pt=1002&&set b_path=\\10.60.100.151\td)
if %taskId:~0,1%==5 (set py_path=\\10.50.5.29\o5\py\model&&set pt=1005&&set b_path=\\10.50.1.22\td_new\td)
if %taskId:~0,1%==8 (set py_path=\\10.70.242.102\o5\py\model&&set pt=1008&&set b_path=\\10.70.242.50\td)
if %taskId:~0,2%==19 (set py_path=\\10.60.100.105\stg_data\input\o5\py\model&&set pt=1009&&set b_path=\\10.70.242.50\td)

echo py_path ::%py_path%
echo pt  :: %pt%
echo b_path :: %b_path%
set output=c:/work/render/%taskId%/output/
if %userId%==119768 goto 119768_test
if %userId%==119614 goto 119768_test
:default
	xcopy /y /f "%py_path%\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
	xcopy /y /f "%py_path%\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
	echo "Using cgrender.py to render"
	echo "c:\python27\python.exe" "%py_path%\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
	"c:\python27\python.exe" "%py_path%\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
goto end

:119768_test
	xcopy /y /f "%py_path%\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
	xcopy /y /f "%py_path%\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
	echo "Using cgrender.py to render"
	echo "c:\python27\python.exe" "%py_path%\cgrender_119768.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
	"c:\python27\python.exe" "%py_path%\cgrender_119768.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
goto end

:end
    echo exitcode: %errorlevel%
    if not %errorlevel%==0 goto fail
    echo Render progress end.
    wmic process where name="rlm.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
	::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
	%b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
	%b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
	REM rd C:\users\enfuzion\Documents\maya\2016.5 /s /q
    exit /b 0

:fail
    echo Render progress failed.
    wmic process where name="rlm.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
    ::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
	%b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
	%b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
	REM rd C:\users\enfuzion\Documents\maya\2016.5 /s /q
    exit /b 1
