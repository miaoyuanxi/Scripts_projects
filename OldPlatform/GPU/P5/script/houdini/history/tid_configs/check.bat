@echo off
set ConfigRoot=//10.50.1.3/pool/script/houdini

set userId=%~1
set taskId=%~2
set _ver=%~3
set _hip=%~4
set _txt=%~5
set _p6=%~6
set _p7=%~7
set _p8=%~8
set _p9=%~9

echo ----------------
echo userId______%userId%
echo taskId______%taskId%
echo _ver________%_ver%
echo _file_______%_file%
echo _info_______%_info%
echo _p6_________%_p6%
echo _p7_________%_p7%
echo _p8_________%_p8%
echo _p9_________%_p9%
echo ----------------

if "%userId%"=="63045" goto Analysis_Houdini_63045
goto Analysis_default

:Analysis_Houdini_63045
	echo Analysis_Houdini_%userId%
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_ver%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%userId% -e _cmd_tid=%taskId% -e _cmd_info=%_info% -e _cmd_hip=%_hip% "%ConfigRoot%/nCZHoudini_Analysis.cmd"
	goto Exit_1



:Analysis_default
	echo Analysis_Houdini_Default
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_ver%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%userId% -e _cmd_tid=%taskId% -e _cmd_info=%_info% -e _cmd_hip=%_hip% "%ConfigRoot%/nCZHoudini_Analysis.cmd"
	goto Exit_1

:Exit_0
echo No configuration applied

:Exit_1
echo Configuration applied