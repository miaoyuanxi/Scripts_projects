@echo off

set setEnv=%~1
set softImage=%~2
set script=%~3
set proj=%~4
set file=%~5
set txt=%~6





if "%softImage%"=="C:/Program Files/Autodesk/Softimage 7.01/Application/bin/XSIbatch.exe" (
	goto softimage7
) else (

	goto softimage
)

:softimage7
call "C:\Program Files\Autodesk\Softimage 2013\Application\bin\setenv.bat"
"C:\Program Files\Autodesk\Softimage 2013\Application\bin\XSIbatch.exe" -script "%script%" -main checkNet -args -projPath "%proj%" -xsiFile "%file%" -txtPath "%txt%"

goto end

:softimage
echo softimage
call "%setEnv%"
"%softImage%" -script "%script%" -main checkNet -args -projPath "%proj%" -xsiFile "%file%" -txtPath "%txt%"
goto end

:end


rem "C:\Program Files\Autodesk\Softimage 2013\Application\bin\setenv.bat"

rem "C:\Program Files\Autodesk\Softimage 2013\Application\bin\XSI.exe"  -script D:\Tech\VBScript\checkNet.vbs -main checkNet -args -projPath "d:\tt\jj" -xsiFile "d:\tt\jj\Scenes\Scene2.scn" -txtPath "d:\tt\xx.txt"

rem "d:\Programs\Autodesk\Softimage 2013\Application\bin\XSI.exe"  -script D:\Tech\VBScript\checkNet.vbs -main checkNet -args -projPath "d:\tt\jj" -xsiFile "d:\tt\jj\Scenes\Scene2.scn" -txtPath "d:\tt\xx.txt"

rem D:\Tech\VBScript\checkXSI.bat "D:\Programs\Autodesk\Softimage 2013\Application\bin\setenv.bat" "D:\Programs\Autodesk\Softimage 2013\Application\bin\XSIbatch.exe" D:\Tech\VBScript\checkNet.vbs C:\jj C:\jj\Scenes\Scene2.scn D:\tt\xx.txt