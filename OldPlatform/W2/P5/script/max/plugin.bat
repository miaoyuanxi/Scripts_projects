@echo off
set cgv=%~1
set pluginDir=%~2
set pluginVersion=%~3

C:/fcopy/FastCopy.exe /force_close /cmd=force_copy "C:\PLUGINS\%pluginDir%\%pluginVersion%\%cgv%\*" /to="C:\Program Files\Autodesk\%cgv%\"


