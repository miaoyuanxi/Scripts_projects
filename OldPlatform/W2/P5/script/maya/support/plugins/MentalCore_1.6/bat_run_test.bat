	echo Turtle in Motion Configure Applied @ 163182
	echo Render Configure Updated - 001 by Neil @ 3/31/2014

	echo BAT info - License initializing...
	xcopy /y /e /v "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\license\MentalCore" "C:\MentalCore\"

	echo BAT info - Modules needed initializing...
	xcopy /y /e /v "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\modules\MentalCore" "C:\Program Files\Autodesk\Maya2013\modules\MentalCore\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\include\MentalCore.mi" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\include\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\include\MentalCore_Phenom.mi" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\include\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\mentalray\shaders\MentalCore.dll" "C:\Program Files\Autodesk\Maya2013\mentalray\shaders\"
	xcopy /y /f  "\\10.50.1.3\p\script\maya\support\plugins\MentalCore_1.6\modules\mentalcore.mod" "C:\Program Files\Autodesk\Maya2013\modules\"
