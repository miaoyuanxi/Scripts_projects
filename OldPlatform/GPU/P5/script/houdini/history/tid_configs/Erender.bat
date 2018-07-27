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
	echo OptionsEnd______


	echo RedirectBegin
		if "%_bat_cid%"=="15315" goto Config_15315
		if "%_bat_cid%"=="63045" goto Config_63045
		if "%_bat_cid%"=="53" goto Config_53
		goto Config_Default

:Config_15315
	echo Configure_%_bat_cid% @ Presona
	set _bat_ext=exr
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini 12.5.533/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_render_file=%_bat_file% -e _cmd_ext=%_bat_ext% "%ConfigRoot%/nCZHoudiniStarter_%_bat_cid%.cmd"
	goto end

:Config_63045
	echo Configure_%_bat_cid% @ HumanArk
	set _bat_ext=jpg
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini %_bat_cgv%/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_render_file=%_bat_file% -e _cmd_ext=%_bat_ext% "%ConfigRoot%/nCZHoudiniStarter_%_bat_cid%.cmd"
	goto end



:Config_53
	echo Configure_%_bat_cid% @ testa1
	set _bat_ext=exr
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini 12.5.469/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_render_file=%_bat_file% -e _cmd_ext=%_bat_ext% "%ConfigRoot%/nCZHoudiniStarter_%_bat_cid%.cmd"
	goto end

:Config_Default
	echo Configure_DEFAULT
	set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini 12.5.469/bin
	"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_render_file=%_bat_file% -e _cmd_ext=%_bat_ext% "%ConfigRoot%/nCZHoudiniStarter_Default.cmd"
	goto end

:end
	echo RenderEnd