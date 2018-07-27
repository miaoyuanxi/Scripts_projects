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
set renderer=%~9

set mel=c:/script/maya/maya_preRender.mel
set rd=c:/renderwork/%taskId%/output/


echo userId_%userId%
echo taskId_%taskId%
echo render_%render%
echo txt_%txt%
echo startframe_%startframe%
echo endframe_%endframe%
echo byframe_%byframe%
echo proj_%proj%
echo mb_%mb%

echo %renderer%
echo "%render%" -s %startframe% -e %endframe% -b %byframe% -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
"%render%" -s %startframe% -e %endframe% -b %byframe% -proj "%proj%" -rd %rd% -mr:art -mr:aml "%mb%"  
