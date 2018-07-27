@echo off

echo Parsing...
set _bat_cid=%~1
set _bat_tid=%~2
set _bat_sf=%~3
set _bat_ef=%~4
set _bat_bf=%~5
set _bat_cgv=%~6
set _bat_pro=%7
set _bat_render_file=%~8
set _bat_rd=%~9



call "c:/script/max/max.bat" "3ds Max 2013" "vray2.40.04" "config"
"C:\Program Files\Autodesk\3ds Max 2013\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/render.ms\";rwRender \"%_bat_cid%\" \"%_bat_tid%\" \"0\" \"%_bat_sf%\" \"0\" \"%_bat_render_file%\" "






