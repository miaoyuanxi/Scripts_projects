@echo off
set pool=%~1
set cgv=%~2
set render=%~3

if not exist "C:/PLUGINS/vray/vray2.40.04/3ds Max 2014" (
	mkdir "C:/PLUGINS/vray/vray2.40.04/3ds Max 2014"
)


xcopy "\\18.1.0.241\pool\PLUGINS\ini" "C:/PLUGINS/"