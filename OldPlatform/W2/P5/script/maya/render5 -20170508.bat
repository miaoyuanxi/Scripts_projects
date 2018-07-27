@echo off
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
	echo "Using cgrender.py to render"
	echo "c:\python27\python.exe" "\\10.60.100.101\o5\py\model\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt 1002
	"c:\python27\python.exe" "\\10.60.100.101\o5\py\model\cgrender.py" --js %json% --pl %plugins_json% --sf %startframe% --ef %endframe% --by %byframe% --pt 1002
goto end

:end
    echo exitcode: %errorlevel%
    if not %errorlevel%==0 goto fail
    echo Render progress end.
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    ::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
    \\10.60.100.151\td\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
	\\10.60.100.151\td\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    exit /b 0

:fail
    echo Render progress failed.
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    ::wmic process where ExecutablePath="C:\\AMPED\\rlm.exe" delete
    \\10.60.100.151\td\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
	\\10.60.100.151\td\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    exit /b 1
