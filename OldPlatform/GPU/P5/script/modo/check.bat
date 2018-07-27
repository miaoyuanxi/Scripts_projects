@echo off

set global_config=//10.50.1.229/renderscene/chenzhong
set _NC_clients_config_ini=%global_config%/_NC_clients_configs/_NC_clients_config_ini.bat
echo global_config = %global_config%

echo AnalysisBegin
	echo OptionsBegin______

	set _bat_cid=%~1
	echo _bat_cid = %_bat_cid%

	set _bat_tid=%~2
	echo _bat_tid = %_bat_tid%

	set _bat_cgv=%~3
	echo _bat_cgv = %_bat_cgv%

	set _bat_file=%~4
	set _bat_file=%_bat_file:\=/%
	echo _bat_file = %_bat_file%

	set _bat_info=%~5
	set _bat_info=%_bat_info:\=/%
	echo _bat_info = %_bat_info%

	set _p6=%~6
	set _p7=%~7
	set _p8=%~8
	set _p9=%~9

	echo OptionsEnd______

	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv%

	set MODO_EXECUTE=C:/Program Files/Luxology/modo/%_bat_cgv%/modo_cl.exe
	set MODO_PYSCRIPT=%global_config%/_NC_modo_scripts/_NC_modo_analysis.py
	"%MODO_EXECUTE%" "-cmd:@%MODO_PYSCRIPT% %_bat_cid%|%_bat_tid%|%_bat_cgv%|\"%_bat_file%\"|%_bat_info%"
	goto end

:end
	echo Analysis complete