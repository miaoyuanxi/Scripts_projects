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

if "%renderer%"=="maxwell" goto render3

if "%render%"=="C:/Program Files/Autodesk/Maya8.5/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2008/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2009/bin/Render.exe" goto render1
if "%render%"=="C:/Program Files/Autodesk/Maya2010/bin/Render.exe" goto render1

if "%render%"=="C:/Program Files/Autodesk/Maya2011/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2012/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2013/bin/Render.exe" goto render2
if "%render%"=="C:/Program Files/Autodesk/Maya2013.5/bin/Render.exe" goto render2


:render1
"%render%" -s %startframe% -e %endframe% -b %byframe% -r mr -art -aml -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% "%mb%"  
goto end

:render2
"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
goto end

:render3
"%render%" -s %startframe% -e %endframe% -b %byframe% -preRender "source \"%mel%\";maya_preRender(\"%proj%\",\"%txt%\",\"%startframe%\");" -proj "%proj%" -rd %rd% -r maxwell "%mb%"  

:end
echo "Rendering Completed!"