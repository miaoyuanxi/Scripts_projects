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
set render=%~3
set txt=%~4
set startframe=%~5
set endframe=%~6
set byframe=%~7
set proj=%~8
set mb=%~9


shift 
set renderer=%~9
set mel=c:/script/maya/maya_preRender.mel
set rd=c:/enfwork/%taskId%/output/


echo task info:
	echo	userId:		%userId%
	echo	taskId:		%taskId%
	echo	render:		%render%
	echo	txt:	%txt%
	echo	startframe:	%startframe%
	echo	endframe:	%endframe%
	echo	byframe:	%byframe%
	echo	proj:	%proj%
	echo	mb:	%mb%
	echo	renderer:	%renderer%

if "%userId%"=="18305" net use W: \\10.50.1.4\dd\inputData\maya\18305\project /persistent:yes

if "%userId%"=="20233" goto render_20233
if "%userId%"=="163455" goto render_163455
if "%userId%"=="163182" goto render_163182
if "%userId%"=="53" goto render_53
if "%userId%"=="14484" goto render_14484
if "%userId%"=="63121" goto render_63121
if "%userId%"=="300050" goto render_300050

if "%userId%"=="18445" goto render_18445
if "%userId%"=="119736" goto render_18445
if "%userId%"=="119362" goto render_18445
if "%userId%"=="119736" goto render_18445

if "%userId%"=="16630" goto render_16630
if "%userId%"=="60987" goto render_60987
if "%userId%"=="163237" goto render_163237
if "%userId%"=="163260" goto render_163260
if "%userId%"=="19514" goto render_19514
if "%userId%"=="161122" goto render_161122
if "%userId%"=="161188" goto render_161188
if "%userId%"=="19419" goto render_19419
if "%userId%"=="300127" goto render_300127
if "%userId%"=="100045" goto render_100045
if "%userId%"=="300112" goto render_300112
if "%renderer%"=="maxwell" goto render3
if "%renderer%"=="afterstudios" goto render_62123
if "%render%"=="C:/Program Files/Autodesk/Maya8.5/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2008/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2009/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2010/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2011/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2012/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2013/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2013.5/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2014/bin/Render.exe" goto render2


:render1
	"%render%" -s %startframe% -e %endframe% -b %byframe% -r mr -art -aml -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% "%mb%"  
	goto end

:render2
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
	goto end

:render3
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -r maxwell "%mb%"  
	goto end

:render_300127
	xcopy /y /f "\\10.50.10.229\renderscene\zhaoxiaofei\hqAnimation\maya.env" "C:\users\enfuzion\Documents\maya\2013-x64"
	xcopy /y /f "\\10.50.10.229\renderscene\zhaoxiaofei\hqAnimation\mtoa.mod" "C:\users\enfuzion\Documents\maya\2013-x64\modules"
	xcopy /y /f "\\10.50.10.229\renderscene\zhaoxiaofei\hqAnimation\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2013-x64\prefs"
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"
goto end
:render_20233
	echo Jiangdi @ 20233
	echo Render Configure Updated - 001 - Initialized by Neil @ 2014/7/4
	echo Render Configure Updated - 002 - _NC_clients_config_ini by Neil @ 2014/7/7
	echo Render Configure Updated - 003 - Disable default pre-mel script by Neil @ 2014/7/22
	
	set _bat_cid=%userId%
	set _bat_cgv=Maya2014
	set _bat_file=%mb%
	set _bat_null=null
	
	echo rd=%rd%
	
	call %_NC_clients_config_ini% %_bat_cid% %_bat_cgv% %_bat_file% %_bat_null%
	
	"%render%" -s %startframe% -e %endframe% -b %byframe% -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"
	goto end	

:render_161188
	echo yidong @ 161188
	set exocortex_LICENSE=C:\rlm\exocortex.lic
	xcopy /y /f "C:\PLUGINS\maya\arnold\replace\maya2012\0.25.2\maya.env" "C:\users\enfuzion\Documents\maya\2012-x64"
	xcopy /y /f "C:\PLUGINS\maya\arnold\replace\maya2012\0.25.2\modules\mtoa.mod" "C:\users\enfuzion\Documents\maya\2012-x64\modules"
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
	goto end
	
	
