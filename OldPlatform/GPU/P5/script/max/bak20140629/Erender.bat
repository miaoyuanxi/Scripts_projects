@echo off

echo Parsing...
set userId=%~1
set taskId=%~2
set startFrame=%~3
set endFrame=%~4
set byFrame=%~5
set cgv=%~6
set proj=%7
set cgFile=%~8
set output=%~9

set cgFile=%cgFile:\=/%




xcopy /y /f  "\\10.50.1.3\pool\script\max\render.ms" "c:/script/max/"
xcopy /y /f  "\\10.50.1.3\pool\script\max\render.bat" "c:/script/max/"
xcopy /y /f  "\\10.50.1.3\pool\script\max\max.bat" "c:/script/max/"
xcopy /y /f  "\\10.50.1.3\pool\script\max\plugin.bat" "c:/script/max/"


"c:/script/max/render.bat" "3ds Max 2009" "vray1.50.sp2" %userId% %taskId% 0 %startFrame% 15 "%cgFile%"




echo -----------------
echo C:/RBNodeService/NodeRun.exe "call \"c:/script/max/render.bat\" \"3ds Max 2009\" \"vray1.50.sp2\" \"%userId%\" \"%taskId%\" \"0\" \"%startFrame%\" \"15\" \"%cgFile%\""
echo C:/RBNodeService/NodeRun.exe "call \"c:/script/max/render.bat\" \"3ds Max 2014\" \"vray2.40.04\" \"%userId%\" \"%taskId%\" \"0\" \"%startFrame%\" \"15\" \"%cgFile%\""

echo c:/script/max/Erender.bat "53" "106769" "1" "1" "1" "" "\\18.1.0.229\inputData\53\LIUJINWU\manaytea" "//18.1.0.229\inputData\53\LIUJINWU\manaytea\region2012_elem.max" "C:/enfwork/106769/output/"