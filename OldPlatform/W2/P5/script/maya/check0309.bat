@echo off

echo --------------------------------------
echo render4.bat Running at %COMPUTERNAME%
netstat
echo 
echo --------------------------------------

set global_config=\\10.50.8.16\p\script\_NC_Settings
set _NC_clients_config_ini=%global_config%\_NC_clients_configs\_NC_clients_config_ini.bat
echo global_config=%global_config%


set userId=%~1
set taskId=%~2
set maya=%~3
set proj=%~4
set mb=%~5
set txt=%~6

set mel=C:/script/maya/checkNet.mel

echo ----------------
echo userId: 	%userId%
echo taskId: 	%taskId%
echo maya: 	%maya%
echo proj:	%proj%
echo mb:	%mb%
echo txt:	%txt%
echo ----------------

if "%userId%"=="62123" goto render_62123
if "%userId%"=="20233" goto Analyse_20233
if "%userId%"=="14484" goto Analyse_14484
if "%userId%"=="119736" goto Analyse_18445

if "%userId%"=="163182" goto Analyse_163182
goto render_default

:Analyse_18445
	echo ---
	echo Render Configure Applied @ 18445
	echo Render Configure Updated - 001 by Neil @ 2014/5/21
	echo Render Configure Updated - mel Script Added by Neil @ 2014/5/21
	echo Render Configure Updated - Platform prerender script disabled by Neil @ 2014/5/21
	echo Render Configure Updated - Custom prerender script enable by Neil @ 2014/6/23
	echo Render Configure Updated - Scritp Root by Neil @ 2014/8/5
	echo Render Configure Upadted - Custom prerender script - import all references before render by Neil @ 2014/09/04
	echo Render Configure Upadted - hotOceanDeformer.dll included @ 2014/09/12
	echo Render Configure Updated - general update @ 20141125

	echo Dir mapping...
	echo file-cluster@\\10.50.24.10\d\inputdata5\119500\119736\file-cluster
	echo 10.50.24.10 file-cluster>>C:\Windows\system32\drivers\etc\hosts
	
	if "%userId%"=="18445" set projPath=%proj:18445\\=18445\%
	if "%userId%"=="18445" set mayaFile=%mb:18445\\=18445\%
	if "%userId%"=="119736" set projPath=%proj:119736\\=119736\%
	if "%userId%"=="119736" set mayaFile=%mb:119736\\=119736\%
	set projPath=%projPath:\=/%
	set mayaFile=%mayaFile:\=/%

	set MAYA_SCRIPT_PATH=%global_config%\_NC_maya_scripts\nCZSupport;%global_config%\_NC_maya_scripts\_18445\scripts
	set MAYA_PLUG_IN_PATH=%global_config%\_NC_maya_scripts\_18445\plugins
	set PATH=%MAYA_PLUG_IN_PATH%;%PATH%
	
	"%maya%" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");"
	goto end

:Analyse_20233
	echo Jiangdi Configure Applied @ 20233
	echo Analyse Configure Updated - 001 by Neil @ 7/7/2014
	
	set _bat_cid=%userId%
	set _bat_cgv=Maya2014
	set _bat_file=%mb%
	set _bat_file=%_bat_file:\\=\%
	set _bat_null=null	
	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%
	
	"%maya%" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");"
	net use * /delete /y
	goto Exit_1
	
:Analyse_163182
	echo TurtleinMotion Configure Applied @ 163182
	echo Analyse Configure Updated - 001 by Neil @ 4/1/2014

	set projPath=%proj:\=/%
	set mayaFile=%mb:\=/%

	net use * /delete /y
	net use P: \\10.50.1.4\d\inputData\maya\163000\163182\render /persistent:yes

	echo BAT info - License initializing...
	xcopy /y /e /v "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\license\MentalCore" "C:\MentalCore\"

	echo BAT info - Modules needed initializing...
	xcopy /y /e /v "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\modules\MentalCore" "C:\Program Files\Autodesk\Maya2013\modules\MentalCore\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\include\MentalCore.mi" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\include\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\include\MentalCore_Phenom.mi" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\include\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\MentalCore.dll" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\modules\mentalcore.mod" "C:\Program Files\Autodesk\Maya2013\modules\"
	
	"%maya%" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");"
	net use * /delete /y
	goto Exit_1

