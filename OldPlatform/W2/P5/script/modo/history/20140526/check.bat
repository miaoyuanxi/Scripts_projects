@echo off
set ConfigRoot=//10.50.8.2/p/script/modo
echo ConfigRoot = %ConfigRoot%


set _bat_cid=%~1
set _bat_tid=%~2
set _bat_cgv=%~3

set _bat_file=%~4
set _bat_file=%_bat_file:\=/%

set _bat_info=%~5
set _bat_info=%_bat_info:\=/%

set _p6=%~6
set _p7=%~7
set _p8=%~8
set _p9=%~9

echo ----------------
echo _bat_cid______%_bat_cid%
echo _bat_tid______%_bat_tid%
echo _bat_cgv________%_bat_cgv%
echo _bat_file_______%_bat_file%
echo _bat_info_______%_bat_info%
echo _p6_________%_p6%
echo _p7_________%_p7%
echo _p8_________%_p8%
echo _p9_________%_p9%
echo ----------------

if "%_bat_cid%"=="53" goto Analysis_config_default
goto Analysis_config_default

:Analysis_config_default
	echo Analysis_config_default
	set MODO_EXECUTE=C:/Program Files/Luxology/modo/%_bat_cgv%/modo_cl.exe
	set MODO_PYSCRIPT=%ConfigRoot%/nCZModo_Analysis.py
	"%MODO_EXECUTE%" "-cmd:@%MODO_PYSCRIPT% %_bat_cid%|%_bat_tid%|%_bat_cgv%|\"%_bat_file%\"|%_bat_info%"
	goto Exit_1

goto Exit_0
:Exit_0
echo No configuration applied
:Exit_1
echo Configuration applied