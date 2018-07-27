@echo off

echo Erender.bat @ 10.50.1.3/p/script/mentalray running...

set _bat_cid=%~1
set _bat_tid=%~2
set _bat_sf=%~3
set _bat_ef=%~4
set _bat_bf=%~5
set _bat_cgv=%~6
set _bat_pro=%~7
set _bat_pro=%_bat_pro:\=/%
set _bat_render_file=%~8
set _bat_render_file=%_bat_render_file:\=/%
set _bat_rd=%~9
set _bat_rd=%_bat_rd:\=/%


echo parameter list:
echo _bat_cid		---  %_bat_cid%
echo _bat_tid		---  %_bat_tid%
echo _bat_sf		---  %_bat_sf%
echo _bat_ef		---  %_bat_ef%
echo _bat_bf		---  %_bat_bf%
echo _bat_cgv		---  %_bat_cgv%
echo _bat_pro		---  %_bat_pro%
echo _bat_render_file	---  %_bat_render_file%
echo _bat_rd		---  %_bat_rd%


echo Projecting...
if "%_bat_cid%"=="63200" goto render_63200
if "%_bat_cid%"=="13450" goto render_13450
if "%_bat_cid%"=="160515" goto render_160515
if "%_bat_cid%"=="19316" goto render_19316

goto RENDER_DEFAULT

:RENDER_DEFAULT
	echo Default Configure Applied
	echo Render Configure Updated - 001 by Neil @ 2014/3/31
	set MI_ROOT=//10.50.1.3/p/script/mentalray/apps/%_bat_cgv%/bin
	"%MI_ROOT%/ray.exe" -memory 100000 -finalgather_display on -task_size 64 -v 5 -x on -render %_bat_sf% %_bat_ef% %_bat_bf% -file_dir %_bat_rd% %_bat_render_file%
	goto end

:render_19316
	echo RENDER_19316 - BG_GS - MentalRay Standalone - China
	echo MI_ROOT UPDATED BY NEIL

	net use * /delete /y
	net use Z: \\10.50.1.4\d\inputData\mentalray\19000\19316\Z /persistent:yes
	net use S: \\10.50.1.4\d\inputData\mentalray\19000\19316\s /persistent:yes
	net use X: \\10.50.1.4\d\inputData\mentalray\19000\19316\X /persistent:yes
	net use M: \\10.50.1.4\d\inputData\mentalray\19000\19316\M /persistent:yes
	set MI_ROOT=\\10.50.1.3\pool\script\mentalray\main\mrstand3.8.1-adsk2011\bin
	set MI_RAY_INCPATH=S:/netplugins/mental3.8.1/mi;S:/netplugins/maya2010/modules/eye/mentalray/mi;S:/netplugins/maya2010/modules/forestGeoShader/mentalray/mi;S:/netplugins/maya2010/modules/hair/mentalray/mi;S:/netplugins/maya2010/modules/particleTools/mentalray/mi;S:/netplugins/maya2010/modules/shaders_dz/mentalray/mi;S:/netplugins/maya2010/modules/shaders_p/mentalray/mi;S:/netplugins/maya2010/modules-external/thirdPartyShaders/mentalray/mi

	set MI_LIBRARY_PATH=S:/netplugins/mental3.8.1/bin;S:/netplugins/maya2010/modules/eye/mentalray/bin;S:/netplugins/maya2010/modules/forestGeoShader/mentalray/bin;S:/netplugins/maya2010/modules/hair/mentalray/bin;S:/netplugins/maya2010/modules/particleTools/mentalray/bin;S:/netplugins/maya2010/modules/shaders_dz/mentalray/bin;S:/netplugins/maya2010/modules/shaders_p/mentalray/bin;S:/netplugins/maya2010/modules-external/thirdPartyShaders/mentalray/bin

	set path=%MI_ROOT%;%PATH%
	set /a sf=%_bat_sf%*2-1
	set /a ef=%_bat_ef%*2

	IF NOT EXIST C:\Temp\ md C:\Temp

	"%MI_ROOT%/ray.exe" -memory 100000 -finalgather_display on -task_size 64 -v 5 -x on -render %_bat_sf% %_bat_ef% %_bat_bf% -file_dir %_bat_rd% %_bat_render_file%
	net use * /delete /y
	goto end

:render_63200
	echo Config_63200 - nagendraprasad - MentalRay Standalone - India
	net use * /delete /y
	net use S: \\10.50.1.4\dd\inputData\mentalray\63200\nagendraprasad\S /persistent:yes
	net use X: \\10.50.1.4\dd\inputData\mentalray\63200\nagendraprasad\X /persistent:yes
	net use M: \\10.50.1.4\dd\inputData\mentalray\63200\nagendraprasad\M /persistent:yes
	set MI_ROOT=\\10.50.1.3\pool\script\mentalray\main\mrstand3.8.1-adsk2011\bin
	set MI_RAY_INCPATH=S:/netplugins/mental3.8.1/mi;S:/netplugins/maya2010/modules/eye/mentalray/mi;S:/netplugins/maya2010/modules/forestGeoShader/mentalray/mi;S:/netplugins/maya2010/modules/hair/mentalray/mi;S:/netplugins/maya2010/modules/shaders_dz/mentalray/mi;S:/netplugins/maya2010/modules/shaders_p/mentalray/mi;S:/netplugins/maya2010/modules-external/thirdPartyShaders/mentalray/mi
	set MI_LIBRARY_PATH=S:/netplugins/mental3.8.1/bin;S:/netplugins/maya2010/modules/eye/mentalray/bin;S:/netplugins/maya2010/modules/forestGeoShader/mentalray/bin;S:/netplugins/maya2010/modules/hair/mentalray/bin;S:/netplugins/maya2010/modules/shaders_dz/mentalray/bin;S:/netplugins/maya2010/modules/shaders_p/mentalray/bin;S:/netplugins/maya2010/modules-external/thirdPartyShaders/mentalray/bin
	set path=%MI_ROOT%;%PATH%
	set /a sf=%_bat_sf%*2-1
	set /a ef=%_bat_ef%*2

	IF NOT EXIST C:\Temp\ md C:\Temp

	"%MI_ROOT%/ray.exe" -memory 100000 -finalgather_display on -task_size 64 -v 5 -x on -render %_bat_sf% %_bat_ef% %_bat_bf% -file_dir %_bat_rd% %_bat_render_file%
	net use * /delete /y
	goto end