:Analyse_14484
	echo DancingDigital Configure Applied @ 14484
	echo Analyse Configure Updated - 001 by Neil @ 2014/3/25

	set projPath=%proj:\=/%
	set mayaFile=%mb:\=/%

	net use * /delete /y
	net use R: \\10.50.1.4\d\inputData\maya\14000\14484\Projects /persistent:yes

	echo BAT info - License initializing...
	xcopy /y /e /v "\\10.50.1.4\d\inputData\maya\14000\14484\Support\MentalCore_1.5v1\license\MentalCore" "C:\MentalCore\"

	echo BAT info - Modules needed initializing...
	xcopy /y /e /v "\\10.50.1.4\d\inputData\maya\14000\14484\Support\MentalCore_1.5v1\modules\MentalCore" "C:\Program Files\Autodesk\Maya2013\modules\MentalCore\"
	xcopy /y /f  "\\10.50.1.4\d\inputData\maya\14000\14484\Support\MentalCore_1.5v1\mentalray\shaders\include\MentalCore.mi" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\include\"
	xcopy /y /f  "\\10.50.1.4\d\inputData\maya\14000\14484\Support\MentalCore_1.5v1\mentalray\shaders\include\MentalCore_Phenom.mi" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\include\"
	xcopy /y /f  "\\10.50.1.4\d\inputData\maya\14000\14484\Support\MentalCore_1.5v1\mentalray\shaders\MentalCore.dll" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\"
	xcopy /y /f  "\\10.50.1.4\d\inputData\maya\14000\14484\Support\MentalCore_1.5v1\modules\mentalcore.mod" "C:\Program Files\Autodesk\Maya2013\modules\"

	"%maya%" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");"
	
	net use * /delete /y
	goto Exit_1

:render_62123
	if "%maya%"=="C:/Program Files/Autodesk/Maya2012/bin/maya.exe" goto render_62123_maya2012
	if "%maya%"=="C:/Program Files/Autodesk/Maya2013/bin/maya.exe" goto render_62123_maya2013
	goto Exit_0

:render_62123_maya2012
	echo render_62123_maya2012
	set MAYA_SCRIPT_PATH=\\10.50.1.3\pool\script\maya\nCZSupport;C:\Program Files\JoeAlter\shaveHaircut\maya2012\scripts;C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\scripts;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\scripts\AETemplates;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\scripts\others
	set MAYA_PLUG_IN_PATH=C:\Program Files\JoeAlter\shaveHaircut\maya2012\plug-ins;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\bin\plug-ins
	set MI_CUSTOM_SHADER_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\ushaders_p_3.3.3_maya_win64\Maya2012\include;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\mentalray\include
	set MI_LIBRARY_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\lib;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\mentalray\lib
	set XBMLANGPATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\icons;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\icons
	set RENDER_ROOT=C:\Program Files\Autodesk\Maya2012\bin
	set path=%RENDER_ROOT%;%path%
	"%RENDER_ROOT%\maya.exe" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");" -log "c:/temp/hellokitty.txt"
	goto Exit_1

:render_62123_maya2013
	echo render_62123_maya2013
	set MAYA_SCRIPT_PATH=\\10.50.1.3\pool\script\maya\nCZSupport;C:\Program Files\JoeAlter\shaveHaircut\maya2013\scripts;C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\scripts;
	set MAYA_PLUG_IN_PATH=C:\Program Files\JoeAlter\shaveHaircut\maya2013\plug-ins;
	set MI_CUSTOM_SHADER_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\include;
	set MI_LIBRARY_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\lib;
	set XBMLANGPATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\icons;
	set RENDER_ROOT=C:\Program Files\Autodesk\Maya2013\bin
	set path=%RENDER_ROOT%;%path%
	"%RENDER_ROOT%\maya.exe" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");" -log "c:/temp/hellokitty.txt"
	rem "%RENDER_ROOT%/maya.exe" -proj "//10.50.1.4/dd/inputData/maya/62123/render" -prompt -command "source \"//10.50.1.3/pool/script/maya/nCZSupport/checkNet_TEST.mel\"" -file "//10.50.1.4/dd/inputData/maya/62123/render/scenes/aaa.mb"
	goto Exit_1


:render_default
	echo render_default
	"%maya%" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");"
	rem D:\Programs\Autodesk\Maya2011\bin\maya.exe -prompt -command "source \"D:/Tech/MEL/Scripts/checkNet.mel\";checkNet(\"F:/Test\",\"F:/Test/scenes/x.ma\",\"d:/tt/x.txt\");"
	goto Exit_1

:Exit_0
echo No configuration applied

:Exit_1
echo Configuration applied