@echo off

set ConfigRoot=//10.50.1.3/pool/script/houdini
echo ConfigRoot = %ConfigRoot%

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


	echo RedirectBegin
		if "%_bat_cid%"=="53" goto Config_Default
		goto Config_Default

:Config_Default
	echo Configure_DEFAULT
	set _bat_ext=""
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_bat_cgv%/bin
	echo RENDER_ROOT=%RENDER_ROOT%=
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_conf=%ConfigRoot% -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_render_file=%_bat_file% -e _cmd_ext=%_bat_ext% "%ConfigRoot%/nCZHoudini_Render_DEFAULT.cmd"
	goto end

:end
	echo RenderEnd