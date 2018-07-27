@echo off
set cgv=%~1
set plugin=%~2
set pluginVersion=%~3





if %plugin%==arnold (
	goto arnold
) 

echo "plugin...."

:arnold

echo "%userprofile%\Documents\maya\%cgv:~-4%-x64\"
xcopy /y /v /e "C:/PLUGINS/maya/arnold/replace/%cgv%/%pluginVersion%" "%userprofile%\Documents\maya\%cgv:~-4%-x64\"


echo c:/script/maya/plugin.bat "maya2012" "arnold" "0.22.1"