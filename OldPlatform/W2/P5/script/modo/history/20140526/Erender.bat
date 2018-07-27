@echo off

set ConfigRoot=D:/Projects/Modo/scripts
echo set ConfigRoot=//10.50.1.3/p/script/modo
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

	set _bat_rd=C:/enfwork/%_bat_tid%/output
	set _ch_info=C:/enfwork/%_bat_tid%/render.txt

	echo RedirectBegin
		if "%_bat_cid%"=="53" goto Render_config_default
		goto Render_config_default

:Render_config_default
	echo Render_config_default
	set PYTHONHOME=%ConfigRoot%/python
	set MODO_EXECUTE=C:/Program Files/Luxology/modo/%_bat_cgv%/modo_cl.exe
	set MODO_PYSCRIPT=%ConfigRoot%/nCZModo_Render.py
	"%MODO_EXECUTE%" "-cmd:@%MODO_PYSCRIPT% %_bat_cid%|%_bat_tid%|%_bat_sf%|%_bat_ef%|%_bat_bf%|%_bat_cgv%|%_bat_pro%|\"%_bat_file%\"|%_bat_rd%|%_ch_info%|%_bat_rop%|%_bat_opt%"
	goto Exit_1

goto Exit_0
:Exit_0
	echo No render configuration applied, null
:Exit_1
	echo Render configure applied, process completed