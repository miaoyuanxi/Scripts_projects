@echo off
set cgv=%~1



rd /s /q "C:\Program Files\Autodesk\3ds Max %cgv%\plugins\vrayplugins"
del /q /f /s "C:\Program Files\Autodesk\3ds Max %cgv%\plugins\vray*.bmi"
del /q /f /s "C:\Program Files\Autodesk\3ds Max %cgv%\plugins\vrender*.dlr"
del /q /f  "C:\Program Files\Autodesk\3ds Max %cgv%\vray*"
del /q /f  "C:\Program Files\Autodesk\3ds Max %cgv%\cgauth.dll"
