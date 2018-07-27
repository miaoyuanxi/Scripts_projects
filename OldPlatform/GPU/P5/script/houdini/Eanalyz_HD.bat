@echo off
	set gROOT=\\10.50.1.20\td\_NC_Settings
	set _NC_clients_config_ini=%gROOT%\_NC_clients_configs\_NC_clients_config_ini.bat
	echo gROOT = %gROOT%

	set _bat_cid=%~1
	echo _bat_cid = %_bat_cid%

	set _bat_tid=%~2
	echo _bat_tid = %_bat_tid%

	set _bat_cgv=%~3
	echo _bat_cgv = %_bat_cgv%

	set _bat_file=%~4
	set _bat_file=%_bat_file:\=/%
	set _bat_file=%_bat_file%
	echo _bat_file = %_bat_file%
	
	SET _RENDER_FILENAME=%~dpn4__%_bat_tid%%~x4
	SET _bat_file_path=%~dp4
	SET _bat_file_path=%_bat_file_path:\=/%
	echo _bat_file_path=%_bat_file_path%
	
	set _bat_inf=%~5
	set _bat_inf=%_bat_inf:\=/%

	set _p6=%~6
	set _p7=%~7
	set _p8=%~8
	set _p9=%~9
	
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
			XCOPY /V /Q /Y /E "\\10.50.242.1\td\plugins\houdini\lic\15\sesinetd.exe" "%_SYSTEM_RUN_PATH%\"
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
			XCOPY /V /Q /Y /E "\\10.50.242.1\td\plugins\houdini\lic\15\hserver.exe" "%_SYSTEM_RUN_PATH%\"
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
			%_HSERVERNAME% -S %_HSERVERIP%
		)

	ECHO.
    ECHO.
	ECHO SOURCING SERVER SETUP ...
	SET _APP_NAME=Houdini
	SET _PLUG_HTOA_NV=NULL
    SET _bat_ext=""
	SET _APPS_FIXED_DIR=td\apps\%_APP_NAME%
	SET _PLUGINS_FIXED_DIR=td\plugins\%_APP_NAME%
	XCOPY /V /Q /Y /E "\\10.50.242.1\td\support\tools\7_zip\*" "%_SYSTEM_RUN_PATH%\"
	echo Calling bat script ...
	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%
	SET _RESOURCE_SERVER_ROOT=\\10.50.242.1
	SET _RESOURCE_LOCAL_ROOT=D:
	SET /A NUM=%RANDOM% %%2
	IF "%NUM%"=="0" SET _RESOURCE_SERVER_ROOT=\\10.50.242.6
		ECHO SOURCING FROM SERVER %_RESOURCE_SERVER_ROOT%
	SET _APP_SERVER_RAR=%_RESOURCE_SERVER_ROOT%\%_APPS_FIXED_DIR%\%_APP_NAME%-%_bat_cgv%.7z
	SET _APP_LOCAL_PATH=%_RESOURCE_LOCAL_ROOT%\%_APPS_FIXED_DIR%
	SET _APP_LOCAL_RUN_PATH=%_APP_LOCAL_PATH%\%_APP_NAME%-%_bat_cgv%
	
    ECHO.
    ECHO.
	ECHO START INSTALLING/UPDATING @ %_APP_NAME%-%_bat_cgv% ...
	ECHO 	COPY START @ %DATE%-%TIME%
	XCOPY /V /Q /Y "%_APP_SERVER_RAR%" "%_APP_LOCAL_PATH%\"
	ECHO 	EXTRACT START @ %DATE%-%TIME%
	7z x -y -aos "%_APP_LOCAL_RUN_PATH%.7z" -o"%_APP_LOCAL_RUN_PATH%"
	DEL /Q "%_APP_LOCAL_RUN_PATH%.7z"
    ECHO 	APPS COPY CLEAN UP DONE @ %DATE%-%TIME%
    
    
    SET _PLUGINS_SERVER_RAR=%_RESOURCE_SERVER_ROOT%\%_PLUGINS_FIXED_DIR%\%_PLUG_HTOA_NV%.7z
    SET _PLUGINS_LOCAL_PATH=%_RESOURCE_LOCAL_ROOT%\%_PLUGINS_FIXED_DIR%
    SET _PLUGINS_LOCAL_RUN_PATH=%_PLUGINS_LOCAL_PATH%\%_PLUG_HTOA_NV%
    SET _PATH_ENV_NV=13.0
    IF NOT X%_bat_cgv:14.0=%==X%_bat_cgv% SET _PATH_ENV_NV=14.0
    IF NOT X%_bat_cgv:15.0=%==X%_bat_cgv% SET _PATH_ENV_NV=15.0
    IF NOT X%_bat_cgv:15.5=%==X%_bat_cgv% SET _PATH_ENV_NV=15.5
    SET _PATH_LOCAL_ENV=C:/Users/%username%/Documents/%_APP_NAME%%_PATH_ENV_NV%
    SET _SOURCE_ENV_NV=%_PLUGINS_LOCAL_RUN_PATH%/houdini.env
    SET _PATH_LOCAL_ENV=%_PATH_LOCAL_ENV:/=\%
    SET _SOURCE_ENV_NV=%_SOURCE_ENV_NV:/=\%
    IF NOT "%_PLUG_HTOA_NV%"=="NULL" (
        ECHO.
        ECHO.
        ECHO INSTALLING/UPDATING %_PLUG_HTOA_NV% ...
        ECHO _PLUG_HTOA_NV=%_PLUG_HTOA_NV%
        ECHO _PLUGINS_SERVER_RAR=%_PLUGINS_SERVER_RAR%
        ECHO _PLUGINS_LOCAL_PATH=%_PLUGINS_LOCAL_PATH%
        ECHO _PLUGINS_LOCAL_RUN_PATH=%_PLUGINS_LOCAL_RUN_PATH%
        ECHO 	%_PLUG_HTOA_NV% COPY START @ %DATE%-%TIME%
        XCOPY /V /Q /Y "%_PLUGINS_SERVER_RAR%" "%_PLUGINS_LOCAL_PATH%\"
        ECHO 	%_PLUG_HTOA_NV% EXTRACT START @ %DATE%-%TIME%
        7z x -y -aos "%_PLUGINS_LOCAL_RUN_PATH%.7z" -o"%_PLUGINS_LOCAL_RUN_PATH%"
        ECHO 	PLUGINS COPY CLEAN UP @ %DATE%-%TIME%
        DEL /Q "%_PLUGINS_LOCAL_RUN_PATH%.7z"
        XCOPY /V /Q /Y "%_SOURCE_ENV_NV%" "%_PATH_LOCAL_ENV%\"
		wmic process where name="JGS_mtoa_licserver.exe" delete
		wmic process where name="rlm.exe" delete
		TIMEOUT /T 5 /NOBREAK
		start %_PLUGINS_LOCAL_RUN_PATH%\AMPED\rlm.exe
	)
	
	ECHO.
	ECHO.
	SET _bat_null=null
	SET _APP_LOCAL_RUN_PATH=%_APP_LOCAL_RUN_PATH:\=/%
	SET _PLUGINS_LOCAL_RUN_PATH=%_PLUGINS_LOCAL_RUN_PATH:\=/%
	echo _APP_LOCAL_RUN_PATH=%_APP_LOCAL_RUN_PATH%
	echo _PLUGINS_LOCAL_RUN_PATH=%_PLUGINS_LOCAL_RUN_PATH%
	SET RUN_ROOT=%_APP_LOCAL_RUN_PATH%\bin
	SET PATH=%PATH%;%RUN_ROOT%
	ECHO RUN_ROOT=%RUN_ROOT%
	SET _bat_file=%_bat_file:\=/%
	"%RUN_ROOT%\hbatch.exe" -e _configroots=%gROOT% -e _isrendering=0 -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_hip=%_bat_file% -e _cmd_hippath=%_bat_file_path% -e _cmd_inf=%_bat_inf% "%gROOT%/_NC_houdini_scripts/_NC_houdini_analyze.cmd"
	goto Endof
:CONV_VAE_TO_MAJ
	for %%z in (A B C D E F G H I J K L M N O P Q R S T U V W X Y Z) DO CALL SET %~1=%%%~1:%%z=%%z%%
	goto Endof
:Endof
	echo RenderEnd @ %date%-%time%