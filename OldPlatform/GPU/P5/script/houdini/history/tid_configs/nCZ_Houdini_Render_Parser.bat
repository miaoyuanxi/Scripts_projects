@echo off

echo Parsing...
set _bat_cid=%~1
set _bat_tid=%~2
set _bat_sf=%~3
set _bat_ef=%~4
set _bat_bf=%~5
set _bat_rd=%~6
set _bat_render_file=%~7

set cgv=%~8

echo Projecting...
if "%_bat_cid%"=="14696" goto render_14696
goto RENDER_DEFAULT

:render_14696
echo render_14696
net use * /delete /y
net use B: //10.50.1.4/dd/inputData/maya/14696/DHLXJ /persistent:yes
set RENDER_ROOT=C:/Program Files/Side Effects Software/Houdini 12.5.469/bin
"%RENDER_ROOT%/hbatch.exe" -e _cmd_cid=%_bat_cid% -e _cmd_tid=%_bat_tid% -e _cmd_sf=%_bat_sf% -e _cmd_ef=%_bat_ef% -e _cmd_bf=%_bat_bf% -e _cmd_rd=%_bat_rd% -e _cmd_render_file=%_bat_render_file% //10.50.1.3/pool/script/houdini/nCZ_Houdini_Render_Start.cmd
goto end

:RENDER_DEFAULT
echo RENDER_DEFAULT
goto end

:end
echo "Rendering Completed!"