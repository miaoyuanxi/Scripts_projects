@echo off

set uid=%~1
set tid=%~2
set cgv=%~3
set txt=%~4
set frame=%~5
set proj=%~6
set rd=%~7
set file=%~8
set pass=%~9

set setEnv=%cgv%/Application/bin/setenv.bat
set softImage=%cgv%/Application/bin/XSIbatch.exe
set script=C:/script/softimage/preRender_XSI.vbs

echo %uid%
echo %tid%
echo %cgv%
echo %setEnv%
echo %softImage%
echo %script%
echo %txt%
echo %frame%
echo %proj%
echo %rd%
echo %file%
echo %pass%

echo -----------------

if "%softImage%"=="C:/Program Files/Autodesk/Softimage 7.01/Application/bin/XSIbatch.exe" (
	goto softimage7
) else (
	goto softimage
) 

:softimage7
echo softimage7...
call "C:/Softimage/XSI_7.01_x64/Application/bin/setenv.bat"
call "c:/Softimage/XSI_7.01_x64/Application/bin/XSIBatch.bat" -render "%file%" -pass "%pass%" -frames %frame%,%frame% -output_dir "%rd%" -script "%script%" -main preRender_XSI -args -projPath "%proj%" -txtPath "%txt%" -renderFrame %frame%
echo del...
del /q /f "c:\enfwork\%tid%\output\*.fgmap"
del /q /f "c:\enfwork\%tid%\output\*.phmap"
goto end

:softimage
echo softimage...
call "%setEnv%"
"%softImage%" -render "%file%" -pass "%pass%" -frames %frame%,%frame% -output_dir "%rd%" -script "%script%" -main preRender_XSI -args -projPath "%proj%" -txtPath "%txt%" -renderFrame %frame%
goto end

:end
echo end...

echo "Rendering Completed!"

rem D:\Tech\VBScript\Render.bat "D:\Programs\Autodesk\Softimage 2013\Application\bin\setenv.bat" "D:\Programs\Autodesk\Softimage 2013\Application\bin\XSIbatch.exe" D:\Tech\VBScript\preRender_XSI.vbs d:\tt\xx.txt 1 C:\jj D:\tt C:\jj\Scenes\Scene2.scn
rem D:\Tech\VBScript\Render.bat "C:\Program Files\Autodesk\Softimage 2013\Application\bin\setenv.bat" "C:\Program Files\Autodesk\Softimage 2013\Application\bin\XSIbatch.exe" D:\Tech\VBScript\preRender_XSI.vbs d:\tt\xx.txt 1 C:\jj D:\tt C:\jj\Scenes\Scene2.scn