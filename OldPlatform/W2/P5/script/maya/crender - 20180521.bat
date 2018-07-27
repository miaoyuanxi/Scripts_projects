@echo off
set userId=%~1
set taskId=%~2
set render=%~3
set txt=%~4
set startframe=%~5
set endframe=%~6
set byframe=%~7
set proj=%8
set mb=%9

shift
set tile_index=%~9

shift
set tiles=%~9

if not defined tile_index set tile_index=0
if not defined tiles set tiles=1

echo task info:
    echo    userId:        %userId%
    echo    taskId:        %taskId%
    echo    render:        %render%
    echo    txt:    %txt%
    echo    startframe:    %startframe%
    echo    endframe:    %endframe%
    echo    byframe:    %byframe%
    echo    proj:    %proj%
    echo    mb:    %mb%
    echo    tile_index:    %tile_index%
    echo    tiles:    %tiles%
REM if %taskId:~0,2%==10 (set py_path=\\10.60.100.105\stg_data\input\o5\py\model&&set pt=1000&&set b_path=\\10.60.100.151\td)
if %taskId:~0,1%==9 (set py_path=\\10.60.100.101\o5\py\model&&set pt=1002&&set b_path=\\10.60.100.151\td)
if %taskId:~0,2%==10 (set py_path=\\10.60.100.101\o5\py\model&&set pt=1002&&set b_path=\\10.60.100.151\td)
if %taskId:~0,1%==5 (set py_path=\\10.50.5.29\o5\py\model&&set pt=1005&&set b_path=\\10.50.1.22\td_new\td)
if %taskId:~0,1%==8 (set py_path=\\10.70.242.102\o5\py\model&&set pt=1008&&set b_path=\\10.70.242.50\td)
if %taskId:~0,2%==19 (set py_path=\\10.80.100.101\o5\py\model&&set pt=1009&&set b_path=\\10.80.243.50\td)
if %taskId:~0,2%==16 (set py_path=\\10.90.100.101\o5\py\model&&set pt=1016&&set b_path=\\10.90.96.51\td1)

echo py_path ::%py_path%
echo pt  :: %pt%
echo b_path :: %b_path%
set output=c:/work/render/%taskId%/output/
echo %mb%
REM dir /ad %mb% && goto arnold
REM if  %mb:~-4%==.hip goto houdini

:cgrender_with_multi_storages
    xcopy /y /f "%py_path%\maya2017\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2017\prefs\"
    xcopy /y /f "%py_path%\maya2016.5\prefs\pluginPrefs.mel" "C:\users\enfuzion\Documents\maya\2016.5\prefs\"
    xcopy /y /f "%py_path%\maya2016\prefs\userPrefs.mel" "C:\users\enfuzion\Documents\maya\2016\prefs\"
    xcopy /y /f "B:\clientFiles\1818426\partio4Maya2016.5\dll\zlib.dll" "C:\Windows\system32\"
    echo "Start py27 to render using cgrender_with_multi_storages."
    echo "c:\python27\python.exe" "%py_path%\cgrender_with_multi_storages.pyc" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt% --sp %proj% --tile_index %tile_index% --tiles %tiles%
    "c:\python27\python.exe" "%py_path%\cgrender_with_multi_storages.pyc" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt% --sp %proj% --tile_index %tile_index% --tiles %tiles%
goto end

:houdini
    echo "start Erender.bat to render houdini."
    set output=c:/work/render/%taskId%/output/
    IF NOT EXIST "%output%" MD "%output%"
    for /f %%i in ('c:\python27\python.exe %py_path%\get_houdini_rop.py %taskId%') do set rop=%%i
    echo \\10.50.1.3\p\script\houdini\_NC_w5_Houdini_Erender.bat 0 0 %startframe% %endframe% %byframe% "cgv" "proj" %mb% %output% %rop% "-V -I -s"
    \\10.50.1.3\p\script\houdini\_NC_w5_Houdini_Erender.bat 0 0 %startframe% %endframe% %byframe% "cgv" "proj" %mb% %output% %rop% "-V -I -s"
goto end

:cgrender
    echo "Start py27 to render using cgrender."
    echo "c:\python27\python.exe" "%py_path%\cgrender.pyc" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
    "c:\python27\python.exe" "%py_path%\cgrender.pyc" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
goto end

:cgrender_test
    echo "Start py27 to render using cgrender_test."
    echo "c:\python27\python.exe" "%py_path%\cgrender_test.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
    "c:\python27\python.exe" "%py_path%\cgrender_test.py" --ti %taskId% --sf %startframe% --ef %endframe% --by %byframe% --pt %pt%
goto end

:arnold
    echo "Start py27 to render arnold."
    echo "c:\python27\python.exe" "%py_path%\arnold_render.py" %taskId% %startframe% %endframe% %byframe% %pt%
    "c:\python27\python.exe" "%py_path%\arnold_render.py" %taskId% %startframe% %endframe% %byframe% %pt%
goto end2

:end2
    echo "Rendering Completed!"

    echo exitcode: %errorlevel%
    if not %errorlevel%==0 goto fail
    echo "exit rlm "
    ::for /f "tokens=2 " %a in ('tasklist  /fi "imagename eq rlm.exe" /nh') do taskkill /f /pid  %a
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
    wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm_Golaem.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    ::wmic process where ExecutablePath="C:\\Golaem\\rlm_Golaem.exe" delete
    echo "end rlm"
	exit /b 0

:end
    echo "Rendering Completed!"
    echo exitcode: %errorlevel%
    if %userId%==963480 (set %errorlevel%==0)
    if %userId%==1811662 (set %errorlevel%==0)
    if %userId%==1849653 goto ok
    echo exitcode: %errorlevel%
    if not %errorlevel%==0 goto fail
    echo "exit rlm "
    ::for /f "tokens=2 " %a in ('tasklist  /fi "imagename eq rlm.exe" /nh') do taskkill /f /pid  %a
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
    wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm_Golaem.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    echo "end rlm"
    exit /b 0

:ok
    echo "the is  ok "
    echo "exit rlm "
    ::for /f "tokens=2 " %a in ('tasklist  /fi "imagename eq rlm.exe" /nh') do taskkill /f /pid  %a
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
    wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm_Golaem.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    echo "end rlm"
    exit /b 0
    
:fail
    ::if %userId%==963480 (if %errorlevel%==1 goto ok)
    ::if %userId%==1811662 (if %errorlevel%==1 goto ok)
    REM if %taskId%==9130813 (if %errorlevel%==1 goto ok)
    if %userId%==1849653 goto ok
    echo "Rendering Failed!"

    ::for /f "tokens=2 " %a in ('tasklist  /fi "imagename eq rlm.exe" /nh') do taskkill /f /pid  %a
    wmic process where name="rlm.exe" delete
    wmic process where name="JGS_mtoa_licserver.exe" delete
    wmic process where name="rlm_redshift.exe" delete
    wmic process where name="rlm_shave.exe" delete
    wmic process where name="joealter.exe" delete
    wmic process where name="rlm_Golaem.exe" delete
    wmic process where ExecutablePath="C:\\AMPED_mili\\rlm.exe" delete
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\Golaem\rlm_Golaem.exe" /cls
    %b_path%\tools\cmdow\cmdow.exe "C:\AMPED\rlm.exe" /cls
    ::wmic process where ExecutablePath="C:\\Golaem\\rlm_Golaem.exe" delete
    echo "end rlm"
    exit /b 1
