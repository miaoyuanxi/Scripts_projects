@echo off

set render=%~1
set mel=%~2
set txt=%~3
set startframe=%~4
set endframe=%~5
set byframe=%~6
set proj=%~7
set rd=%~8
set mb=%~9


shift 
set renderer=%~9

echo %renderer%

if "%renderer%"=="maxwell" goto render3
if "%renderer%"=="_3delight" goto render4
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

:render4
"C:/Program Files/Autodesk/Maya2011/bin/mayapy.exe" Z:\VJ_Studio_Tools\scripts\demMain.py  "%mb%" "%rd:output/=%" %rd% %startframe%
goto end

:render_62123
echo Configure - AfterStudios
set proj=%proj:\=/%
set mb=%mb:\=/%
set rd=%rd:\=/%

if "%render%"=="C:/Program Files/Autodesk/Maya2012/bin/Render.exe" goto render_62123_maya2012
if "%render%"=="C:/Program Files/Autodesk/Maya2013/bin/Render.exe" goto render_62123_maya2013
goto end

:render_62123_maya2012
echo render_62123_maya2012
set MAYA_SCRIPT_PATH=\\10.50.1.3\pool\script\maya\nCZSupport;C:\Program Files\JoeAlter\shaveHaircut\maya2012\scripts;C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\scripts;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\scripts\AETemplates;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\scripts\others
set MAYA_PLUG_IN_PATH=C:\Program Files\JoeAlter\shaveHaircut\maya2012\plug-ins;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\bin\plug-ins
set MI_CUSTOM_SHADER_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\include;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\mentalray\include
set MI_LIBRARY_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\lib;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\mentalray\lib
set XBMLANGPATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2012\icons;\\10.50.1.4\dd\inputData\maya\62123\Support\realflow_maya_win_5.0.10\icons
set RENDER_ROOT=C:\Program Files\Autodesk\Maya2012\bin
set path=%RENDER_ROOT%;%path%
"%RENDER_ROOT%\render.exe" -proj %proj% -rd %rd% -s %startframe% -e %endframe% -b %byframe% -mr:art -mr:aml -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");nCMayapreRender(\"%proj%\", \"%rd%\");" "%mb%"  
goto end

:render_62123_maya2013
echo render_62123_maya2013
set MAYA_SCRIPT_PATH=\\10.50.1.3\pool\script\maya\nCZSupport;C:\Program Files\JoeAlter\shaveHaircut\maya2013\scripts;C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\scripts;
set MAYA_PLUG_IN_PATH=C:\Program Files\JoeAlter\shaveHaircut\maya2013\plug-ins;
set MI_CUSTOM_SHADER_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\include;
set MI_LIBRARY_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\lib;
set XBMLANGPATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\icons;
set RENDER_ROOT=C:\Program Files\Autodesk\Maya2013\bin
set path=%RENDER_ROOT%;%path%
"%RENDER_ROOT%\render.exe" -proj %proj% -rd %rd% -s %startframe% -e %endframe% -b %byframe% -mr:art -mr:aml -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");nCMayapreRender(\"%proj%\", \"%rd%\");" "%mb%"  
goto end

:end
echo "Rendering Completed!"