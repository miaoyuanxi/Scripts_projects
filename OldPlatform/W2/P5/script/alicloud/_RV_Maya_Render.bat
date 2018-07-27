set uid=%~1
set sf=%~2
set ef=%~3
set bf=%~4
set proj=%~5
set rFile=%~6
set rd=%~7
set opt1=%~8
set opt2=%~9

echo task info:
	echo	uid:	%uid%
	echo	sf:		%sf%
	echo	ef:		%ef%
	echo	bf:		%bf%
	echo	proj:	%proj%
	echo	rFile:	%rFile%
	echo	rd:		%rd%
	echo	opt:	%opt1%
	echo	opt:	%opt2%
	
if "%userId%"=="53" goto render_53

:render_53
	echo Configure Applied @ 53
	echo Redshift3d render
	set _bat_cgv=2016
	set render=C:\Program Files\Autodesk\Maya%_bat_cgv%\bin\render.exe
	
	"%render%" -s %sf% -e %ef% -b %bf% -proj "%proj%" -rd %rd% "%rFile%"
	goto _RV_EOF


:_RV_EOF
echo "Rendering Completed!"