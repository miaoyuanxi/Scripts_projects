@echo off

set setEnv=%~1
set softImage=%~2
set script=%~3
set txt=%~4
set frame=%~5
set proj=%~6
set rd=%~7
set file=%~8
set pass=%~9

if "%softImage%"=="C:/Program Files/Autodesk/Softimage 7.01/Application/bin/XSIbatch.exe" (
	goto softimage7
) else (
	goto softimage
) 

:softimage7
call "C:/Softimage/XSI_7.01_x64/Application/bin/setenv.bat"
"c:/Softimage/XSI_7.01_x64/Application/bin/XSIBatch.bat" -render "%file%" -pass "%pass%" -frames %frame%,%frame% -output_dir "%rd%" -script "%script%" -main preRender_XSI -args -projPath "%proj%" -txtPath "%txt%" -renderFrame %frame%

goto end

:softimage
echo softimage
call "%setEnv%"
"%softImage%" -render "%file%" -pass "%pass%" -frames %frame%,%frame% -output_dir "%rd%" -script "%script%" -main preRender_XSI -args -projPath "%proj%" -txtPath "%txt%" -renderFrame %frame%

goto end

:end
echo "Rendering Completed!"

rem D:\Tech\VBScript\Render.bat "D:\Programs\Autodesk\Softimage 2013\Application\bin\setenv.bat" "D:\Programs\Autodesk\Softimage 2013\Application\bin\XSIbatch.exe" D:\Tech\VBScript\preRender_XSI.vbs d:\tt\xx.txt 1 C:\jj D:\tt C:\jj\Scenes\Scene2.scn
rem D:\Tech\VBScript\Render.bat "C:\Program Files\Autodesk\Softimage 2013\Application\bin\setenv.bat" "C:\Program Files\Autodesk\Softimage 2013\Application\bin\XSIbatch.exe" D:\Tech\VBScript\preRender_XSI.vbs d:\tt\xx.txt 1 C:\jj D:\tt C:\jj\Scenes\Scene2.scn