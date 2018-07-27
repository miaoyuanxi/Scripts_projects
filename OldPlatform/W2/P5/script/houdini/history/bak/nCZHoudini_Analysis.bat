@echo off
set global_config=//10.50.1.229/renderscene/chenzhong
set _NC_clients_config_ini=%global_config%/_NC_clients_configs/_NC_clients_config_ini.bat
echo global_config = %global_config%

set _bat_cid=%~1
echo _bat_cid = %_bat_cid%

set _bat_tid=%~2
echo _bat_tid = %_bat_tid%

set _bat_cgv=%~3
echo _bat_cgv = %_bat_cgv%

set _bat_file=%~4
set _bat_file=%_bat_file:\=/%
echo _bat_file = %_bat_file%

set _bat_inf=%~5
set _bat_inf=%_bat_inf:\=/%

set _p6=%~6
set _p7=%~7
set _p8=%~8
set _p9=%~9

set _bat_null=null
call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%

set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_bat_cgv%/bin
"%RENDER_ROOT%/hbatch.exe" -e _configroots=%global_config% -e _isrendering=0 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_hip=%_bat_file% -e _cmd_inf=%_bat_inf% "%global_config%/_NC_houdini_scripts/_NC_houdini_start.cmd"

goto Endof

:Endof
	net use * /delete /y