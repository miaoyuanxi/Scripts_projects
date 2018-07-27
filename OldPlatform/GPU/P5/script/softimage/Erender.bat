@echo off

set _bat_cid=%~1
set _bat_tid=%~2
set _bat_sf=%~3
set _bat_ef=%~4
set _bat_bf=%~5
set _bat_cgv=%~6
set _bat_pro=%7
set _bat_render_file=%~8
set _bat_rd=%~9





call "C:/Softimage/XSI_7.01_x64/Application/bin/setenv.bat"
"c:/Softimage/XSI_7.01_x64/Application/bin/XSIBatch.bat" -render "%_bat_render_file%" -frames %_bat_sf%,%_bat_ef% -output_dir "%_bat_rd%" 