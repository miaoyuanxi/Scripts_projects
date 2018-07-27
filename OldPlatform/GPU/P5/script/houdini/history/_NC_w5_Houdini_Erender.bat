@echo off

set gROOT=\\10.50.1.20\td\_NC_Settings
set _NC_clients_config_ini=%gROOT%\_NC_clients_configs\_NC_clients_config_ini.bat

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
		set _bat_file_path=%~dp8
		set _bat_file_path=%_bat_file_path:\=/%
		echo _bat_file_path=%_bat_file_path%

		set _bat_rd=%~9
		set _bat_rd=%_bat_rd:\=/%
		echo _bat_rd = %_bat_rd%

		shift
		set _bat_rop=%~9
		set _bat_rop=%_bat_rop:\=/%
		echo _bat_rop = %_bat_rop%
		

		shift
		set _bat_opt=%~9
		echo _bat_opt=%_bat_opt%
		set _bat_opt=%_bat_opt: =@%
	
	echo OptionsEnd______
	echo Configuring @ %date%-%time%

	set _bat_gen_cache=F
	set _bat_null=null
	set _bat_ext=exr
	
	if not x%_bat_opt:render=%==x%_bat_opt% set _bat_gen_cache=T
	
	echo Calling bat script ...
	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%
	
	set RUN_ROOT=%gROOT%\_NC_global_plugins\Houdini\%_bat_cgv%\bin
	set PATH=%RUN_ROOT%;%PATH%
	if "%_bat_gen_cache%"=="T" (
		echo Cache Start @ %date%-%time%
		"%RUN_ROOT%\hbatch.exe" -e _configroots=%gROOT% -e _isrendering=1 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_hip=%_bat_file% -e _cmd_ext=%_bat_ext% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% -e _cmd_hippath=%_bat_file_path% -e _cmd_fileshortname=%_bat_file_short_name% "%gROOT%\_NC_houdini_scripts\_NC_w5_houdini_cache.cmd"
	)
	
	if "%_bat_gen_cache%"=="F" (
		echo Render Start @ %date%-%time%
		"%RUN_ROOT%\hbatch.exe" -e _configroots=%gROOT% -e _isrendering=1 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_hip=%_bat_file% -e _cmd_ext=%_bat_ext% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% -e _cmd_hippath=%_bat_file_path% -e _cmd_fileshortname=%_bat_file_short_name% "%gROOT%\_NC_houdini_scripts\_NC_w5_houdini_render.cmd"
	)
	goto Endof
:Endof
	echo RenderEnd @ %date%-%time%