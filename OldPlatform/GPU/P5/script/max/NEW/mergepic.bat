@echo off
set cgv=%~1
set render=%~2
set userId=%~3
set taskId=%~4
set imgFrame=%~5
set imgwidth=%~6
set imgHeight=%~7
set workTaskPath=%~8


call "c:/script/max/max.bat" "%cgv%" "scanline" "config"
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/mergepic.ms\";RBmerge \"%taskId%\" %imgFrame% %imgwidth% %imgHeight% \"%workTaskPath%\" "

