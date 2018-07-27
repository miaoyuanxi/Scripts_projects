@echo off
set cgv=%~1
set render=%~2


rd /s /q "C:\Program Files\Autodesk\%cgv%\plugins\vrayplugins"
del /q /f /s "C:\Program Files\Autodesk\%cgv%\plugins\vray*.bmi"
del /q /f /s "C:\Program Files\Autodesk\%cgv%\plugins\vrender*.dlr"
del /q /f  "C:\Program Files\Autodesk\%cgv%\vray*"

if %render:~0,4%==vray (
	goto vrayRender
) else (
	goto defaultRender

)

:vrayRender
if "%cgv%"=="3ds Max 2014"  (
	goto vraySetEN
) 
if "%cgv%"=="3ds Max 2013"  (
	goto vraySetEN
)
if "%cgv%"=="3ds Max 2012"  (
	goto vraySet
)
if "%cgv%"=="3ds Max 2011"  (	
	goto vraySet
)
if "%cgv%"=="3ds Max 2010"  (	
	goto vraySet
)
if "%cgv%"=="3ds Max 2009"  (	
	goto vraySet
)
if "%cgv%"=="3ds Max 2008"  (	
	goto vraySet
)
if "%cgv%"=="3ds Max 9"  (	
	goto vraySet
)

:defaultRender
if "%cgv%"=="3ds Max 2014"  (
	goto defaultSetEn
) 
if "%cgv%"=="3ds Max 2013"  (
	goto defaultSetEn
)
if "%cgv%"=="3ds Max 2012"  (
	goto defaultSet
)
if "%cgv%"=="3ds Max 2010"  (	
	goto defaultSet
)
if "%cgv%"=="3ds Max 2011"  (	
	goto defaultSet
)
if "%cgv%"=="3ds Max 2009"  (	
	goto defaultSet
)
if "%cgv%"=="3ds Max 2008"  (	
	goto defaultSet
)
if "%cgv%"=="3ds Max 9"  (	
	goto defaultSet
)


:vraySetEN
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\en-US\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" "C:\PLUGINS\ini\vray\%render%\%cgv%\plugin.ini" 
set Path=C:\PLUGINS\vray\%render%\%cgv%;%Path%
goto max

:vraySet
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" "C:\PLUGINS\ini\vray\%render%\%cgv%\plugin.ini" 
set Path=C:\PLUGINS\vray\%render%\%cgv%;%Path%
goto max

:defaultSetEn
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\en-US\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" 
goto max

:defaultSet
c:\concat.exe "C:\Program Files\Autodesk\%cgv%\plugin.ini" "C:\PLUGINS\ini\standard\%cgv%.ini" 
goto max










:max
echo finish
"C:\Program Files\Autodesk\%cgv%\3dsmax.exe" 
