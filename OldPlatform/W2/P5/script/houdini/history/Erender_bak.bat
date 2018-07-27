@echo off

set global_root=\\10.50.8.2\p\_NC_Settings
set _NC_clients_config_ini=%global_root%\_NC_clients_configs\_NC_clients_config_ini.bat
echo current_config = %global_root%

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
		set _bat_file_short_name=%~n8
		set _bat_file=%_bat_file:\=/%
		echo _bat_file = %_bat_file%

		set _bat_rd=%~9
		set _bat_rd=%_bat_rd:\=/%
		echo _bat_rd = %_bat_rd%

		shift
		set _bat_rop=%~9
		echo _bat_rop1 = %_bat_rop%
		set _bat_rop=%_bat_rop:_NC_0001=/%
		echo _bat_rop2 = %_bat_rop%
		set _bat_rop=%_bat_rop:\=/%
		echo _bat_rop3 = %_bat_rop%

		shift
		set _bat_opt=%~9
		echo _bat_opt=%_bat_opt%
		set _bat_opt=%_bat_opt: =@%
	
	echo OptionsEnd______
	echo RedirectBegin	
		
		if "%_bat_cid%"=="164684" goto Render_Configure_164684
		if "%_bat_cid%"=="164798" goto Render_Configure_164798
		if "%_bat_cid%"=="164438" goto Render_Configure_164438	
		goto Config_Default

:Render_Configure_164684
	set _bat_null=null	
	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%

	set _bat_ext="exr"
	set _bat_rd=c:/enfwork/%_bat_tid%/output
	if NOT EXIST %_bat_rd% mkdir "%_bat_rd%/"

	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_bat_cgv%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _configroots=%global_root% -e _isrendering=1 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_hip=%_bat_file% -e _cmd_ext=%_bat_ext% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% "%global_root%/_NC_houdini_scripts/_NC_houdini_start_164684.cmd"
	goto end
	
:Render_Configure_164798
	set _bat_null=null	
	set _bat_file=%_bat_file:164798//=164798/%
	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%
	
	set _bat_ext="exr"
	set _bat_rd=c:/enfwork/%_bat_tid%/output
	if NOT EXIST %_bat_rd% mkdir "%_bat_rd%/"

	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_bat_cgv%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _configroots=%global_root% -e _isrendering=1 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_hip=%_bat_file% -e _cmd_ext=%_bat_ext% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% "%global_root%/_NC_houdini_scripts/_NC_houdini_start_164798.cmd"
	goto end
	
:Render_Configure_164438
	
	echo Render Configure Updated - 001 - Initialized by li 4/9
	set _bat_file=%_bat_file:164438//=164438/%
	
	echo Fixed _bat_file = %_bat_file%	
	
	set _bat_ext="exr"
	set _bat_rd=c:/enfwork/%_bat_tid%/output
	if NOT EXIST %_bat_rd% mkdir "%_bat_rd%/"
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_bat_cgv%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _configroots=%global_root% -e _isrendering=1 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_hip=%_bat_file% -e _cmd_ext=%_bat_ext% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% "%global_root%/_NC_houdini_scripts/_NC_houdini_start.cmd"
	goto end

	
:Config_Default	
	set _bat_null=null	
	set _bat_ext=exr
	set _bat_rd=c:/enfwork/%_bat_tid%/output/%_bat_file_short_name%/
	
	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%
	
	if NOT EXIST %_bat_rd% mkdir "%_bat_rd%/"
	
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_bat_cgv%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _configroots=%global_root% -e _isrendering=1 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_hip=%_bat_file% -e _cmd_ext=%_bat_ext% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% "%global_root%/_NC_houdini_scripts/_NC_houdini_start.cmd"
	goto end




:end
	echo RenderEnd
	