@echo off
REM c:/script/maya/check.bat "100001" "578199" "C:/Program Files/Autodesk/maya2013/bin/maya.exe" "" "Z:/BaLL.mb" "C:/WORK/helper/4402/analyse_net.txt"
REM c:/script/maya/check.bat "100001" "578199" "B:/NewTek/2015.3/bin/lwsn.exe" "" "\\10.50.242.1\d\inputdata\100000\100001\lightwave\M\Scenes\Miranda_Tumbling_test.lws" "C:/WORK/helper/4402/analyse_net.txt"
REM # Author: Liu Qiang
REM # Tel:    13811571784
REM # QQ:     386939142

set user_id=%~1
set task_id=%~2
set cg_software_path=%~3
set cg_project=%~4
set cg_file=%~5
set cg_info_file=%~6

if  %cg_software_path:~-8%==maya.exe goto Maya
if  %cg_software_path:~-8%==lwsn.exe goto LightWave

:Default
	echo Can not find the analyze program for %cg_software_path%.
	goto Exit


:Maya
	REM if %user_id%==962276 call B:\custom_config\962276\HQ.bat
	REM if %user_id%==1810948 call B:\custom_config\1810948\lebrain.bat
	REM if %user_id%==1818936 call B:\custom_config\1818936\env.bat
    REM if %user_id%==1842922 call B:\custom_config\1842922\ch.bat
    REM if %user_id%==1843804 call B:\custom_config\1843804\Analyse.bat
    REM if %user_id%==1845580 call B:\custom_config\1845580\domemaster3d.bat
    if EXIST "C:\users\enfuzion\Documents\maya\2016.5\prefs" rd /s/q  "C:\users\enfuzion\Documents\maya\2016.5\prefs"
    xcopy /y /f "\\10.60.100.101\o5\py\model\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
    xcopy /y /f "\\10.60.100.101\o5\py\model\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
::set cg_software_path=%cg_software_path:~0,-8%mayabatch.exe
REM set cmd="%cg_software_path%" -command "python \"options={'cg_file': '%cg_file%', 'cg_info_file': '%cg_info_file%', 'cg_software': 'Maya'};^
REM import sys;sys.path.insert(0, '//10.60.100.105/stg_data/input/o5/py/model');^
REM from check_all import *;^
REM analyze = eval(options['cg_software']+'Analyze(options)');^
REM analyze.run();analyze.write_info_file()\""
    REM if %user_id%==1851585 call B:\clientFiles\1851585\imax.bat
    set cmd="C:\Python27\python.exe" "\\10.60.100.101\o5\py\model\check_all.py" --cgsw "Maya" --ui %user_id% --ti %task_id% --sfp "%cg_software_path%" --proj "" --cgfile "%cg_file%" --cg_info_file "%cg_info_file%" --pt 1002
    echo %cmd%
    echo Run: %cmd%
    %cmd%
    goto End


:LightWave
    set cmd="C:\Python27\python.exe" \\10.50.5.29\o5\py\model\check_all.py --cgfl "%cg_file%" --cgin "%cg_info_file%" --cgsw LightWave --ti %task_id%
    echo Run: %cmd%
    %cmd%
    goto End


:End

    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    ::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
    \\10.50.1.22\td_new\td\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    \\10.50.1.22\td_new\td\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls

:Exit
