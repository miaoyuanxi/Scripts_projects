netsh interface ip set dns "Local Area Connection" static 114.114.114.114
xcopy /f /y /e  "B:\plugins\C4D\octane_GPU\host\hosts1\hosts" "C:\Windows\System32\drivers\etc\"
start "" "C:\Program Files\MAXON\CINEMA 4D R18\CINEMA 4D.exe"
ping /n 5 127.0.0.1>nul
start "" "C:\Program Files\OTOY\OctaneRender 3.06.0\octane.exe"
ping /n 5 127.0.0.1>nul
xcopy /f /y "B:\plugins\C4D\octane_GPU\test.vbs" "D:\Temp"
start "" "D:\Temp\test.vbs"
ping /n 30 127.0.0.1>nul
echo %USERDOMAIN%
md "B:\plugins\C4D\octane_GPU\octane_GPU_3.06.0\CINEMA 4D R18\%USERDOMAIN%"
xcopy /f /y /e "C:\Users\enfuzion\AppData\Roaming\MAXON" "B:\plugins\C4D\octane_GPU\octane_GPU_3.06.0\CINEMA 4D R18\%USERDOMAIN%\MAXON\"
ping /n 20 127.0.0.1>nul
taskkill.exe /im octane.exe /f
xcopy /f /y /e "C:\Users\enfuzion\AppData\Roaming\OctaneRender" "B:\plugins\C4D\octane_GPU\octane_GPU_3.06.0\CINEMA 4D R18\%USERDOMAIN%\OctaneRender\"
:taskkill.exe /im "CINEMA 4D.exe" /f




:xcopy /f /y /e  "B:\plugins\C4D\octane_GPU\host\hosts2\hosts" "C:\Windows\System32\drivers\etc\"
:netsh interface ip set dns "Local Area Connection" static 10.60.100.3
:netsh interface IP add dns "Local Area Connection" addr=10.60.102.1