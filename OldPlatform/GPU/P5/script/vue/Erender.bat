@echo off

echo Parsing...
set userId=%~1
set taskId=%~2
set startFrame=%~3
set endFrame=%~4
set byFrame=%~5
set cgv=%~6
set proj=%7
set cgFile=%~8
set output=%~9
set cgFile="%cgFile:\=/%"


echo userId=%userId%
echo taskId=%taskId%
echo startFrame=%startFrame%
echo endFrame=%endFrame%
echo byFrame=%byFrame%
echo cgv=%cgv%
echo proj=%proj%
echo cgFile=%cgFile%


set py_file_temp=B:\plugins\VUE\vue_temp.py
set py_file=c:\work\render\%taskId%\temp

if not exist %py_file% (
mkdir %py_file%
)
set py_file=%py_file%/vue_render.py
set py_file=%py_file:\=/%
if EXIST "%py_file%" del /a/f/q  "%py_file%"



if not exist %output% (
mkdir %output%
)
set output=%output:\=/%


set mu_pa_output=D:\vue_mp_output
if EXIST %mu_pa_output% (
del /a/f/q "%mu_pa_output%\*.*"
    )else ( mkdir %mu_pa_output%
    ) 
set mu_pa_output=%mu_pa_output:\=/%




set python_app=C:\Python27\python.exe
set vue_create="B:\plugins\VUE\vue_create.py"

if %userId%==1840063 goto render_python_10
if %userId%==963394 goto render_python_9
if %userId%==1811340 goto render_python_9
if %userId%==119768 goto render_python_9
if %cgv%==10 goto render_def 
if %cgv%==9.5 goto render_python_9
if %cgv%==2014 goto render_python_2014
if %cgv%==2015 goto render_python_2015
if %cgv%==2016 goto render_python_2016
::\\10.50.244.116\p5\script\vue\Erender.bat "119768" "5172405" "1" "1" "1" "10" "" "G:/test_10.vue" "C:\work\render\5172405\output"

:render_def 
    echo cgv=%cgv%
    echo "Rendering Strat" @ %date%-%time%
    "C:/Program Files/e-on software/Vue %cgv% xStream/Application/Vue %cgv% xStream RenderNode.exe"  -file "%cgFile%" -range %startFrame% %endFrame%  -output "%output%"
    goto end 


:render_python_2014
    echo "Rendering Seting" @ %date%-%time%
    set process_name="Vue 12 xStream.exe"


    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue 12 xStream\Temp" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue 12 xStream\Temp"
    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue 12 xStream\Config\renderstack" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue 12 xStream\Config\renderstack"
    robocopy /e /ns /nc /nfl /ndl /np "B:\plugins\VUE\2014\Config" "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue 12 xStream\Config"
    set software="C:/Program Files/e-on software/VueXstream_2014_6_FAiNT (vc100)/Application/Vue 12 xStream.exe"    
    goto render_strat

:render_python_2015
    echo "Rendering Seting" @ %date%-%time%
    set process_name="Vue xStream 2015.exe"
    wmic process where name="WerFault.exe" delete

    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2015\Temp" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2015\Temp"
    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2015\Config\renderstack" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2015\Config\renderstack"
    robocopy /e /ns /nc /nfl /ndl /np "B:\plugins\VUE\2015\Config" "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2015\Config"
    set software="C:/Program Files/e-on software/Vue xStream 2015/Application/Vue xStream 2015.exe"

    goto render_strat
    
:render_python_2016
    echo "Rendering Seting" @ %date%-%time%
    set process_name="Vue xStream 2016.exe"
    wmic process where name="WerFault.exe" delete

    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2016\Temp" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2016\Temp"
    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2016\Config" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2016\Config"
    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2016\Config\renderstack" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2016\Config\renderstack"
    robocopy /e /ns /nc /nfl /ndl /np "B:\plugins\VUE\2016\Config" "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue xStream 2016\Config"
    set software="C:/Program Files/e-on software/Vue xStream 2016/Application/Vue xStream 2016.exe"

    goto render_strat

