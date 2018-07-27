set maya=%~1
set mel=%~2
set proj=%~3
set mb=%~4
set txt=%~5

set MAYA_SCRIPT_PATH=\\10.50.1.3\pool\script\maya\nCZSupport;C:\Program Files\JoeAlter\shaveHaircut\maya2013\scripts;C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\scripts;
set MAYA_PLUG_IN_PATH=C:\Program Files\JoeAlter\shaveHaircut\maya2013\plug-ins;
set MI_CUSTOM_SHADER_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\include;
set MI_LIBRARY_PATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\lib;
set XBMLANGPATH=C:\nCZ_RayWing_Extra_Addons\Shaders\shaders_p_3.3.3_maya_win64\Maya2013\icons;
set RENDER_ROOT=C:/Program Files/Autodesk/Maya2013/bin
set path=%RENDER_ROOT%;%path%

"%RENDER_ROOT%/maya.exe" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");"