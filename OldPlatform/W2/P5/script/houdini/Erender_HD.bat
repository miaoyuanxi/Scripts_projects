@echo off

SET gROOT=B:\scripts\Houdini
SET _NC_clients_config_ini=%gROOT%\Econfig_HD.bat

echo RenderBegin
	echo OptionsBegin______
		SET _bat_cid=%~1
		echo _bat_cid = %_bat_cid%

		SET _bat_tid=%~2
		echo _bat_tid = %_bat_tid%

		SET _bat_sf=%~3
		echo _bat_sf = %_bat_sf%

		SET _bat_ef=%~4
		echo _bat_ef = %_bat_ef%

		SET _bat_bf=%~5
		echo _bat_bf = %_bat_bf%

		SET _bat_cgv=%~6
		echo _bat_cgv = %_bat_cgv%

		SET _bat_pro=%~7
		SET _bat_pro=%_bat_pro:\=/%
		echo _bat_pro = %_bat_pro%

		SET _bat_file=%~8
		SET _bat_file_short_name=%~n8
		SET _RENDER_FILENAME=%~dpn8__%_bat_tid%%~x8
		
		echo _bat_file = %_bat_file%
		SET _bat_file_path=%~dp8
		SET _bat_file_path=%_bat_file_path:\=/%
		echo _bat_file_path=%_bat_file_path%

		SET _bat_rd=%~9
		SET _bat_rd=%_bat_rd:\=/%
		echo _bat_rd = %_bat_rd%

		shift
		SET _bat_rop=%~9
		SET _bat_rop=%_bat_rop:_NC_0001=/%
		SET _bat_rop=%_bat_rop:\=/%
		echo _bat_rop = %_bat_rop%

		shift
		SET _bat_opt=%~9
		echo _bat_opt=%_bat_opt%
		SET _bat_opt=%_bat_opt: =@%
	
	echo OptionsEnd______
	echo Configuring @ %date%-%time%

	ECHO.
	SET _bat_file=%_bat_file:/=\%
	SET _RENDER_FILENAME=%_RENDER_FILENAME:/=\%
	IF NOT EXIST "%_RENDER_FILENAME%" (
		ECHO MAKING NEW TARGET FILE ...
		COPY /Y "%_bat_file%" "%_RENDER_FILENAME%"
		TIMEOUT /T 10 /NOBREAK
	)
	IF EXIST "%_RENDER_FILENAME%" (
		SET _bat_file=%_RENDER_FILENAME%
	)
	
	ECHO.
	SET _BUFF=NULL
	SET _SYSTEM_RUN_PATH=C:\Windows\System32
	SET _HSERVERIP=10.50.10.231
	SET _HSERVERNAME=hserver
	SET PATH=%_SYSTEM_RUN_PATH%;%PATH%
	SET _SN_HSS=HoudiniServer
	SET _SN_HLSS=HoudiniLicenseServer
 	SET _HSS=NULL
	SET _HLSS=NULL
	SET _BUFF=NULL
	ECHO CHECKING %_SN_HLSS%
		FOR /f "tokens=1-2 delims=:" %%a IN ('sc query %_SN_HLSS%^| findstr "STATE"') DO (
			SET _BUFF=%%b
		)
		SET _BUFF=%_BUFF: =_%
		CALL :CONV_VAE_TO_MAJ _BUFF
		if not x%_BUFF:RUNNING=%==x%_BUFF% SET _HLSS=RUNNING
		if not x%_BUFF:STOPPED=%==x%_BUFF% SET _HLSS=STOPPED
		ECHO _HLSS=%_HLSS%
		if "%_HLSS%"=="STOPPED" (
			ECHO START %_HLSS% ...
			sc start %_SN_HLSS%
		)
		if "%_HLSS%"=="NULL" (
			ECHO INSTALL %_HLSS% ...
			XCOPY /V /Q /Y /E "B:\plugins\houdini\lic\15\sesinetd.exe" "%_SYSTEM_RUN_PATH%\"
			sc create %_SN_HLSS% binPath= "%_SYSTEM_RUN_PATH%\sesinetd.exe"
			ECHO START %_HLSS% ...
			sc start %_SN_HLSS%
		)
	
	ECHO.
	ECHO CHECKING %_SN_HSS%
		SET _BUFF=NULL
		FOR /f "tokens=1-2 delims=:" %%a IN ('sc query %_SN_HSS%^| findstr "STATE"') DO (
			SET _BUFF=%%b
		)
		SET _BUFF=%_BUFF: =_%
		CALL :CONV_VAE_TO_MAJ _BUFF
		if not x%_BUFF:RUNNING=%==x%_BUFF% SET _HSS=RUNNING
		if not x%_BUFF:STOPPED=%==x%_BUFF% SET _HSS=STOPPED
		ECHO _HSS=%_HSS%
		if "%_HSS%"=="STOPPED" (
			ECHO START %_HSS% ...
			sc start %_SN_HSS%
		)
		if "%_HSS%"=="NULL" (
			ECHO INSTALL %_HSS% ...
			XCOPY /V /Q /Y /E "B:\plugins\houdini\lic\15\hserver.exe" "%_SYSTEM_RUN_PATH%\"
			sc create %_SN_HSS% binPath= "%_SYSTEM_RUN_PATH%\hserver.exe"
			ECHO START %_HSS% ...
			sc start %_SN_HSS%
		)
		SET _BUFF=NULL
		FOR /f "tokens=1-2 delims=:" %%a IN ('sc query %_SN_HSS%^| findstr "STATE"') DO (
			SET _BUFF=%%b
		)
		SET _BUFF=%_BUFF: =_%
		CALL :CONV_VAE_TO_MAJ _BUFF
		if not x%_BUFF:RUNNING=%==x%_BUFF% SET _HSS=RUNNING
		if "%_HSS%"=="RUNNING" (
			"%_SYSTEM_RUN_PATH%\%_HSERVERNAME%.exe" -S %_HSERVERIP%
		)
		
	ECHO.
	ECHO SOURCING SERVER SETUP ...
	SET _APP_NAME=Houdini
	SET _PLUG_HTOA_NV=NULL
    SET _bat_ext=""
	echo Calling bat script ...
	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%
	
	SET _APPS_FIXED_DIR=td\apps\%_APP_NAME%
	SET _PLUGINS_FIXED_DIR=td\plugins\%_APP_NAME%
	XCOPY /V /Q /Y /E "B:\tools\7-Zip\*" "%_SYSTEM_RUN_PATH%\"
	
	SET _RESOURCE_SERVER_ROOT=\\10.50.242.1
	SET _RESOURCE_LOCAL_ROOT=D:
	SET /A NUM=%RANDOM% %%2
	IF "%NUM%"=="0" SET _RESOURCE_SERVER_ROOT=\\10.50.242.6
		ECHO SOURCING FROM SERVER %_RESOURCE_SERVER_ROOT%
	SET _APP_SERVER_RAR=%_RESOURCE_SERVER_ROOT%\%_APPS_FIXED_DIR%\%_APP_NAME%-%_bat_cgv%.7z
	SET _APP_LOCAL_PATH=%_RESOURCE_LOCAL_ROOT%\%_APPS_FIXED_DIR%
	SET _APP_LOCAL_RUN_PATH=%_APP_LOCAL_PATH%\%_APP_NAME%-%_bat_cgv%
	
	IF EXIST "%_APP_LOCAL_RUN_PATH%" (
		ECHO START DEL  %_APP_LOCAL_RUN_PATH% @ %DATE%-%TIME%
		rd /q /s "%_APP_LOCAL_RUN_PATH%"
	)
	ECHO %_APP_NAME%-%_bat_cgv% NOT EXIST
	ECHO START INSTALLING @ %_APP_NAME%-%_bat_cgv% ...
	TIMEOUT /T 5 /NOBREAK
	ECHO 	COPY START @ %DATE%-%TIME%
	XCOPY /V /Q /Y "%_APP_SERVER_RAR%" "%_APP_LOCAL_PATH%\"
	ECHO 	EXTRACT START @ %DATE%-%TIME%
	
	7z X "%_APP_LOCAL_RUN_PATH%.7z" -bd -o"%_APP_LOCAL_RUN_PATH%"
	SET _APP_LOCAL_RUN_PATH_FAULT=%_APP_LOCAL_RUN_PATH%\%_APP_NAME%-%_bat_cgv%
	IF EXIST %_APP_LOCAL_RUN_PATH_FAULT% (
		ROBOCOPY /MOVE -E /NDL /NFL %_APP_LOCAL_RUN_PATH_FAULT%  %_APP_LOCAL_RUN_PATH%
	)
	
	ECHO 	COPY CLEAN UP @ %DATE%-%TIME%
	DEL /Q "%_APP_LOCAL_RUN_PATH%.7z"
	echo END INSTALLING @ %_APP_NAME%-%_bat_cgv%
	
	
	ECHO _PLUG_HTOA_NV=%_PLUG_HTOA_NV%
	SET _PLUGINS_SERVER_RAR=%_RESOURCE_SERVER_ROOT%\%_PLUGINS_FIXED_DIR%\%_PLUG_HTOA_NV%.rar
	SET _PLUGINS_LOCAL_PATH=%_RESOURCE_LOCAL_ROOT%\%_PLUGINS_FIXED_DIR%
	SET _PLUGINS_LOCAL_RUN_PATH=%_PLUGINS_LOCAL_PATH%\%_PLUG_HTOA_NV%
	RD /S /Q "%_PLUGINS_LOCAL_RUN_PATH%
	
	SET _RLM_RUN_PATH=C:\AMPED
	SET _CP_SOURCE_FOLDER=%_RESOURCE_SERVER_ROOT%\%_PLUGINS_FIXED_DIR%\AMPED
	SET _CP_SOURCE_FOLDER=%_CP_SOURCE_FOLDER:/=\%
		
	IF NOT "%_PLUG_HTOA_NV%"=="NULL" (
		IF NOT EXIST "%_PLUGINS_LOCAL_RUN_PATH%" (
			ECHO INSTALLING %_PLUG_HTOA_NV% ...
			TIMEOUT /T 5 /NOBREAK
			ECHO 	COPY START @ %DATE%-%TIME%
			XCOPY /V /Q /Y "%_PLUGINS_SERVER_RAR%" "%_PLUGINS_LOCAL_PATH%\"
			ECHO 	EXTRACT START @ %DATE%-%TIME%
			unrar X -idq "%_PLUGINS_LOCAL_RUN_PATH%.rar" *.* "%_PLUGINS_LOCAL_RUN_PATH%\"
			ECHO 	COPY CLEAN UP @ %DATE%-%TIME%
			DEL /Q "%_PLUGINS_LOCAL_RUN_PATH%.rar"
		)
		
		wmic process where name="JGS_mtoa_licserver.exe" delete
		wmic process where name="rlm.exe" delete
		TIMEOUT /T 5 /NOBREAK
		start %_PLUGINS_LOCAL_RUN_PATH%\AMPED\rlm.exe
	)
	
	ECHO.
	ECHO.
	SET _bat_gen_cache=F
	SET _bat_null=null

	if not exist %_bat_rd% mkdir %_bat_rd%
	SET _bat_rd=%_bat_rd:\=/%
	echo _bat_opt=%_bat_opt%
	if not x%_bat_opt:--gc=%==x%_bat_opt% SET _bat_gen_cache=T
	SET _APP_LOCAL_RUN_PATH=%_APP_LOCAL_RUN_PATH:\=/%
	SET _PLUGINS_LOCAL_RUN_PATH=%_PLUGINS_LOCAL_RUN_PATH:\=/%
	echo _APP_LOCAL_RUN_PATH=%_APP_LOCAL_RUN_PATH%
	echo _PLUGINS_LOCAL_RUN_PATH=%_PLUGINS_LOCAL_RUN_PATH%
	SET RUN_ROOT=%_APP_LOCAL_RUN_PATH%\bin
	SET HFS=%_APP_LOCAL_RUN_PATH%
	SET PATH=%PATH%;%RUN_ROOT%

	ECHO RUN_ROOT=%RUN_ROOT%
	SET _bat_file=%_bat_file:\=/%
	if "%_bat_gen_cache%"=="T" (
        TIMEOUT /T 15 /NOBREAK
		echo Cache Start @ %date%-%time%
		"%RUN_ROOT%\hbatch.exe" -e _configroots=%gROOT% -e _isrendering=1 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_hip=%_bat_file% -e _cmd_ext=%_bat_ext% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% -e _cmd_hippath=%_bat_file_path% -e _cmd_fileshortname=%_bat_file_short_name% "%gROOT%\_NC_houdini_scripts\_NC_houdini_cache.cmd"
	)
	if "%_bat_gen_cache%"=="F" (
        TIMEOUT /T 15 /NOBREAK
		echo Render Start @ %date%-%time%
		"%RUN_ROOT%\hbatch.exe" -e _configroots=%gROOT% -e _isrendering=1 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_hip=%_bat_file% -e _cmd_ext=%_bat_ext% -e _cmd_rop=%_bat_rop% -e _cmd_opt=%_bat_opt% -e _cmd_hippath=%_bat_file_path% -e _cmd_fileshortname=%_bat_file_short_name% "%gROOT%\_NC_houdini_scripts\_NC_houdini_render.cmd"
	)
	
	IF NOT "%_PLUG_HTOA_NV%"=="NULL" (
		TIMEOUT /T 5 /NOBREAK
		wmic process where name="rlm.exe" delete
	)
	goto Endof

:CONV_VAE_TO_MAJ
	for %%z in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) DO CALL SET %~1=%%%~1:%%z=%%z%%
	goto Endof
:Endof