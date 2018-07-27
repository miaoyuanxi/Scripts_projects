@echo off

set global_config=//10.50.1.229/renderscene/chenzhong
set _NC_clients_config_ini=%global_config%/_NC_clients_configs/_NC_clients_config_ini.bat
echo global_config = %global_config%

echo RenderBegin
	echo OptionsBegin______
		set _bat_cid=%~1
		echo _bat_cid = %_bat_cid%

		set _bat_tid=%~2
		echo _bat_tid = %_bat_tid%

		set _bat_sf=%~3
		echo _bat_sf = %_bat_sf%

		set _bat_ef=%~4
		echo _bat_ef = %_bat_ef%

		set _bat_bf=%~5
		echo _bat_bf = %_bat_bf%

		set _bat_cgv=%~6
		echo _bat_cgv = %_bat_cgv%

		set _bat_pro=%~7
		set _bat_pro=%_bat_pro:\=/%
		echo _bat_pro = %_bat_pro%

		set _bat_file=%~8
		set _bat_file=%_bat_file:\=/%
		echo _bat_file = %_bat_file%

		set _bat_rd=%~9
		set _bat_rd=%_bat_rd:\=/%
		echo _bat_rd = %_bat_rd%

		shift
		set _bat_rop=%~9
		echo _bat_rop=%_bat_rop%

		shift
		set _bat_opt=%~9
		echo _bat_opt=%_bat_opt%
		set _bat_opt=%_bat_opt: =@%
	
	echo OptionsEnd______

	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv%
	
	set _bat_rd=C:/enfwork/%_bat_tid%/output
	set _ch_info=C:/enfwork/%_bat_tid%/render.txt

	set MODO_EXECUTE=C:/Program Files/Luxology/modo/%_bat_cgv%/modo_cl.exe
	set MODO_PYSCRIPT=%global_config%/_NC_modo_scripts/_NC_modo_render.py
	"%MODO_EXECUTE%" "-cmd:@%MODO_PYSCRIPT% %_bat_cid%|%_bat_tid%|%_bat_sf%|%_bat_ef%|%_bat_bf%|%_bat_cgv%|%_bat_pro%|\"%_bat_file%\"|%_bat_rd%|%_ch_info%|%_bat_rop%|%_bat_opt%"
	goto end

:end
	echo RenderEnd