:render_python_10
    echo "Rendering Seting" @ %date%-%time%   
    set process_name="Vue 10 xStream.exe"
    wmic process where name="WerFault.exe" delete
    ::wmic process where name=%process_name% delete
    ::TIMEOUT /T 15 /NOBREAK
    taskkill /F /IM %process_name% /T   
    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Temp" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Temp"
    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Config" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Config"
    robocopy /e /ns /nc /nfl /ndl /np "B:\plugins\VUE\%cgv%\Config" "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Config"
    set software="C:/Program Files/e-on software/Vue 10 xStream/Application/Vue %cgv% xStream.exe"
    echo "Rendering Strat" @ %date%-%time%
    %python_app%  %vue_create% %cgFile% %startFrame% %endFrame% %byFrame% %output% %mu_pa_output% %py_file_temp%  %py_file% %software%
    %software% "-p%py_file%" 
    %python_app% B:\plugins\VUE\vue_process.py %process_name%
    goto end 

:render_python_9
    echo "Rendering Seting" @ %date%-%time%  
    set process_name="Vue 9.5 xStream.eon"
    echo "test ::::::::"  %userId%
    ::wmic process where name=%process_name% delete
    ::TIMEOUT /T 15 /NOBREAK
    taskkill /F /IM %process_name% /T
    wmic process where name="WerFault.exe" delete
    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Temp" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Temp"
    if EXIST "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Config" rd/s/q  "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Config"
    
    robocopy /e /ns /nc /nfl /ndl /np "B:\plugins\VUE\%cgv%\Config" "C:\Users\enfuzion\AppData\Roaming\e-on software\Vue %cgv% xStream\Config"
    set software="C:/Program Files/e-on software/Vue %cgv% xStream/Vue %cgv% xStream.exe"

    echo %python_app%  %vue_create% %cgFile% %startFrame% %endFrame% %byFrame% %output% %mu_pa_output% %py_file_temp%  %py_file% %software%
    call %python_app%  %vue_create% %cgFile%  %startFrame%  %endFrame%  %byFrame%  %output%  %mu_pa_output%  %py_file_temp%  %py_file% %software%
    echo "_________"

    TIMEOUT /T 20 /NOBREAK
    echo "4000"
    echo %software% "-p%py_file%" 
    call %software% "-p%py_file%" 
    echo "_______________"
    TIMEOUT /T 20 /NOBREAK
    echo "2000"
    call %python_app% B:\plugins\VUE\vue_process.py %process_name%
    ::%python_app% B:\plugins\VUE\vue_process.py %process_name%
    goto end 

:render_strat    
    echo "Rendering Strat" @ %date%-%time%
    taskkill /F /IM "_SendLog.exe" /T
    wmic process where name="WerFault.exe" delete
    wmic process where name=%process_name% delete

    echo %python_app%  %vue_create% %cgFile% %startFrame% %endFrame% %byFrame% %output% %mu_pa_output% %py_file_temp%  %py_file%
    echo %software% "-p%py_file%"      
    call %python_app%  %vue_create% %cgFile% %startFrame% %endFrame% %byFrame% %output% %mu_pa_output% %py_file_temp%  %py_file% %software%
    call %software% "-p%py_file%" 
    goto end

:end
    ::wmic process where name="_SendLog.exe" delete
    ::wmic process where name="C:\Program Files\e-on software\Vue 10 xStream\Application\_SendLog.exe" delete
    taskkill /F /IM "_SendLog.exe" /T
    taskkill /F /IM %process_name% /T
    wmic process where name=%process_name% delete
    wmic process where name="WerFault.exe" delete
    ::if EXIST "%py_file%" del /a/f/q  "%py_file%"
    echo "Rendering Completed!" @ %date%-%time%

