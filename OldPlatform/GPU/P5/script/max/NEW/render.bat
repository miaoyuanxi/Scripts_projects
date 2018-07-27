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


if "%userId%"=="20233" (
xcopy /y /f "\\10.50.1.229\renderscene\liyuguang\soft_ok\vrayPanoramaStereoCamera\vrayPanoramaStereoCamera2012.dlo" "C:\PLUGINS\vray\vray2.10.01\3ds Max 2012\plugins\vrayplugins\"
xcopy /y /f "\\10.50.1.229\renderscene\liyuguang\soft_ok\vrayPanoramaStereoCamera\vrayPanoramaStereoCamera2012.dlo" "C:\PLUGINS\vray\vray2.30.01\3ds Max 2012\plugins\vrayplugins\"
xcopy /y /f "\\10.50.1.229\renderscene\liyuguang\soft_ok\vrayPanoramaStereoCamera\vrayPanoramaStereoCamera2014.dlo" "C:\PLUGINS\vray\vray3.00.03\3ds Max 2014\plugins\vrayplugins\"
xcopy /y /v /e "\\10.50.1.229\renderscene\liyuguang\soft_ok\3dhippie_max2012\3ds Max 2012" "C:\Program Files\Autodesk\3ds Max 2012\"
xcopy /y /f "\\10.50.1.229\renderscene\liyuguang\soft_ok\20233\max_vray2014shakepixed\vray2014.dll" "C:\PLUGINS\vray\vray3.00.03\3ds Max 2014\"
xcopy /y /f "\\10.50.1.229\renderscene\liyuguang\soft_ok\20233\maxmaya_mentalray\max2013_64bit\panorama_stereo_lens.dll" "C:\Program Files\Autodesk\3ds Max 2014\NVIDIA\shaders_autoload\mentalray\shaders\"
xcopy /y /f "\\10.50.1.229\renderscene\liyuguang\soft_ok\20233\maxmaya_mentalray\max2013_64bit\panorama_stereo_lens_max.mi"  "C:\Program Files\Autodesk\3ds Max 2014\NVIDIA\shaders_autoload\mentalray\include\"
net use * /delete /y
net use z: \\10.50.1.3\d\inputdata\max\20000\20233\Z_Warren /persistent:yes


)


if "%userId%"=="163310" (
xcopy /y /v /e "\\10.50.1.3\d\inputdata\max\163000\163310\lostfiles" "c:\work\render\%taskId%\"
)

xcopy /y /v "\\10.50.1.3\d\inputdata\max\163000\163310\KEYFRAMES_PJT_BLU\MAPS\MAPS\BLU_Lighting_Rendering\_BLU_CHR_Assets\Hassan\30_5_2014\BLU_Production\Production\Character\Primary\Hassan\Maps_WIP\Hassan_Body\Final\Hassan_Feet_Rigth_Diff?se.tif" "c:\work\render\%taskId%\"

xcopy /y /f /v "\\10.50.8.2\p\tools\PNG\3ds Max 2014\png.bmi" "C:\Program Files\Autodesk\3ds Max 2014\stdplugs\"

xcopy /y /f /v "\\10.50.8.2\p9\script\max\NEW\render.ms"  "c:/script/max/"




call "c:/script/max/max.bat" "%cgv%" "%render%" "config"
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" -silent  -mxs "filein \"c:/script/max/render.ms\";rwRender \"%userId%\" \"%taskId%\" \"%sonId%\" \"%frame%\" \"%kg%\" \"%jobName%\" \"%maxFile%\" "
echo rendr compleded
