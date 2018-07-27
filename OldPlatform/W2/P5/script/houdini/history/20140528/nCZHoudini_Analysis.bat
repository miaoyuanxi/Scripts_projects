@echo off
set ConfigRoot=//10.50.8.2/p/script/houdini
echo ConfigRoot = %ConfigRoot%


set _uid=%~1
set _tid=%~2
set _ver=%~3

set _hip=%~4
set _hip=%_hip:\=/%

set _info=%~5
set _info=%_info:\=/%

set _p6=%~6
set _p7=%~7
set _p8=%~8
set _p9=%~9

echo ----------------
echo _uid______%_uid%
echo _tid______%_tid%
echo _ver________%_ver%
echo _hip_______%_hip%
echo _info_______%_info%
echo _p6_________%_p6%
echo _p7_________%_p7%
echo _p8_________%_p8%
echo _p9_________%_p9%
echo ----------------

if "%_uid%"=="19899" goto Analysis_Houdini_19899
if "%_uid%"=="63045" goto Analysis_Houdini_63045
if "%_uid%"=="18660" goto Analysis_Houdini_18660
if "%_uid%"=="163494" goto Analysis_Houdini_163494
if "%_uid%"=="19294" goto Analysis_Houdini_19294
goto Analysis_default

:Analysis_Houdini_19899
	echo Analysis_Houdini_%_uid%
	set _hip=%_hip:19899//=19899/%
	set _info=%_info:19899//=19899/%
	echo Fixed _hip=%_hip%
	echo Fixed _info=%_info%
	set _ver=13.0.237
	echo Version override as %_ver%
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_ver%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_uid% -e _cmd_tid=%_tid% -e _cmd_info=%_info% -e _cmd_hip=%_hip% -e _cmd_conf=%ConfigRoot% "%ConfigRoot%/nCZHoudini_Analysis.cmd"
	goto Exit_1

:Analysis_Houdini_19294
	echo Analysis_Houdini_%_uid%
	set _hip=%_hip:19294//=19294/%
	set _info=%_info:19294//=19294/%
	echo Fixed _hip=%_hip%
	echo Fixed _info=%_info%
	set _ver=13.0.314
	echo Version override as %_ver%
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_ver%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_uid% -e _cmd_tid=%_tid% -e _cmd_info=%_info% -e _cmd_hip=%_hip% -e _cmd_conf=%ConfigRoot% "%ConfigRoot%/nCZHoudini_Analysis.cmd"
	goto Exit_1

:Analysis_Houdini_163494
	echo Analysis_Houdini_%_uid%
	set _hip=%_hip:163494//=163494/%
	set _info=%_info:163494//=163494/%
	echo Fixed _hip=%_hip%
	echo Fixed _info=%_info%
	set _ver=13.0.314
	echo version override as %_ver%
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_ver%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_uid% -e _cmd_tid=%_tid% -e _cmd_info=%_info% -e _cmd_hip=%_hip% -e _cmd_conf=%ConfigRoot% "%ConfigRoot%/nCZHoudini_Analysis.cmd"
	goto Exit_1

:Analysis_Houdini_63045
	echo Analysis_Houdini_%_uid%
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_ver%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_uid% -e _cmd_tid=%_tid% -e _cmd_info=%_info% -e _cmd_hip=%_hip% -e _cmd_conf=%ConfigRoot% "%ConfigRoot%/nCZHoudini_Analysis.cmd"
	goto Exit_1

:Analysis_Houdini_18660
	echo Analysis_Houdini_18660
	set _ver=13.0.237
	echo Be awared! Version override as: 13.0.237
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_ver%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_uid% -e _cmd_tid=%_tid% -e _cmd_info=%_info% -e _cmd_hip=%_hip% -e _cmd_conf=%ConfigRoot% "%ConfigRoot%/nCZHoudini_Analysis.cmd"
	goto Exit_1

:Analysis_default
	echo Analysis_Houdini_Default
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_ver%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_uid% -e _cmd_tid=%_tid% -e _cmd_info=%_info% -e _cmd_hip=%_hip% -e _cmd_conf=%ConfigRoot% "%ConfigRoot%/nCZHoudini_Analysis.cmd"
	goto Exit_1

:Exit_0
echo No configuration applied

:Exit_1
echo Configuration applied