@echo off
set cgv=%~1
set render=%~2
set userId=%~3
set taskId=%~4
set sonId=%~5
set frame=%~6
set kg=%~7
set maxFile=%~8


echo %cgv%
echo %render%


call "c:/script/max/max.bat" "%cgv%" "%render%" "config"
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/render.ms\";rwRender \"%userId%\" \"%taskId%\" \"%sonId%\" \"%frame%\" \"%kg%\" \"%maxFile%\" "


echo rendr compleded
