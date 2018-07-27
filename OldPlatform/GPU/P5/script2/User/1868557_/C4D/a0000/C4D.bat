@echo off
set cgv=%~1
set taskId=%~2
set cgFile=%~3
set txtPath=%~4

set myplugin=%~dp0..\
::B:\plugins\C4D\

xcopy /f /y /e  "\\10.60.100.101\p5\script2\User\1868557\C4D\a0000\Analys.pyp" "C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R13_05DFD2A0\plugins\"
xcopy /f /y /e  "\\10.60.100.101\p5\script2\User\1868557\C4D\a0000\Analys.pyp" "C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R14_4A9E4467\plugins\"
xcopy /f /y /e  "\\10.60.100.101\p5\script2\User\1868557\C4D\a0000\Analys.pyp" "C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R15_53857526\plugins\"
xcopy /f /y /e  "\\10.60.100.101\p5\script2\User\1868557\C4D\a0000\Analys.pyp" "C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R16_14AF56B1\plugins\"
xcopy /f /y /e  "\\10.60.100.101\p5\script2\User\1868557\C4D\a0000\Analys.pyp" "C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R17_8DE13DAD\plugins\"
xcopy /f /y /e  "\\10.60.100.101\p5\script2\User\1868557\C4D\a0000\Analys.pyp" "C:\Users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R18_62A5E681\plugins\"

if "%cgv%"=="CINEMA 4D R18"  (
	goto StartC4D
)
if "%cgv%"=="CINEMA 4D R17"  (
	goto StartC4D
)
if "%cgv%"=="CINEMA 4D R16"  (
	goto StartC4D
)
if "%cgv%"=="CINEMA 4D R15"  (
	goto StartC4D
) 
if "%cgv%"=="CINEMA 4D R14"  (
	goto StartC4D
)
if "%cgv%"=="CINEMA 4D R13"  (
	goto StartC4D
)

:StartC4D

echo taskId:%taskId%
echo cgFile:%cgFile%
echo txtPath:%txtPath%
echo run:%cgv%
	"C:\Program Files\MAXON\%cgv%\CINEMA 4D 64 Bit.exe" -taskId:%taskId% -cgFile:%cgFile% -txtPath:%txtPath%

