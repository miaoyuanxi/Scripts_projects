@echo off
set cgv=%~1
set render=%~2
set userId=%~3
set taskId=%~4
set sonId=%~5
set frame=%~6
set kg=%~7
set cgFile=%~8

echo %cgv%
echo %render%

if %render:~0,4%==vray (
	goto vrayRender
) else (
	goto defaultRender

)

:vrayRender
echo vray render
c:/concat.exe "C:/Program Files/Autodesk/%cgv%/plugin.ini" "C:/PLUGINS/ini/standard/%cgv%.ini" "C:/PLUGINS/ini/vray/%render%/%cgv%/plugin.ini" 
set path=C:/PLUGINS/vray/%render%/%cgv%;%path%
echo %path%
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/render.ms\";rwRender \"%userId%\" \"%taskId%\" \"%sonId%\" \"%frame%\" \"%kg%\" \"%cgFile%\" "
goto end


:defaultRender
echo default render
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" 
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/render.ms\";rwRender \"%userId%\" \"%taskId%\" \"%sonId%\" \"%frame%\" \"%kg%\" \"%cgFile%\" "
goto end



:end

echo rendr compleded