:render_160515
	echo Glukoza Configure Applied @ 160515
	echo Render Configure Updated - 001 by Neil @ 2014/3/31

	net use * /delete /y
	net use S: \\10.50.1.4\dd\inputData\mentalray\160515\Glukoza\S /persistent:yes
	net use X: \\10.50.1.4\dd\inputData\mentalray\160515\Glukoza\X /persistent:yes
	net use M: \\10.50.1.4\dd\inputData\mentalray\160515\Glukoza\M /persistent:yes

	IF NOT EXIST C:\Temp\ md C:\Temp

	set MI_ROOT=//10.50.1.3/p/script/mentalray/apps/%_bat_cgv%/bin

	set netplugins_include=mental3.8.1
	if not x%_bat_cgv:3.8.1=%==x%_bat_cgv% set netplugins_include=mental3.8.1
	if not x%_bat_cgv:3.9.1=%==x%_bat_cgv% set netplugins_include=mental3.9.1
	if not x%_bat_cgv:3.10.1=%==x%_bat_cgv% set netplugins_include=mental3.10.1
	if not x%_bat_cgv:3.11.1=%==x%_bat_cgv% set netplugins_include=mental3.11.1

	echo cgv = %_bat_cgv%
	echo netplugins_include = %netplugins_include%

	set MI_RAY_INCPATH=S:/netplugins/%netplugins_include%/mi;S:/netplugins/maya2010/modules/eye/mentalray/mi;S:/netplugins/maya2010/modules/forestGeoShader/mentalray/mi;S:/netplugins/maya2010/modules/hair/mentalray/mi;S:/netplugins/maya2010/modules/shaders_dz/mentalray/mi;S:/netplugins/maya2010/modules/shaders_p/mentalray/mi;S:/netplugins/maya2010/modules-external/thirdPartyShaders/mentalray/mi
	set MI_LIBRARY_PATH=S:/netplugins/%netplugins_include%/bin;S:/netplugins/maya2010/modules/eye/mentalray/bin;S:/netplugins/maya2010/modules/forestGeoShader/mentalray/bin;S:/netplugins/maya2010/modules/hair/mentalray/bin;S:/netplugins/maya2010/modules/shaders_dz/mentalray/bin;S:/netplugins/maya2010/modules/shaders_p/mentalray/bin;S:/netplugins/maya2010/modules-external/thirdPartyShaders/mentalray/bin	
	
	set path=%MI_ROOT%;%PATH%
	set /a sf=%_bat_sf%*2-1
	set /a ef=%_bat_ef%*2

	echo "%MI_ROOT%/ray.exe" -finalgather_display on -v 5 -x on -render %sf% %ef% %_bat_bf% -file_dir %_bat_rd% %_bat_render_file%
	net use * /delete /y
	goto end

:render_13450
	echo 13450 - Tani - MentalRay Standalone - China
	net use * /delete /y
	net use S: \\10.50.1.4\dd\inputData\mentalray\13450\Tani\S /persistent:yes
	net use X: \\10.50.1.4\dd\inputData\mentalray\13450\Tani\X /persistent:yes
	net use M: \\10.50.1.4\dd\inputData\mentalray\13450\Tani\M /persistent:yes
	set MI_ROOT=\\10.50.1.3\pool\script\mentalray\main\mrstand3.8.1-adsk2011\bin
	set MI_RAY_INCPATH=S:/netplugins/mental3.8.1/mi;S:/netplugins/maya2010/modules/eye/mentalray/mi;S:/netplugins/maya2010/modules/forestGeoShader/mentalray/mi;S:/netplugins/maya2010/modules/hair/mentalray/mi;S:/netplugins/maya2010/modules/shaders_dz/mentalray/mi;S:/netplugins/maya2010/modules/shaders_p/mentalray/mi;S:/netplugins/maya2010/modules-external/thirdPartyShaders/mentalray/mi
	set MI_LIBRARY_PATH=S:/netplugins/mental3.8.1/bin;S:/netplugins/maya2010/modules/eye/mentalray/bin;S:/netplugins/maya2010/modules/forestGeoShader/mentalray/bin;S:/netplugins/maya2010/modules/hair/mentalray/bin;S:/netplugins/maya2010/modules/shaders_dz/mentalray/bin;S:/netplugins/maya2010/modules/shaders_p/mentalray/bin;S:/netplugins/maya2010/modules-external/thirdPartyShaders/mentalray/bin
	set path=%MI_ROOT%;%PATH%

	set /a sf=%_bat_sf%*2-1
	set /a ef=%_bat_ef%*2

	echo making c:\temp
	IF NOT EXIST c:\Temp\ md c:\Temp
	echo finished making c:\temp

	echo _bat_sf		---  %sf%
	echo _bat_ef		---  %ef%

	"%MI_ROOT%\ray.exe" -memory 100000 -finalgather_display on -task_size 64 -v 4 -render %sf% %ef% %_bat_bf% -file_dir %_bat_rd% %_bat_render_file%
	net use * /delete /y
	goto end	


:end
echo "Rendering Completed!"