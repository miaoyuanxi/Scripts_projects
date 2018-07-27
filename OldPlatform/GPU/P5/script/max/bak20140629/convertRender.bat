@echo off
set cgv=%~1
set render=%~2


del /q /f /s "C:\Program Files\Autodesk\%cgv%\plugins\vrayplugins"
del /q /f /s "C:\Program Files\Autodesk\%cgv%\plugins\vrayraw2010.bmi"
del /q /f /s "C:\Program Files\Autodesk\%cgv%\plugins\vrender2010.dlr"

if %render:~0,4%==vray (
	goto vrayRender
) else (
	goto defaultRender

)

:vrayRender
if "%cgv%"=="3ds Max 2014"  (
	goto vrayConcatEnus
) 
if "%cgv%"=="3ds Max 2013"  (
	goto vrayConcatEnus
)
if "%cgv%"=="3ds Max 2012"  (
	goto vrayConcat
)
if "%cgv%"=="3ds Max 2011"  (	
	goto vrayConcat
)
if "%cgv%"=="3ds Max 2009"  (	
	goto vrayConcat
)
if "%cgv%"=="3ds Max 2008"  (	
	goto vrayConcat
)
if "%cgv%"=="3ds Max 9"  (	
	goto vrayConcat
)

:defaultRender
if "%cgv%"=="3ds Max 2014"  (
	goto defaultConcatEnus
) 
if "%cgv%"=="3ds Max 2013"  (
	goto defaultConcatEnus
)
if "%cgv%"=="3ds Max 2012"  (
	goto defaultConcat
)
if "%cgv%"=="3ds Max 2011"  (	
	goto defaultConcat
)
if "%cgv%"=="3ds Max 2009"  (	
	goto defaultConcat
)
if "%cgv%"=="3ds Max 2008"  (	
	goto defaultConcat
)
if "%cgv%"=="3ds Max 9"  (	
	goto defaultConcat
)
if "%cgv%"=="3ds Max 2014" or "%cgv%"=="3ds Max 2013"  (
	goto defaultConcatEnus
) else (
	goto defaultConcat
)

:vrayConcatEnus
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\en-US\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" "C:\PLUGINS\ini\vray\%render%\%cgv%\plugin.ini" 
set Path=C:\PLUGINS\vray\%render%\%cgv%;%Path%
goto max

:vrayConcat
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" "C:\PLUGINS\ini\vray\%render%\%cgv%\plugin.ini" 
set Path=C:\PLUGINS\vray\%render%\%cgv%;%Path%
goto max

:defaultConcatEnus
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\en-US\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" 
goto max

:defaultConcat
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" 
goto max










:max
echo finish
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" 
