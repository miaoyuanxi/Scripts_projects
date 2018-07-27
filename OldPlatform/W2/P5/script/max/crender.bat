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


if %userId%==100001 (
	goto vray3.00.07
)

if %userId%==165826 (
	goto vray3.00.07
)

if %userId%==166387 (
	goto vray3.00.07
)

if %userId%==120106 (
	goto vray3.00.08
)


if %userId%==962302 (
	goto RayFire 1.65formax2015
)
:RayFire 1.65formax2015
xcopy /q /y /e /v "\\10.50.8.16\td\liyuguang\soft_ok\max\RayFire 1.65formax2015\Autodesk" "C:\Program Files\Autodesk\"
goto end
if %userId%==962085 (
	goto vray3.00.07
)

:vray3.00.07
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\vray3.00.07\*.*" "C:\PLUGINS\vray\vray3.00.07\"
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\ini\standard\*.ini" "C:\PLUGINS\ini\standard\"
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\ini\vray\*.*" "C:\PLUGINS\ini\vray\"
goto end

:vray3.00.08
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\vray3.00.08\*.*" "C:\PLUGINS\vray\vray3.00.08\"
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\ini\standard\*.ini" "C:\PLUGINS\ini\standard\"
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\ini\vray\*.*" "C:\PLUGINS\ini\vray\"
goto end

:vray2.50.01
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\vray2.50.01\*.*" "C:\PLUGINS\vray\vray2.50.01\"
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\ini\standard\*.ini" "C:\PLUGINS\ini\standard\"
xcopy /y /f /e /v "\\10.50.8.16\td\quanshiyin\run\vray\ini\vray\*.*" "C:\PLUGINS\ini\vray\"
goto end

:end
call "c:/script/max/max.bat" "%cgv%" "%render%" "config"
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/crender.ms\";rwRender \"%userId%\" \"%taskId%\" \"%sonId%\" \"%frame%\" \"%kg%\" \"%jobName%\" \"%maxFile%\" "
echo rendr compleded
