@echo off
ECHO.
ECHO.
ECHO.

SET __PY=B:\plugins\houdini\Enalyze.py
SET _CID=%~1
SET _TID=%~2
SET _HIP=%~3
SET _HIP=%_HIP:\=/%
SET _INF=%~4
SET _INF=%_INF:\=/%
if EXIST "D:\PLUGINS\houdini" rd/s/q  "D:\PLUGINS\houdini"
"C:/Python27/python.exe" "%__PY%" "%_CID%" "%_TID%" "%_HIP%" "%_INF%"

ECHO.
ECHO.
ECHO.