:render_19419
	if exist "C:\Program Files\Autodesk\Maya2013\modules\MentalCore" rd /s /q "C:\Program Files\Autodesk\Maya2013\modules\MentalCore"
	xcopy /y /f /e /v "\\10.50.10.229\renderscene\zhaoxiaofei\MentalCore1.5\Maya2013" "C:\Program Files\Autodesk\Maya2013\"
	xcopy /y /f /e /v "\\10.50.10.229\renderscene\zhaoxiaofei\MentalCore1.5\lic" "C:\MentalCore\"
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
	goto end
	
:render_100045
	xcopy /y /f "\\10.50.1.229\renderscene\zhaoxiaofei\100045\Maya.env" "C:\users\enfuzion\Documents\maya\2014-x64\"
	xcopy /y /f "\\10.50.1.229\renderscene\zhaoxiaofei\100045\mtoa.mod" "C:\users\enfuzion\Documents\maya\2014-x64\modules\"
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%" 
	goto end
	
:render_60987
	echo DancingDigital Configure Applied @ 163237
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:rt 24 "%mb%"
	goto end

:render_19514
	echo Configure Applied @ 19514
	xcopy /y /f  "\\10.50.10.229\soft\zxf\replace\2013\1.0.0Release\Maya.env" "C:\users\enfuzion\Documents\maya\2013-x64\"
	xcopy /y /f  "\\10.50.10.229\soft\zxf\replace\2013\1.0.0Release\modules\mtoa.mod" "C:\users\enfuzion\Documents\maya\2013-x64\modules\"
	xcopy /y /v /e "\\10.50.10.229\soft\zxf\2013_v1.0.0_Release" "C:\solidangle\mtoadeploy\2013_v1.0.0_Release\"
	xcopy /y /v /e "\\10.50.10.229\renderscene\zhaoxiaofei\soft\arnoldShader\scripts" "C:\solidangle\mtoadeploy\2013_v1.0.0_Release\scripts\mtoa\ui\ae\"
	xcopy /y /v /e "\\10.50.10.229\renderscene\zhaoxiaofei\soft\arnoldShader\shaders" "C:\solidangle\mtoadeploy\2013_v1.0.0_Release\shaders\"
	xcopy /y /f "\\10.50.10.229\renderscene\zhaoxiaofei\soft\arnoldShader\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2013-x64\prefs\"

	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
goto end

:render_161122	
	echo Betop3d_h Configure Applied @ 161122
	echo Render Configure Updated - 001 - Initialized by Neil @ 2014/3/21
	echo Render Configure Updated - 002 - E Drive Mapping Added in by Neil @ 2014/4/15
	echo Render Configure Updated - 003 - Project DIR Fixed Before Mapping Update by Neil @ 4/16/2014
	echo Render Configure Updated - 004 - Maya Full File Name Fixed Before Rendering Update by Neil @ 4/16/2014


	set projPath=%proj:161122\\=161122\%
	set mayaFile=%mb:161122\\=161122\%
	set projPath=%projPath:\=/%
	set mayaFile=%mayaFile:\=/%

	echo Fixed projPath=%projPath%
	echo Fixed mayaFile=%mayaFile%

	set mel=//dataip/p/script/maya/maya_preRender.mel
	set peregrinel_LICENSE=C:\rlm\peregrinel.lic
	set MTOA_PROCEDURAL_PATH=C:\Yeti1.3.5Maya2012\bin

	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\yeti_135_w_x64\rlm\peregrinel.lic" "C:\rlm\" 
	xcopy /y /e /v "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\yeti_135_w_x64\Yeti1.3.5Maya2012" "C:\Yeti1.3.5Maya2012\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\yeti_135_w_x64\Yeti1.3.5Maya2012\pgYetiMaya.mod" "C:\Program Files\Autodesk\Maya2012\modules\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\yeti_135_w_x64\Yeti1.3.5Maya2012\bin\pgYetiArnold.dll" "C:\solidangle\mtoadeploy\2012_1.0.0.1\shaders\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\yeti_135_w_x64\Yeti1.3.5Maya2012\plug-ins\pgYetiArnoldMtoa.dll" "C:\solidangle\mtoadeploy\2012_1.0.0.1\extensions\"
	xcopy /y /e /v "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\yeti_135_w_x64\maya2012" "C:\Program Files\Autodesk\Maya2012\"
	xcopy /y /f /v "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\yeti_135_w_x64\maya2013" "C:\Program Files\Autodesk\Maya2013\"

	xcopy /y /e /v "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\2014_v1.0.0_Release" "C:\solidangle\mtoadeploy\2014_v1.0.0_Release\"
	xcopy /y /e /v "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\arnold\2012_1.0.0.1" "C:\solidangle\mtoadeploy\2012_1.0.0.1\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2012-x64\prefs\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\2014_v1.0.0_Release\mtoa.mod" "C:\users\enfuzion\Documents\maya\2014-x64\modules\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\arnold\2012_1.0.0.1_env\Maya.env" "C:\users\enfuzion\Documents\maya\2012-x64\"
	xcopy /y /f  "\\10.50.100.1\d\inputdata\maya\161000\161122\Support\arnold\2012_1.0.0.1_env\mtoa.mod" "C:\users\enfuzion\Documents\maya\2012-x64\modules\"

	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%projPath%\",\"%txt%\",\"%startframe%\");" -proj "%projPath%" -rd %rd% -mr:art -mr:aml "%mayaFile%"  
	
	net use * /delete /y
	goto end

