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
	if %user_id%==962276 call \\10.60.100.102\td\custom_config\962276\HQ.bat
	if %user_id%==1810948 call \\10.60.100.102\td\custom_config\1810948\lebrain.bat
	if %user_id%==1818936 call \\10.60.100.102\td\custom_config\1818936\env.bat
    if %user_id%==1842922 call \\10.60.100.102\td\custom_config\1842922\ch.bat
    xcopy /y /f "\\10.60.100.101\o5\py\model\maya2017\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
	set cg_software_path=%cg_software_path:~0,-8%mayabatch.exe
	set cmd="%cg_software_path%" -command "python \"options={'cg_file': '%cg_file%', 'cg_info_file': '%cg_info_file%', 'cg_software': 'Maya'};^
import sys;sys.path.insert(0, '//10.60.100.101/o5/py/model');^
from check_all import *;^
analyze = eval(options['cg_software']+'Analyze(options)');^
analyze.run();analyze.write_info_file()\""
	goto End


:LightWave
	set cmd="C:\Python27\python.exe" \\10.60.100.101\o5\py\model\check_all.py --cgfl "%cg_file%" --cgin "%cg_info_file%" --cgsw LightWave --ti %task_id%
	goto End


:End
	echo Run: %cmd%
	%cmd%

:Exit
