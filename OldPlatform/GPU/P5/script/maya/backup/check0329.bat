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
	set cg_software_path=%cg_software_path:~0,-8%mayapy.exe
	set cmd="%cg_software_path%" \\10.50.5.29\o5\py\model\check_all.py --cgfl "%cg_file%" --cgin "%cg_info_file%" --cgsw Maya
	goto End


:LightWave
	set cmd="C:\Python27\python.exe" \\10.50.5.29\o5\py\model\check_all.py --cgfl "%cg_file%" --cgin "%cg_info_file%" --cgsw LightWave --ti %task_id%
	goto End


:End
	echo Run: %cmd%
	%cmd%

:Exit
