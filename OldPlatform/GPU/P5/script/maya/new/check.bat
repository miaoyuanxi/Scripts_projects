@echo off
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

goto render_default

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