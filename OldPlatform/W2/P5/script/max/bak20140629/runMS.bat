@echo off
set cgv=%~1
set render=%~2
set msFile=%~3

echo %cgv%
echo %render%


if "%cgv%"=="3ds Max 2014" (
	echo max 2014
)

if %render:~0,4%==vray (
	goto vrayRender
) else (
	goto defaultRender

)

:vrayRender
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\en-US\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" "C:\PLUGINS\ini\vray\%render%\%cgv%\plugin.ini" 
set Path=C:\PLUGINS\vray\%render%\%cgv%;%Path%
goto end

:defaultRender
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\en-US\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" "C:\PLUGINS\ini\vray\vray2.40.04\%cgv%\plugin.ini" 
set Path=C:\PLUGINS\vray\vray2.40.04\%cgv%;%Path%
goto end


:end
"C:/Program Files/Autodesk/%cgv%/3dsmax.exe" -q -mip -silent -U MAXScript "%msFile%" 

