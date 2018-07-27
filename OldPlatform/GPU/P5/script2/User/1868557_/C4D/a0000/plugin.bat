@echo off
set cgv=%~1
set pluginDir=%~2
set pluginVersion=%~3
set Node=%~4

echo ------------------------
echo cgv=%cgv%
echo pluginDir=%pluginDir%
echo pluginVersion=%pluginVersion%
echo Node=%~4
echo ------------------------

if %pluginDir%==vray (
	goto vray
)
if %pluginDir%==alShaders (
	goto alShaders
)
if %pluginDir%==People_in_Motion (
	goto People_in_Motion
)
if %pluginDir%==GSG_HDRI_Studio_Pack (
	goto GSG_HDRI_Studio_Pack
)
if %pluginDir%==MagicSolo (
	goto MagicSolo
)
if %pluginDir%==SuperText (
	goto SuperText
)
if %pluginDir%==Thrausi (
	goto Thrausi
)
if %pluginDir%==Transform (
	goto Transform
)
if %pluginDir%==realflow (
	goto realflow
)

if %pluginDir%==CV_VRCam (
	goto CV_VRCam
)

if %pluginDir%==vonc_depliage (
	goto vonc_depliage
)

if %pluginDir%==Cineversity (
	goto Cineversity
)
if %pluginDir%==Tools4DTopologyVertexMaps (
	goto Tools4DTopologyVertexMaps
)
if %pluginDir%==1821033_plugins (
	goto 1821033_plugins
)
if %pluginDir%==964138_plugins (
	goto 964138_plugins
)
if %pluginDir%==1821067_plugins (
	goto 1821067_plugins
)
if %pluginDir%==1822391_plugins (
	goto 1822391_plugins
)
if %pluginDir%==1821381_plugins (
	goto 1821381_plugins
)
if %pluginDir%==1821841_plugins (
	goto 1821841_plugins
)
if %pluginDir%==ShadowCatcher (
	goto ShadowCatcher
)
if %pluginDir%==TurbulenceFD (
	goto TurbulenceFD
)
if %pluginDir%==X_Particles (
	goto X_Particles
)
if %pluginDir%==Forester (
	goto Forester
)

if %pluginDir%==laubwerk_surfacespread (
	goto laubwerk_surfacespread
)

if %pluginDir%==unfolder (
	goto unfolder
)

if %pluginDir%==NitroBlast (
	goto NitroBlast
)


if %pluginDir%==InfiniteOcean (
	goto InfiniteOcean
)

if %pluginDir%==c4dtoa (
	goto c4dtoa
)
if %pluginDir%==SubstanceCinema4D (
	goto SubstanceCinema4D
)
if %pluginDir%==maxwell (
	goto maxwell
)
if %pluginDir%==C4Dome (
	goto C4Dome
)
else (
	goto end
)




:laubwerk_surfacespread
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\%pluginDir%_%pluginVersion%\%cgv%" "C:\Program Files\MAXON\%cgv%"
goto end

::----------------------------------------------vray------------------------------------------
:vray
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\vray_%pluginVersion%\%cgv%\vray_key\%Node%\VrayBridge.key" "C:\Program Files\MAXON\%cgv%\"
::xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\vray_%pluginVersion%\%cgv%\VrayBridge.key" "C:\Program Files\MAXON\%cgv%\"
C:\fcopy\FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\%pluginDir%\vray_%pluginVersion%\%cgv%\plugins\VrayBridge\" /to="C:\Program Files\MAXON\%cgv%\plugins\VrayBridge"
goto end

::---------------------------------------------c4dtoa------------------------------------------
:c4dtoa
echo c4dtoa
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\c4dtoa_%pluginVersion%\%cgv%\ai.dll" "C:\Program Files\MAXON\%cgv%\"
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\c4dtoa_%pluginVersion%\%cgv%\solidangle.lic" "C:\Program Files\MAXON\%cgv%\"
C:\fcopy\FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\%pluginDir%\c4dtoa_%pluginVersion%\%cgv%\plugins\C4DtoA\" /to="C:\Program Files\MAXON\%cgv%\plugins\C4DtoA"
goto end

::---------------------------------------------People_in_Motion------------------------------------------
:People_in_Motion
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\People_in_Motion_%pluginVersion%\%cgv%\library" "C:\Program Files\MAXON\%cgv%\library"
xcopy /y /v /e "B:\plugins\C4D\%pluginDir%\People_in_Motion_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------unfolder--------------------------------------------
:unfolder
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\unfolder_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------NitroBlast--------------------------------------------
:NitroBlast
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\NitroBlast_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------Tools4DTopologyVertexMaps--------------------------------------------
:Tools4DTopologyVertexMaps
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\Tools4DTopologyVertexMaps_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------CV_VRCam--------------------------------------------
:CV_VRCam
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\CV_VRCam_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\CV_VRCam_%pluginVersion%\%cgv%\library" "C:\Program Files\MAXON\%cgv%\library"
goto end

