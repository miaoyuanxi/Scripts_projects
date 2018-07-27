@echo off
set cgv=%~1
set render=%~2
set userId=%~3
set taskId=%~4
set sonId=%~5
set frame=%~6
set kg=%~7
set jobName=%~8
set maxFile=%~9

echo cgv=%cgv%
echo render=%render%
echo userId=%userId%
echo taskId=%taskId%
echo sonId=%sonId%
echo frame=%frame%
echo kg=%kg%
echo jobName=%jobName%
echo maxFile=%maxFile%




call "c:/script/max/max.bat" "%cgv%" "%render%" "config"
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/render.ms\";rwRender \"%userId%\" \"%taskId%\" \"%sonId%\" \"%frame%\" \"%kg%\" \"%jobName%\" \"%maxFile%\" "


echo rendr compleded
