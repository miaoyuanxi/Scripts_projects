@echo off

echo --------------------------------------
echo render5.bat Running at %COMPUTERNAME%
netstat
echo
echo --------------------------------------

set userId=%~1
set taskId=%~2
set render=%~3
set txt=%~4
set startframe=%~5
set endframe=%~6
set byframe=%~7
set proj=%~8
set mb=%~9

shift
set json=%~9

shift
set plugins_json=%~9

echo task info:
	echo	userId:		%userId%
	echo	taskId:		%taskId%
	echo	render:		%render%
	echo	txt:	    %txt%
	echo	startframe:	%startframe%
	echo	endframe:	%endframe%
	echo	byframe:	%byframe%
	echo	proj:	    %proj%
	echo	mb:	        %mb%
	echo    json:       %json%
  echo    plugins_json:       %plugins_json%

:default
	echo "Start py27 to render maya"
	echo "c:\python27\python.exe" "c:\script\py\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt 1005
	"c:\python27\python.exe" "c:\script\py\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt 1005
goto end

:end
    echo exitcode: %errorlevel%
    if not %errorlevel%==0 goto fail
    echo Render progress end.
    exit /b 0

:fail
    echo Render progress failed.
    exit /b 1