@echo off

set maya=%~1
set mel=%~2
set proj=%~3
set mb=%~4
set txt=%~5

"%maya%" -prompt -command "source \"%mel%\";checkNet(\"%proj%\",\"%mb%\",\"%txt%\");"
