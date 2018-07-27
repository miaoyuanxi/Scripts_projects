@echo off
set cgv=%~1
set render=%~2
set userId=%~3
set taskId=%~4
set maxFile=%~5
set netTxt=%~6

call "c:/script/max/max.bat" "%cgv%" "%render%" "config"
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/renderbus2.ms\";read \"%userId%\" \"%taskId%\" \"%maxFile%\" \"%netTxt%\" "