:render_163237
	echo DancingDigital Configure Applied @ 60987
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:rt 24 "%mb%"
	goto end

:render_163260
	echo DancingDigital Configure Applied @ 163260
	set GLM_CROWD_HOME=C:\Program Files\Golaem\GolaemCrowd-3.1.0.1-Maya2014
	set MAYA_MODULE_PATH=%GLM_CROWD_HOME%;%MAYA_MODULE_PATH%
	set PATH=%GLM_CROWD_HOME%\bin;%PATH%;%SystemRoot%;%SystemRoot%\system;
	set ARNOLD_PROCEDURAL_PATH=%GLM_CROWD_HOME%\procedurals
	set ARNOLD_PLUGIN_PATH=%GLM_CROWD_HOME%\shaders;%ARNOLD_PLUGIN_PATH%
	set MI_CUSTOM_SHADER_PATH=%GLM_CROWD_HOME%\procedurals\;%MI_CUSTOM_SHADER_PATH%
	set VRAY_PLUGINS_x64=%GLM_CROWD_HOME%\procedurals;%VRAY_PLUGINS_x64%
	setlocal enabledelayedexpansion
	set VRAY_FOR_MAYA%MAYA_VERSION%_PLUGINS_x64=%GLM_CROWD_HOME%\procedurals;!VRAY_FOR_MAYA%MAYA_VERSION%_PLUGINS_x64!
	set VRAY_FOR_MAYA_SHADERS=%GLM_CROWD_HOME%\shaders;%VRAY_FOR_MAYA_SHADERS%

	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"
	goto end


:render_53
	echo DancingDigital Configure Applied @ 53
	set GLM_CROWD_HOME=C:\Program Files\Golaem\GolaemCrowd-3.1.0.1-Maya2014
	set MAYA_MODULE_PATH=%GLM_CROWD_HOME%;%MAYA_MODULE_PATH%
	set PATH=%GLM_CROWD_HOME%\bin;%PATH%;%SystemRoot%;%SystemRoot%\system;
	set ARNOLD_PROCEDURAL_PATH=%GLM_CROWD_HOME%\procedurals
	set ARNOLD_PLUGIN_PATH=%GLM_CROWD_HOME%\shaders;%ARNOLD_PLUGIN_PATH%
	set MI_CUSTOM_SHADER_PATH=%GLM_CROWD_HOME%\procedurals\;%MI_CUSTOM_SHADER_PATH%
	set VRAY_PLUGINS_x64=%GLM_CROWD_HOME%\procedurals;%VRAY_PLUGINS_x64%
	setlocal enabledelayedexpansion
	set VRAY_FOR_MAYA%MAYA_VERSION%_PLUGINS_x64=%GLM_CROWD_HOME%\procedurals;!VRAY_FOR_MAYA%MAYA_VERSION%_PLUGINS_x64!
	set VRAY_FOR_MAYA_SHADERS=%GLM_CROWD_HOME%\shaders;%VRAY_FOR_MAYA_SHADERS%

	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"
	goto end