::----------------------------------------------Forester--------------------------------------------
:Forester
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\Forester_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------vonc_depliage--------------------------------------------
:vonc_depliage
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\vonc_depliage_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------SubstanceCinema4D--------------------------------------------
:SubstanceCinema4D
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\Forester_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------TurbulenceFD--------------------------------------------
:TurbulenceFD
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\TurbulenceFD_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------TurbulenceFD--------------------------------------------
:X_Particles
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\X_Particles_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::----------------------------------------------alShaders--------------------------------------------
:alShaders
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\alShaders_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end
::----------------------------------------------realflow--------------------------------------------
:realflow
echo ceshi_2016
xcopy /y /v /e "B:\plugins\C4D\%pluginDir%\realflow_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------Cineversity--------------------------------------------
:Cineversity
xcopy /y /v /e "B:\plugins\C4D\%pluginDir%\Cineversity_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------ShadowCatcher--------------------------------------------
:ShadowCatcher
xcopy /y /v /e "B:\plugins\C4D\%pluginDir%\ShadowCatcher_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------HDRI Studio--------------------------------------------
:HDRI Studio
xcopy /y /v /e "B:\plugins\C4D\%pluginDir%\HDRI Studio_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------Tools4DVoxygen--------------------------------------------
:Tools4DVoxygen
xcopy /y /v /e "B:\plugins\C4D\%pluginDir%\Tools4D_Voxygen_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------GSG_HDRI_Studio_Pack--------------------------------------------
:GSG_HDRI_Studio_Pack
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\GSG_HDRI_Studio_Pack_%pluginVersion%\%cgv%\library" "C:\Program Files\MAXON\%cgv%\library"
goto end

::---------------------------------------------MagicSolo--------------------------------------------
:MagicSolo
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\MagicSolo_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------SuperText--------------------------------------------
:SuperText
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\SuperText_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------Thrausi--------------------------------------------
:Thrausi
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\Thrausi_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------Transform--------------------------------------------
:Transform
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\Transform_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"
goto end

::---------------------------------------------1821067_plugins--------------------------------------------
:1821067_plugins
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\1821067_plugins_%pluginVersion%\%cgv%\library" "C:\Program Files\MAXON\%cgv%\library"
goto end

::---------------------------------------------1822391_plugins--------------------------------------------
:1822391_plugins
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\1822391_plugins_%pluginVersion%\%cgv%\library" "C:\Program Files\MAXON\%cgv%\library"
goto end

::---------------------------------------------1821381_plugins--------------------------------------------
:1821381_plugins
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\1821381_plugins_%pluginVersion%\%cgv%\library" "C:\Program Files\MAXON\%cgv%\library"
goto end

::---------------------------------------------964138_plugins--------------------------------------------
:964138_plugins
C:\fcopy\FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\%pluginDir%\964138_plugins_%pluginVersion%\%cgv%\plugins\CINEMA 4D R17_0.53\" /to="C:\Program Files\MAXON\%cgv%"
goto end

::---------------------------------------------1821841_plugins--------------------------------------------
:1821841_plugins
C:\fcopy\FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\%pluginDir%\1821841_plugins_%pluginVersion%\%cgv%\library" /to="C:\Program Files\MAXON\%cgv%\library"
goto end

::---------------------------------------------1821033_plugins--------------------------------------------
:1821033_plugins
C:\fcopy\FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\%pluginDir%\1821033_plugins_%pluginVersion%\%cgv%\plugins\CINEMA 4D R17_0.53\" /to="C:\Program Files\MAXON\%cgv%"
goto end

::---------------------------------------------maxwell--------------------------------------------
:maxwell
C:\fcopy\FastCopy.exe /force_close /cmd=sync "B:\plugins\C4D\%pluginDir%\maxwell_%pluginVersion%\%cgv%\plugins\Maxwell\" /to="C:\Program Files\MAXON\%cgv%"
goto end

::---------------------------------------------InfiniteOcean--------------------------------------------
:InfiniteOcean
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\InfiniteOcean_%pluginVersion%\%cgv%" "C:\Program Files\MAXON\%cgv%\"
goto end
::--------------------------------------------C4Dome---------------------------------------------------------
:C4Dome
xcopy /f /y /e "B:\plugins\C4D\%pluginDir%\C4Dome_%pluginVersion%\%cgv%\plugins" "C:\Program Files\MAXON\%cgv%\plugins"

:end
echo %cgv% %pluginDir% %pluginVersion%
