@echo off

set maya=%~1
set mel=%~2
set proj=%~3
set mb=%~4
set txt=%~5

set mel=//10.50.10.3/pool/script/maya/checkNet.mel

set MAYA_SCRIPT_PATH=\\10.50.10.3\pool\script\maya\nCZSupport

"%maya%" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");"


