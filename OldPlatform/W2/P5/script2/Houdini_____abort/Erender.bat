@echo off
ECHO.
ECHO.
ECHO.

SET __PY=B:\plugins\houdini\Erender.py
SET _CID=%~1
SET _TID=%~2
SET _SFM=%~3
SET _EFM=%~4
SET _BFM=%~5
SET _HIP=%~6
SET _HIP=%_HIP:\=/%
SET _ROP=%~7
SET _ROP=%_ROP:\=/%
SET _RRD=%~8
SET _RRD=%_RRD:\=/%
SET _OPT=%~9

"C:/Python27/python.exe" "%__PY%" "%_CID%" "%_TID%" "%_SFM%" "%_EFM%" "%_BFM%" "%_HIP%" "%_ROP%" "%_RRD%" "%_OPT%"

ECHO.
ECHO.
ECHO.