:render_163455
	echo Kallol Configure Applied @ 163455
	echo Render Configure Updated - 001 - Initialized by Neil @ 4/10/2014

	set projPath=%proj:\=/%
	set mayaFile=%mb:\=/%

	set MAYA_SCRIPT_PATH=\\10.50.1.3\p\script\maya\nCZSupport

	"%render%" -mr:art -mr:aml -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%projPath%\",\"%txt%\",\"%startframe%\");" -proj "%projPath%" -rd %rd% "%mayaFile%"  

	goto end

:render_300112
	echo Kallol Configure Applied @ 300112

	echo Render Configure Updated - 001 - Initialized by liyuguang  @ 7/20/2014
	xcopy /y /v /e "\\10.50.1.229\renderscene\liyuguang\soft_ok\arnold_1.1.03_2015\Program Files\Autodesk" "C:\Program Files\Autodesk\"
	xcopy /y /v /e "\\10.50.1.229\renderscene\liyuguang\soft_ok\arnold_1.1.03_2015\solidangle\mtoadeploy" "C:\solidangle\mtoadeploy\"
	xcopy /y /f "\\10.50.1.229\renderscene\liyuguang\soft_ok\arnold_1.1.03_2015\modules\*.*" "C:\users\enfuzion\Documents\maya\2015-x64\modules\"
	xcopy /y /f "\\10.50.1.229\renderscene\liyuguang\soft_ok\arnold_1.1.03_2015\Maya.env" "C:\users\enfuzion\Documents\maya\2015-x64\"

	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
	
	goto end

:render_163182
	echo TurtleinMotion Configure Applied @ 163182
	echo Render Configure Updated - 001 - Initialized by Neil @ 3/31/2014
	echo Render Configure Updated - 002 - Auto Hyperthread Enable by Neil @ 3/31/2014
	echo Render Configure Updated - 003 - preRender Disable by Neil @ 4/1/2014
	echo Render Configure Updated - 004 - MentalCore License Update by Neil @ 4/2/2014
	echo Render Configure Updated - 005 - MentalCore Double License Update by Neil @ 4/2/2014
	echo Render Configure Updated - 006 - Project DIR as P Drive Update by Neil @ 4/12/2014
	echo Render Configure Updated - 007 - Project DIR Fixed Before Mapping Update by Neil @ 4/12/2014
	echo Render Configure Updated - 008 - Maya Full File Name Fixed Before Rendering Update by Neil @ 4/12/2014

	set MENTALCORE_LICENSE=\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\license\MentalCore

	set projPath=%proj:163182\\=163182\%
	set mayaFile=%mb:163182\\=163182\%

	echo Fixed projPath=%projPath%
	echo Fixed mayaFile=%mayaFile%

	net use * /delete /y
	net use P: "%projPath%" /persistent:yes

	echo BAT info - License initializing...
	xcopy /y /e /v "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\license\MentalCore" "C:\MentalCore\"
	xcopy /y /f "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\license\MentalCore\mentalcore.lic" "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\"

	echo BAT info - Modules needed initializing...
	xcopy /y /e /v "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\modules\MentalCore" "C:\Program Files\Autodesk\Maya2013\modules\MentalCore\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\include\MentalCore.mi" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\include\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\include\MentalCore_Phenom.mi" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\include\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\MentalCore.dll" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\modules\mentalcore.mod" "C:\Program Files\Autodesk\Maya2013\modules\"
	
	"%render%" -mr:art -mr:aml -s %startframe% -e %endframe% -b %byframe% -proj "%projPath%" -rd %rd% "%mayaFile%"  

	goto end

:render_14484
	echo DancingDigital Configure Applied @ 14484
	echo Render Configure Updated - 001 by Neil @ 2014/3/25

	set projPath=%proj:\=/%
	set mayaFile=%mb:\=/%
	set mel=//10.50.100.1/p/script/maya/maya_preRender.mel

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

	
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%projPath%\",\"%txt%\",\"%startframe%\");" -proj "%projPath%" -rd %rd% -mr:art -mr:aml "%mayaFile%"  
	
	net use * /delete /y
	goto end

:render_63121
	echo ---
	echo DOD4 Configure Applied @ 63121
	echo ---

	xcopy /y /f  "\\10.50.100.1\p\script\maya\support\plugins\arnold\2013_1.0.0.1\env\Maya.env" "C:\users\enfuzion\Documents\maya\2013-x64\"
	xcopy /y /f  "\\10.50.100.1\p\script\maya\support\plugins\arnold\2013_1.0.0.1\env\mtoa.mod" "C:\users\enfuzion\Documents\maya\2013-x64\modules\"

	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
	goto end

:render_300050
	echo ---
	echo DOD4 Configure Applied @ 63121
	echo ---

	xcopy /y /f  "\\10.50.10.229\soft\zxf\2013_1.0.0.1\env\Maya.env" "C:\users\enfuzion\Documents\maya\2013-x64\"
	xcopy /y /f  "\\10.50.10.229\soft\zxf\2013_1.0.0.1\env\mtoa.mod" "C:\users\enfuzion\Documents\maya\2013-x64\modules\"

	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
	goto end

:render_18445
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
	echo Dir mapping...
	echo file-cluster@\\10.50.24.10\d\inputdata5\119362\119362\file-cluster
	echo 10.50.24.10 file-cluster>>C:\Windows\system32\drivers\etc\hosts
	
	if "%userId%"=="18445" set projPath=%proj:18445\\=18445\%
	if "%userId%"=="18445" set mayaFile=%mb:18445\\=18445\%
	if "%userId%"=="119736" set projPath=%proj:119736\\=119736\%
	if "%userId%"=="119736" set mayaFile=%mb:119736\\=119736\%
	
	if "%userId%"=="119362" set projPath=%proj:119362\\=119362\%
	if "%userId%"=="119362" set mayaFile=%mb:119362\\=119362\%
	
	set projPath=%projPath:\=/%
	set mayaFile=%mayaFile:\=/%

	set MAYA_SCRIPT_PATH=%global_config%\_NC_maya_scripts\nCZSupport;%global_config%\_NC_maya_scripts\_18445\scripts
	set MAYA_PLUG_IN_PATH=%global_config%\_NC_maya_scripts\_18445\plugins
	set mel=%global_config%\_NC_maya_scripts\nCZSupport\nCMayapreRender.mel
	set mel=%mel:\=/%
	set PATH=%MAYA_PLUG_IN_PATH%;%PATH%
	
	echo Fixed projPath=%projPath%
	echo Fixed mayaFile=%mayaFile%
	echo MAYA_SCRIPT_PATH=%MAYA_SCRIPT_PATH%
	echo MAYA_PLUG_IN_PATH=%MAYA_PLUG_IN_PATH%
	
	"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";nCMayapreRender(\"%projPath%\",\"%rd%\");" -proj "%projPath%" -rd %rd% -mr:art -mr:aml "%mayaFile%"
	goto end

:render_16630
	echo ---
	echo LWJ Configure Applied @ 16630
	echo ---
	set ts=32
	if not x%mb:_ts4_=%==x%mb% set ts=4
	if not x%mb:_ts8_=%==x%mb% set ts=8
	if not x%mb:_ts16_=%==x%mb% set ts=16
	if not x%mb:_ts24_=%==x%mb% set ts=24
	if not x%mb:_ts32_=%==x%mb% set ts=32
	if not x%mb:_ts48_=%==x%mb% set ts=48
	if not x%mb:_ts56_=%==x%mb% set ts=56

	echo	task_size:	%ts%

	net use * /delete /y
	net use Z: \\10.50.1.4\dd\inputData\maya\16630\GoolaCity /persistent:yes
	net use Y: \\10.50.1.4\dd\inputData\maya\16630\GoolaCity\VJ_Studio_Tools\2011\Y /persistent:yes
	set RENDER_ROOT=C:/Program Files/Autodesk/Maya2012/bin
	set PYTHONPATH=//10.50.1.4/dd/inputData/maya/16630/GoolaCity/VJ_Studio_Tools/scripts
	set MAYA_SCRIPT_PATH=//10.50.1.4/dd/inputData/maya/16630/GoolaCity/VJ_Studio_Tools/scripts;C:/Program Files/JoeAlter/shaveHaircut/maya2012/scripts
	set MAYA_PLUG_IN_PATH=C:/Program Files/JoeAlter/shaveHaircut/maya2012/plug-ins;C:/Program Files/3Delight/maya/plugins
	echo set MI_CUSTOM_SHADER_PATH=//10.50.1.4/dd/inputData/maya/16630/GoolaCity/VJ_Studio_Tools/shaders_p_3.3.4_maya_win64/include
	echo set MI_LIBRARY_PATH=//10.50.1.4/dd/inputData/maya/16630/GoolaCity/VJ_Studio_Tools/shaders_p_3.3.4_maya_win64/lib
	set path=//10.50.1.4/dd/inputData/maya/16630/GoolaCity/VJ_Studio_Tools/bin;%RENDER_ROOT%;%path%
	"%render%" -r mr -ts %ts% -mem 60000 -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -art -aml "%mb%"  
	goto end

:render_62123
echo Configure - AfterStudios
set p=%proj:\=/%
set m=%mb:\=/%

echo project____%p%
echo mb file____%m%

if "%render%"=="C:/Program Files/Autodesk/Maya2012/bin/Render.exe" goto render_62123_maya2012
if "%render%"=="C:/Program Files/Autodesk/Maya2013/bin/Render.exe" goto render_62123_maya2013
goto end

	:render_62123_maya2012
	echo render_62123_maya2012
	echo delete prefs
	rd "C:\users\enfuzion\Documents\maya\2012-x64\prefs" /s /q
	set MAYA_SCRIPT_PATH=\\10.50.1.3\pool\script\maya\nCZSupport;C:\Program Files\JoeAlter\shaveHaircut\maya2012\scripts;C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\scripts;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\scripts\AETemplates;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\scripts\others
	set MAYA_PLUG_IN_PATH=C:\Program Files\JoeAlter\shaveHaircut\maya2012\plug-ins;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\bin\plug-ins
	set MI_CUSTOM_SHADER_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\include;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\mentalray\include
	set MI_LIBRARY_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\lib;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\mentalray\lib
	set XBMLANGPATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\icons;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\icons
	set RENDER_ROOT=C:\Program Files\Autodesk\Maya2012\bin
	set path=%RENDER_ROOT%;%path%
	if "%taskId%"=="1000634" goto render_62123_maya2012_hyperThread_disable
	goto render_62123_maya2012_hyperThread_enable
		:render_62123_maya2012_hyperThread_disable
		echo render_62123_maya2012_hyperThread_disable
		"%RENDER_ROOT%\render.exe" -r mr -rt 8 -aml -rnm 0 -proj %proj% -rd %rd% -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");nCMayapreRender(\"%p%\",\"%rd%\")" %m%
		goto end
		

		:render_62123_maya2012_hyperThread_enable
		echo render_62123_maya2012_hyperThread_enable
		"%RENDER_ROOT%\render.exe" -proj %proj% -rd %rd% -s %startframe% -e %endframe% -b %byframe% -mr:art -mr:aml -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");nCMayapreRender(\"%p%\",\"%rd%\")" %m%
		goto end

	:render_62123_maya2013
	echo render_62123_maya2013
	echo delete prefs
	rd "C:\users\enfuzion\Documents\maya\2012-x64\prefs" /s /q
	set MAYA_SCRIPT_PATH=\\10.50.1.3\pool\script\maya\nCZSupport;C:\Program Files\JoeAlter\shaveHaircut\maya2013\scripts;C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\scripts;
	set MAYA_PLUG_IN_PATH=C:\Program Files\JoeAlter\shaveHaircut\maya2013\plug-ins;
	set MI_CUSTOM_SHADER_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\include;
	set MI_LIBRARY_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\lib;
	set XBMLANGPATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\icons;
	set RENDER_ROOT=C:\Program Files\Autodesk\Maya2013\bin
	set path=%RENDER_ROOT%;%path%
	"%RENDER_ROOT%\render.exe" -proj %proj% -rd %rd% -s %startframe% -e %endframe% -b %byframe% -mr:art -mr:aml -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");nCMayapreRender(\"%p%\",\"%rd%\")" %m%  
	goto end

:end
echo "Rendering Completed!"